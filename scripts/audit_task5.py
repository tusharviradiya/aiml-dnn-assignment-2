"""Audit Task 5 prediction evidence, checkpoint selection and gradient probes."""
import json
from pathlib import Path
import nbformat
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import accuracy_score,f1_score

torch.set_num_threads(4)
root=Path('.')
metrics=root/'problem1/metrics'
config=json.loads((metrics/'task5_config.json').read_text())
nb=nbformat.read('problem1/problem1.ipynb',as_version=4)
from notebook_scope import load_definitions
scope=load_definitions('problem1')
scope['CHANNELS']=('body_acc_x','body_acc_y','body_acc_z','body_gyro_x','body_gyro_y','body_gyro_z','total_acc_x','total_acc_y','total_acc_z')
for prefix in ('def download_har','def load_har_split','def subject_split','def fit_normalizer','def make_adding',
               'class HARClassifier','class AddingRegressor','class MyRNNCell','class MyLSTMCell','class MyGRUCell'):
    exec(next(c.source for c in nb.cells if c.source.startswith(prefix)),scope)
exec(next(c.source for c in nb.cells if c.cell_type=='code' and 'REFERENCE_CLASSES =' in c.source),scope)
exec(next(c.source for c in nb.cells if c.source.startswith('def copy_reference_weights')),scope)
scope['ADDING_BASE']=config['adding_base']
exec(next(c.source for c in nb.cells if c.source.startswith('def hidden_gradient_probe')),scope)
folder=next(p for p in Path('data/har').rglob('UCI HAR Dataset') if (p/'train/y_train.txt').is_file())
xtrain,ytrain,subjects=scope['load_har_split'](folder,'train')
x,y,subtest=scope['load_har_split'](folder,'test')
cache=Path('data/experiments/task5')/config['run_id']
runs=pd.read_csv(metrics/'har_hidden_sweep_runs.csv')
history=pd.read_csv(metrics/'har_hidden_sweep_history.csv')
predictions=pd.read_csv(metrics/'har_hidden_sweep_predictions.csv')
summary=pd.read_csv(metrics/'har_hidden_sweep_summary.csv')
assert len(runs)==24 and len(history)==240 and len(predictions)==24*2947
assert not runs.duplicated(['model','hidden_size','seed']).any()
for r in runs.itertuples():
    file=(Path('data/experiments/har')/config['har_base']['run_id']/f'{r.model}_{r.seed}.pt') if r.hidden_size==64 else cache/'har'/f'h{r.hidden_size}'/f'{r.model}_{r.seed}.pt'
    saved=torch.load(file,weights_only=True)
    model=scope['HARClassifier'](r.model,r.hidden_size).eval();model.load_state_dict(saved['state_dict'])
    ti,vi,_=scope['subject_split'](subjects,r.seed)
    mean,std=scope['fit_normalizer'](xtrain[ti])
    np.testing.assert_allclose(saved['mean'].numpy(),mean);np.testing.assert_allclose(saved['std'].numpy(),std)
    with torch.no_grad():pred=torch.cat([model(b).argmax(-1) for b in torch.from_numpy(scope['normalize'](x,mean,std)).split(128)]).numpy()
    e=predictions[(predictions.model==r.model)&(predictions.hidden_size==r.hidden_size)&(predictions.seed==r.seed)].sort_values('sample')
    np.testing.assert_array_equal(pred,e.predicted)
    np.testing.assert_allclose(accuracy_score(y,pred),r.test_acc)
    np.testing.assert_allclose(f1_score(y,pred,average='macro'),r.macro_f1)
    assert sum(p.numel() for p in model.parameters())==r.params
    hist=history[(history.model==r.model)&(history.hidden_size==r.hidden_size)&(history.seed==r.seed)]
    assert int(hist.loc[hist.val_macro_f1.idxmax(),'epoch'])==r.best_epoch==saved['best_epoch']
for r in summary.itertuples():
    g=runs[(runs.model==r.model)&(runs.hidden_size==r.hidden_size)]
    np.testing.assert_allclose([r.accuracy_mean,r.accuracy_std,r.f1_mean,r.f1_std],
                              [g.test_acc.mean(),g.test_acc.std(ddof=1),g.macro_f1.mean(),g.macro_f1.std(ddof=1)])
