"""Audit the final independently fresh P2 execution, then package the combined revision."""
import sys,time,json,subprocess
from pathlib import Path
stage=Path('.cache/improvement-p2-final')
initial=json.loads((stage/'gpu-runtime.json').read_text())['source_hashes']['problem2']
# The copied runtime initially describes the first P2 attempt. Wait for new source evidence.
while True:
 r=json.loads((stage/'gpu-runtime.json').read_text())
 if r['source_hashes']['problem2']!=initial:
  assert r['runs']['problem2']['status']=='passed','Final P2 execution failed'
  break
 time.sleep(5)
logdir=Path('.cache/improvement-run')
for script in ['promote_final_problem2','audit_problem2','audit_kv_cache','build_gpu_report','validate_gpu_submission','check_improvement_readme','package_submission','verify_extracted_submission','write_improvement_audit']:
 print('START',script,flush=True)
 with (logdir/(script+'.log')).open('w') as f:r=subprocess.run([sys.executable,'scripts/'+script+'.py'],stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(script+' failed; inspect log')
 print('PASS',script,flush=True)
print('ALL FINAL REVISION CHECKS PASSED',flush=True)
