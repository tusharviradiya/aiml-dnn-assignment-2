"""Execute Task 4 with existing dependency definitions, preserving Tasks 1–3 outputs."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
import sys

path=Path('problem1/problem1.ipynb')
original=nbformat.read(path,as_version=4)
start=next(i for i,c in enumerate(original.cells) if c.source.startswith('# Problem 1 — Task 4:'))
end=next((i for i,c in enumerate(original.cells) if i>start and c.source.startswith('# Problem 1 — Task 5:')),len(original.cells))
# Reuse setup/functions only; do not execute prior data plots or HAR experiments.
setup=[original.cells[1].source,'from torch import nn']
for prefix in ('def make_adding','import copy','def save_har_result'):
    setup.append(next(c.source for c in original.cells if c.source.startswith(prefix)))
selected=nbformat.v4.new_notebook(metadata=original.metadata)
selected.cells=[nbformat.v4.new_code_cell('\n'.join(setup))]+original.cells[start:end]
km=KernelManager(kernel_name='python3')
km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
client=NotebookClient(selected,km=km,timeout=1800,startup_timeout=30,resources={'metadata':{'path':'problem1'}})
try:
    client.execute()
finally:
    original.cells[start:end]=selected.cells[1:]
    nbformat.write(original,path)
    for cell in selected.cells:
        for output in cell.get('outputs',[]):
            if output.output_type=='stream': print(output.text,end='')
print('PASS: Task 4 executed; earlier notebook cells preserved')
