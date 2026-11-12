"""Independent cache correctness and benchmark/ledger reconciliation; never trains."""
from pathlib import Path
import json,hashlib
import numpy as np,pandas as pd,torch
from notebook_scope import problem2_scope
s=problem2_scope();root=Path('.')
saved=torch.load('data/experiments/review/lm-h4-causal1.pt',map_location='cpu',weights_only=True)
model=s['CharacterTransformer'](65,saved['config']).to(s['DEVICE']).eval();model.load_state_dict(saved['state_dict'])
s['verify_kv_cache'](model)
# Use distinct batch contents to detect accidental cache broadcasting.
with torch.inference_mode():
 ids=torch.stack((torch.arange(137,device=s['DEVICE'])%65,(torch.arange(137,device=s['DEVICE'])+7)%65)).long()
 cache=s['CachedCharacterGenerator'](model);cache.prefill(ids[:,:64]);max_abs=0.;max_scaled=0.
 for end in range(65,138):
  got=cache.decode_step(ids[:,end-1:end])[:,-1]
  expected=model(ids[:,max(0,end-128):end])[:,-1]
  max_abs=max(max_abs,float((got-expected).abs().max()))
  max_scaled=max(max_scaled,float(((got-expected).abs()/(1e-5+1e-5*expected.abs())).max()))
  torch.testing.assert_close(got,expected,atol=1e-5,rtol=1e-5)
print('PASS distinct batch inputs, incremental positions and rolling rebuilds; max absolute error',max_abs,'fraction of combined FP32 tolerance',max_scaled)
raw=json.loads(Path('problem2/metrics/kv_benchmark.json').read_text())
assert raw['request']['checkpoint_sha256']==hashlib.sha256(Path('data/experiments/review/lm-h4-causal1.pt').read_bytes()).hexdigest()
ledger=pd.read_csv('results.csv');rows=ledger[ledger.notes.str.contains('kv-cache-benchmark',regex=False,na=False)]
assert len(rows)==8 and len(raw['trials'])==8
for r in raw['trials']:
 times=np.array(r['timing_seconds']);assert len(times)==10 and (times>0).all()
 np.testing.assert_allclose([r['mean_seconds'],r['std_seconds'],r['tokens_per_second']],
                          [times.mean(),times.std(ddof=1),r['new_characters']/times.mean()],rtol=1e-12)
 ids=torch.tensor([[s['stoi'][c] for c in r['prompt']]],device=s['DEVICE'])
 out=s['greedy_decode'](model,ids,r['new_characters'],r['cached'])
 assert hashlib.sha256(out.cpu().numpy().tobytes()).hexdigest()==r['output_sha256']
 match=[json.loads(n) for n in rows.notes if json.loads(n)['prompt_length']==r['prompt_length'] and json.loads(n)['new_characters']==r['new_characters'] and json.loads(n)['cached']==r['cached']]
 assert len(match)==1 and match[0]['timing_seconds']==r['timing_seconds']
 other=next(a for a in raw['trials'] if a['prompt_length']==r['prompt_length'] and a['new_characters']==r['new_characters'] and a['cached']!=r['cached'])
 ratio=other['mean_seconds']/r['mean_seconds'] if r['cached'] else r['mean_seconds']/other['mean_seconds']
 np.testing.assert_allclose(ratio,r['speedup'],rtol=1e-12)
 assert pd.isna(rows[rows.notes.apply(lambda n:json.loads(n)['cached']==r['cached'])].sec_per_epoch).all()
# An unmasked model cannot reuse causal caches.
config=dict(saved['config'],causal=False)
try:s['CachedCharacterGenerator'](s['CharacterTransformer'](65,config).to(s['DEVICE']).eval())
except ValueError:pass
else:raise AssertionError('Unmasked model accepted')
print('PASS KV cache independent logits, greedy output hashes, all raw trials/aggregates/CSV rows and invalid-mode checks')
