"""Restore audited ledger order only after verifying every run value is unchanged."""
from pathlib import Path
import io
import pandas as pd

baseline=Path('docs/baseline-2026-11-09/results.csv').read_text()
extra=Path('docs/review-evidence/additional-results.csv').read_text()
canonical=baseline.rstrip('\n')+'\n'+extra.split('\n',1)[1]
expected=pd.read_csv(io.StringIO(canonical))
actual=pd.read_csv('results.csv')
keys=['problem','model','seed','notes']
assert not actual.duplicated(keys).any()
pd.testing.assert_frame_equal(actual.sort_values(keys).reset_index(drop=True),
                              expected.sort_values(keys).reset_index(drop=True),
                              check_exact=False,rtol=1e-12,atol=1e-12)
Path('results.csv').write_text(canonical)
print('PASS: all values verified; baseline bytes/order and supplemental ledger restored')
