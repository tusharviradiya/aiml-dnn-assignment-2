# DNN Programming Assignment 2 — 2026aj05073

Python 3.10+ and PyTorch 2.x; tested with Python 3.14.4 on CPU (four threads).
Exact tested versions are in `requirements.txt`. From this repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
MPLCONFIGDIR=.cache/matplotlib JUPYTER_RUNTIME_DIR=.cache/jupyter .venv/bin/python scripts/execute_problem1.py
MPLCONFIGDIR=.cache/matplotlib JUPYTER_RUNTIME_DIR=.cache/jupyter .venv/bin/python scripts/execute_problem2.py
```

Alternatively open each notebook with this environment's kernel and Restart & Run
All. Both notebooks support the repository root or their own directory as working
directory. The first run downloads only official UCI HAR (~61 MB) and Tiny
Shakespeare (~1.1 MB). Internet is needed initially. Data/checkpoints stay in ignored
`data/`; matching completed runs are reused, and `results.csv` is saved after each
run. Set the notebook's `FORCE_*_RERUN` flag to retrain.

Variant: ID ends in 3, so the individual ablation is LSTM effective forget bias 0
versus 1. The assignment's variants table is absent: recurrent h=64 and seeds 0/1/2
are provisional. CPU language model uses the expressly allowed d=64/two-layer
exception, context 128 and four heads. HAR Transformer uses patch 8, CLS, d=64 and
two layers. Fixed budgets: HAR10 epochs; adding and language models5 epochs.

Problem 1 Tasks 1–5 are verified. Problem 2 Tasks 2–5 are verified; attention tests pass,
with only the instructor hand fixture pending. P2 training took10.22 CPU minutes
excluding evaluation/setup; T4 runtime is **not measured**. All 36 adding runs remain unsolved under the five-epoch budget. The
instructor's hand-attention example is missing; an illustrative fixture is clearly
labelled. Final report/PDF and submission ZIP are pending. AI assistance is
disclosed under the professor permission reported by the user.

Verification (no training): `scripts/test_verification.py`,
`scripts/audit_har.py`, `scripts/audit_adding.py`, `scripts/audit_task5.py`,
and `scripts/audit_problem2.py`, using `.venv/bin/python`.
`execute_checks.py problem1 --strict` or `problem2 --strict` runs and saves component
checks. Targeted P1 runners: `execute_adding.py` and `execute_task5.py`.
Details, actual results and assumptions: `docs/assignment-progress.md`,
`docs/development-log.md`, `docs/decisions.md`, and `docs/task*-results.md`.
