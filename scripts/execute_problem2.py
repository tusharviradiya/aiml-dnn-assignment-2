"""Execute all Problem 2 cells with the invoking environment and save outputs."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

path = Path('problem2/problem2.ipynb')
notebook = nbformat.read(path, as_version=4)
nbformat.validate(notebook)
manager = KernelManager(kernel_name='python3')
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(notebook, km=manager, timeout=3600, startup_timeout=30,
                        resources={'metadata': {'path': 'problem2'}})
try:
    client.execute()
finally:
    nbformat.write(notebook, path)
    for cell in notebook.cells:
        for output in cell.get('outputs', []):
            if output.output_type == 'stream': print(output.text, end='')
assert not any(o.output_type == 'error' for c in notebook.cells for o in c.get('outputs', []))
print('PASS: Problem 2 notebook executed top to bottom; outputs saved')
