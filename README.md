# DNN Programming Assignment 2

Task 1 and the three recurrent cells are implemented; Transformer components and experiments remain pending. See `docs/assignment-progress.md` for rubric tracking.

## Environment and execution

Test environment: Python 3.14.4, CPU PyTorch 2.x; exact versions in `requirements.txt`.
From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
MPLCONFIGDIR=.cache/matplotlib JUPYTER_RUNTIME_DIR=.cache/jupyter .venv/bin/python scripts/execute_problem1.py
```

Alternatively open `problem1/problem1.ipynb` with this environment's kernel and Restart & Run All. Internet is required for the first official HAR download (~61 MB); cached data lives in ignored `data/`. The notebook works from the root or `problem1/` directory. Outputs and the class-balance figure are saved. Problem 2 contains interfaces and reference checks only.

Student ID: 2026aj05073; odd-ID forget-bias ablation. Variant table missing: provisional hidden size 64 and split/model seeds 0/1/2. Adding-data seeds are fixed by the assignment. T4 total runtime: not measured; training has not begun. Final report, student-ID packaging and generated language samples remain pending. AI assistance and assumptions are recorded in `docs/decisions.md`.

## Targeted checks (no Task 1 rerun)

```sh
.venv/bin/python scripts/test_verification.py
.venv/bin/python scripts/execute_checks.py problem1
.venv/bin/python scripts/execute_checks.py problem2
```

These save verification outputs and report pending student work honestly. Add `--strict`
to require custom components to pass (Problem 1 passes; Problem 2 remains pending). See `docs/student-work-map.md` for the remaining student-authored work.
