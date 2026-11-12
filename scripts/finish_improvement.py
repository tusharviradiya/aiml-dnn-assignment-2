"""Wait for successful fresh execution, then audit and package the revision."""
from pathlib import Path
import json,subprocess,sys,time
root=Path('.').absolute();stage=root/'.cache/improvement-run';record=stage/'gpu-runtime.json'
while True:
 if record.exists():
  runtime=json.loads(record.read_text())
  if any(v['status']=='failed' for v in runtime['runs'].values()):raise RuntimeError('Fresh execution failed; inspect execution.log')
  if len(runtime['runs'])==2 and all(v['status']=='passed' for v in runtime['runs'].values()):break
 time.sleep(10)
for script in ['promote_improvement','audit_gpu_recurrent','audit_task5','audit_problem2','audit_kv_cache','build_gpu_report','validate_gpu_submission','package_submission','verify_extracted_submission']:
 print('START',script,flush=True)
 with (stage/(script+'.log')).open('w') as f:
  r=subprocess.run([sys.executable,'scripts/'+script+'.py'],stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(script+' failed; inspect its log')
 print('PASS',script,flush=True)
print('ALL REVISION CHECKS PASSED',flush=True)
