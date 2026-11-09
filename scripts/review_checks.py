"""Independent review checks: scalar oracle, model invariance, evidence integrity."""
from pathlib import Path
import json, hashlib, math, random
import nbformat
import numpy as np
import pandas as pd
import torch
from torch import nn
from research_review import definitions, OUT, CACHE

torch.set_num_threads(4)

def run():
    hashes=json.loads(Path('docs/baseline-2026-11-09/model-source-hashes.json').read_text())
    for problem in ('problem1','problem2'):
        for cell in nbformat.read(f'{problem}/{problem}.ipynb',4).cells:
            key=cell.source.splitlines()[0] if cell.source else ''
            if key in hashes:
                assert hashlib.sha256(cell.source.encode()).hexdigest()==hashes[key],key
    baseline=pd.read_csv('docs/baseline-2026-11-09/results.csv')
    now=pd.read_csv('results.csv'); extra=pd.read_csv(OUT/'additional-results.csv')
    pd.testing.assert_frame_equal(now.iloc[:82].reset_index(drop=True),baseline,check_exact=False,rtol=1e-14,atol=1e-14)
    pd.testing.assert_frame_equal(now.iloc[82:].reset_index(drop=True),extra,check_exact=False,rtol=1e-14,atol=1e-14)
    assert len(extra)==10 and now.columns.tolist()==baseline.columns.tolist()
    assert not now.duplicated(['problem','model','seed','notes']).any()
    s=definitions('problem1',['def make_adding','class AddingRegressor'])
    for kind in ('RNN','LSTM','GRU'):
        for mode in ('overfit','validation-pilot'):
            record=json.loads((OUT/f'adding-{kind}-{mode}.json').read_text())
            saved=torch.load(CACHE/f'adding-{kind}-{mode}.pt',weights_only=True)
            model=s['AddingRegressor'](kind,64).eval();model.load_state_dict(saved['state_dict'])
            x,y=s['make_adding'](1000,50,1)
            with torch.no_grad():pred=torch.cat([model(b) for b in torch.from_numpy(x).split(128)]).double().numpy()
            mse=np.mean((pred-y.astype('float64'))**2)
            assert abs(mse-record['best_val_mse'])<1e-12
            assert record['test_evaluated'] is False
            if mode=='validation-pilot':
                history=pd.read_csv('problem1/metrics/adding_history.csv')
                old=history[(history.model==kind)&(history.seq_len==50)&(history.seed==0)]
                np.testing.assert_allclose(old[['train_mse','val_mse']].values,
                    [[h['train_mse'],h['val_mse']] for h in record['history'][:5]],atol=1e-14,rtol=0)
            assert record['best_epoch']==min(record['history'],key=lambda h:h['val_mse'])['epoch']
    # Validate scalar nonuniform attention arithmetic, not a reimplementation of softmax.
    s=definitions('problem2',['def scaled_dot_product_attention','class MyMultiHeadAttention',
        'class MyEncoderBlock','def sinusoidal_positions','class HAREncoder'])
    a=1/math.sqrt(2);E=math.exp(a)
    q=torch.tensor([[1.,0.],[0.,1.],[1.,1.]],dtype=torch.float64)
    k=torch.tensor([[1.,0.],[0.,1.],[1.,-1.]],dtype=torch.float64)
    v=torch.tensor([[1.,0.],[0.,2.],[3.,4.]],dtype=torch.float64)
    expected=np.array([[E/(2*E+1),1/(2*E+1),E/(2*E+1)],
                       [1/(1+E+1/E),E/(1+E+1/E),(1/E)/(1+E+1/E)],
                       [E/(2*E+1),E/(2*E+1),1/(2*E+1)]])
    actual,w=s['scaled_dot_product_attention'](q[None,None],k[None,None],v[None,None])
    np.testing.assert_allclose(w.numpy()[0,0],expected,atol=1e-14,rtol=0)
    expected_out=np.array([[r[0]+3*r[2],2*r[1]+4*r[2]] for r in expected])
    np.testing.assert_allclose(actual.numpy()[0,0],expected_out,atol=1e-14,rtol=0)
    (OUT/'nonuniform-hand-example.json').write_text(json.dumps(dict(Q=q.tolist(),K=k.tolist(),V=v.tolist(),weights=expected.tolist(),output=expected_out.tolist()),indent=2)+'\n')
    # Trained none-position encoder: controlled permutations hold weights fixed.
    ck=torch.load('data/experiments/problem2/13613c052b7f52c4/har/none_0.pt',weights_only=True)
    model=s['HAREncoder']('none',ck['config']).eval();model.load_state_dict(ck['state_dict'])
    torch.manual_seed(13);x=torch.randn(4,16,8,9)
    with torch.no_grad():
        logits=model(x.reshape(4,128,9))
        patch=float((logits-model(x[:,torch.arange(15,-1,-1)].reshape(4,128,9))).abs().max())
        within=float((logits-model(x.flip(2).reshape(4,128,9))).abs().max())
    assert patch<1e-5 and within>1e-5
    (OUT/'patch-order-check.json').write_text(json.dumps(dict(input='fixed synthetic normalized Gaussian probe, seed13; trained none_0 weights',
         patch_reversal_max_logit_delta=patch,within_patch_reversal_max_logit_delta=within,
         interpretation='whole-patch permutation invariant; within-patch offsets retain order; no predictive-accuracy or causal-superiority claim'),indent=2)+'\n')
    # Replay every continued validation loss independently and reproduce samples.
    from research_review import lm_scope
    ls=lm_scope();text=Path('data/tiny_shakespeare/input.txt').read_text();chars=sorted(set(text))
    tokens=torch.tensor([chars.index(c) for c in text]);val=tokens[int(.9*len(tokens)):]
    for heads,causal in ((4,True),(1,True),(8,True),(4,False)):
        name=f'lm-h{heads}-causal{int(causal)}';r=json.loads((OUT/f'{name}.json').read_text())
        saved=torch.load(CACHE/f'{name}.pt',weights_only=True)
        model=ls['CharacterTransformer'](65,saved['config']).eval();model.load_state_dict(saved['state_dict'])
        dataset=ls['CharacterBlocks'](val,128);total=0.;count=0
        with torch.no_grad():
            for x,y in torch.utils.data.DataLoader(dataset,batch_size=64):
                total+=float(nn.functional.cross_entropy(model(x).flatten(0,1),y.flatten(),reduction='sum'));count+=y.numel()
        assert abs(total/count-r['best_val_loss'])<1e-7
        assert abs(r['bits_per_char']-r['best_val_loss']/math.log(2))<1e-12
        assert len(r['history'])==5
        assert abs(r['best_val_loss']-min([r['before']]+[h['val_loss'] for h in r['history']]))<1e-12
        if heads==4:
            probe=val[:32].reshape(1,-1);changed=probe.clone();changed[:,16:]=(changed[:,16:]+1)%65
            with torch.no_grad():delta=float((model(probe)[:,:16]-model(changed)[:,:16]).abs().max())
            if causal:assert delta<1e-5
            else:assert delta>1e-5
            (OUT/f'continued-causality-{int(causal)}.json').write_text(json.dumps(dict(causal=causal,prefix_max_difference=delta),indent=2)+'\n')

    samples=json.loads((OUT/'continued-samples.json').read_text())
    assert len(samples)==4 and all(len(r['sample'])==500 for r in samples)
    ls.update(chars=chars,stoi={c:i for i,c in enumerate(chars)})
    source=next(c.source for c in nbformat.read('problem2/problem2.ipynb',4).cells if c.source.startswith('def load_language'))
    exec(source,ls)
    for sample in samples:
        saved=torch.load(CACHE/f'lm-h4-causal{int(sample["causal"])}.pt',weights_only=True)
        model=ls['CharacterTransformer'](65,saved['config']).eval();model.load_state_dict(saved['state_dict'])
        actual=ls['generate_characters'](model,sample['prompt'],sample['temperature'],500,20,700)
        assert actual==sample['sample']
    # Next-token boundary oracle, with absolute split offsets independent of Dataset.
    blocks=ls['CharacterBlocks'](tokens,128)
    for index in (0,len(blocks)-1):
        x,y=blocks[index];assert torch.equal(y,tokens[index*128+1:index*128+129])
    val_blocks=ls['CharacterBlocks'](val,128)
    assert torch.equal(val_blocks[0][0],tokens[int(.9*len(tokens)):int(.9*len(tokens))+128])
    for length in (64,128,256,512):
        raw=json.loads(Path(f'problem2/metrics/context_raw_{length}.json').read_text())
        row=pd.read_csv('problem2/metrics/context_scaling.csv').set_index('context').loc[length]
        np.testing.assert_allclose(np.mean(raw['timing_seconds']),row.mean_seconds,atol=1e-12)
        np.testing.assert_allclose(np.std(raw['timing_seconds'],ddof=1),row.std_seconds,atol=1e-12)
        peaks=[]
        for trace in raw['memory_trials']:
            current=0;peak=0
            for _,delta in trace['events_ns_bytes']:current+=delta;peak=max(current,peak)
            assert peak==trace['peak_bytes'];peaks.append(peak)
        assert len(peaks)==3 and int(np.median(peaks))==row.peak_incremental_bytes
    print('PASS: baseline preserved, 10 supplemental rows, adding checkpoint validation, scalar attention oracle, trained patch invariance, all four continued LM validations, 4x500 samples, raw timings and 12 profiler traces')

if __name__=='__main__':run()
