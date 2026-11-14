"""Refresh saved notebook outputs using matching caches; Adam cannot be constructed."""
from pathlib import Path
import hashlib,json,os,sys,time
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from verify_presentation_revision import verify

root=Path('.').resolve()
verify()
os.environ.update(DNN_VERIFY_CACHED_ONLY='1',MPLCONFIGDIR=str(root/'.cache/matplotlib'),JUPYTER_RUNTIME_DIR=str(root/'.cache/jupyter'))
record={'mode':'cached replay with Adam construction rejected; not a fresh training/runtime measurement','runs':{}}
for problem in ('problem1','problem2'):
    path=root/problem/f'{problem}.ipynb';notebook=nbformat.read(path,4)
    first=next(c for c in notebook.cells if c.cell_type=='code');source=first.source
    first.source="import torch\ndef _reject_training(*args, **kwargs):\n    raise RuntimeError('Presentation verification: attempted training')\ntorch.optim.Adam=_reject_training\n"+source
    manager=KernelManager(kernel_name='python3')
    manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
    client=NotebookClient(notebook,km=manager,timeout=600,startup_timeout=30,resources={'metadata':{'path':str(root/problem)}})
    start=time.perf_counter()
    try: client.execute()
    finally: first.source=source
    nbformat.write(notebook,path)
    cells=[c for c in notebook.cells if c.cell_type=='code']
    assert [c.execution_count for c in cells]==list(range(1,len(cells)+1))
    assert not any(o.output_type=='error' for c in cells for o in c.outputs)
    record['runs'][problem]={'passed':True,'code_cells':len(cells),'replay_seconds':time.perf_counter()-start}
    print('PASS root cached replay',problem,record['runs'][problem],flush=True)
verify()
Path('.cache/presentation-replay.json').write_text(json.dumps(record,indent=2)+'\n')
