"""Meaningful tests for future training resume and evidence-preserving verification."""
from pathlib import Path
import tempfile
import copy,json,hashlib,random,os
import nbformat
import numpy as np
import torch
from torch import nn
n=nbformat.read('problem1/problem1.ipynb',4)
scope=dict(Path=Path,copy=copy,json=json,hashlib=hashlib,random=random,os=os,np=np,torch=torch)
exec(next(c.source for c in n.cells if c.source.startswith('# Reproducibility infrastructure')),scope)
torch.set_num_threads(4)
random.seed(38);np.random.seed(38);torch.manual_seed(38)
generator=torch.Generator().manual_seed(38)
model=nn.Sequential(nn.Linear(3,7),nn.Dropout(.25),nn.Linear(7,1));model.train()
optimizer=torch.optim.Adam(model.parameters(),lr=.001)
x=torch.randn(8,3);y=torch.randn(8,1)
def update():
 optimizer.zero_grad();loss=(model(x)-y).square().mean();loss.backward();optimizer.step();return float(loss.detach())
update()
with tempfile.TemporaryDirectory(dir='.cache') as directory:
 path=Path(directory)/'resume.pt'
 scope['save_training_state'](path,model,optimizer,1,[{'loss':1.}],generator,best_metric=1.)
 expected_rng=(random.random(),float(np.random.random()),torch.rand(3),torch.randperm(8,generator=generator))
 expected_loss=update();expected={k:v.clone() for k,v in model.state_dict().items()}
 saved=scope['restore_training_state'](path,model,optimizer,generator)
 actual_rng=(random.random(),float(np.random.random()),torch.rand(3),torch.randperm(8,generator=generator))
 assert expected_rng[:2]==actual_rng[:2]
 for a,b in zip(expected_rng[2:],actual_rng[2:]):assert torch.equal(a,b)
 assert update()==expected_loss
 assert all(torch.equal(v,expected[k]) for k,v in model.state_dict().items())
 assert saved['epoch']==1 and saved['selection']['best_metric']==1.
 os.environ['DNN_VERIFY_CACHED_ONLY']='1'
 try:scope['replay_or_missing'](Path(directory)/'missing')
 except RuntimeError:pass
 else:raise AssertionError('Missing cache silently accepted')
print('PASS: optimizer moments, Python/NumPy/Torch/loader RNG restore reproduce next stochastic Adam update exactly; missing-cache guard rejects training')
# Logger replay must preserve every byte when a row already matches.
ns=dict(pd=__import__('pandas'),np=np)
exec(next(c.source for c in n.cells if c.source.startswith('def save_har_result')),ns)
ns['RESULT_COLUMNS']=__import__('pandas').read_csv('results.csv',nrows=0).columns.tolist()
with tempfile.TemporaryDirectory(dir='.cache') as directory:
 path=Path(directory)/'ledger.csv';row=dict.fromkeys(ns['RESULT_COLUMNS']);row.update(problem='P1',model='fixture',seed=0,notes='test',test_mse=.123456789012345)
 ns['save_har_result'](row,path);before=path.read_bytes();ns['save_har_result'](row,path)
 assert path.read_bytes()==before
print('PASS: completed-row replay preserves exact CSV bytes')
# Exercise the missing-cache training/generation branch on a disposable one-update fixture.
from notebook_scope import load_definitions
with tempfile.TemporaryDirectory(dir='.cache') as directory:
 task_root=Path(directory);cache=task_root/'cache';metrics=task_root/'metrics'
 cache.mkdir();metrics.mkdir()
 s=load_definitions('problem1',dict(ROOT=task_root,SUPPLEMENT_CACHE=cache,SUPPLEMENT_METRICS=metrics,
                                   RESULT_COLUMNS=ns['RESULT_COLUMNS']))
 previous=os.environ.pop('DNN_VERIFY_CACHED_ONLY',None)
 try:
  result=s['run_adding_diagnostics']('RNN','overfit',epochs=1,n_train=32,name='disposable-fixture')
  assert result['best_epoch']==1 and not result['test_evaluated']
  assert (cache/'disposable-fixture.resume.pt').is_file()
  replay=s['run_adding_diagnostics']('RNN','overfit',epochs=1,n_train=32,name='disposable-fixture')
  assert replay['checkpoint_sha256']==result['checkpoint_sha256']
 finally:
  if previous is not None:os.environ['DNN_VERIFY_CACHED_ONLY']=previous
print('PASS: disposable one-update notebook diagnostic trains, saves resumable state and independently replays validation; no assessed result is added')
