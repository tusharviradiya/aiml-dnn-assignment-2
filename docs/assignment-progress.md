# Assignment progress

Updated: 2026-11-09. Status values: Not Started, In Progress, Completed, Blocked.
Overall: Tasks 1–4 Completed: 35/100 marks of rubric coverage verified (not an awarded grade). Transformer scaffolding exists. User-reported professor permission now allows AI implementation of remaining work. Nine HAR experiments completed and saved. Marks below denote rubric coverage, not awarded marks.

| Task | Marks | Status | Acceptance criteria / pending work |
|---|---:|---|---|
| P1.1 Data pipelines | 5 | Completed | Official HAR download; nine ordered channels; shapes/labels; subject splits; training-only normalization; class balance; exact adding generator and assertions; executed notebook |
| P1.2 Scratch cells | 10 | Completed | Student implements RNN/LSTM/GRU; library agreement 1e-5; hand counts and dual biases |
| P1.3 HAR comparisons | 10 | Completed | Equal budgets; three seeds/model; accuracy and macro-F1 mean/sample std; parameters/time; best confusion matrix |
| P1.4 Adding comparisons | 10 | Completed | Four lengths × three models × three seeds; MSE/baseline; solved counts; T=200 curves; MSE vs length |
| P1.5a Gradients | part of 15 | Not Started | T=100, all models, before/after training, log-scale hidden-state gradient norms |
| P1.5b Hidden sweep | part of 15 | Not Started | HAR LSTM/GRU at 16/32/64/128 |
| P1.5c Individual ablation | part of 15 | Not Started | ID parity: RNN clipping or LSTM forget bias, T=200 |
| P1.5d Analysis | part of 15 | Not Started | One page: memory, failures, trade-offs, wearable choice supported by evidence |
| P2.1 Attention | 10 | Not Started | Student code; normalization/reference/causality tests; hand example |
| P2.2 Multi-head/block | 10 | Not Started | Student code; pre-LN/residual/dropout/4d FFN/sinusoidal positions; parameter derivation |
| P2.3 HAR encoder | 10 | Not Started | CLS classifier; recurrent comparison; none/sinusoidal/learned positions |
| P2.4 Language model | 10 | Not Started | Fixed configuration and contiguous split; loss/BPC/curves; three 500-character top-k samples |
| P2.5a Heatmaps | part of 10 | Not Started | Two heads on a sentence and interpretation |
| P2.5b Heads | part of 10 | Not Started | 1/4/8 heads at fixed width |
| P2.5c No mask | part of 10 | Not Started | Training loss and generation effects |
| P2.5d Scaling | part of 10 | Not Started | Time/memory at 64/128/256/512; quadratic-growth discussion |
| Optional bonus | up to 5 | Not Started | KV cache or LSTM language-model comparison |
| Report | — | Not Started | Six pages; numbered/cited figures/tables; AI statement and references |
| Packaging | — | Not Started | Exact student-ID ZIP/root naming; ≤25 MB; PDF; executed notebooks; samples; pinned requirements; one-page README; download-and-open verification |

## Task 1 verification checklist

All items verified by the executed notebook: official shapes and channel order; labels; disjoint training/test subjects; three deterministic four-subject validation splits; frozen normalization; class-balance artifact; 12 prescribed adding datasets; reproducibility; notebook run-all.

## Outstanding information

Student ID 2026aj05073: odd-ID forget-bias ablation. Variant table missing; recurrent h=64 and seeds 0/1/2 are provisional. Instructor attention example, portal and final deadline confirmation remain outstanding for later tasks.

## Task 2 subtasks (10 marks total)

| Subtask | Status | Evidence |
|---|---|---|
| Interfaces and verification infrastructure | Completed | Prior reference and negative-control tests passed |
| MyRNNCell implementation/equivalence | Completed | 8 cases; max error 1.192093e-7; 4800 parameters |
| MyLSTMCell implementation/equivalence | Completed | 8 cases; max error 2.384186e-7; 19200 parameters |
| MyGRUCell implementation/equivalence | Completed | 8 cases; max error 2.384186e-7; 14400 parameters |
| Parameter derivation and constructor checks | Completed | Single-/two-bias totals, registration, finite initialization and reproducibility verified |
| Backward checks | Completed | Inputs/states/parameters agree; largest error 2.220446e-16 |
| Final Task 2 acceptance | Completed | Full notebook executed top to bottom; outputs saved; strict suite and documentation complete under reported permission |

