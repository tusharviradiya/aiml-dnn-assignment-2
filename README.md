# DNN Assignment 2 — 2026aj05073

Viradiya Tushar Rajeshbhai.

Verified CPU submission: Python 3.14.4, PyTorch 2.15.0+cpu, four CPU threads.
Exact versions are in `requirements.txt`. From the extracted
`2026aj05073_DNN_Assignment/` directory:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name dnn-assignment
```

Select the `dnn-assignment` kernel in a Jupyter-compatible editor. Restart & Run All
`problem1/problem1.ipynb`, then `problem2/problem2.ipynb`; save outputs. The editor
is separate from the pinned kernel environment. Both notebooks contain all tests,
experiments and figure code. Relative paths support the extracted root or notebook
directories. Initial dataset downloads require internet: UCI HAR (~61 MB) and
Tiny Shakespeare (~1.1 MB). Data/checkpoints/environments are excluded from the ZIP.
Absent experiment caches trigger training; matching local caches replay results.
`DNN_VERIFY_CACHED_ONLY=1` rejects missing caches.

Settings: h=64, HAR encoder d=64, seeds 0/1/2 and a self-created three-token example
are disclosed assumptions because the variant table and instructor fixture were
not supplied. ID ends in 3: forget-bias 0/1 ablation. HAR uses 10 epochs; adding uses
5. The explicit CPU exception is used for the LM: d=64, two layers, context128,
four heads. Head/mask variants use five epochs plus five continuation epochs,
resetting Adam consistently from validation-selected baselines. Primary samples:
500 new characters each, temperatures 0.2/0.8/1.5, top-k20, seed700.

Measured training: baseline **44.7 CPU minutes**, LM continuations **9.13 additional
CPU minutes**; adding diagnostics **123 seconds wall time**. These scopes exclude
other execution/setup overhead. **T4 and GTX 1650 runtimes are unmeasured.** CPU
measurements are the disclosed substitute for the README's requested T4 timing.
Final validation uses historical caches; full fresh training was not repeated.

Limitations: all 36 baseline adding runs remain unsolved; LM comparisons are
single-seed. Historical optimizer/RNG states are missing; future runs save resume
snapshots. No bonus is claimed. Six content pages include the AI-use disclosure;
references occupy one excluded page.

OpenAI Codex/Codex CLI assisted with scratch implementations, pipelines, training,
tests, execution, plots, analysis/report drafting and packaging. The student
confirmed the root DOCX as the current brief permitting this assistance. Actual
AI assistance remains disclosed. Portal deadline confirmation, upload, downloaded
archive inspection and receipt retention remain student actions.
