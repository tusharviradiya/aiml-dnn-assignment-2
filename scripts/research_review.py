"""Supplemental, validation-only diagnostics; never edits scratch definitions.

Run from the repository root. Baseline training/results stay unchanged. Checkpoints
are local; compact histories and an exact-schema supplemental ledger are submitted.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import math
import random
import time
import nbformat
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader, TensorDataset

OUT = Path('docs/review-evidence')
CACHE = Path('data/experiments/review')
OUT.mkdir(parents=True, exist_ok=True)
CACHE.mkdir(parents=True, exist_ok=True)
torch.set_num_threads(4)
DEVICE = torch.device('cpu')
COLUMNS = pd.read_csv('results.csv', nrows=0).columns.tolist()


def definitions(problem, prefixes):
    scope = dict(globals())
    notebook = nbformat.read(f'{problem}/{problem}.ipynb', 4)
    for prefix in prefixes:
        exec(next(c.source for c in notebook.cells if c.source.startswith(prefix)), scope)
    return scope


def seed(value):
    random.seed(value); np.random.seed(value); torch.manual_seed(value)


def save_json(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def log_run(row):
    # Append without serializing old records, preserving every baseline byte.
    target = OUT / 'additional-results.csv'
    frame = pd.DataFrame([row], columns=COLUMNS)
    if target.exists():
        old = pd.read_csv(target)
        if row['notes'] in old.notes.tolist():
            return
    frame.to_csv(target, mode='a', header=not target.exists(), index=False)
    frame.to_csv('results.csv', mode='a', header=False, index=False)


def adding():
    scope = definitions('problem1', ['def make_adding', 'class AddingRegressor'])
    make = scope['make_adding']; Model = scope['AddingRegressor']
    histories, diagnostics = [], []
    for kind in ('RNN', 'LSTM', 'GRU'):
        for mode in ('overfit', 'validation-pilot'):
            name = f'adding-{kind}-{mode}'
            cached = OUT / f'{name}.json'
            if cached.exists():
                print('CACHE', name, flush=True); continue
            seed(0)
            x, y = make(32 if mode == 'overfit' else 10000, 50, 0)
            # Independent target oracle, state reset and gradient checks.
            np.testing.assert_allclose((x[:, :, 0]*x[:, :, 1]).sum(1), y, atol=1e-7)
            model = Model(kind, 64)
            probe = torch.from_numpy(x[:4]); model.eval()
            with torch.no_grad():
                first = model(probe)
                model(torch.flip(probe, [1]))
                torch.testing.assert_close(first, model(probe), rtol=0, atol=0)
            initial = {k: v.clone() for k, v in model.state_dict().items()}
            loader = DataLoader(TensorDataset(torch.from_numpy(x), torch.from_numpy(y)),
                                batch_size=32 if mode == 'overfit' else 128,
                                shuffle=mode != 'overfit',
                                generator=torch.Generator().manual_seed(0))
            vx, vy = make(1000, 50, 1)  # NO test data generated in these pilots.
            optimizer = torch.optim.Adam(model.parameters(), lr=.001)
            best, best_epoch, best_state = float('inf'), 0, None
            history = []
            epochs = 1200 if mode == 'overfit' else 25
            start_all = time.perf_counter()
            for epoch in range(1, epochs+1):
                model.train(); total = 0.; norms = []
                started = time.perf_counter()
                for bx, by in loader:
                    optimizer.zero_grad(set_to_none=True)
                    loss = F.mse_loss(model(bx), by); assert torch.isfinite(loss)
                    loss.backward()
                    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1., error_if_nonfinite=True)
                    norms.append(float(norm)); optimizer.step(); total += float(loss.detach())*len(by)
                seconds = time.perf_counter()-started
                if mode == 'overfit' and epoch % 100 and epoch != 1:
                    continue
                model.eval()
                with torch.no_grad():
                    fitted = model(torch.from_numpy(x[:32]))
                    train32 = float(F.mse_loss(fitted, torch.from_numpy(y[:32])))
                    pred = torch.cat([model(b) for b in torch.from_numpy(vx).split(128)])
                    vmse = float(((pred.double()-torch.from_numpy(vy).double())**2).mean())
                history.append(dict(epoch=epoch, train_mse=total/len(y), train32_mse=train32,
                                    val_mse=vmse, grad_norm_mean=float(np.mean(norms)), seconds=seconds))
                if vmse < best:
                    best, best_epoch = vmse, epoch
                    best_state = copy.deepcopy(model.state_dict())
                print(name, epoch, 'train', total/len(y), 'val', vmse, flush=True)
            changed = sum(float((model.state_dict()[k]-v).square().sum()) for k,v in initial.items())
            assert changed > 0 and all(np.isfinite(r['grad_norm_mean']) for r in history)
            result = dict(model=kind, mode=mode, seed=0, T=50, lr=.001, clip=1., hidden=64,
                          epochs=epochs, batch=32 if mode=='overfit' else 128,
                          best_val_mse=best, best_epoch=best_epoch, history=history,
                          final_train32_mse=train32, changed_squared_norm=changed,
                          wall_seconds=time.perf_counter()-start_all, test_evaluated=False)
            torch.save(dict(state_dict=best_state, result=result), CACHE/f'{name}.pt')
            save_json(f'{name}.json', result)
            row = dict.fromkeys(COLUMNS)
            row.update(problem='P1', model=kind+'-diagnostic-'+mode, seed=0, seq_len=50,
                       params=sum(p.numel() for p in model.parameters()),
                       sec_per_epoch=(sum(h['seconds'] for h in history)/len(history)),
                       notes=json.dumps(dict(review='2026-11-09', diagnostic=result | {'history': []}),sort_keys=True))
            # These are training/validation diagnostics; test_mse remains empty.
            log_run(row)


def lm_scope():
    return definitions('problem2', ['def scaled_dot_product_attention', 'class MyMultiHeadAttention',
        'class MyEncoderBlock', 'def sinusoidal_positions', 'class CharacterTransformer'])


def language():
    scope=lm_scope(); Model=scope['CharacterTransformer']; Blocks=scope['CharacterBlocks']
    text=Path('data/tiny_shakespeare/input.txt').read_text(); chars=sorted(set(text))
    ids=torch.tensor([chars.index(c) for c in text]); cut=int(.9*len(ids))
    base=Path('data/experiments/problem2/13613c052b7f52c4/lm')
    # Same additional five epochs, lr and batch for all four variants. Restart Adam
    # for ALL variants: baseline optimizers were not saved. Acknowledge this confound.
    for heads,causal in ((4,True),(1,True),(8,True),(4,False)):
        name=f'lm-h{heads}-causal{int(causal)}'
        if (OUT/f'{name}.json').exists():
            print('CACHE',name,flush=True);continue
        saved=torch.load(base/f'heads{heads}_causal{int(causal)}.pt',weights_only=True)
        config=saved['config']; seed(0)
        model=Model(len(chars),config); model.load_state_dict(saved['state_dict'])
        optimizer=torch.optim.Adam(model.parameters(),lr=.001)
        train=DataLoader(Blocks(ids[:cut],128),batch_size=64,shuffle=False)
        val=DataLoader(Blocks(ids[cut:],128),batch_size=64,shuffle=False)
        def evaluate():
            model.eval(); total=0.;count=0
            with torch.no_grad():
                for x,y in val:
                    total+=float(F.cross_entropy(model(x).flatten(0,1),y.flatten(),reduction='sum'))
                    count+=y.numel()
            return total/count
        before=evaluate();best=before;best_epoch=0;best_state=copy.deepcopy(model.state_dict());history=[]
        for epoch in range(1,6):
            model.train();total=0.;count=0;start=time.perf_counter()
            for x,y in train:
                optimizer.zero_grad(set_to_none=True)
                loss=F.cross_entropy(model(x).flatten(0,1),y.flatten());assert torch.isfinite(loss)
                loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True)
                optimizer.step();total+=float(loss.detach())*y.numel();count+=y.numel()
            seconds=time.perf_counter()-start;vl=evaluate()
            history.append(dict(epoch=epoch,train_loss=total/count,val_loss=vl,seconds=seconds))
            if vl<best:best,best_epoch,best_state=vl,epoch,copy.deepcopy(model.state_dict())
            print(name,epoch,'train',total/count,'validation',vl,flush=True)
        result=dict(heads=heads,causal=causal,before=before,best_val_loss=best,best_epoch=best_epoch,
                    bits_per_char=best/math.log(2),history=history,config=config,
                    protocol='five additional epochs from validation-selected baseline; Adam reset for all variants',
                    source_sha256=hashlib.sha256(Path('problem2/problem2.ipynb').read_bytes()).hexdigest())
        torch.save(dict(state_dict=best_state,config=config,chars=chars),CACHE/f'{name}.pt')
        save_json(f'{name}.json',result)
        row=dict.fromkeys(COLUMNS)
        row.update(problem='P2',model=f'Char-Transformer-h{heads}-'+('causal' if causal else 'unmasked')+'-continued',seed=0,seq_len=128,
                   params=sum(p.numel() for p in model.parameters()),sec_per_epoch=np.mean([h['seconds'] for h in history]),
                   val_loss_nats=best,bits_per_char=best/math.log(2),
                   notes=json.dumps(dict(review='2026-11-09',**{k:v for k,v in result.items() if k!='history'}),sort_keys=True))
        log_run(row)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['adding','language'])
    {'adding':adding,'language':language}[parser.parse_args().stage]()
