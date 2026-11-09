"""Independently audit Task 4 checkpoints and recorded adding evidence; no training."""
from pathlib import Path
import json
import nbformat
import numpy as np
import pandas as pd
import torch
from torch import nn

folder=Path('problem1/metrics')
config=json.loads((folder/'adding_config.json').read_text())
torch.set_num_threads(config['threads'])
nb=nbformat.read('problem1/problem1.ipynb',as_version=4)
scope={'torch':torch,'nn':nn,'np':np}
for prefix in ('def make_adding','class AddingRegressor'):
    exec(next(c.source for c in nb.cells if c.source.startswith(prefix)),scope)
make_adding=scope['make_adding']
results=pd.read_csv('results.csv')
rows=results[results.notes.str.contains(config['run_id'],regex=False,na=False)]
runs=pd.read_csv(folder/'adding_runs.csv')
history=pd.read_csv(folder/'adding_history.csv')
preds=pd.read_csv(folder/'adding_predictions.csv')
summary=pd.read_csv(folder/'adding_summary.csv')
assert len(rows)==len(runs)==36
assert len(history)==180 and len(preds)==36000
assert not rows.duplicated(['model','seq_len','seed']).any()
assert rows[['test_acc','macro_f1','val_loss_nats','bits_per_char']].isna().all().all()
for row in rows.itertuples():
    file=Path('data/experiments/adding')/config['run_id']/f'{row.model}_{row.seq_len}_{row.seed}.pt'
    saved=torch.load(file,weights_only=True)
    model=scope['AddingRegressor'](row.model,config['hidden_size']).eval()
    model.load_state_dict(saved['state_dict'])
    x,y=make_adding(1000,row.seq_len,2)
    with torch.no_grad():
        prediction=torch.cat([model(batch) for batch in torch.from_numpy(x).split(config['batch_size'])]).numpy()
    evidence=preds[(preds.model==row.model)&(preds.seq_len==row.seq_len)&(preds.seed==row.seed)].sort_values('sample')
    np.testing.assert_allclose(prediction,evidence.predicted,rtol=0,atol=1e-14)
    mse=float(np.mean((prediction.astype(np.float64)-y.astype(np.float64))**2))
    np.testing.assert_allclose(row.test_mse,mse,rtol=1e-12)
    hist=history[(history.model==row.model)&(history.seq_len==row.seq_len)&(history.seed==row.seed)].sort_values('epoch')
    assert hist.epoch.tolist()==list(range(1,config['epochs']+1))
    assert saved['best_epoch']==int(hist.loc[hist.val_mse.idxmin(),'epoch'])
    assert sum(p.numel() for p in model.parameters())==row.params
    np.testing.assert_allclose(hist.train_seconds.mean(),row.sec_per_epoch)
    record=runs[(runs.model==row.model)&(runs.seq_len==row.seq_len)&(runs.seed==row.seed)].iloc[0]
    assert bool(record.solved)==(mse<0.05)
    np.testing.assert_allclose(record.baseline_mse,np.mean((y.astype(np.float64)-1)**2))
    print(f'PASS: {row.model} T={row.seq_len} seed={row.seed}: checkpoint, predictions, MSE, epoch, solved status')
for row in summary.itertuples():
    group=rows[(rows.model==row.model)&(rows.seq_len==row.seq_len)]
    assert len(group)==3
    np.testing.assert_allclose(row.test_mse_mean,group.test_mse.mean())
    np.testing.assert_allclose(row.test_mse_std,group.test_mse.std(ddof=1))
    assert row.solved==int((group.test_mse<0.05).sum())
print('PASS: all 36 adding runs and 12 summary groups audited independently')
print(summary.to_string(index=False))
