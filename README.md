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

Chosen settings: **h=64, d=64, seeds 0, 1, 2**, permitted by the instructor email.
The main Transformer uses four heads; d=64 also divides the 1/4/8-head ablation.
HAR uses 10 epochs; adding uses five. The CPU LM uses two layers/context128/five
epochs; the HAR encoder uses patch8, CLS and two layers. We retain the odd-ID
LSTM initial forget-bias 0/1 ablation from the original experimental instructions.
Our own 3×2 Q/K/V example has a hand calculation verified against code.

All82 experiments total44.7 CPU training minutes, excluding evaluation,
setup, generation and profiling. **T4 runtime was not measured.**

Both full notebooks and independent audits pass. All36 adding runs remain unsolved
under five epochs; language samples are weak. The due date is Saturday14 November2026.
AI assistance, including scratch implementations, is fully disclosed. The user reports
professor permission, but the supplied clarification email does not waive the original
AI-writing prohibition: permission evidence remains an integrity condition. No optional
bonus is claimed. Portal upload/download confirmation remains external work.

`report.pdf`: six A4 content pages plus one excluded AI/reference page.
`docs/assignment-progress.md` tracks acceptance; results/decisions/logs are in `docs/`.
Quick checks: `.venv/bin/python scripts/test_verification.py` and
`.venv/bin/python scripts/test_cache_fingerprints.py` (no training).
`audit_har.py`, `audit_adding.py`, `audit_task5.py`, `audit_problem2.py` in `scripts/`
replay local checkpoints; run the notebooks first after a clean extraction.
Optional report rebuild uses system LaTeX: `scripts/build_report.py`; validate with
`scripts/validate_report.py` (Poppler tools), package with `scripts/package_submission.py`.
The generated ZIP is locally verified; portal upload/download verification is manual.
