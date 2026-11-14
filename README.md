# DNN Assignment 2 — 2026aj05073

Viradiya Tushar Rajeshbhai.

Verified on NVIDIA GeForce GTX 1650 (4 GB), driver 595.99.02, Python 3.14.4,
PyTorch 2.11.0+cu128/CUDA 12.8, four CPU threads. Exact package versions are pinned
in `requirements.txt`. CUDA package installation needs several GB of downloads;
dataset downloads need about 62 MB. From the extracted submission root:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name dnn-assignment-gpu
```

Select `dnn-assignment-gpu` in a Jupyter-compatible editor. Restart & Run All
`problem1/problem1.ipynb`, then `problem2/problem2.ipynb`; save both. Main training
automatically selects CUDA when available; `DNN_DEVICE=cuda` explicitly requires it.
Tests, gradient probes and supplemental adding diagnostics may use CPU. Paths work
from the extracted root or notebook directories. All required experiment/test code
is inside the notebooks; internal scripts and metric files are unnecessary.
Data/checkpoints/environments are excluded. Missing caches train afresh; matching
caches replay. `DNN_VERIFY_CACHED_ONLY=1` rejects missing experiment caches.

Before this presentation revision, fresh notebook executions took **96.27 minutes** total:
P1 90.22, final P2 6.05 minutes. This sums independent
fresh P1 and final P2 runs; an earlier P2 inference-optimization attempt is preserved
and excluded. Includes tests, training, evaluation, plots, CPU diagnostics and cache
benchmarks; excludes setup and staged downloads. T4 timing is unmeasured; actual
local GTX1650 timings are reported. This revision changes documentation/plots only;
its cached verification is separate from that fresh runtime.

Settings: recurrent h=64; HAR encoder d=64/two layers; seeds 0/1/2. The LM uses
standard d=128/four layers, context128, four heads. HAR:10 epochs; adding and paired forget-bias runs:50.
Odd-ID forget-bias0/1 ablation included. Head/mask baselines get five epochs and
five continuation epochs with Adam deliberately reset consistently. Primary samples
contain500 new characters each at temperatures0.2/0.8/1.5, top-k20, seed700.

Missing variant table/instructor hand fixture are handled as disclosed assumptions:
chosen sizes/seeds and a self-created three-token example. The revised adding grid solves 18/36 runs; LM ablations use one seed. The KV-cache bonus is included. Inference benchmarks use three warmups and ten paired synchronized trials, including prefill. Cache rebuilding after128 tokens preserves sliding-window positions; the500-character benchmark reports this limitation. Inference times live in CSV notes, not sec_per_epoch. Fresh runs save
optimizer/RNG resume snapshots. Six assessed report pages include the AI disclosure;
references use one excluded page. GPU checkpoint replay and package checks are
recorded in the local audit; fresh hardware may give small numerical/timing differences.

OpenAI Codex assisted with scratch implementations, pipelines, experiments, tests,
execution, plots, analysis/report drafting and packaging. Claude supplied an external review. The current assignment
permits AI assistance for scratch components. Confirm the portal's
deadline; after upload, download/open the archive and retain the receipt.
