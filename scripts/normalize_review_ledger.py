"""Check canonical historical ledger bytes. Explicit repair is a separate opt-in mutation."""
from pathlib import Path
import argparse,datetime,io
import pandas as pd
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--restore-order',action='store_true',help='Back up and normalize ordering only after every value matches')
args=parser.parse_args()
baseline=Path('docs/baseline-2026-11-09/results.csv').read_text()
extra=Path('docs/review-evidence/additional-results.csv').read_text()
canonical=baseline.rstrip('\n')+'\n'+extra.split('\n',1)[1]
expected=pd.read_csv(io.StringIO(canonical));actual=pd.read_csv('results.csv')
keys=['problem','model','seed','notes'];assert not actual.duplicated(keys).any()
pd.testing.assert_frame_equal(actual.sort_values(keys).reset_index(drop=True),
                              expected.sort_values(keys).reset_index(drop=True),check_exact=False,rtol=1e-12,atol=1e-12)
if args.restore_order:
 backup=Path('data/ledger-backups');backup.mkdir(parents=True,exist_ok=True)
 name=datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f')+'.csv'
 (backup/name).write_bytes(Path('results.csv').read_bytes())
 Path('results.csv').write_text(canonical)
 print('REPAIRED: values unchanged; original bytes backed up at',backup/name)
else:
 assert Path('results.csv').read_bytes()==canonical.encode(),'Ordering/serialization differs; check provenance before any explicit repair'
 print('PASS: all values and canonical bytes verified read-only; nothing rewritten')
