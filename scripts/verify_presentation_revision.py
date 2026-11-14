"""Bind presentation edits to the preserved fresh run without relabeling its timing."""
from pathlib import Path
import ast
import hashlib
import json
import zipfile
import nbformat

BASELINE_SHA = '3f3a21ecbccf46cc608f36ffd40a812a60d9465314d55d3aa860f28e99a62fc3'
BACKUP = Path('.cache/presentation-revision-2026-11-13')
MANIFEST = Path('docs/presentation-revision.json')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def code_hash(notebook):
    return hashlib.sha256('\n'.join(c.source for c in notebook.cells if c.cell_type == 'code').encode()).hexdigest()

def verify(check_evidence=True):
    record = json.loads(MANIFEST.read_text())
    archive = BACKUP/'2026aj05073_DNN_Assignment.zip'
    assert sha(archive) == record['baseline_archive_sha256'] == BASELINE_SHA
    runtime = json.loads(Path('gpu-runtime.json').read_text())
    assert sha('gpu-runtime.json') == record['fresh_runtime_sha256'] == sha(BACKUP/'gpu-runtime.json')
    changed = {}
    with zipfile.ZipFile(archive) as z:
        for problem, allowed in (('problem1', [50]), ('problem2', [77])):
            before = nbformat.reads(z.read(f'2026aj05073_DNN_Assignment/{problem}/{problem}.ipynb').decode(), 4)
            after = nbformat.read(f'{problem}/{problem}.ipynb', 4)
            assert len(before.cells) == len(after.cells)
            assert code_hash(before) == runtime['source_hashes'][problem]
            assert code_hash(after) == record['revised_source_hashes'][problem]
            changed[problem] = [i for i,(a,b) in enumerate(zip(before.cells,after.cells))
                                if a.cell_type == 'code' and a.source != b.source]
            assert changed[problem] == allowed, changed
            for a,b in zip(before.cells,after.cells):
                assert a.cell_type == b.cell_type and a.metadata.get('tags',[]) == b.metadata.get('tags',[])
            if problem == 'problem1':
                assert [i for i,(a,b) in enumerate(zip(before.cells,after.cells)) if a.cell_type=='markdown' and a.source!=b.source] == [67,112]
                old_alias = ast.literal_eval(ast.parse(before.cells[50].source).body[0].value)
                new_alias = ast.literal_eval(ast.parse(after.cells[50].source).body[0].value)
                assert set(new_alias)-set(old_alias) == {'d67adbf8b29e3f05'}
                assert all(new_alias[k]==v for k,v in old_alias.items())
                assert new_alias['d67adbf8b29e3f05']['run_id'] == '0957de1893d476b8'
                # Markdown participates in this historical hash. Executable dependencies remain identical.
                config=json.loads(Path('problem1/metrics/task5_config.json').read_text());config.pop('run_id')
                start=112;end=next(i for i,c in enumerate(after.cells) if c.source.startswith('# Supplemental adding diagnostics'))
                deps=[c.source for c in after.cells if c.source.startswith(('def run_har(', 'def run_adding(', 'class HARClassifier','class AddingRegressor'))]
                digest=hashlib.sha256((json.dumps(config,sort_keys=True)+'\n'.join(deps+[c.source for c in after.cells[start:end]])).encode()).hexdigest()[:16]
                assert digest == 'd67adbf8b29e3f05'
                for i in range(start,end):
                    if before.cells[i].cell_type=='code': assert before.cells[i].source==after.cells[i].source
            else:
                definitions=ast.parse(after.cells[77].source).body
                assert len(definitions)==1 and isinstance(definitions[0],ast.FunctionDef) and definitions[0].name=='render_report_figures'
    if check_evidence:
        snapshot=json.loads((BACKUP/'evidence-before.json').read_text())
        exceptions={'problem1/metrics/cache_aliases.json'}
        for name,digest in snapshot.items():
            if name not in exceptions: assert sha(name)==digest, f'Experimental evidence changed: {name}'
        # Replay may materialize the one reviewed compatibility entry, nothing else.
        old=json.loads((BACKUP/'problem1/metrics/cache_aliases.json').read_text())
        new=json.loads(Path('problem1/metrics/cache_aliases.json').read_text())
        assert new==old or (set(new)-set(old)=={'d67adbf8b29e3f05'} and all(new[k]==v for k,v in old.items())
                           and new['d67adbf8b29e3f05']==new_alias['d67adbf8b29e3f05'])
        for folder in ('data','problem1/metrics','problem2/metrics'):
            assert {str(p) for p in Path(folder).rglob('*') if p.is_file()} == {p for p in snapshot if p.startswith(folder+'/')}, f'New evidence in {folder}'
    print('PASS presentation-only revision: baseline fresh hashes retained; exact alias/plot edits only; measurements unchanged')
    return changed

if __name__=='__main__':
    verify()
