# DNN Assignment 2 — 2026aj05073

Viradiya Tushar Rajeshbhai.

AI assistance during development included earlier scratch-code drafts, pipelines, experiments, tests, debugging, plots, analysis/report drafting, verification and packaging. The student reports manually implementing the final scratch components; this review verifies correctness, not personal authorship. The latest supplied assignment removes the earlier AI-use restriction and declaration requirement; AI permission is reported by the student.

Tested: Python 3.14.4, PyTorch 2.15.0+cpu, four CPU threads. Exact package versions
are in `requirements.txt`; the assignment requires Python 3.10 or later.
From the extracted `2026aj05073_DNN_Assignment/` directory:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name dnn-assignment
```

Open `problem1/problem1.ipynb` in a Jupyter-compatible notebook editor, select
`dnn-assignment`, and Restart & Run All; then repeat for `problem2/problem2.ipynb`.
Save both notebooks after execution. The editor is separate from the pinned kernel
environment. All experiment, test and figure code is inside the notebooks;
internal scripts and metric files are unnecessary. Paths work from the extracted
root or notebook directories. Initial downloads need internet: UCI HAR (~61 MB)
and Tiny Shakespeare (~1.1 MB).

**Settings:** h=64, d=64, seeds 0, 1, 2 and a self-created three-token example are explicit assumptions under the DOCX missing-information clause: its referenced variant table and instructor example were not supplied. The official
CPU exception allows the two-layer d=64 LM (context 128, four heads).
HAR uses 10 epochs; the 36-run adding grid uses 5. The odd-ID forget-bias 0/1
ablation is included.

The primary four-head causal LM continues its selected five-epoch baseline for
five extra epochs, resetting Adam for every continued variant. Its three samples
have 500 new characters each, temperatures 0.2/0.8/1.5, top-k 20, prompt
`ROMEO:\n`, and sampling seed 700. The 92 CSV rows comprise 82 baseline runs,
6 validation-only adding diagnostics and 4 LM continuations.

Matching local `data/` caches replay results; absent caches trigger training.
Set `DNN_VERIFY_CACHED_ONLY=1` to fail on missing caches. Data, checkpoints and
environments are excluded from the ZIP. Fresh execution regenerates metrics,
figures and samples; hardware timings vary. Historical optimizer/RNG states are
missing; future runs save resume snapshots. The pinned dependencies were freshly installed in a separate environment;
`pip check` passed. Both notebooks were verified there using existing experiment
caches. Full uncached training was not repeated.

Measured baseline training: 44.7 CPU minutes; LM continuation: 9.13 additional
training minutes; adding diagnostics: 123 seconds wall time. Other execution
and validation overhead is excluded. **T4 runtime is unmeasured**, leaving that
README requirement unmet. All 36 original adding runs are unsolved; LM evidence
is single-seed. No bonus is claimed. The PDF has six assessed A4 pages plus one
excluded references-only page. Portal upload, download/open verification
and receipt remain outstanding.
