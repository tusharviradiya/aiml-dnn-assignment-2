"""Run the extracted submission with explicitly reused local data/checkpoints.

Run package_submission.py first. This verifies portability and full notebook
integration; it does not claim an uncached download/retraining test.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import nbformat

root=Path('.').resolve()
record=json.loads((root/'.cache/submission-verification.json').read_text())
extracted=Path(record['extraction'])
assert extracted.is_dir() and extracted.is_relative_to(root/'.cache/submission-check')
assert hashlib.sha256((root/record['archive']).read_bytes()).hexdigest()==record['sha256']
manifest=json.loads((extracted/'submission-manifest.json').read_text())
for name,metadata in manifest['files'].items():
    assert hashlib.sha256((extracted/name).read_bytes()).hexdigest()==metadata['sha256']
# This local-only relative symlink is not stored in the archive.
local_data=extracted/'data'
assert not local_data.exists(), 'Use a fresh extraction to rerun this verification'
local_data.symlink_to(os.path.relpath(root/'data',extracted),target_is_directory=True)
environment={**os.environ,'MPLCONFIGDIR':'.cache/matplotlib','JUPYTER_RUNTIME_DIR':'.cache/jupyter'}
commands=['scripts/test_verification.py','scripts/test_cache_fingerprints.py',
          'scripts/execute_problem1.py','scripts/execute_problem2.py',
          'scripts/audit_har.py','scripts/audit_adding.py','scripts/audit_task5.py','scripts/audit_problem2.py']
for script in commands:
    log=root/'.cache'/('extracted-'+Path(script).stem+'.log')
    print('VERIFY',script,'log:',log.relative_to(root),flush=True)
    with log.open('w') as output:
        completed=subprocess.run([sys.executable,script],cwd=extracted,env=environment,stdout=output,stderr=subprocess.STDOUT)
    if completed.returncode:
        raise RuntimeError(f'{script} failed; see {log.relative_to(root)}')
for problem in ('problem1','problem2'):
    before=nbformat.read(root/problem/f'{problem}.ipynb',4)
    after=nbformat.read(extracted/problem/f'{problem}.ipynb',4)
    assert [c.source for c in before.cells]==[c.source for c in after.cells]
result=dict(passed=True,mode='extracted full notebooks/audits with explicitly reused local data/checkpoints',
            archive_sha256=record['sha256'],extraction=str(extracted),commands=commands)
(root/'.cache/extracted-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: extracted notebooks and all audits; same source; no .git required; local cache reuse explicitly scoped')
