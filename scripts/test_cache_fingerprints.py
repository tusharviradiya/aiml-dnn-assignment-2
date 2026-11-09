"""Check that plots/outputs reuse reviewed caches and training edits invalidate them."""
from pathlib import Path
import hashlib
import json
import tempfile
import nbformat

notebook=nbformat.read('problem1/problem1.ipynb',4)
helper=next(c.source for c in notebook.cells if c.source.startswith('def experiment_fingerprint'))
config=json.loads(Path('problem1/metrics/adding_config.json').read_text())
expected=config.pop('run_id')
prefixes=('from pathlib import Path','def make_adding','class AddingRegressor','def evaluate_adding',
          'def run_adding(','def save_har_result','def experiment_fingerprint')
Path('.cache').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir='.cache') as folder:
    root=Path(folder);(root/'problem1/metrics').mkdir(parents=True)
    path=root/'problem1/problem1.ipynb';nbformat.write(notebook,path)
    (root/'problem1/metrics/cache_aliases.json').write_text(Path('problem1/metrics/cache_aliases.json').read_text())
    scope=dict(ROOT=root,nbformat=nbformat,hashlib=hashlib,json=json)
    exec(helper,scope);fingerprint=scope['experiment_fingerprint']
    assert fingerprint(config,prefixes)==expected
    assert fingerprint({**config,'lr':.002},prefixes)!=expected
    notebook.cells.append(nbformat.v4.new_markdown_cell('Extra analysis: no training source change.'))
    notebook.cells[1].execution_count=999
    nbformat.write(notebook,path);assert fingerprint(config,prefixes)==expected
    cell=next(c for c in notebook.cells if c.source.startswith('class AddingRegressor'))
    cell.source+='\n# Deliberate dependency change for invalidation test.'
    nbformat.write(notebook,path);assert fingerprint(config,prefixes)!=expected
print('PASS reviewed cache reuse; config/training changes invalidate; plots/outputs do not')
