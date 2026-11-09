"""Hash evidence before/after independent audits; any mutation fails this verifier."""
from pathlib import Path
import hashlib,json,os,subprocess,sys

def snapshot():
 paths=[Path('results.csv'),Path('report.pdf'),Path('problem2/generated_samples.txt')]
 for folder in ('problem1','problem2','docs/review-evidence','data/experiments'):
  paths.extend(p for p in Path(folder).rglob('*') if p.is_file())
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

if __name__=='__main__':
 commands=['scripts/test_verification.py','scripts/test_cache_fingerprints.py','scripts/test_reproducibility.py',
           'scripts/audit_har.py','scripts/audit_adding.py','scripts/audit_task5.py','scripts/audit_problem2.py','scripts/review_checks.py','scripts/normalize_review_ledger.py']
 before=snapshot();records=[]
 for script in commands:
  log=Path('.cache/repro-work')/(Path(script).stem+'.log')
  print('READ-ONLY VERIFY',script,flush=True)
  with log.open('w') as output:
   result=subprocess.run([sys.executable,script],stdout=output,stderr=subprocess.STDOUT,
                         env={**os.environ,'MPLCONFIGDIR':'.cache/matplotlib'})
  records.append(dict(script=script,exit_code=result.returncode,log=str(log)))
  if result.returncode:raise RuntimeError(f'{script} failed: {log}')
 after=snapshot()
 changed=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)]
 assert not changed,changed
 Path('.cache/readonly-audits.json').write_text(json.dumps(dict(passed=True,files_hashed=len(before),commands=records,evidence_sha256=before),indent=2)+'\n')
 print('PASS: all nine audits; no checked evidence was created, removed or rewritten')
