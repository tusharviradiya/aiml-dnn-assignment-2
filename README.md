# DNN Assignment 2 — 2026aj05073

Viradiya Tushar Rajeshbhai. Tested on Python 3.14.4 / PyTorch 2.15.0+cpu,
four CPU threads; exact versions are in `requirements.txt`. Python 3.10+ is
required by the assignment; the pinned environment was tested on 3.14.4.

From the extracted submission root:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name dnn-assignment
```

Open `problem1/problem1.ipynb`, select that kernel, Restart & Run All; then do
the same for `problem2/problem2.ipynb`. All experiment, test and report-figure
code is in those two notebooks. No internal scripts, reviews or metric files
are required. Run Problem 1 first. Relative paths work from the root or each
notebook directory. Outputs are saved in the supplied notebooks; save again
after execution. Initial downloads require internet: official UCI HAR (~61 MB)
and Tiny Shakespeare (~1.1 MB). Only the prescribed datasets are used.

**Chosen settings: h=64, d=64, seeds 0, 1, 2.** These are freely chosen under
the instructor's size/seed clarification. CPU LM: two layers, context128,
four heads (the assignment CPU exception). HAR runs use10 epochs; the
required36-run adding grid uses5. The odd-ID initial LSTM forget-bias0/1
ablation is retained. The three-token attention example is self-created.

The primary LM is the four-head causal continuation: five extra epochs from
its selected five-epoch baseline, with Adam reset for every continued variant.
`problem2/generated_samples.txt` contains its three500-new-character samples
at temperatures0.2/0.8/1.5, top-k20, prompt `ROMEO:\n`, sampling seed700.
Baseline head/mask comparisons retain matched initialization and budgets;
continuations, validation-only adding pilots and test results are labelled separately.
The CSV's92 rows retain82 baseline runs,6 adding diagnostics and4 continuations.

Matching local `data/` checkpoints replay results; absent caches trigger fresh
training. Set `DNN_VERIFY_CACHED_ONLY=1` to abort on a missing cache. Fresh runs
regenerate metrics, figures and samples; timings vary by hardware. Historical
runs lack optimizer/RNG states. Future training saves separate resume snapshots.
Raw data/checkpoints are excluded as required; cached replay requires local
caches. Full uncached reproduction was not repeated for this release.

Measured original training totals44.7 CPU minutes; LM continuation adds9.13
training minutes and adding diagnostics123 seconds wall time, excluding other
execution/validation overhead. **T4 runtime was not measured.** All36 original
adding runs are unsolved; the single-seed LM remains limited. No bonus claimed.
The report has six A4 content pages plus an excluded AI-use/reference page.
AI assistance is accurately disclosed there. Portal upload, download/open
verification and receipt remain external steps.
