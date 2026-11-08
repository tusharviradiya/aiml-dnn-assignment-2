# Assignment progress

Updated: 2026-11-08. Status values: Not Started, In Progress, Completed, Blocked.
Overall: Task 1 Completed with provisional seeds: 5/100 marks of rubric coverage verified (not a grade); 95/100 remain. No model experiments run. Marks below denote rubric coverage, not awarded marks.

| Task | Marks | Status | Acceptance criteria / pending work |
|---|---:|---|---|
| P1.1 Data pipelines | 5 | Completed | Official HAR download; nine ordered channels; shapes/labels; subject splits; training-only normalization; class balance; exact adding generator and assertions; executed notebook |
| P1.2 Scratch cells | 10 | In Progress | Student implements RNN/LSTM/GRU; library agreement 1e-5; hand counts and dual biases |
| P1.3 HAR comparisons | 10 | Not Started | Equal budgets; three seeds/model; accuracy and macro-F1 mean/sample std; parameters/time; best confusion matrix |
| P1.4 Adding comparisons | 10 | Not Started | Four lengths × three models × three seeds; MSE/baseline; solved counts; T=200 curves; MSE vs length |
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

Student ID and missing variants table: provisional seeds 0/1/2 are documented; rerun when supplied. Instructor attention example, portal and final deadline confirmation remain outstanding for later tasks.

## Task 2 subtasks (10 marks total; no invented sub-mark allocation)

| Subtask | Status | Evidence / remaining work |
|---|---|---|
| Interfaces and explanatory guidance | Completed | Three clearly labelled student-only constructor/forward TODOs; shapes and equation references |
| Verification infrastructure | Completed | Helpers and negative controls passed; full notebook ran; actual custom-cell equivalence awaits student code |
| MyRNNCell implementation/equivalence | Blocked | Student must implement constructor and forward; no numerical match claimed |
| MyLSTMCell implementation/equivalence | Blocked | Student implementation pending; packed i/f/g/o gates |
| MyGRUCell implementation/equivalence | Blocked | Student implementation pending; packed r/z/n gates and PyTorch reset convention |
| Parameter derivation/reference counts | Completed | All six formula totals and actual PyTorch counts 4800/19200/14400 verified |
| Actual custom parameter counts | Blocked | Requires student parameters; strict verifier checks two-bias counts |
| Final Task 2 acceptance | Blocked | All three student cells, numerical tests, custom counts, strict completion check and notebook execution required |

Task 3 has not started. Infrastructure completion does not earn or imply Task 2 completion.
