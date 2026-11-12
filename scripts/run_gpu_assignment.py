"""Run both notebooks sequentially, record wall time and save every cell output."""
from pathlib import Path
import os,sys,time,json,subprocess
import nbformat,torch
from nbclient import NotebookClient
from jupyter_client import KernelManager
os.environ['DNN_DEVICE']='cuda'
os.environ.pop('DNN_VERIFY_CACHED_ONLY',None)
assert torch.cuda.is_available()
root=Path.cwd()
record={'gpu':torch.cuda.get_device_name(0),'torch':str(torch.__version__),'scope':'Complete notebook execution excluding environment setup and dataset download','runs':{}}
(root/'gpu-environment.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
for problem in ('problem1','problem2'):
 path=root/problem/f'{problem}.ipynb';nb=nbformat.read(path,4)
 km=KernelManager(kernel_name='python3');km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
 def saved(cell,cell_index,**kwargs):
  nbformat.write(nb,path)
  print(problem,'cell',cell_index,'complete',flush=True)
 client=NotebookClient(nb,km=km,timeout=None,startup_timeout=60,resources={'metadata':{'path':str(path.parent)}},on_cell_executed=saved)
 start=time.perf_counter();status='failed'
 try:
  client.execute();status='passed'
 finally:
  nbformat.write(nb,path)
  record['runs'][problem]={'status':status,'seconds':time.perf_counter()-start}
  (root/'gpu-runtime.json').write_text(json.dumps(record,indent=2))
 print(problem,status,flush=True)
