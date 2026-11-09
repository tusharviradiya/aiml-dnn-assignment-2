"""Independently replay Problem 2 checkpoints and reconcile saved evidence.

Never trains. Uses actual notebook model definitions and independent metric code.
"""
from pathlib import Path
import ast
import contextlib
import io
import json
import math
import nbformat
import numpy as np
import pandas as pd
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path('.')
METRICS = ROOT/'problem2'/'metrics'
protocol = json.loads((METRICS/'config.json').read_text())
notebook = nbformat.read('problem2/problem2.ipynb', as_version=4)
scope = {}
# The pre-execution cells contain setup, assertions, model/helper definitions only.
with contextlib.redirect_stdout(io.StringIO()):
    for cell in notebook.cells:
        if cell.source.startswith('## Execute HAR'):
            break
        if cell.cell_type == 'code':
            exec(compile(cell.source, 'problem2/problem2.ipynb', 'exec'), scope)
assert scope['RUN_ID'] == protocol['run_id']
assert scope['CODE_HASH'] == protocol['code_hash']
cache = scope['P2_CACHE']
device = scope['DEVICE']
# Check actual model source rather than banning the allowed test references.
for cell in notebook.cells:
    if 'cache_dependency' not in cell.metadata.get('tags', []):
        continue
    for node in ast.walk(ast.parse(cell.source)):
        if isinstance(node, ast.Attribute):
            assert node.attr not in ('MultiheadAttention', 'Transformer', 'TransformerEncoder',
                                     'TransformerEncoderLayer', 'TransformerDecoder', 'TransformerDecoderLayer',
                                     'scaled_dot_product_attention'), 'Forbidden framework implementation in model source'

def close(a, b, tolerance=1e-7):
    assert abs(float(a)-float(b)) < tolerance, (a,b)

ledger = pd.read_csv('results.csv')
assert ledger.columns.tolist() == scope['RESULT_COLUMNS']
assert not ledger.duplicated(['problem','model','seed','notes']).any()
# Preserve every pre-existing P1 row, allowing CSV float round-trip precision only.
before = pd.read_csv(ROOT/'problem1'/'metrics'/'experiment_ledger.csv')
assert len(before)==69 and before.problem.eq('P1').all()
pd.testing.assert_frame_equal(before[before.problem=='P1'].reset_index(drop=True),
                              ledger[ledger.problem=='P1'].reset_index(drop=True),check_exact=False,rtol=1e-12,atol=1e-12)
har_runs = pd.read_csv(METRICS/'har_runs.csv')
har_history = pd.read_csv(METRICS/'har_history.csv')
har_predictions = pd.read_csv(METRICS/'har_predictions.csv')
assert len(har_runs)==9 and len(har_history)==90 and len(har_predictions)==9*2947
for position in ('none','sinusoidal','learned'):
    for seed in (0,1,2):
        stem=cache/'har'/f'{position}_{seed}'
        result=json.loads(stem.with_suffix('.json').read_text())
        checkpoint=torch.load(stem.with_suffix('.pt'),map_location='cpu',weights_only=True)
        assert checkpoint['source_hash']==protocol['code_hash'] and checkpoint['config']==result['config']
        tr,va,held=scope['subject_split'](scope['subjects_train'],seed)
        mean,std=scope['fit_normalizer'](scope['x_train_raw'][tr])
        np.testing.assert_array_equal(checkpoint['mean'].numpy(),mean)
        np.testing.assert_array_equal(checkpoint['std'].numpy(),std)
        assert result['held_subjects']==held.tolist()
        model=scope['HAREncoder'](position,result['config']).to(device)
        model.load_state_dict(checkpoint['state_dict']); model.eval()
        with torch.no_grad():
            inputs=torch.from_numpy(scope['normalize'](scope['x_test_raw'],mean,std))
            predictions=torch.cat([model(x.to(device)).argmax(-1).cpu() for x in inputs.split(128)]).numpy()
        np.testing.assert_array_equal(predictions,result['predictions'])
        rows=har_predictions[(har_predictions.position==position)&(har_predictions.seed==seed)].sort_values('index')
        np.testing.assert_array_equal(rows.prediction,predictions)
        np.testing.assert_array_equal(rows.target,scope['y_test'])
        row=result['row']; close(row['test_acc'],accuracy_score(scope['y_test'],predictions),1e-12)
        close(row['macro_f1'],f1_score(scope['y_test'],predictions,average='macro'),1e-12)
        assert row['params']==sum(p.numel() for p in model.parameters())
        selected=max(result['history'],key=lambda h:h['val_f1'])
        assert selected['epoch']==result['best_epoch']
        close(selected['val_f1'],result['best_val_f1'],1e-12)
        close(np.mean([h['seconds'] for h in result['history']]),row['sec_per_epoch'],1e-10)
        assert len(ledger[(ledger.model==row['model'])&(ledger.seed==seed)&(ledger.notes==row['notes'])])==1
        saved=har_history[(har_history.position==position)&(har_history.seed==seed)]
        np.testing.assert_allclose(saved.train_loss,[h['train_loss'] for h in result['history']],atol=1e-12)
        val_inputs=torch.from_numpy(scope['normalize'](scope['x_train_raw'][va],mean,std))
        with torch.no_grad():
            val_predictions=torch.cat([model(x.to(device)).argmax(-1).cpu() for x in val_inputs.split(128)]).numpy()
        close(f1_score(scope['y_train_raw'][va],val_predictions,average='macro'),result['best_val_f1'],1e-12)
