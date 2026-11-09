# Assignment progress

Updated: 2026-11-09. Status values: Not Started, In Progress, Completed, Blocked.
Overall: P1 Tasks 1–5 and P2 Tasks 2–5 Completed: 90/100 marks of fully verified task coverage (not an awarded grade), plus tested P2 attention awaiting the missing instructor hand example. All 13 P2 runs audited; results.csv has 82 rows. Report/packaging remain pending. User-reported professor permission permits AI-assisted implementation. Marks below denote rubric coverage, not awarded marks.

| Task | Marks | Status | Acceptance criteria / pending work |
|---|---:|---|---|
| P1.1 Data pipelines | 5 | Completed | Official HAR download; nine ordered channels; shapes/labels; subject splits; training-only normalization; class balance; exact adding generator and assertions; executed notebook |
| P1.2 Scratch cells | 10 | Completed | Custom RNN/LSTM/GRU; library agreement 1e-5; hand counts and dual biases |
| P1.3 HAR comparisons | 10 | Completed | Equal budgets; three seeds/model; accuracy and macro-F1 mean/sample std; parameters/time; best confusion matrix |
| P1.4 Adding comparisons | 10 | Completed | Four lengths × three models × three seeds; MSE/baseline; solved counts; T=200 curves; MSE vs length |
| P1.5a Gradients | part of 15 | Completed | T=100, all models, before/after training, log-scale hidden-state gradient norms |
| P1.5b Hidden sweep | part of 15 | Completed | HAR LSTM/GRU at 16/32/64/128 |
| P1.5c Individual ablation | part of 15 | Completed | ID parity: RNN clipping or LSTM forget bias, T=200 |
| P1.5d Analysis | part of 15 | Completed | One page: memory, failures, trade-offs, wearable choice supported by evidence |
| P2.1 Attention | 10 | In Progress | Custom attention/reference/causality/backward tests pass; illustrative hand fixture passes; instructor example absent |
| P2.2 Multi-head/block | 10 | Completed | Reference agreement <1e-5; pre-LN/residual/dropout/4d FFN/positions; 198272 total block parameters reconciled |
| P2.3 HAR encoder | 10 | Completed | CLS classifier; recurrent comparison; none/sinusoidal/learned positions |
| P2.4 Language model | 10 | Completed | Fixed configuration and contiguous split; loss/BPC/curves; three 500-character top-k samples |
| P2.5a Heatmaps | part of 10 | Completed | Two heads on a sentence and interpretation |
| P2.5b Heads | part of 10 | Completed | 1/4/8 heads at fixed width |
| P2.5c No mask | part of 10 | Completed | Training loss and generation effects |
| P2.5d Scaling | part of 10 | Completed | Time/memory at 64/128/256/512; quadratic-growth discussion |
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

## Historical next work (2026-11-09; superseded below)

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

## Task 5 execution (2026-11-09)

Three-seed gradient probes, 24-point HAR sweep (6 existing h=64 runs reused; 18 new runs) and six odd-ID forget-bias runs implemented. Uses exact previous budgets (10 HAR epochs, 5 adding epochs). Gradient graph verified by matching library predictions and all recurrent parameter gradients. Completion pending measured evidence and audit.

### Task 5 acceptance

Completed 18 graph-verified gradient probes, 24 HAR sweep points (six reused/eighteen new) and six paired forget-bias runs. All predictions, parameter counts, validation selections, metrics and sample-standard-deviation summaries independently audited. Initial paired models differ only in effective forget bias. Saved all histories/predictions, three required plots (visually inspected), task5-results.md and the concise report analysis problem1-analysis.md. results.csv now has 69 rows; no duplicates for reused width64 runs. Targeted Task 5 notebook execution passed; fresh full-notebook integration and final report pagination remain part of final packaging.

- Restart verification: 24 cached new runs + six reused h64 baseline runs; 69 ledger rows remain. Generalized helper defaults verified against the original caches using a temporary ledger.

## Problem 2 implementation and execution (2026-11-09)

Custom attention, multi-head attention, pre-LN block and sinusoidal encoding implemented under reported professor permission. Strict component checks pass: maximum attention error 3.576279e-7, multi-head 1.804112e-16, encoder 8.881784e-16, positions 5.960464e-8. Attention backward error 8.881784e-16. Invalid masks/dimensions rejected; whole-block/LM causality and finite parameter gradients verified. Encoder parameter formulas match actual models. Original instructor example remains unavailable; illustrative hand fixture explicitly distinguished.

Implemented HAR positional comparison (three variants × three seeds, patch 8, d=64/two layers/10 epochs), CPU-exception Shakespeare LM (d=64/two layers/context 128, five epochs), 1/4/8-head and no-mask comparisons, sampling, two-head heatmaps and profiler-based context scaling. Training has launched; completion requires actual saved results and independent checkpoint audit. No experimental results assumed.

HAR evidence now saved: nine runs,90 epochs,26523 test predictions; positional means90.54/90.61/91.20% for none/sinusoidal/learned. Validation selects sinusoidal. Independent replay remains pending; Task A stays In Progress.

Main LM saved:108481 parameters,2.234945 nats/3.224344 BPC at epoch 5. One-head ablation saved:2.202787 nats. Remaining ablations/generation/scaling and independent audit pending.

## Problem 2 acceptance (2026-11-09)

- All custom component strict/negative-control/backward/count/causality checks pass. P2.2 Completed. P2.1 remains In Progress solely because the referenced instructor numerical example is absent. User-supplied arXiv1706.03762 is the original mathematical reference, but review did not find that worked three-token Q/K/V fixture. Illustrative hand calculation passes and is labelled accurately.
- P2.3 Completed: nine HAR positional runs/90 epochs; validation selects sinusoidal. Independent replay verifies 26523 predictions, frozen training statistics, metrics, checkpoint selection and sample std. None/sinusoidal/learned mean accuracy90.54/90.61/91.20%; parameter/time comparison with P1 GRU recorded.
- P2.4 Completed: CPU exception d=64/two layers/context 128/four heads; full contiguous90/10 split; five epochs;2.234945 nats, 3.224344 BPC. Three labelled 500-character top-k samples exactly reproduced from checkpoint.
- P2.5 Completed: two measured head heatmaps/interpretation; matched1/4/8-head runs; no-mask training/generation and actual future-dependence diagnostic; measured context 64/128/256/512 time/tensor peak with quadratic discussion. One-seed and CPU limitations stated.
- Notebook executes top to bottom with outputs saved; second full execution reuses 13 caches with no duplicate ledger rows. Independent audit reproduces all four LM losses,2000 generated characters, attention weights and diagnostics. Four figure files visually inspected. docs/problem2-results.md and notebook analysis cite actual evidence.
- All 69 previous P1 ledger rows preserved; total 82. No datasets/checkpoints/environments staged or committed. Full P1 integration, final PDF/report pagination and ZIP remain packaging work. No commit/push yet.
