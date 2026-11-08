"""Run prepared verification sections and save outputs without rerunning HAR.

Successful execution means infrastructure ran, not that pending student work passed.
Use --strict to require all selected custom implementations to pass.
"""
import argparse
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('problem', choices=['problem1', 'problem2'])
parser.add_argument('--strict', action='store_true')
args = parser.parse_args()
path = Path(args.problem) / f'{args.problem}.ipynb'
original = nbformat.read(path, as_version=4)
nbformat.validate(original)
start = 0
if args.problem == 'problem1':
    start = next(i for i, c in enumerate(original.cells)
                 if c.cell_type == 'markdown' and c.source.startswith('# Problem 1 — Task 2:'))
selected = nbformat.v4.new_notebook(metadata=original.metadata)
selected.cells = [nbformat.v4.new_code_cell('import torch')] + original.cells[start:]
if args.strict:
    function = 'require_task2_complete' if args.problem == 'problem1' else 'require_problem2_components'
    selected.cells.append(nbformat.v4.new_code_cell(f'print({function}())'))
km = KernelManager(kernel_name='python3')
km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(selected, km=km, timeout=180, startup_timeout=30,
                        resources={'metadata': {'path': args.problem}})
try:
    client.execute()
finally:
    original.cells[start:] = selected.cells[1:1+len(original.cells)-start]
    nbformat.write(original, path)
    for cell in selected.cells:
        for output in cell.get('outputs', []):
            if output.output_type == 'stream':
                print(output.text, end='')
print('Verification section executed; PENDING entries remain incomplete.')
