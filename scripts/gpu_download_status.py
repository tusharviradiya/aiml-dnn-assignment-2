"""Inspect retained CUDA wheel bytes; this command never uses the network."""
from pathlib import Path
import json
base=Path('.cache/gpu-wheels');manifest=json.loads((base/'manifest.json').read_text())
received=0;complete=[]
for _,name,size,_ in manifest:
 target=base/name
 if target.is_file() and target.stat().st_size==size:
  received+=size;complete.append(name)
 else:
  parts=base/(name+'.parts')
  if parts.is_dir():received+=sum(min(p.stat().st_size,8*1024*1024,size-int(p.name)) for p in parts.iterdir() if p.is_file() and p.name.isdecimal())
total=sum(item[2] for item in manifest)
print(json.dumps({'retained_GB':round(received/1e9,3),'total_GB':round(total/1e9,3),'remaining_GB':round((total-received)/1e9,3),'percent':round(100*received/total,1),'complete_wheels':len(complete),'total_wheels':len(manifest)},indent=2))
