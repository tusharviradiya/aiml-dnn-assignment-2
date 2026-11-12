"""Fresh final P2 run; preserve independent successful P1 runtime and first P2 attempt."""
from pathlib import Path
import json,hashlib,sys,time,os,subprocess
import nbformat,torch
from nbclient import NotebookClient
from jupyter_client import KernelManager
os.environ['DNN_DEVICE']='cuda';os.environ.pop('DNN_VERIFY_CACHED_ONLY',None)
root=Path.cwd();assert torch.cuda.is_available() and not list((root/'data/experiments').rglob('*.json'))
p=root/'problem2/problem2.ipynb';n=nbformat.read(p,4)
r=json.loads((root/'gpu-runtime.json').read_text());r['previous_problem2_attempt']=dict(r['runs'].pop('problem2'),evidence='.cache/improvement-run')
r['scope']='Sum of independent fresh complete P1 and final P2 notebook executions; excludes environment setup, staged downloads and preserved earlier P2 optimization attempt'
r['source_hashes']['problem2']=hashlib.sha256('\n'.join(c.source for c in n.cells if c.cell_type=='code').encode()).hexdigest()
km=KernelManager(kernel_name='python3');km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
class Logged(NotebookClient):
 def process_message(self,msg,cell,cell_index):
  if msg.get('msg_type')=='stream':print(msg.get('content',{}).get('text',''),end='',flush=True)
  return super().process_message(msg,cell,cell_index)
start=time.perf_counter();status='failed'
try:Logged(n,km=km,timeout=None,startup_timeout=60,resources={'metadata':{'path':str(p.parent)}}).execute();status='passed'
finally:
 nbformat.write(n,p);r['runs']['problem2']=dict(status=status,seconds=time.perf_counter()-start)
 (root/'gpu-runtime.json').write_text(json.dumps(r,indent=2)+'\n')
print('Final P2',status,flush=True)
