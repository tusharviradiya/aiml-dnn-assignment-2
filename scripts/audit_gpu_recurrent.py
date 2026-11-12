"""Recompute recurrent predictions on the recorded device; never trains."""
from pathlib import Path
import json
import nbformat,numpy as np,pandas as pd,torch
from torch import nn
from sklearn.metrics import accuracy_score,f1_score
root=Path('.');metrics=root/'problem1/metrics'
protocol=json.loads((metrics/'har_config.json').read_text());device=torch.device(protocol['device'])
assert device.type=='cuda' and torch.cuda.is_available()
torch.set_num_threads(protocol['threads']);torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
nb=nbformat.read('problem1/problem1.ipynb',4);scope=dict(torch=torch,nn=nn,np=np)
for prefix in ('class HARClassifier','class AddingRegressor','def make_adding'):
 exec(next(c.source for c in nb.cells if c.source.startswith(prefix)),scope)
channels=('body_acc_x','body_acc_y','body_acc_z','body_gyro_x','body_gyro_y','body_gyro_z','total_acc_x','total_acc_y','total_acc_z')
har=next(p for p in (root/'data/har').rglob('UCI HAR Dataset') if (p/'train/y_train.txt').is_file())
x=np.stack([np.loadtxt(har/f'test/Inertial Signals/{c}_test.txt',dtype=np.float32) for c in channels],axis=-1)
y=np.loadtxt(har/'test/y_test.txt',dtype=np.int64)-1
train_x=np.stack([np.loadtxt(har/f'train/Inertial Signals/{c}_train.txt',dtype=np.float32) for c in channels],axis=-1)
subjects=np.loadtxt(har/'train/subject_train.txt',dtype=np.int64)
ledger=pd.read_csv('results.csv');preds=pd.read_csv(metrics/'har_predictions.csv');history=pd.read_csv(metrics/'har_history.csv')
rows=ledger[(ledger.problem=='P1')&ledger.notes.str.contains(protocol['run_id'],regex=False,na=False)]
assert len(rows)==9
for row in rows.itertuples():
 file=root/'data/experiments/har'/protocol['run_id']/f'{row.model}_{row.seed}.pt'
 saved=torch.load(file,map_location='cpu',weights_only=True)
 held=np.random.default_rng(row.seed).choice(np.unique(subjects),4,replace=False);tr=train_x[~np.isin(subjects,held)]
 np.testing.assert_allclose(saved['mean'].numpy(),tr.mean((0,1),keepdims=True,dtype=np.float64))
 np.testing.assert_allclose(saved['std'].numpy(),tr.std((0,1),keepdims=True,dtype=np.float64))
 model=scope['HARClassifier'](row.model,protocol['hidden_size']).to(device).eval();model.load_state_dict(saved['state_dict'])
 normalized=torch.from_numpy(((x-saved['mean'].numpy())/saved['std'].numpy()).astype(np.float32))
 with torch.no_grad():pred=torch.cat([model(b.to(device)).argmax(-1).cpu() for b in normalized.split(protocol['batch_size'])]).numpy()
 evidence=preds[(preds.model==row.model)&(preds.seed==row.seed)].sort_values('sample')
 np.testing.assert_array_equal(pred,evidence.predicted);np.testing.assert_array_equal(y,evidence.true)
 assert abs(accuracy_score(y,pred)-row.test_acc)<1e-12 and abs(f1_score(y,pred,average='macro')-row.macro_f1)<1e-12
 epochs=history[(history.model==row.model)&(history.seed==row.seed)].sort_values('epoch')
 assert epochs.epoch.tolist()==list(range(1,protocol['epochs']+1))
 assert int(epochs.loc[epochs.val_macro_f1.idxmax(),'epoch'])==saved['best_epoch']
 assert sum(p.numel() for p in model.parameters())==row.params
 np.testing.assert_allclose(epochs.train_seconds.mean(),row.sec_per_epoch,atol=1e-12)
 print('PASS GPU HAR',row.model,row.seed,flush=True)
config=json.loads((metrics/'adding_config.json').read_text());preds=pd.read_csv(metrics/'adding_predictions.csv');history=pd.read_csv(metrics/'adding_history.csv')
rows=ledger[(ledger.problem=='P1')&ledger.notes.str.contains(config['run_id'],regex=False,na=False)]
assert len(rows)==36
for row in rows.itertuples():
 file=root/'data/experiments/adding'/config['run_id']/f'{row.model}_{row.seq_len}_{row.seed}.pt'
 saved=torch.load(file,map_location='cpu',weights_only=True)
 model=scope['AddingRegressor'](row.model,config['hidden_size']).to(device).eval();model.load_state_dict(saved['state_dict'])
 x,y=scope['make_adding'](1000,row.seq_len,2)
 with torch.no_grad():pred=torch.cat([model(b.to(device)).cpu() for b in torch.from_numpy(x).split(config['batch_size'])]).numpy()
 evidence=preds[(preds.model==row.model)&(preds.seq_len==row.seq_len)&(preds.seed==row.seed)].sort_values('sample')
 np.testing.assert_allclose(pred,evidence.predicted,atol=1e-7,rtol=1e-6)
 mse=np.mean((pred.astype(np.float64)-y.astype(np.float64))**2)
 np.testing.assert_allclose(mse,row.test_mse,atol=1e-8,rtol=1e-6)
 epochs=history[(history.model==row.model)&(history.seq_len==row.seq_len)&(history.seed==row.seed)].sort_values('epoch')
 assert epochs.epoch.tolist()==list(range(1,config['epochs']+1))
 assert int(epochs.loc[epochs.val_mse.idxmin(),'epoch'])==saved['best_epoch']
 assert sum(p.numel() for p in model.parameters())==row.params
 np.testing.assert_allclose(epochs.train_seconds.mean(),row.sec_per_epoch,atol=1e-12)
 print('PASS GPU adding',row.model,row.seq_len,row.seed,flush=True)
print('PASS independently reproduced all nine HAR and 36 adding checkpoints')
