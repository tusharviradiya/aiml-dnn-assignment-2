# Development log

## 2026-11-08 — P1.1 implementation (in progress)

Inspected the existing repository: only the source assignment was present, with no commits and no AGENTS.md. Created the Task 1 notebook, inline assertions, execution script, tracking documents, ignore rules and results schema. No restricted model implementations added.

Errors: an initial file-search command had an invalid argument and was corrected with a directory scan; `python` was unavailable, so Python 3 was used. Sandbox DNS blocked pip and the official dataset download; retried with explicit network approval. Dependency installation and real-data execution are pending. No commit hash exists; no commit or push performed.

## 2026-11-08 — P1.1 validation completed

Installed pinned dependencies in ignored `.venv`; Python 3.14.4 and PyTorch 2.15.0+cpu. Downloaded the official archive. The sandboxed Jupyter launch stalled before cells ran; interrupted it and executed with approved local-kernel access. The first real run found an extra `__MACOSX/UCI HAR Dataset` directory; fixed discovery to require actual training labels. The subsequent full notebook execution exited 0 and saved all outputs.

Verified shapes 7352×128×9 and 2947×128×9; all nine channel positions; labels; 21/9 non-overlapping subjects; three four-subject validation splits; training-only channel statistics; finite normalized values; constant-channel rejection; class-balance image; all 12 prescribed adding datasets; reproducibility. Split train/validation counts: seed 0 = 5886/1466, seed 1 = 5905/1447, seed 2 = 6017/1335. Constant-1 test MSE at T=50/100/200/400: 0.175392/0.169709/0.167942/0.152720. These are data baselines, not trained-model results.

Task 1 marked Completed with documented provisional seeds. Student-specific rerun remains pending the missing variant table. Results CSV remains header-only. User approved the Task 1 commit on 2026-11-08. Commit message: `feat(problem1): implement and validate Task 1 data pipelines`. No push requested or performed. The commit hash is available through `git log` after creation.

## 2026-11-08 — P1.2 infrastructure preparation (In Progress)

Reviewed tracking documents, Task 1 source/saved assertions, project structure, installed PyTorch equation documentation and Git status. Task 1 is committed as `702ce01`; only the source assignment was untracked before this task. Task 1 remains completed with provisional split seeds; the variant table is still missing.

Appended student-only MyRNNCell/MyLSTMCell/MyGRUCell interfaces, shape contracts, equation guidance, single-/two-bias parameter derivations, weight-copy verification, sequence/state comparisons and honest pending/strict-completion handling. Added negative controls for invalid outputs and unfinished implementations. No custom cell equations were implemented. Full notebook execution is pending. No commit/push performed.

Validation completed: full notebook execution exited 0; all Task 1 assertions passed again, all six parameter formulas and actual PyTorch counts passed, copying/comparator negative-control tests passed. Each unfinished custom cell explicitly reported PENDING. The strict completion function was separately invoked and rejected unfinished code with NotImplementedError. No custom-cell numerical equivalence is claimed. Task 1 source cells were verified unchanged and its original saved cells preserved to avoid unrelated output/metadata churn. Task 2 outputs are saved. A follow-up check initially used system Python without torch; rerunning with `.venv/bin/python` resolved it. Task 2 remains In Progress, with student implementations blocking acceptance. No commits/pushes performed.

## 2026-11-08 — MyRNNCell constructor review blocked

User reported constructor ready. Inspected the on-disk notebook cell 26 and Git status: the notebook is unchanged from preparation commit `4cec9af` and still contains the constructor TODO. Executing the saved class and calling MyRNNCell(9, 64) raised NotImplementedError: MyRNNCell parameter setup is not implemented. Parameter registration, shapes, initialization and the 4800 count therefore cannot be verified yet. Awaiting saved notebook edits or pasted constructor code. No student code overwritten; no forward implementation or success claimed.

## 2026-11-08 — Autonomous preparation

Re-read the original assignment, current notebooks and tracking documents; preserved uncommitted constructor-review documentation. All recurrent implementations remain placeholders. The user confirmed experiment code must stay student-authored. Prepared independent constructor checks, targeted notebook execution, P2 interfaces/reference checks and an experiment acceptance map. No restricted or experiment implementation was written.