## Historical preparation and blockers (2026-11-08; superseded by permission on 2026-11-09)

The user confirmed that experiment code remains student-authored because no broader
AI authorization has been obtained. P1 experiment code is absent; it is not technically
blocked by custom cells because library recurrent models are permitted in comparisons.
P2 experiments also require student Transformer implementations. Analysis is blocked
on real results. The optional bonus has not been selected. See `student-work-map.md`.

| Infrastructure subtask | Status | Evidence |
|---|---|---|
| Constructor diagnostics without forward | Completed | Valid reference fixture accepted; nonfinite/wrong-shape/unregistered/frozen fixtures rejected |
| Targeted verification runner | Completed | P1 Task 2 and P2 executed with saved outputs; Task 1 cells/outputs unchanged; strict gates reject placeholders |
| P2 interfaces and guidance | Completed | Student-only attention, multi-head, encoder and positional TODOs |
| P2 verification preparation | Completed | Attention oracle/hand fixture and negative controls pass; reference block count 198272 confirmed; custom components remain unverified |
| Student experiment acceptance checklist | Completed | Fairness, split leakage, seeds, metrics, ablations, timing and logging documented |

The illustrative attention example does not satisfy the missing instructor-supplied
example requirement. Strict custom checks remain pending, not passed. No training or
generation has run; results.csv remains header-only.

## Current next work (2026-11-09)

Professor permission for full AI assistance is reported by the user and recorded in decisions.md. Former student-authorship blockers are lifted. Nine HAR runs now populate results.csv. Next: adding-problem experiments and Transformer implementation. Missing variant table and instructor hand example remain documented assumptions/pending information.

## Task 3 execution (2026-11-09)

Implemented last-hidden-state library classifiers, seeded loaders, training-only statistics, validation checkpoint selection, atomic per-run CSV persistence, source/data/config fingerprints and aggregation/plot code. Nine full-data runs are pending completion: 3 models × seeds 0/1/2, h=64, batch 128, 10 epochs, Adam 1e-3 and clipping 1.0. All use the same CPU thread count. Verification and actual outputs determine completion; no results are assumed.

### Task 3 verified evidence

- Completed all nine full-data, 10-epoch runs with fixed matching budgets.
- Classifier shape/last-state/parameter/backward tests, metric fixtures and atomic CSV upsert tests passed.
- Actual predictions from all saved checkpoints independently reproduced; training-only normalization, validation-selected epochs, metric values, sample std and timing reconciled.
- `problem1/metrics/har_runs.csv`, `har_summary.csv`, `har_history.csv`, `har_predictions.csv`, and `har_config.json` preserve results, 90 epoch records and 26523 predictions.
- Confusion matrix and learning curves saved and visually inspected. GRU selected by mean validation macro-F1; representative seed 2, epoch 9 selected by validation only.
- Test accuracy mean ± sample std: RNN 70.52 ± 4.91%, LSTM 87.71 ± 0.29%, GRU 88.19 ± 1.04%. CPU timings only; variant h=64/seeds 0/1/2 remain provisional.

- Cache restart verified: nine cached runs reused without retraining or duplicate rows. Targeted Task 2 verification preserves Task 3 outputs exactly. All existing Task 1/2 source and saved cells preserved.

## Task 4 execution (2026-11-09)

Implemented 36 matched-budget adding runs, scalar regressors, parameter/gradient checks, sample-weighted MSE evaluation, validation checkpoint selection, atomic per-run logging, solved-run aggregation and required plots. Training budget fixed before results: 5 epochs, batch 128, h=64, Adam 1e-3, clipping 1.0, all prescribed data sizes and seeds. Execution and actual evidence pending.

### Task 4 acceptance

All 36 full-data runs and 180 epochs completed. Classifier/count/gradient and sample-weighted MSE assertions passed. Independent checkpoint audit verified all 36000 predictions, selected epochs, MSE, baseline, solved flags, counts, timing and summary statistics. Both required plots generated and visually inspected. Cache restart reused all 36 runs without duplicates. results.csv contains 45 rows (9 HAR + 36 adding). Earlier Task 1–3 cells/outputs unchanged. All runs unsolved; five-epoch budget limitation documented in task4-results.md.
