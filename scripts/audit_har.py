"""Independently reconcile saved HAR evidence and reproduce checkpoint predictions.

Run from repository root after notebook experiments. Requires ignored dataset/cache.
Does not train or alter results.
"""
from pathlib import Path
import json
import nbformat
import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.metrics import accuracy_score, f1_score

folder = Path('problem1/metrics')
config = json.loads((folder / 'har_config.json').read_text())
torch.set_num_threads(config['threads'])
nb = nbformat.read('problem1/problem1.ipynb', as_version=4)
scope = {'torch': torch, 'nn': nn}
exec(next(c.source for c in nb.cells if c.source.startswith('class HARClassifier')), scope)
model_class = scope['HARClassifier']
channels = ('body_acc_x','body_acc_y','body_acc_z','body_gyro_x','body_gyro_y','body_gyro_z',
            'total_acc_x','total_acc_y','total_acc_z')
root = next(p for p in Path('data/har').rglob('UCI HAR Dataset') if (p/'train/y_train.txt').is_file())
x = np.stack([np.loadtxt(root/'test/Inertial Signals'/f'{c}_test.txt',dtype=np.float32) for c in channels],axis=-1)
y = np.loadtxt(root/'test/y_test.txt',dtype=np.int64)-1
train_x = np.stack([np.loadtxt(root/'train/Inertial Signals'/f'{c}_train.txt',dtype=np.float32) for c in channels],axis=-1)
subjects = np.loadtxt(root/'train/subject_train.txt',dtype=np.int64)
results = pd.read_csv('results.csv')
rows = results[results.notes.str.contains(config['run_id'], regex=False, na=False)]
history = pd.read_csv(folder/'har_history.csv')
predictions = pd.read_csv(folder/'har_predictions.csv')
runs = pd.read_csv(folder/'har_runs.csv')
summary = pd.read_csv(folder/'har_summary.csv',index_col='model')
assert len(rows) == len(runs) == 9
assert not rows.duplicated(['model','seed']).any()
assert len(history) == 90 and len(predictions) == 9*2947
assert rows[['test_mse','val_loss_nats','bits_per_char']].isna().all().all()
for row in rows.itertuples():
    saved = torch.load(Path('data/experiments/har')/config['run_id']/f'{row.model}_{row.seed}.pt',weights_only=True)
    held = np.random.default_rng(row.seed).choice(np.unique(subjects),4,replace=False)
    training = train_x[~np.isin(subjects,held)]
    np.testing.assert_allclose(saved['mean'].numpy(),training.mean((0,1),keepdims=True,dtype=np.float64))
    np.testing.assert_allclose(saved['std'].numpy(),training.std((0,1),keepdims=True,dtype=np.float64))
    model = model_class(row.model,config['hidden_size']).eval()
    model.load_state_dict(saved['state_dict'])
    normalized = torch.from_numpy(((x-saved['mean'].numpy())/saved['std'].numpy()).astype(np.float32))
    with torch.no_grad():
        pred = torch.cat([model(batch).argmax(-1) for batch in normalized.split(config['batch_size'])]).numpy()
    evidence = predictions[(predictions.model==row.model)&(predictions.seed==row.seed)].sort_values('sample')
    np.testing.assert_array_equal(pred,evidence.predicted)
    np.testing.assert_array_equal(y,evidence.true)
    assert abs(accuracy_score(y,pred)-row.test_acc)<1e-12
    assert abs(f1_score(y,pred,average='macro')-row.macro_f1)<1e-12
    epochs = history[(history.model==row.model)&(history.seed==row.seed)].sort_values('epoch')
    assert epochs.epoch.tolist()==list(range(1,11))
    selected_epoch = int(epochs.loc[epochs.val_macro_f1.idxmax(),'epoch'])
    assert selected_epoch==saved['best_epoch']
    assert abs(epochs.train_seconds.mean()-row.sec_per_epoch)<1e-12
    assert sum(p.numel() for p in model.parameters())==row.params
    print(f'PASS: {row.model} seed {row.seed}: checkpoint predictions, train-only stats, metrics, selection and timing')
for kind in summary.index:
    group=rows[rows.model==kind]
    for metric,prefix in [('test_acc','accuracy'),('macro_f1','macro_f1')]:
        np.testing.assert_allclose(summary.loc[kind,prefix+'_mean'],group[metric].mean())
        np.testing.assert_allclose(summary.loc[kind,prefix+'_std'],group[metric].std(ddof=1))
print('PASS: all nine runs independently reconciled with recorded evidence')
print(summary.to_string())
