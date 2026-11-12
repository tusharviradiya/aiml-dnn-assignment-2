from pathlib import Path
import json,shutil,hashlib
import pandas as pd
root=Path('.');stage=root/'.cache/improvement-run'
runtime=json.loads((stage/'gpu-runtime.json').read_text());assert len(runtime['runs'])==2 and all(v['status']=='passed' for v in runtime['runs'].values())
assert runtime['fresh_experiments']
for p in ('problem1','problem2'):
 shutil.copytree(stage/p,root/p,dirs_exist_ok=True)
for p in ('experiments','measurements'):shutil.copytree(stage/'data'/p,root/'data'/p,dirs_exist_ok=True)
for p in ('results.csv','gpu-runtime.json','gpu-environment.txt'):shutil.copy2(stage/p,root/p)
a=pd.read_csv('problem1/metrics/adding_runs.csv');assert len(a)==36
assert json.loads(Path('problem1/metrics/adding_config.json').read_text())['epochs']==50
assert len(pd.read_csv('results.csv'))==100
minutes=sum(v['seconds'] for v in runtime['runs'].values())/60
p=Path('README.md');s=p.read_text();start=s.index('A successful fresh run took');end=s.index('\nSettings:',start)
s=s[:start]+f'''A successful fresh run took **{minutes:.2f} minutes** total: Problem 1
{runtime['runs']['problem1']['seconds']/60:.2f} and Problem 2 {runtime['runs']['problem2']['seconds']/60:.2f} minutes.
This includes tests, training, evaluation, plots, CPU diagnostics and KV-cache
benchmarks; excludes package installation and staged dataset downloads. T4 timing
is unmeasured; these are actual local GTX 1650 measurements.
'''+s[end:]
s=s.replace('HAR:10 epochs; adding:5.','HAR:10 epochs; adding and paired forget-bias runs:50.')
s=s.replace('All36 adding grid runs\nremain unsolved; LM ablations use one seed. No bonus is claimed.',f"The revised adding grid solves {int(a.solved.sum())}/36 runs; LM ablations use one seed. The KV-cache bonus is included.")
s=s.replace('Fresh runs save','Inference benchmarks use three warmups and ten paired synchronized trials, including prefill. Cache rebuilding after128 tokens preserves sliding-window positions; the500-character benchmark reports this limitation. Inference times live in CSV notes, not sec_per_epoch. Fresh runs save')
s=s.replace('The current assignment\npermits AI assistance', 'Claude supplied an external review. The current assignment\npermits AI assistance')
p.write_text(s)
print('Promoted complete fresh execution',minutes,'minutes, solved',int(a.solved.sum()))