print('PASS: all 24 HAR sweep checkpoints, predictions, statistics and selections')
forget=pd.read_csv(metrics/'forget_bias_runs.csv');fp=pd.read_csv(metrics/'forget_bias_predictions.csv')
fh=pd.read_csv(metrics/'forget_bias_history.csv');fs=pd.read_csv(metrics/'forget_bias_summary.csv')
assert len(forget)==6 and len(fp)==6000 and len(fh)==30
for r in forget.itertuples():
    saved=torch.load(cache/'forget'/f'bias{r.forget_bias}'/f'LSTM_200_{r.seed}.pt',weights_only=True)
    assert saved['config']['effective_forget_bias']==r.forget_bias
    model=scope['AddingRegressor']('LSTM').eval();model.load_state_dict(saved['state_dict'])
    xx,yy=scope['make_adding'](1000,200,2)
    with torch.no_grad():pred=torch.cat([model(b) for b in torch.from_numpy(xx).split(128)]).numpy()
    e=fp[(fp.forget_bias==r.forget_bias)&(fp.seed==r.seed)].sort_values('sample')
    np.testing.assert_allclose(pred,e.predicted,rtol=0,atol=1e-14)
    mse=np.mean((pred.astype(np.float64)-yy.astype(np.float64))**2)
    np.testing.assert_allclose(mse,r.test_mse);assert bool(r.solved)==(mse<0.05)
    h=fh[(fh.forget_bias==r.forget_bias)&(fh.seed==r.seed)]
    assert int(h.loc[h.val_mse.idxmin(),'epoch'])==r.best_epoch
# Check paired initialization directly, before training updates can change biases.
for seed in [0,1,2]:
    torch.manual_seed(seed);zero=scope['AddingRegressor']('LSTM')
    torch.manual_seed(seed);one=scope['AddingRegressor']('LSTM')
    with torch.no_grad():
        for model,value in [(zero,0),(one,1)]:
            model.recurrent.bias_ih_l0[64:128].fill_(value);model.recurrent.bias_hh_l0[64:128].zero_()
            assert torch.all(model.recurrent.bias_ih_l0[64:128]+model.recurrent.bias_hh_l0[64:128]==value)
    for name,p in zero.named_parameters():
        other=dict(one.named_parameters())[name]
        if name=='recurrent.bias_ih_l0':
            assert torch.equal(p[:64],other[:64]) and torch.equal(p[128:],other[128:])
        else:assert torch.equal(p,other)
for r in fs.itertuples():
    g=forget[forget.forget_bias==r.forget_bias]
    np.testing.assert_allclose([r.test_mse_mean,r.test_mse_std],[g.test_mse.mean(),g.test_mse.std(ddof=1)])
    assert r.solved==int(g.solved.sum())
print('PASS: six ablation checkpoints/predictions/statistics; only initial forget biases differ in paired seeds')
grad=pd.read_csv(metrics/'hidden_gradients.csv');assert len(grad)==1800
for kind in ['RNN','LSTM','GRU']:
    for seed in [0,1,2]:
        for trained in [False,True]:
            expected=pd.DataFrame(scope['hidden_gradient_probe'](kind,seed,trained))
            actual=grad[(grad.model==kind)&(grad.seed==seed)&(grad.phase==('after' if trained else 'before'))].sort_values('t')
            np.testing.assert_allclose(actual.norm,expected.norm,rtol=1e-8,atol=1e-300)
print('PASS: all 18 gradient probes reproduced; fused-library output and parameter-gradient comparisons passed')
ledger=pd.read_csv('results.csv');selected=ledger[ledger.notes.str.contains(config['run_id'],regex=False,na=False)]
assert len(selected)==24 and selected.problem.eq('P1').all()
assert not ledger.duplicated(['problem','model','seed','notes']).any()
print('PASS: 24 new Task 5 ledger rows; six HAR width64 runs reused without duplication')
