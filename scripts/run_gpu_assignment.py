"""Run both notebooks sequentially, record wall time and save every cell output."""
from pathlib import Path
import os,sys,time,json,subprocess,hashlib
import nbformat,torch
from nbclient import NotebookClient
from jupyter_client import KernelManager
class LoggedNotebookClient(NotebookClient):
    def process_message(self, msg, cell, cell_index):
        if msg.get('msg_type') == 'stream':
            content=msg.get('content', {})
            print(content.get('text',''),end='',flush=True)
        return super().process_message(msg,cell,cell_index)

os.environ['DNN_DEVICE']='cuda'
os.environ.pop('DNN_VERIFY_CACHED_ONLY',None)
assert torch.cuda.is_available()
root=Path.cwd()
assert '1650' in torch.cuda.get_device_name(0)
assert not list((root/'data/experiments').rglob('*.json')), 'Fresh benchmark requires no existing experiment results; preserve prior evidence in a separate workspace'
assert list((root/'data/har').rglob('y_train.txt')), 'Stage local raw HAR data before benchmarking'
assert (root/'data/tiny_shakespeare').is_dir(), 'Stage local raw text before benchmarking'
source_hashes={p:hashlib.sha256('\n'.join(c.source for c in nbformat.read(root/p/f'{p}.ipynb',4).cells if c.cell_type=='code').encode()).hexdigest() for p in ('problem1','problem2')}
record={'gpu':torch.cuda.get_device_name(0),'torch':str(torch.__version__),'scope':'Complete notebook execution excluding environment setup and dataset download','source_hashes':source_hashes,'fresh_experiments':True,'runs':{}}
(root/'gpu-environment.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
for problem in ('problem1','problem2'):
 path=root/problem/f'{problem}.ipynb';nb=nbformat.read(path,4)
 km=KernelManager(kernel_name='python3');km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
 def saved(cell,cell_index,**kwargs):
  nbformat.write(nb,path)
  print(problem,'cell',cell_index,'complete',flush=True)
 client=LoggedNotebookClient(nb,km=km,timeout=None,startup_timeout=60,resources={'metadata':{'path':str(path.parent)}},on_cell_executed=saved)
 start=time.perf_counter();status='failed'
 try:
  client.execute();status='passed'
 finally:
  nbformat.write(nb,path)
  record['runs'][problem]={'status':status,'seconds':time.perf_counter()-start}
  (root/'gpu-runtime.json').write_text(json.dumps(record,indent=2))
 print(problem,status,flush=True)
