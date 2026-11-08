"""Execute and save the notebook, using the invoking Python environment."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
import sys

path = Path('problem1/problem1.ipynb')
nb = nbformat.read(path, as_version=4)
nbformat.validate(nb)
km = KernelManager(kernel_name='python3')
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(nb, km=km, timeout=600, resources={'metadata': {'path': 'problem1'}})
try:
    client.execute()
finally:
    nbformat.write(nb, path)
for cell in nb.cells:
    for output in cell.get('outputs', []):
        if output.output_type == 'stream':
            print(output.text, end='')
assert not any(o.output_type == 'error' for c in nb.cells for o in c.get('outputs', []))
print('PASS: notebook completed top to bottom; outputs saved')
