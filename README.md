# DNN Programming Assignment 2

Problem 1 Tasks 1–3 are implemented and verified; Task 4 adding experiments are implemented and verified; later experiments and Transformer implementations remain pending. See `docs/assignment-progress.md` for rubric tracking.

## Environment and execution

Test environment: Python 3.14.4, CPU PyTorch 2.x; exact versions in `requirements.txt`.
From the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
MPLCONFIGDIR=.cache/matplotlib JUPYTER_RUNTIME_DIR=.cache/jupyter .venv/bin/python scripts/execute_problem1.py
```

Alternatively open `problem1/problem1.ipynb` with this environment's kernel and Restart & Run All. Internet is required for the first official HAR download (~61 MB); cached data lives in ignored `data/`. The notebook works from the root or `problem1/` directory. Notebook outputs, HAR figures and metrics are saved. Matching completed HAR runs are cached under ignored data/experiments; set FORCE_HAR_RERUN=True in the notebook to retrain. Problem 2 contains interfaces and reference checks only.

Student ID: 2026aj05073; odd-ID forget-bias ablation. Variant table missing: provisional hidden size 64 and split/model seeds 0/1/2. Adding-data seeds are fixed by the assignment. T4 runtime: not measured. Nine 10-epoch HAR runs completed on CPU; training totaled about 124 seconds, excluding validation and setup. Final report, student-ID packaging and generated language samples remain pending. AI assistance and assumptions are recorded in `docs/decisions.md`.

## Targeted checks (no Task 1 rerun)

```sh
.venv/bin/python scripts/test_verification.py
.venv/bin/python scripts/audit_har.py
.venv/bin/python scripts/execute_adding.py
.venv/bin/python scripts/audit_adding.py
.venv/bin/python scripts/execute_checks.py problem1
.venv/bin/python scripts/execute_checks.py problem2
```

These save verification outputs and report pending student work honestly. Add `--strict`
to require custom components to pass (Problem 1 passes; Problem 2 remains pending). See `docs/student-work-map.md` for the remaining student-authored work.

Task 4 uses five epochs per run on CPU; results may remain unsolved under this short budget. The targeted adding runner preserves earlier outputs and reuses its matching completed runs.
 Adding training took 25.3 CPU minutes excluding evaluation/setup; all 36 runs remained unsolved.