summary=pd.read_csv(METRICS/'har_summary.csv',index_col=0)
for name,rows in har_runs.groupby('model'):
    for column,key in (('test_acc','acc'),('macro_f1','f1')):
        close(summary.loc[name,key+'_mean'],rows[column].mean(),1e-12)
        close(summary.loc[name,key+'_std'],rows[column].std(ddof=1),1e-12)
print('PASS: nine HAR checkpoints, 26523 predictions, subject statistics, validation selection, counts and sample std')

lm_runs=pd.read_csv(METRICS/'lm_runs.csv'); lm_history=pd.read_csv(METRICS/'lm_history.csv')
assert len(lm_runs)==4 and len(lm_history)==20
lm_results=[]
for heads,causal in ((4,True),(1,True),(8,True),(4,False)):
    key=f'lm/heads{heads}_causal{int(causal)}'
    result=json.loads((cache/key).with_suffix('.json').read_text()); lm_results.append(result)
    checkpoint=torch.load((cache/key).with_suffix('.pt'),map_location='cpu',weights_only=True)
    assert checkpoint['source_hash']==protocol['code_hash'] and checkpoint['config']==result['config']
    assert checkpoint['chars']==scope['chars']
    model=scope['CharacterTransformer'](65,result['config']).to(device)
    model.load_state_dict(checkpoint['state_dict']); model.eval()
    loader=DataLoader(scope['CharacterBlocks'](scope['val_ids'],128),batch_size=64,shuffle=False)
    nats_sum=0.; count=0
    with torch.no_grad():
        for x,y in loader:
            logits=model(x.to(device)); y=y.to(device)
            nats_sum+=F.cross_entropy(logits.flatten(0,1),y.flatten(),reduction='sum').item(); count+=y.numel()
    row=result['row']; close(nats_sum/count,row['val_loss_nats'],1e-7)
    close(row['bits_per_char'],row['val_loss_nats']/math.log(2),1e-12)
    assert row['params']==sum(p.numel() for p in model.parameters())
    selected=min(result['history'],key=lambda h:h['val_loss'])
    assert selected['epoch']==result['best_epoch']
    close(selected['val_loss'],row['val_loss_nats'],1e-12)
    close(np.mean([h['seconds'] for h in result['history']]),row['sec_per_epoch'],1e-10)
    assert len(ledger[(ledger.model==row['model'])&(ledger.notes==row['notes'])])==1
    saved=lm_history[(lm_history.heads==heads)&(lm_history.causal==causal)]
    np.testing.assert_allclose(saved.val_loss,[h['val_loss'] for h in result['history']],atol=1e-12)
assert lm_runs.params.nunique()==1
# Head count and mask must not alter parameter initialization at fixed width.
initial = None
for result in lm_results:
    scope['seed_everything'](result['config']['seed'])
    model = scope['CharacterTransformer'](65,result['config'])
    state = {name:value.detach().cpu().clone() for name,value in model.named_parameters()}
    if initial is None:
        initial = state
    else:
        assert state.keys()==initial.keys()
        assert all(torch.equal(state[name],initial[name]) for name in state)
    for key in ('d','layers','context','dropout','batch_size','epochs','lr','clip_norm','seed'):
        assert result['config'][key]==lm_results[0]['config'][key]
