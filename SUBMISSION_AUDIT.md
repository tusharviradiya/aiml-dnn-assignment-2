# Final verified submission — 13 November 2026 presentation revision

Archive: `2026aj05073_DNN_Assignment.zip`; 1,893,436 bytes; 16 required files.
SHA-256: `ffff31c5ebcd06578282917e85a7d7acfa7de86f5cd387e555951f6efcc858f3`.

Viradiya Tushar Rajeshbhai, 2026aj05073. Local NVIDIA GeForce GTX1650 (4GB); PyTorch2.11.0+cu128. T4 timing was not measured. The actual local GPU timing is disclosed. AI assistance, including permitted scratch components, is explicitly disclosed in report.pdf.

Fresh complete execution: P1 5413.090s; P2 362.981s; total 96.27min. Includes training, tests, evaluation, plots, CPU diagnostics and KV benchmark; excludes environment setup and staged dataset downloads. No P1 training caches or final P2 training caches were reused. P1 and final P2 are independently fresh notebook runs; the earlier preserved P2 optimization attempt is excluded from the total. The original fresh code hashes remain bound to the preserved baseline ZIP. The current submission changes only report plotting, an exact Task5 Markdown-fingerprint compatibility entry and documentation; it was verified separately by cached-only replay with Adam blocked. gpu-runtime.json is unchanged. See docs/presentation-revision.json and scripts/verify_presentation_revision.py for the reviewed source difference and unchanged-measurement checks.

Current verdict: **READY TO SUBMIT**. The [final rubric review](FINAL_SUBMISSION_REVIEW.md) records all changes, qualified estimates and test evidence. No new training was run for this presentation revision. The final archive also passed isolated extraction: both notebooks executed without internal helpers; CSV, samples and all packaged figures reproduced exactly.

## Revised adding evidence

All36 primary runs and six paired forget-bias runs completed50 epochs under the frozen protocol. All first-five-epoch train/validation histories match the previous GPU grid exactly. Validation selects checkpoints; test MSE determines solved counts. Earlier test results had already been observed, so this is disclosed as follow-up work, not a new untouched holdout.

| Model | T | Test MSE mean | Sample std | Solved/3 |
|---|---:|---:|---:|---:|
| GRU | 50 | 0.000238 | 0.000058 | 3 |
| GRU | 100 | 0.000581 | 0.000057 | 3 |
| GRU | 200 | 0.000493 | 0.000190 | 3 |
| GRU | 400 | 0.001764 | 0.000396 | 3 |
| LSTM | 50 | 0.002012 | 0.000542 | 3 |
| LSTM | 100 | 0.025186 | 0.031006 | 2 |
| LSTM | 200 | 0.168243 | 0.000256 | 0 |
| LSTM | 400 | 0.153601 | 0.000043 | 0 |
| RNN | 50 | 0.116151 | 0.082032 | 1 |
| RNN | 100 | 0.169745 | 0.000937 | 0 |
| RNN | 200 | 0.168346 | 0.000209 | 0 |
| RNN | 400 | 0.153994 | 0.000453 | 0 |

Forget-bias results:
- Bias0: 0.166789 ± 0.002848; 0/3 solved.
- Bias1: 0.167462 ± 0.003357; 0/3 solved.

## KV bonus

Inference uses existing scratch projections and unchanged causal weights. Offset masks, chunked prefixes, reset, invalid modes, rolling boundaries and GPU logits agree with full-prefix inference at absolute/relative tolerances1e-5. Every benchmark greedy output agrees exactly. Three warmups and ten alternating paired synchronized trials; batch1/FP32 and prefill included.

| Prompt + new characters | Uncached/cached mean latency ratio |
|---|---:|
| 8 + 64 | 1.301 |
| 32 + 64 | 1.211 |
| 64 + 64 | 1.245 |
| 7 + 500 | 0.981 |

The cache rebuilds after the128-token window shifts, preserving the original position reset and prior-token dependencies. The500-character benchmark reports this limitation honestly. Raw measurements are in CSV notes; inference timings do not misuse sec_per_epoch.

## Verification and submission

All independent recurrent, Task5, Transformer and KV audits passed. results.csv has100 rows and exactly12 prescribed columns. Report: six assessed A4/11pt/2cm pages including AI disclosure, plus references only. Required figures/tables are captioned, numbered and referenced. README renders to one page. ZIP allowlist/CRC/hash/size checks pass, with datasets/checkpoints/environments/internal helpers excluded. Both notebooks pass isolated ZIP extraction with original raw timing replay and an Adam guard that rejects training; CSV, samples and packaged figures reproduce exactly.

The immediately preceding verified ZIP/source/evidence remain in `.cache/presentation-revision-2026-11-13/`; the older five-epoch backup remains in `.cache/pre-improvement-2026-11-12/`. The protocol was frozen in docs/improvement-protocol.md before this revised training. Logs and runtime evidence are in `.cache/improvement-run/` and gpu-runtime.json.

Technical work is complete. The missing variant table/hand fixture assumptions remain disclosed; the student confirmed identity, local GPU choice and AI permission. Remaining personal steps: verify the course portal deadline, upload this exact ZIP, download/open the uploaded copy and retain the receipt. No portal upload was performed. Marks and bonus acceptance remain instructor decisions.