Initial independent verification-infrastructure tests passed: valid library-backed constructor fixture (4800 parameters); rejection of nonfinite/wrong-shape/unregistered/frozen parameters; strict recurrent/Transformer gates reject placeholders; attention random/hand fixtures accept a library oracle and reject causal leakage; positional checker rejects all-zero encoding. Notebook execution is pending. These are tests of the checkers, not evidence that student components pass.

Verification execution completed: targeted P1 Task 2 and full P2 notebook runs both exited 0 and saved outputs; all actual student components explicitly remain PENDING. Confirmed the reference encoder has 196608 matrix weights and 198272 total parameters under the documented contract. Compared notebook contents against HEAD: all pre-existing P1 source cells are unchanged; Task 1 cells and outputs are unchanged. Notebook schema validation and `git diff --check` pass. Reviewed tracked diffs and new files. New checkers have tested fixtures/negative controls; actual custom multi-head/encoder numerical paths still await student implementations. No experiments run, no results.csv changes, no commits/pushes.

## 2026-11-09 — Task 2 implemented and verified

The user reported professor permission for full AI assistance and supplied student ID 2026aj05073. Recorded the reported exception, AI disclosure requirement, odd-ID forget-bias ablation and missing-variant assumptions. Prior scaffolding commit: a95269d.

Implemented MyRNNCell, MyLSTMCell and MyGRUCell using only direct parameters and tensor equations, preserving the existing test contract. Constructors initialize uniformly within ±1/sqrt(h). Used PyTorch-compatible gate order and two-bias GRU candidate semantics. Added backward-gradient verification for inputs, initial states and all parameters.

Strict Task 2 execution passed: 8 cases per model across two dtypes, two seeds and two shapes. Maximum forward errors: RNN 1.1920928955078125e-7; LSTM and GRU 2.384185791015625e-7. Actual counts: 4800/19200/14400. Constructor finite-value, registration, shape, reproducibility and dtype checks passed. Maximum gradient errors: RNN 0, LSTM 1.110e-16, GRU 2.220e-16. Full Problem 1 notebook executed top to bottom with exit 0 and saved outputs; Task 1 assertions still pass. Task 2 marked Completed under reported professor permission, with AI authorship disclosed in notebook/docs. No training experiments, results rows, commits or pushes.

## 2026-11-09 — Task 3 implementation and experiment launch

Reviewed existing Task 1/2 code and confirmed CPU-only environment. Added HAR classifiers, model/metric/persistence assertions, paired-seed training, validation-only selection, data/config/source cache fingerprints, nine-run execution cells and saved evidence/plots. Updated verification runners to stop before experiments. Launched full notebook execution; run results and acceptance remain pending. Prior Task 2 commit: 10e685f.

## 2026-11-09 — Task 3 experiments completed and audited

Full notebook execution exited 0. Run fingerprint 878cc93e6862a042: all nine runs completed, each 10 epochs; rows persisted after every run. RNN/LSTM/GRU accuracy means: 0.7052369641/0.8770501075/0.8819138107; sample std: 0.0491374003/0.0029255779/0.0103536792. Macro-F1 means: 0.6813982892/0.8767547349/0.8819234176. Classifier counts 5190/19590/14790; CPU seconds/epoch means 0.677409/1.181613/2.279295.

Validation selected GRU architecture and seed 2, epoch 9 for the confusion matrix (test accuracy 0.8713946386); this was not the highest-test-score run, by design. Saved/visually inspected confusion matrix and learning curves. All model/metric/persistence assertions passed. Added scripts/audit_har.py: independently reloads nine checkpoints, recomputes training-only statistics, reproduces 26523 test predictions, reconciles all metrics, epochs, parameter counts, timings and ddof=1 summary statistics. Audit passed. Quick verification suite still passes without triggering experiments. No numerical failures encountered. Cache-restart verification passed: all nine runs reused matching completed caches, results.csv remained nine rows, and the notebook completed without retraining. Targeted strict Task 2 checks passed and preserved every Task 3 cell/output exactly. Preserved pre-existing Task 1/2 cells verbatim after successful regression checks to avoid unrelated output metadata changes. No commits/pushes performed.
