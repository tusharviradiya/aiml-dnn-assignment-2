# DNN Programming Assignment 2 — 2026aj05073

Viradiya Tushar Rajeshbhai. Tested: Python 3.14.4, PyTorch 2.15.0+cpu, four
CPU threads; exact dependencies are pinned in `requirements.txt`.

From the repository/submission root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/execute_problem1.py
.venv/bin/python scripts/execute_problem2.py
```

Alternatively open each notebook with this environment's kernel and Restart & Run
All. Both run from the root or their own directory; outputs are saved. On restricted
hosts, set `MPLCONFIGDIR=.cache/matplotlib` and
`JUPYTER_RUNTIME_DIR=.cache/jupyter`. The first run downloads only official HAR
(~61 MB) and Shakespeare (~1.1 MB); internet is needed initially. Ignored `data/`
holds raw data/checkpoints; the submission contains neither. Runs save `results.csv`
after completion and reuse exact matching caches. Set notebook `FORCE_*_RERUN`
flags to retrain. Exact reviewed legacy-cache aliases are documented in decisions.

Variant: odd ID selects LSTM initial effective forget bias0 versus1. The missing
variants table requires provisional recurrent h64/seeds0/1/2. HAR uses10 epochs;
adding uses5. CPU language model follows the permitted d64/two-layer exception,
context128/four heads/five epochs. HAR encoder uses patch8, CLS, d64/two layers.

All82 experiments total44.7 CPU training minutes, excluding evaluation,
setup, generation and profiling. **T4 runtime was not measured.**

Both full notebooks pass; independent checkpoint/sample audits pass. All36 adding
runs remain unsolved under five epochs; language samples are weak. P2 attention
passes tests, but the missing instructor hand fixture remains pending; our worked
example is explicitly illustrative. Variant values and portal/deadline confirmation
also remain outstanding. AI assistance is disclosed in the report under professor
permission reported by the user. No optional bonus is claimed.

`report.pdf`: six A4 content pages plus one excluded AI/reference page.
`docs/assignment-progress.md` tracks acceptance; results/decisions/logs are in `docs/`.
Quick checks: `.venv/bin/python scripts/test_verification.py` and
`.venv/bin/python scripts/test_cache_fingerprints.py` (no training).
`audit_har.py`, `audit_adding.py`, `audit_task5.py`, `audit_problem2.py` in `scripts/`
replay local checkpoints; run the notebooks first after a clean extraction.
Optional report rebuild uses system LaTeX: `scripts/build_report.py`; validate with
`scripts/validate_report.py` (Poppler tools), package with `scripts/package_submission.py`.
The generated ZIP is locally verified; portal upload/download verification is manual.
