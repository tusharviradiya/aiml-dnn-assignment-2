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
import os
_first_code = next(c for c in notebook.cells if c.cell_type == 'code')
_original_source = _first_code.source
if os.environ.get('DNN_VERIFY_CACHED_ONLY') == '1':
    _first_code.source = ("import torch\ndef _reject_training(*args, **kwargs):\n    raise RuntimeError('Verification-only run: cache miss would retrain; aborting')\ntorch.optim.Adam = _reject_training\n" + _original_source)
try:
    client.execute()
finally:
    _first_code.source = _original_source
    nbformat.write(notebook, path)
    for cell in notebook.cells:
        for output in cell.get('outputs', []):
            if output.output_type == 'stream': print(output.text, end='')
assert not any(o.output_type == 'error' for c in notebook.cells for o in c.get('outputs', []))
print('PASS: Problem 2 notebook executed top to bottom; outputs saved')
