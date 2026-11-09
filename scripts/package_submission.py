"""Create, reopen and extract the prescribed student-ID submission ZIP.

No datasets, checkpoints, virtual environment, Git metadata or caches are included.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import zipfile
import nbformat
import pandas as pd

STUDENT='2026aj05073'
FOLDER=f'{STUDENT}_DNN_Assignment'
OUTPUT=Path(f'{FOLDER}.zip')
required=['README.md','requirements.txt','report.pdf','results.csv','problem1/problem1.ipynb',
          'problem2/problem2.ipynb','problem2/generated_samples.txt']
files=[Path(name) for name in required]
for directory in ('docs','scripts','problem1/figures','problem1/metrics','problem2/figures','problem2/metrics'):
    files.extend(p for p in Path(directory).rglob('*') if p.is_file() and
                 p.suffix in ('.md','.tex','.py','.json','.csv','.png','.npz','.txt'))
files=sorted(set(files))
assert all(p.is_file() and not p.is_symlink() for p in files)
assert all(not set(p.parts)&{'data','.venv','.git','.cache','__pycache__'} for p in files)
assert all(p.suffix not in ('.pt','.pth','.ckpt','.docx','.zip') for p in files)
for path in (Path('problem1/problem1.ipynb'),Path('problem2/problem2.ipynb')):
    notebook=nbformat.read(path,4);nbformat.validate(notebook)
    cells=[c for c in notebook.cells if c.cell_type=='code']
    assert all(c.execution_count is not None for c in cells)
    assert not any(o.output_type=='error' for c in cells for o in c.outputs)
ledger=pd.read_csv('results.csv')
assert len(ledger)==92 and ledger.problem.value_counts().to_dict()=={'P1':75,'P2':17}
assert not ledger.duplicated(['problem','model','seed','notes']).any()
assert len(Path('README.md').read_text().split())<=550, 'README exceeds one-page word budget'
info=subprocess.check_output(['pdfinfo','report.pdf'],text=True)
assert 'Pages:           7' in info and '(A4)' in info
manifest=dict(student_id=STUDENT,content_pages=6,excluded_pages=1,
              files={p.as_posix():dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files})
with zipfile.ZipFile(OUTPUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for path in files:archive.write(path,f'{FOLDER}/{path.as_posix()}')
    archive.writestr(f'{FOLDER}/submission-manifest.json',json.dumps(manifest,indent=2)+'\n')
assert OUTPUT.stat().st_size<=25_000_000
# Extract into a fresh named location; never remove a previous check directory.
check_parent=Path('.cache')/'submission-check'
check_parent.mkdir(parents=True,exist_ok=True)
import tempfile
check=Path(tempfile.mkdtemp(prefix='check-',dir=check_parent))
with zipfile.ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    for name in archive.namelist():
        path=PurePosixPath(name)
        assert not path.is_absolute() and '..' not in path.parts and path.parts[0]==FOLDER
    archive.extractall(check)
extracted=check/FOLDER
for name,record in manifest['files'].items():
    path=extracted/name
    assert path.stat().st_size==record['bytes']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
for name in required:assert (extracted/name).is_file()
assert (extracted/'problem1/figures').is_dir() and (extracted/'problem2/figures').is_dir()
fonts=subprocess.check_output(['pdffonts',str(extracted/'report.pdf')],text=True)
for line in fonts.splitlines()[2:]:
    if line.strip():assert 'yes' in line, 'Unembedded PDF font'
verification=dict(archive=str(OUTPUT),bytes=OUTPUT.stat().st_size,files=len(files)+1,
                  extraction=str(extracted),sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                  crc_passed=True,all_file_hashes_passed=True)
Path('.cache/submission-verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification,indent=2))