assert len(scope['train_ids'])==int(.9*len(scope['text'])) and len(scope['chars'])==65
for data in (scope['train_ids'],scope['val_ids']):
    blocks=scope['CharacterBlocks'](data,128)
    for i in (0,len(blocks)-1):
        x,y=blocks[i]
        assert torch.equal(x,data[i*128:i*128+128]) and torch.equal(y,data[i*128+1:i*128+129])
print('PASS: four LM checkpoints, contiguous split/targets, selected validation nats/BPC, counts and histories')

# Sampling/inspection helpers occur after training; load definitions only.
for cell in notebook.cells:
    if cell.cell_type=='code' and cell.source.startswith('def load_language'):
        exec(cell.source,scope)
model=scope['load_language'](lm_results[0])
samples=json.loads((METRICS/'samples.json').read_text())
assert [s['temperature'] for s in samples]==[.2,.8,1.5]
labelled=(ROOT/'problem2'/'generated_samples.txt').read_text()
for sample in samples:
    assert len(sample['sample'])==500 and sample['sample'] in labelled
    reproduced=scope['generate_characters'](model,sample['prompt'],sample['temperature'],500,sample['top_k'],sample['seed'])
    assert reproduced==sample['sample']
no_mask=(METRICS/'no_mask_sample.txt').read_text(); assert len(no_mask)==500
unmasked=scope['load_language'](lm_results[-1])
assert no_mask==scope['generate_characters'](unmasked,samples[0]['prompt'],.8,500,20,700)
attention=np.load(METRICS/'attention_heads.npz'); weights=attention['weights']; sentence=str(attention['sentence'])
with torch.no_grad():
    _,actual=model(torch.tensor([[scope['stoi'][c] for c in sentence]],device=device),True)
np.testing.assert_array_equal(actual[0][0,:2].cpu().numpy(),weights)
assert weights.shape==(2,len(sentence),len(sentence))
np.testing.assert_allclose(weights.sum(-1),1,atol=2e-7)
assert np.count_nonzero(np.triu(weights,1))==0
scaling=pd.read_csv(METRICS/'context_scaling.csv')
assert scaling.context.tolist()==[64,128,256,512]
assert (scaling.mean_seconds>0).all() and (scaling.peak_incremental_bytes>0).all()
np.testing.assert_array_equal(scaling.attention_score_elements,8*4*scaling.context**2)
for name in ('har_positions.png','lm_ablations.png','attention_heads.png','context_scaling.png'):
    assert (ROOT/'problem2'/'figures'/name).stat().st_size>1000
assert len(ledger[ledger.problem=='P2'])==13
print('PASS: all 2000 generated characters reproduced; saved two-head attention and context-scaling evidence')
print('PASS: Problem 1 ledger preserved; 13 completed P2 runs, no forbidden model layers or duplicate rows')

# Diagnostics added after training must also reflect actual saved samples/model behavior.
from collections import Counter
stats=pd.read_csv(METRICS/'sample_statistics.csv')
for row,sample in zip(stats.itertuples(index=False),[r['sample'] for r in samples]+[no_mask]):
    counts=np.array(list(Counter(sample).values()),dtype=float)
    probabilities=counts/counts.sum()
    assert row.distinct_characters==len(counts)
    close(row.empirical_char_entropy_bits,-(probabilities*np.log2(probabilities)).sum(),1e-12)
    close(row.newline_fraction,sample.count('\n')/500,1e-12)
diagnostic=json.loads((METRICS/'mask_diagnostic.json').read_text())
ids=torch.tensor([[scope['stoi'][c] for c in sentence]],device=device)
changed=ids.clone();changed[:,5:]=(changed[:,5:]+1)%65
with torch.no_grad():
    causal_delta=(model(ids)[:,:5]-model(changed)[:,:5]).abs().max().item()
    unmasked_delta=(unmasked(ids)[:,:5]-unmasked(changed)[:,:5]).abs().max().item()
close(causal_delta,diagnostic['causal_prefix_max_change'],1e-12)
close(unmasked_delta,diagnostic['unmasked_prefix_max_change'],1e-7)
assert causal_delta<1e-5 and unmasked_delta>1e-5
print('PASS: sample diversity diagnostics and trained-model future perturbation reproduced')
