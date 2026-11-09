"""Reject stale supplemental experiments before evaluation, logging or training.

Uses real preserved caches for positive compatibility checks and disposable copies
for tamper/change controls. Never modifies original evidence or trains a model.
"""
from pathlib import Path
import copy, hashlib, json, os, shutil, tempfile
import nbformat
import torch
from notebook_scope import load_definitions, problem2_scope

torch.set_num_threads(4)
root=Path('.').resolve()
cache=root/'data/experiments/review'
s=load_definitions('problem1',dict(SUPPLEMENT_CACHE=cache))
ls=problem2_scope();ls['SUPPLEMENT_CACHE']=cache
checks=0

def reject(scope, action):
    global checks
    try: action()
    except scope['CacheCompatibilityError']: checks+=1
    else: raise AssertionError('Stale/unproven cache accepted')

def no_evaluation(*args,**kwargs):
    raise AssertionError('Cache mismatch reached evaluation/training/write branch')

# Valid legacy replay requires exact metadata, weights AND the reconstructed contract.
for kind in ('RNN','LSTM','GRU'):
    for mode in ('overfit','validation-pilot'):
        requested,*_=s['adding_diagnostic_request'](kind,mode)
        assert s['replay_or_missing'](cache/f'adding-{kind}-{mode}',requested)['model']==kind
print('PASS: all six historical adding bindings match resolved protocols and source/data fingerprints')

s['AddingRegressor']=no_evaluation
for settings in ({'epochs':26},{'n_train':9999},{'batch_size':64},{'seed':1},
                 {'seq_len':100},{'hidden':32},{'lr':.002},{'clip':.5},
                 {'n_val':999},{'train_data_seed':4},{'validation_seed':5}):
    reject(s,lambda settings=settings:s['run_adding_diagnostics']('RNN','validation-pilot',**settings))
for epochs,n in ((1200,32),(1,10000)):
    reject(s,lambda:s['run_adding_diagnostics']('RNN','validation-pilot',epochs=epochs,n_train=n))
for bad in ({'epochs':0},{'n_train':0}):
    try:s['run_adding_diagnostics']('RNN','validation-pilot',**bad)
    except ValueError:pass
    else:raise AssertionError('Zero budget silently replaced with default')

baselines=[]
for heads,causal in ((4,True),(1,True),(8,True),(4,False)):
    baseline=json.loads((ls['P2_CACHE']/f'lm/heads{heads}_causal{int(causal)}.json').read_text())
    request,_=ls['lm_continuation_request'](baseline)
    assert ls['replay_or_missing'](cache/f'lm-h{heads}-causal{int(causal)}',request)['config']==baseline['config']
    baselines.append(baseline)
print('PASS: all four historical LM bindings include the current originating baseline identity and continuation protocol')
ls['evaluate_language']=no_evaluation
reject(ls,lambda:ls['run_lm_continuation'](baselines[0],epochs=6))
changed=copy.deepcopy(baselines[0]);changed['best_epoch']-=1
reject(ls,lambda:ls['run_lm_continuation'](changed))

with tempfile.TemporaryDirectory(dir='.cache') as directory:
    tmp=Path(directory)
    # Source edits must invalidate compatibility, even with the same experiment name.
    for problem,scope,action in (
        ('problem1',s,lambda:s['run_adding_diagnostics']('RNN','validation-pilot')),
        ('problem2',ls,lambda:ls['run_lm_continuation'](baselines[0]))):
        (tmp/problem).mkdir();notebook=nbformat.read(root/problem/f'{problem}.ipynb',4)
        target='class AddingRegressor' if problem=='problem1' else 'def evaluate_language'
        cell=next(c for c in notebook.cells if c.source.startswith(target) or '\n'+target in c.source)
        cell.source=cell.source.replace('def forward(self,x):','def forward(self,x):\n        x=x+0.001') if problem=='problem1' else cell.source.replace('loss_sum=0.','loss_sum=1.')
        # Ensure this negative control really changes executable source.
        assert cell.source != next(c.source for c in nbformat.read(root/problem/f'{problem}.ipynb',4).cells if c.source.startswith(target) or '\n'+target in c.source)
        nbformat.write(notebook,tmp/problem/f'{problem}.ipynb')
        previous=scope['ROOT'];scope['ROOT']=tmp
        try:reject(scope,action)
        finally:scope['ROOT']=previous

    # Preserve architecture/validation metadata but change one baseline tensor byte.
    old_base=ls['P2_CACHE'];ls['P2_CACHE']=tmp/'baselines'
    try:
        path=(ls['P2_CACHE']/baselines[0]['key']).with_suffix('.pt');path.parent.mkdir(parents=True)
        saved=torch.load((old_base/baselines[0]['key']).with_suffix('.pt'),weights_only=True)
        tensor=next(v for v in saved['state_dict'].values() if v.is_floating_point())
        tensor.view(-1)[0]+=.01
        torch.save(saved,path)
        reject(ls,lambda:ls['run_lm_continuation'](baselines[0]))
    finally:ls['P2_CACHE']=old_base

    # Data change with identical sizes/settings is not a compatible experiment.
    original_tokens=ls['train_ids'];ls['train_ids']=original_tokens.clone();ls['train_ids'][0]=(ls['train_ids'][0]+1)%65
    try:reject(ls,lambda:ls['run_lm_continuation'](baselines[0]))
    finally:ls['train_ids']=original_tokens

    # Prospective records validate complete contracts. Unknown legacy records and
    # partial/corrupt checkpoints are rejected rather than overwritten.
    request,*_=s['adding_diagnostic_request']('RNN','validation-pilot')
    stem=tmp/'new-style';torch.save({'fixture':torch.tensor([1.])},stem.with_suffix('.pt'))
    digest=hashlib.sha256(stem.with_suffix('.pt').read_bytes()).hexdigest()
    record=dict(cache_contract=request,checkpoint_sha256=digest)
    stem.with_suffix('.json').write_text(json.dumps(record))
    assert s['replay_or_missing'](stem,request)==record
    reject(s,lambda:s['replay_or_missing'](stem,{**request,'epochs':26}))
    record.pop('cache_contract');stem.with_suffix('.json').write_text(json.dumps(record))
    reject(s,lambda:s['replay_or_missing'](stem,request))
    record['cache_contract']=request;stem.with_suffix('.json').write_text(json.dumps(record))
    stem.with_suffix('.pt').write_bytes(b'corrupted fixture')
    reject(s,lambda:s['replay_or_missing'](stem,request))
    stem.with_suffix('.pt').unlink()
    reject(s,lambda:s['replay_or_missing'](stem,request))
print(f'PASS: {checks} stale/source/data/baseline/protocol/integrity negative controls rejected before result reuse; no original evidence overwritten')
