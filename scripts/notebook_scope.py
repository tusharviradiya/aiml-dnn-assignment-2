"""Read-only loaders for notebook definitions and existing experiment metadata.

No notebook setup/experiment cells execute: imports and definitions alone are loaded.
Dataset/checkpoint absence is an error here, never a download or training request.
"""
from pathlib import Path
import ast
import copy
import hashlib
import json
import math
import os
import random
import time
import urllib.request
import zipfile
import nbformat
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset,DataLoader,TensorDataset
from sklearn.metrics import accuracy_score,f1_score


def load_definitions(problem,scope=None):
    scope=dict(globals()) | dict(ROOT=Path('.'),DATA=Path('data'),METRICS=Path(problem)/'metrics',FIGURES=Path(problem)/'figures') | (scope or {})
    notebook=nbformat.read(Path(problem)/f'{problem}.ipynb',4)
    for cell in notebook.cells:
        if cell.cell_type!='code':continue
        tree=ast.parse(cell.source)
        nodes=[node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
        if nodes:exec(compile(ast.Module(body=nodes,type_ignores=[]),str(problem)+'/definitions','exec'),scope)
    return scope


def problem2_scope():
    root=Path('.');metrics=root/'problem2/metrics'
    protocol=json.loads((metrics/'config.json').read_text())
    s=load_definitions('problem2',dict(ROOT=root,DATA=root/'data',METRICS=metrics,FIGURES=root/'problem2/figures',
        DEVICE=torch.device(protocol['device']),HAR_CONFIG=protocol['har'],LM_CONFIG=protocol['lm'],
        SEEDS=(0,1,2),CODE_HASH=protocol['code_hash'],RUN_ID=protocol['run_id'],P2_RESULTS={},
        RESULT_COLUMNS=pd.read_csv('results.csv',nrows=0).columns.tolist(),
        CHANNELS=('body_acc_x','body_acc_y','body_acc_z','body_gyro_x','body_gyro_y','body_gyro_z',
                  'total_acc_x','total_acc_y','total_acc_z')))
    notebook=nbformat.read('problem2/problem2.ipynb',4)
    actual=hashlib.sha256('\n'.join(c.source for c in notebook.cells if 'cache_dependency' in c.metadata.get('tags',[])).encode()).hexdigest()
    hash_cell=next(c.source for c in notebook.cells if c.source.startswith('# Hash only declared dependency'))
    aliases=next(n.value for n in ast.parse(hash_cell).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCE_HASH_ALIASES' for t in n.targets))
    assert ast.literal_eval(aliases).get(actual,actual)==protocol['code_hash']
    folder=next(p for p in Path('data/har').rglob('UCI HAR Dataset') if (p/'train/y_train.txt').is_file())
    s['x_train_raw'],s['y_train_raw'],s['subjects_train']=s['load_har_split'](folder,'train')
    s['x_test_raw'],s['y_test'],s['subjects_test']=s['load_har_split'](folder,'test')
    text=Path('data/tiny_shakespeare/input.txt').read_text();chars=sorted(set(text));stoi={c:i for i,c in enumerate(chars)}
    ids=torch.tensor([stoi[c] for c in text]);cut=int(.9*len(ids))
    s.update(text=text,chars=chars,stoi=stoi,train_ids=ids[:cut],val_ids=ids[cut:],
             P2_CACHE=root/'data/experiments/problem2'/protocol['run_id'])
    return s
