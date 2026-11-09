"""Run Task 5 using existing definitions and data; preserve prior outputs."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

path=Path('problem1/problem1.ipynb')
original=nbformat.read(path,as_version=4)
start=next(i for i,c in enumerate(original.cells) if c.source.startswith('# Problem 1 — Task 5:'))
setup=[original.cells[1].source]
for prefix in ('from torch import nn','import copy','def download_har','def load_har_split','def subject_split','def fit_normalizer',
               'def make_adding','def copy_reference_weights','class MyRNNCell','class MyLSTMCell','class MyGRUCell',
               'class HARClassifier','def evaluate_har','def save_har_result','def run_har(',
               'class AddingRegressor','def evaluate_adding','def run_adding('):
    setup.append(next(c.source for c in original.cells if c.cell_type=='code' and (c.source.startswith(prefix) or (prefix=='from torch import nn' and 'REFERENCE_CLASSES =' in c.source))))
setup.append("HAR_DIR=download_har()\nx_train_raw,y_train_raw,subjects_train=load_har_split(HAR_DIR,'train')\nx_test_raw,y_test,subjects_test=load_har_split(HAR_DIR,'test')")
selected=nbformat.v4.new_notebook(metadata=original.metadata)
selected.cells=[nbformat.v4.new_code_cell('\n'.join(setup))]+original.cells[start:]
km=KernelManager(kernel_name='python3')
km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
client=NotebookClient(selected,km=km,timeout=1800,startup_timeout=30,resources={'metadata':{'path':'problem1'}})
try:client.execute()
finally:
    original.cells[start:]=selected.cells[1:]
    nbformat.write(original,path)
    for cell in selected.cells:
        for output in cell.get('outputs',[]):
            if output.output_type=='stream':print(output.text,end='')
print('PASS: Task 5 executed; prior outputs preserved')
