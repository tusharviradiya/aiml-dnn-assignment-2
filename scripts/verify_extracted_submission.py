"""Execute only the two packaged notebooks, with explicitly reused local caches.

No helper file is copied into extraction. Fresh training is guarded off. This tests
self-contained portability and saved evidence, not a clean download/training run.
"""
from pathlib import Path
import hashlib,json,os,sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
root=Path('.').resolve()
record=json.loads((root/'.cache/submission-verification.json').read_text())
extracted=root/record['extraction']
assert extracted.is_relative_to(root/'.cache/submission-check')
assert hashlib.sha256((root/record['archive']).read_bytes()).hexdigest()==record['sha256']
for name,m in record['manifest'].items():assert hashlib.sha256((extracted/name).read_bytes()).hexdigest()==m['sha256']
assert not any((extracted/name).exists() for name in ('scripts','docs','problem1/metrics','problem2/metrics'))
local_data=extracted/'data';assert not local_data.exists()
local_data.symlink_to(os.path.relpath(root/'data',extracted),target_is_directory=True)
os.environ.update(DNN_VERIFY_CACHED_ONLY='1',MPLCONFIGDIR=str(root/'.cache/matplotlib'),JUPYTER_RUNTIME_DIR=str(root/'.cache/jupyter'))
results_before=(extracted/'results.csv').read_bytes()
samples_before=(extracted/'problem2/generated_samples.txt').read_bytes()
counts={}
for problem in ('problem1','problem2'):
 path=extracted/problem/f'{problem}.ipynb';notebook=nbformat.read(path,4)
 first=next(c for c in notebook.cells if c.cell_type=='code');source=first.source
 first.source="import torch\ndef _reject_training(*args, **kwargs):\n    raise RuntimeError('Cached-only extraction: attempted training')\ntorch.optim.Adam=_reject_training\n"+source
 manager=KernelManager(kernel_name='python3')
 manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
 client=NotebookClient(notebook,km=manager,timeout=600,resources={'metadata':{'path':str(extracted/problem)}})
 try:client.execute()
 finally:first.source=source
 nbformat.write(notebook,path)
 cells=[c for c in notebook.cells if c.cell_type=='code']
 assert [c.execution_count for c in cells]==list(range(1,len(cells)+1))
 assert not any(o.output_type=='error' for c in cells for o in c.outputs)
 original=nbformat.read(root/problem/f'{problem}.ipynb',4)
 assert [c.source for c in notebook.cells]==[c.source for c in original.cells]
 counts[problem]=len(cells)
 print('PASS packaged',problem,len(cells),'cells',flush=True)
assert (extracted/'results.csv').read_bytes()==results_before
assert (extracted/'problem2/generated_samples.txt').read_bytes()==samples_before
assert (extracted/'report.pdf').read_bytes()==(root/'report.pdf').read_bytes()
for problem in ('problem1','problem2'):
 # Recomputed deterministic figures must be byte-identical; timing is replayed.
 for name in record['manifest']:
  if name.startswith(problem+'/figures/'):
   assert (extracted/name).read_bytes()==(root/name).read_bytes(),name
result=dict(passed=True,mode='minimal ZIP, self-contained notebooks, reused local data/checkpoints, Adam guard, no fresh training',
            archive_sha256=record['sha256'],code_cells=counts,exact_csv_samples_and_figures=True,extraction=str(extracted))
(root/'.cache/extracted-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: minimal extraction executes without excluded helpers; CSV, samples and all included figures reproduced exactly')
