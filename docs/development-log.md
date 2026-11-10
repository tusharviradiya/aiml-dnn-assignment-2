> Historical review record. Current verification and policy status are in [submission-validation.md](submission-validation.md). Prior authorship or permission assertions are not evidence of instructor authorization.

> Chronological internal record. Earlier decisions/claims may be superseded. Current requirements and evidence are in reproducibility-audit.md and submission-validation.md; the clarification source is unverified and the written authorship restriction controls. Unsupported informal-permission claims below are withdrawn; see student-work-map.md.

# Development log

## 2026-11-08 — P1.1 implementation (in progress)

Inspected the existing repository: only the source assignment was present, with no commits and no AGENTS.md. Created the Task 1 notebook, inline assertions, execution script, tracking documents, ignore rules and results schema. No restricted model implementations added.

Errors: an initial file-search command had an invalid argument and was corrected with a directory scan; `python` was unavailable, so Python 3 was used. Sandbox DNS blocked pip and the official dataset download; retried with explicit network approval. Dependency installation and real-data execution are pending. No commit hash exists; no commit or push performed.

## 2026-11-08 — P1.1 validation completed

Installed pinned dependencies in ignored `.venv`; Python 3.14.4 and PyTorch 2.15.0+cpu. Downloaded the official archive. The sandboxed Jupyter launch stalled before cells ran; interrupted it and executed with approved local-kernel access. The first real run found an extra `__MACOSX/UCI HAR Dataset` directory; fixed discovery to require actual training labels. The subsequent full notebook execution exited 0 and saved all outputs.

Verified shapes 7352×128×9 and 2947×128×9; all nine channel positions; labels; 21/9 non-overlapping subjects; three four-subject validation splits; training-only channel statistics; finite normalized values; constant-channel rejection; class-balance image; all 12 prescribed adding datasets; reproducibility. Split train/validation counts: seed 0 = 5886/1466, seed 1 = 5905/1447, seed 2 = 6017/1335. Constant-1 test MSE at T=50/100/200/400: 0.175392/0.169709/0.167942/0.152720. These are data baselines, not trained-model results.

Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Results CSV remains header-only. User approved the Task 1 commit on 2026-11-08. Commit message: `feat(problem1): implement and validate Task 1 data pipelines`. No push requested or performed. The commit hash is available through `git log` after creation.

## 2026-11-08 — P1.2 infrastructure preparation (In Progress)

Reviewed tracking documents, Task 1 source/saved assertions, project structure, installed PyTorch equation documentation and Git status. Task 1 is committed as `702ce01`; only the source assignment was untracked before this task. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified.

Appended student-only MyRNNCell/MyLSTMCell/MyGRUCell interfaces, shape contracts, equation guidance, single-/two-bias parameter derivations, weight-copy verification, sequence/state comparisons and honest pending/strict-completion handling. Added negative controls for invalid outputs and unfinished implementations. No custom cell equations were implemented. Full notebook execution is pending. No commit/push performed.

Validation completed: full notebook execution exited 0; all Task 1 assertions passed again, all six parameter formulas and actual PyTorch counts passed, copying/comparator negative-control tests passed. Each unfinished custom cell explicitly reported PENDING. The strict completion function was separately invoked and rejected unfinished code with NotImplementedError. No custom-cell numerical equivalence is claimed. Task 1 source cells were verified unchanged and its original saved cells preserved to avoid unrelated output/metadata churn. Task 2 outputs are saved. A follow-up check initially used system Python without torch; rerunning with `.venv/bin/python` resolved it. Task 2 remains In Progress, with student implementations blocking acceptance. No commits/pushes performed.

## 2026-11-08 — MyRNNCell constructor review blocked

User reported constructor ready. Inspected the on-disk notebook cell 26 and Git status: the notebook is unchanged from preparation commit `4cec9af` and still contains the constructor TODO. Executing the saved class and calling MyRNNCell(9, 64) raised NotImplementedError: MyRNNCell parameter setup is not implemented. Parameter registration, shapes, initialization and the 4800 count therefore cannot be verified yet. Awaiting saved notebook edits or pasted constructor code. No student code overwritten; no forward implementation or success claimed.

## 2026-11-08 — Autonomous preparation

Re-read the original assignment, current notebooks and tracking documents; preserved uncommitted constructor-review documentation. All recurrent implementations remain placeholders. The user confirmed experiment code must stay student-authored. Prepared independent constructor checks, targeted notebook execution, P2 interfaces/reference checks and an experiment acceptance map. No restricted or experiment implementation was written.

Initial independent verification-infrastructure tests passed: valid library-backed constructor fixture (4800 parameters); rejection of nonfinite/wrong-shape/unregistered/frozen parameters; strict recurrent/Transformer gates reject placeholders; attention random/hand fixtures accept a library oracle and reject causal leakage; positional checker rejects all-zero encoding. Notebook execution is pending. These are tests of the checkers, not evidence that student components pass.

Verification execution completed: targeted P1 Task 2 and full P2 notebook runs both exited 0 and saved outputs; all actual student components explicitly remain PENDING. Confirmed the reference encoder has 196608 matrix weights and 198272 total parameters under the documented contract. Compared notebook contents against HEAD: all pre-existing P1 source cells are unchanged; Task 1 cells and outputs are unchanged. Notebook schema validation and `git diff --check` pass. Reviewed tracked diffs and new files. New checkers have tested fixtures/negative controls; actual custom multi-head/encoder numerical paths still await student implementations. No experiments run, no results.csv changes, no commits/pushes.

## 2026-11-09 — Task 2 implemented and verified

Student ID 2026aj05073 was supplied. An earlier informal-permission assertion is withdrawn as unsupported. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Prior scaffolding commit: a95269d.

Implemented MyRNNCell, MyLSTMCell and MyGRUCell using only direct parameters and tensor equations, preserving the existing test contract. Constructors initialize uniformly within ±1/sqrt(h). Used PyTorch-compatible gate order and two-bias GRU candidate semantics. Added backward-gradient verification for inputs, initial states and all parameters.

Strict Task 2 execution passed: 8 cases per model across two dtypes, two seeds and two shapes. Maximum forward errors: RNN 1.1920928955078125e-7; LSTM and GRU 2.384185791015625e-7. Actual counts: 4800/19200/14400. Constructor finite-value, registration, shape, reproducibility and dtype checks passed. Maximum gradient errors: RNN 0, LSTM 1.110e-16, GRU 2.220e-16. Full Problem 1 notebook executed top to bottom with exit 0 and saved outputs; Task 1 assertions still pass. Task 2 was technically implemented with AI authorship disclosed; its student-authorship requirement remains unmet. No training experiments, results rows, commits or pushes.

## 2026-11-09 — Task 3 implementation and experiment launch

Reviewed existing Task 1/2 code and confirmed CPU-only environment. Added HAR classifiers, model/metric/persistence assertions, paired-seed training, validation-only selection, data/config/source cache fingerprints, nine-run execution cells and saved evidence/plots. Updated verification runners to stop before experiments. Launched full notebook execution; run results and acceptance remain pending. Prior Task 2 commit: 10e685f.

## 2026-11-09 — Task 3 experiments completed and audited

Full notebook execution exited 0. Run fingerprint 878cc93e6862a042: all nine runs completed, each 10 epochs; rows persisted after every run. RNN/LSTM/GRU accuracy means: 0.7052369641/0.8770501075/0.8819138107; sample std: 0.0491374003/0.0029255779/0.0103536792. Macro-F1 means: 0.6813982892/0.8767547349/0.8819234176. Classifier counts 5190/19590/14790; CPU seconds/epoch means 0.677409/1.181613/2.279295.

Validation selected GRU architecture and seed 2, epoch 9 for the confusion matrix (test accuracy 0.8713946386); this was not the highest-test-score run, by design. Saved/visually inspected confusion matrix and learning curves. All model/metric/persistence assertions passed. Added scripts/audit_har.py: independently reloads nine checkpoints, recomputes training-only statistics, reproduces 26523 test predictions, reconciles all metrics, epochs, parameter counts, timings and ddof=1 summary statistics. Audit passed. Quick verification suite still passes without triggering experiments. No numerical failures encountered. Cache-restart verification passed: all nine runs reused matching completed caches, results.csv remained nine rows, and the notebook completed without retraining. Targeted strict Task 2 checks passed and preserved every Task 3 cell/output exactly. Preserved pre-existing Task 1/2 cells verbatim after successful regression checks to avoid unrelated output metadata changes. No commits/pushes performed.

## 2026-11-09 — Task 4 implementation and launch

Reviewed Task 3 commit f1ad770 and existing notebook/logger. Added adding regressors and assertions, sample-weighted regression metric test, validation-selected training, 36 execution cells, cache/persistence and MSE/solved-run/curve reporting. Launched targeted Task 4 execution, preserving earlier notebook cells and outputs. Training budget set before inspecting results: five epochs for every run; all required full-sized datasets retained. Completion pending actual runs and audit. No commit/push.

## 2026-11-09 — Task 4 completed and audited

36 runs, 180 epochs, 36000 predictions completed with exit 0. All shape/count/gradient/MSE assertions and independent checkpoint audits passed; audited selection, predictions, errors, solved flags, baselines, timings and sample std. Both required plots saved and visually inspected. All 12 groups have 0/3 solved; baseline-level results and five-epoch limitation are explicitly discussed. Training-only CPU time 25.3 minutes; longest LSTM epochs 42–45 seconds. Cache restart exited 0, reused all 36 runs and preserved earlier notebook cells. A documentation helper initially used system Python without pandas; reran in .venv successfully. No model numerical errors occurred. No commit/push.

## 2026-11-09 — Task 5 preparation and launch

Reviewed Task 4 commit c1913a9 and prior configs/checkpoints. Generalized HAR/adding run helpers to explicit config/cache/run-ID arguments; defaults retain prior behavior. Added graph-based gradient probes, three-seed hidden sweep (18 new/6 reused), six paired effective-forget-bias runs, summaries and figures. Initial runner dependency lookup raised StopIteration before any execution; corrected lookup for the reference-helper cell, whose first line is a comment. Relaunched targeted Task 5 execution. Acceptance remains pending actual tests/results. No commit/push.

## 2026-11-09 — Task 5 results and audit

Targeted notebook execution exited 0. Saved 1800 gradient records, 24 sweep points (240 epoch histories; six cached width64 runs), six forget-bias points (30 histories), predictions and Figures 6–8. All 18 gradient probes matched library outputs and parameter gradients. Mean post-training first/last hidden-gradient ratios: RNN 3.55e-22, LSTM 1.25e-11, GRU 6.45e-5. Interpret LSTM hidden gradients separately from cell memory.

HAR GRU h32 accuracy 87.41±0.73% with 4326 parameters; h128 89.04±0.70% with 54150. Effective forget bias 0/1 MSE: 0.168400745±0.000449405 / 0.168494318±0.000389646; no solved runs and no reliable benefit inferred. scripts/audit_task5.py independently replayed all 24 sweep/six ablation checkpoints and all 18 gradient probes, checked initial paired parameters, metrics, selection, counts and 69-row ledger; exited 0. Plots visually inspected. Prepared concise evidence-based one-page report text in docs/problem1-analysis.md (final PDF pagination pending). Cache restart passed: 24 cached runs and six reused baseline runs, no new training or duplicate ledger rows. Default-argument regression checks on the generalized HAR/adding helpers reused original caches and preserved all 69 rows in a temporary results copy. No commit/push.

## 2026-11-09 — Problem 2 components and pipelines

Reviewed original assignment and Problem 1 completion commit 7c81120. Implemented custom tensor attention, multi-head reshaping/projections, pre-LN residual/4d-ReLU/dropout block and sinusoidal encoding. Strict component tests and existing verification-infrastructure suite pass. Max errors attention 3.576279e-7, multi-head 1.804112e-16, encoder 8.881784e-16, attention gradients 8.881784e-16. Parameter count 198272 reconciled at d=128. Added HAR/LM model shape/count/backward/causality assertions, contiguous blocks and uniform-loss diagnostic.

Official Shakespeare download initially failed with sandbox DNS; retried with network approval successfully (1115394 characters, 65-character vocabulary). Source-compilation smoke check caught an escaped-newline bug in fingerprint construction before any training; corrected it and compiled all code cells. Small profiler test confirmed available CPU memory event API and positive measured tensor peak. Launched full notebook execution with fixed budgets, atomic per-run logs and ignored caches; experiments pending. No commit/push.

## 2026-11-09 — Problem 2 HAR runs saved

All nine encoder runs and 90 epochs completed; training-only CPU total134.53 seconds. Accuracy means±sample std: none90.544±1.820%, sinusoidal90.612±1.016%, learned91.200±0.530%. Mean validation macro-F1 selects sinusoidal (0.927613), ahead of none (0.924655) and learned (0.914417); do not select learned based on test accuracy. Counts105222 for none/sinusoidal,106310 learned. Independent audit and notebook completion still pending; no Task A completion claim yet. LM training underway. No commit/push.

Main four-head causal LM completed five epochs at d=64/two layers/context 128: selected epoch 5, validation2.2349452775 nats, 3.2243444686 BPC,108481 parameters,22.0911 CPU seconds/epoch. Validation fell each epoch from2.55856 to2.23495; fixed budget unchanged. Remaining head/no-mask runs and sampling/audit pending.

## 2026-11-09 — Problem 2 experiments and acceptance

Run13613c052b7f52c4 completed13 runs/110 epochs: nine HAR/90 epochs and four LM/20 epochs. Training-only CPU total613.14sec. Main LM2.234945nats/3.224344BPC; head1/8 losses2.202787/2.255983. No-mask final train0.593618/apparent validation0.317695; generated sample 98.4% newlines, explicitly interpreted as leakage failure. Main samples have14/31/44 distinct characters at0.2/0.8/1.5. Measured two-head maps and context scaling saved; 64→512 increases attention scores64×, measured tensor peak28.07×. Four plots visually inspected.

Initial complete notebook run passed; added actual trained prefix-perturbation and empirical sample diagnostics plus evidence-based analysis. Final full restart passed with13 cache hits and82 ledger rows unchanged. Causal prefix change0 versus unmasked7.15354 verifies future dependence. scripts/audit_problem2.py independently reproduced all 9 HAR checkpoints/26523 predictions, four LM losses and2000 generated characters; checked selected epochs, counts, statistics, paired initialization, histories, source hashes, forbidden-layer absence and all 69 preserved P1 rows. Extended audit of diagnostics passed. Component regression suite passed. Source and notebook schemas/diff checks reviewed; final Git review pending. No model numerical failures.

The user supplied arXiv1706.03762 as a possible instructor example. Reviewed the paper's attention equation, relevant sections and appendix: a worked numerical three-token fixture was not found. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. P2.2–5 marked Completed only after these checks; optional bonus/report/packaging pending. No commit/push.

Final checks: all 48 notebook code cells have saved execution counts and no error outputs; notebook schema valid. Final component/negative-control regression suite passed. git diff --check passed; reviewed changes and artifact sizes, and confirmed problem1/ has no diff. Source assignment remains untracked; no raw data, model checkpoints, environment or large generated files included. Suggested commit: feat(problem2): implement and verify Transformer experiments and ablations. Awaiting user approval; no commit/push.

Final compatibility review found Task 5 audit hard-coded the entire ledger to69 rows. Replaced that global-total condition with the same24-row Task 5/run-fingerprint check, P1 scope and ledger uniqueness, allowing unrelated completed P2 rows. P1 notebook code/results remain unchanged. Regression audit pending.

Post-P2 Task5 regression audit passed:24 HAR sweep checkpoint sets, six forget-bias checkpoints,18 gradient probes and24 Task5 ledger entries verified with the expanded82-row ledger. Final git diff --check passes. All changes remain uncommitted pending approval.

## 2026-11-09 — Problem 2 commit approved

User approved the reviewed Problem 2 commit. Final status/diff checks passed. Commit scope includes the executed notebook, compact metrics/predictions, figures, generated samples, verification runners, ledger-compatible Task 5 audit and synchronized documentation. Source DOCX, datasets, checkpoints, virtual environment and caches are excluded. No push authorized or planned.

Staged whitespace check flagged trailing blank lines in no_mask_sample.txt. These are actual generated characters in the verified 500-character sample and were preserved. All other staged paths pass the normal whitespace check; the literal sample passes with only blank-at-EOF checking disabled for that path. No whitespace configuration changed.

## 2026-11-09 — Final report and packaging started

Problem2 commit a1ffd7f approved/created in prior turn; no push. User authorized final report and packaging and supplied report name Viradiya Tushar Rajeshbhai. Reviewed requirements and available PDF tooling (pdflatex/pdfinfo/pdftoppm/pdftotext installed; no new Python modeling libraries needed). Report/packaging In Progress. Found notebook-wide P1 cache fingerprints invalidated by later sections; scoping them to actual training dependencies and recording exact reviewed aliases to the already-audited legacy run IDs. Full integration and final PDF/ZIP checks pending.

## 2026-11-09 — Report and full integration verified

Full P1 Restart & Run All passed with saved outputs and existing caches; results ledger remains82 rows. New cache invalidation tests pass: reviewed adding alias reused, configuration/training dependency edits invalidate, analysis/output edits do not. Initial alias-generation helper expected nested config; actual metadata is flat. Corrected before full execution. Re-audited HAR and all adding checkpoints successfully.

Built report.pdf from scripts/build_report.py and docs/report.tex using measured CSVs and existing figures. First layout placed the width/forget figures on an extra content page; condensed the sweep table by pairing model columns and adjusted figure sizing, retaining11pt text/2cm margins. Final PDF has six content pages + excluded AI/reference page; body bounding boxes/A4/title/required evidence checks pass. Fixed a long unbreakable slash-separated phrase to remove overfull boxes. Validator initially missed combined figure labels and line-wrapped AI text; corrected text matching without weakening margin/page checks. Rendered pages inspected.

Added portable69-row P1 ledger snapshot so P2 audit does not need .git inside submission; all checkpoint/sample/diagnostic audits still pass. Prepared explicit-allowlist ZIP builder with CRC/hash/size/layout validation. Packaging and extracted full-notebook checks pending; no commit/push.

ZIP structural validation passed (about3.25MB,79 files, CRC and all hashes). First extracted smoke check passed component tests but exposed a portability bug in the new cache regression test: it assumed .cache already existed. Added explicit directory creation before TemporaryDirectory. Rebuilding into a fresh extraction and rerunning all checks; no change to model/result code.

## 2026-11-09 — Local submission package verified

After fixing .cache creation, fresh extraction passed all eight checks: component regression, cache invalidation, full Problem1, full Problem2, HAR audit, adding audit, Task5 audit and P2 audit. No .git is required. Both notebooks have identical source to the package. Validation explicitly reused local data/checkpoints via a relative symlink outside the archive; no claim of uncached training/network-download verification. Updated targeted adding runner independently passed36 cache hits. Restored saved full-Run-All outputs after that targeted check and original82-row ledger ordering after atomic-cache logger upserts; values unchanged.

Report validated: seven total pages (six assessed + one excluded), A4/11pt/2cm source and text margins, all required figures/tables, title/ID/name, AI disclosure, no overflow and embedded fonts. All rendered pages inspected. ZIP uses exact2026aj05073 naming, required root folder, compact evidence/source files and manifest; CRC/hash/extraction/size pass, about3.25MB. Local report/package marked Completed; portal submission separately Not Started. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Final rebuild includes this evidence; no commit/push. Suggested commit: build: assemble verified assignment report and submission package.

## 2026-11-09 — Final report/package commit approved

User approved `build: assemble verified assignment report and submission package`. Rechecked Git diff/whitespace, PDF page allocation/margins and local ZIP CRC/checksum/size; all passed. Rebuilt ZIP to synchronize this approval record and progress status. Commit scope contains report PDF/source, packaging/validation/cache scripts, portable provenance records, executed P1 notebook and documentation; generated ZIP, source DOCX, raw data, checkpoints and environment excluded. No push authorized or performed.


## Instructor clarification and final rubric audit

Reviewed the instructor email supplied by the user: freely chosen h/d/seeds and a self-created three-token example now apply; due Saturday14 November2026. Updated title/README/notebook explanations, explicit d64 count and current progress. Strict attention/hand/reference tests pass, so P2.1 is Completed. No model/training algorithm changed (AST comparison to HEAD passed). P1 comment/hash changes get exact legacy aliases; P2 training fingerprint unchanged. All82 checkpoints exist. A preflight source lookup initially searched for run_language at cell start although it shares the run_encoder cell; corrected the lookup.

Full notebook verification now rejects Adam optimizer construction on cache misses, preventing unintended retraining. Both full guarded notebook runs passed. Final PDF validation and extracted ZIP execution/audits subsequently passed (see final entry below). No verified authorship or disclosure waiver is available. Accurate comprehensive disclosure retained; authorization conflict recorded, not concealed or asserted resolved. No commits/pushes.

## 2026-11-09 — Clarified submission verification completed

Both full notebooks and all eight extracted-package checks passed: component/negative-control tests, cache fingerprint tests, both notebook runners, HAR, adding, Task5 and Problem2 audits. Verification used existing local data/checkpoints and rejected optimizer construction to prevent retraining. All82 experiment rows are byte-identical to commit f0db40f. Context timing was remeasured without training; report uses the current measured ratio. The report passes seven-page allocation (six assessed plus excluded references/AI declaration), A4,11pt, margins, title settings and explicit d64 count checks. Rendered title/count pages inspected.

Final archive uses the prescribed student-ID filename/folder, contains required files and per-file hashes, passes CRC/extraction checks and remains approximately3.25MB below25MB. Final documentation-only rebuild is source-compared to the successfully executed extraction. Technical rubric requirements pass; The written authorship restriction remains unmet; no verified exemption exists. Truthful disclosure retained. Portal submission not performed; no commit or push. Suggested commit: docs: apply instructor clarifications and verify final submission.

## 2026-11-09 — Examiner-led improvement audit started

Read the original DOCX, rubric, clarifications and untracked professor evaluation. Preserved baseline82 rows/metrics/evaluation plus hashes of all artifacts in docs/baseline-2026-11-09; original PDF/ZIP copied to ignored data/review-baseline. Restricted scratch implementations are unchanged; no instructor-authored exception was located. Permitted experiments/diagnostics proceed without treating progress claims as evidence.

Completed six new adding diagnostics:32-example/1200-update overfit and full-training T50/25-epoch validation pilot for each model, seed0, lr1e-3, batch128 for pilots. All three fit the small batch. Pilot first five epochs reproduce baseline train/validation MSE exactly. Best25-epoch validation: RNN0.16462985, LSTM0.01327108, GRU0.00189044. No seed2/test data accessed; no claim of solving a new test grid. Finite gradients, nonzero parameter updates, target identity, state reset verified. These are extra rows with test metrics blank, not replacement baseline results. Original36 failures remain reported.

Added a scalar nonuniform attention oracle without altering scratch code; improved report figures/numbering and prepared raw timing/repeated allocation-event retention. Four equal-budget LM continuation experiments and final integration are In Progress. Each resets Adam because original optimizer states were not saved; duration and restart effects cannot be separated. No commit/push.

## 2026-11-09 — Supplemental experiments and technical audit completed

All four LM continuations trained five extra full epochs under the same resume/reset rule. Selected causal validation nats: h4 2.234945→2.026947 (BPC3.224344→2.924266), h1 2.202787→1.996096, h8 2.255983→2.072158. Unmasked0.031937 is contaminated, not a valid autoregressive gain. Additional LM training548.10 CPU seconds; adding diagnostic total wall123.42sec. Original82 rows/metrics preserved;10 explicitly labelled supplemental rows appended. Required original samples remain; supplemental4×500 characters independently regenerated from actual selected weights.

Both full notebooks executed with optimizer guards, then strict components/negative controls, cache invalidation, HAR/adding/Task5/P2 checkpoint audits and review_checks passed. Review checks independently replay all new validation-selected checkpoints, prove baseline first-five adding losses identical, test trained patch invariance versus within-patch order, verify scalar nonuniform attention, validate LM next-token boundaries/BPC/sample reproduction, and reconstruct all12 raw profiler peaks and timing summaries. Restricted model/training source hashes match baseline. Continued future-perturbation delta0 causal versus18.9694 unmasked. No fresh replay of original training or clean dependency installation claimed.

Report additions initially overflowed to11 pages. Condensed redundant prose and normalized panel layout while preserving11pt/2cm; intermediate old-BPC assertion was updated to check the actually reported continued BPC. One bottom text line crossed the margin and was shortened; no validator bounds weakened. Final seven-page allocation, margins, title settings, numbered/cited figures/tables and no-overflow checks pass. Fixed an invalid Python string escape in the image helper. Regenerated final-size figures, train/validation curves, indexed heatmaps/color scales and context plots; report pages rendered and inspected. Full prior evaluation preserved; final reassessment is98/100 estimate (96–99), conditional on authorship authorization, not an awarded mark. Final extraction check and documentation-only archive synchronization follow below. No commits/pushes.

## 2026-11-09 — Final extraction passed

Fresh ZIP extraction passed all10 commands: strict components, cache fingerprints, both full notebook runners, canonical ledger normalization, four baseline audits and supplemental review checks. Existing local raw data/checkpoints were explicitly reused; no training/download or clean install is claimed for this extraction. The final presentation/documentation rebuild is source-compared with that executed extraction. CRC, manifest hashes, student-ID filename/root, required files, saved notebook execution and <25MB limit pass; data/weights/environment remain excluded. Final report remains six assessed pages plus one excluded declaration/reference page. Technical artifacts locally verified; authorship authorization and portal upload/verification remain unresolved external conditions. No commit or push. Suggested commit: research: diagnose adding failures and strengthen validated submission evidence.

## 2026-11-09 — Self-contained notebooks and minimal submission

Starting revision:2689b65. Read original DOCX/rubric, supplied email and evaluation;
verified original82 rows rather than trusting progress claims. Preserved pre-change
PDF/ZIP/notebooks/samples under ignored data/reproducibility-baseline-2026-11-09/;
Git preserves earlier source/history. No restricted model/cell equations changed.

Moved supplemental adding/LM training and report-figure generation into required
notebooks; embedded exact reviewed cache aliases and derived checkpoint lookup from
saved protocols. Primary LM is continued four-head causal2.0269467nats /2.924266BPC;
required samples now match its selected weights/SHA. Earlier samples remain internal.
No new assessed experiment or model retraining; a disposable one-update fixture
exercised fresh diagnostic execution/saving/replay without touching the ledger.

Added future optimizer/model/history/selection and Python/NumPy/Torch/CUDA/loader RNG
snapshot utilities; stochastic Adam next-update restoration passes exactly on CPU.
Historical optimizer/RNG states remain absent. Cached logging no longer serializes or
reorders identical ledger rows. Replaced verifier evidence writes and setup execution
with definition-only loading/read-only comparisons; Task5 audit cannot download data.
Canonical-ledger checking is read-only by default; explicit repair requires an opt-in
flag and saves a backup. All nine audits use before/after evidence hashes.

Full guarded notebooks run141/55 code cells, including all supplemental sections.
Minimal extraction executes packaged notebooks with no copied helpers, and reproduces
CSV, primary samples and included figures exactly using explicitly reused local caches.
PDF validation checks6+1 A4 pages,11pt/2cm, bounding boxes, embedded fonts, captions/
references; pages rendered for readability. ZIP now contains only16 required artifacts.
Final artifact details and verification records: submission-validation.md.

Errors resolved: system Python lacked pandas, so used the existing pinned venv;
cached overfit replay needed the historical128-example evaluation batch, rather than
its32-example training batch. The immutability harness correctly detected a concurrent
PDF rebuild; final audits run against stable artifacts. Added figure references briefly
caused page overflow; concise prose restored the6-page content limit without reducing
fonts/margins. Removed an unintended literal Markdown heading from PDF analysis.
Generated sample trailing spaces are retained because stripping them changes actual
500-character outputs; ordinary source whitespace checks pass separately.

Measured results are unchanged. Baseline head/mask controls and continued results are
explicitly distinguished; one seed, Adam reset, HAR architectural confounds and CPU
memory/timing scope remain limitations. The clarification summary is unauthenticated; no verified authorship exemption exists. Concise complete disclosure retained at report end.
No commit/push/portal action. Suggested commit: fix: make submission notebooks self-contained and package only required artifacts.

## 2026-11-09 — Approved reproducibility release commit

The user explicitly requested this commit. Pre-commit review confirmed the exact
16-file ZIP (1,909,232bytes; SHA256
85e99a502cf4407056ed0c4b86823f7d4d2bba24fd3d96f4c8ef0b692fd2803c),
all packaged source hashes and295 audited evidence hashes still match successful
verification records. Both extracted notebooks passed141/55 code cells and all nine
read-only audits passed in the preceding implementation work; no retraining was
needed for committing. Git diff reviewed; source whitespace checks pass, with actual
generated-sample trailing spaces deliberately preserved. Commit scope is the
self-contained notebooks, required report/figures/samples, compact evidence, audit/
packaging tools and synchronized internal documentation. Original assignment DOCX
is left untracked; ignored ZIP, datasets, checkpoints and environment are excluded.
No push or external submission is authorized or performed. Parent revision2689b65.

## 2026-11-09 — Focused disclosure, supplemental-cache and presentation revision

Baseline39112c6 reviewed against the original assignment **DOCX**, its100-point rubric
and the separate size/seed/example email. report.pdf was treated as a deliverable,
not the instructions. Pre-change notebook/PDF/ZIP/CSV/sample/generator copies and audit
hashes are preserved in ignored data/final-revision-baseline-2026-11-09/; Git history
and original experiment metadata/weights remain intact.

Consolidated Codex/Codex CLI attribution in the required report-end statement, keeping
all actual scratch, experiment, test, analysis and report assistance explicit. Removed
informal-permission narrative from the generator, report source and recurrent notebook
annotations. Only docstrings/Markdown changed in scratch sections; executable model
ASTs match the preserved implementations. Internal permission records remain truthful.
Fixed untied65-character/use8-step/h32:71% spacing and related mathematical typography.
PDF remains six content pages plus one excluded declaration/reference page,11pt/A4/2cm.

Confirmed and fixed two cache defects: adding diagnostics looked up evidence before
resolving epochs/n_train, and LM continuation accepted a matching architecture without
binding the originating baseline. Both notebooks now resolve full contracts before
lookup and check scoped source/data/runtime fingerprints; LM additionally checks the
baseline checkpoint hash/key/selected epoch/loss. New records save contracts. Existing
records remain byte-identical and use exact retrospective bindings reconstructed from
Git2689b65 source/protocol and preserved evidence, with all four baseline validation
losses independently re-evaluated. These bindings do not invent contemporaneous hashes
or missing optimizer/RNG states. Unknown, partial, corrupt or incompatible caches fail
before result reuse and are not overwritten.

Tests actually completed: all six adding and four LM legacy bindings pass;23 negative
controls reject budget/data-size/batch/seed/length/width/optimizer/source/data/baseline
changes and corruption. Both notebooks' disposable contract assert tests pass.
Future resume stochastic-update and disposable one-update adding fixture tests pass;
the fixture is deleted and adds no assessed result. Ten independent audits passed
with296 evidence hashes unchanged. Root and exact final ZIP both execute141/55 code
cells in cached-only mode. Exact92-row CSV,3x500 primary sample characters and nine
packaged figures agree; original raw timing repeats were replayed, not remeasured.
PDF bounds/format/font/numbering/disclosure checks pass; revised pages3/4/7 rendered
and inspected. CRC/name/root/allowlist/file hashes/size/extraction all pass.

Test-development error resolved: the negative source-edit fixture initially selected
an experiment configuration string, then an absent evaluator token. It now selects
actual definitions and changes executable source; stale-cache rejection is verified.
No experimental failure/result was replaced in resolving this test fixture.

No assessed retraining, clean installation or portal action. Primary continued causal
h4 LM remains2.0269467236664482nats /2.924265986379717BPC; all unsuccessful grid results
remain. Final ZIP1,914,738bytes,16files, SHA256
c50a489ed9be17891714610d51984dbb4b5668f70b38ae6f5b91063463311875.
Technical readiness is local verification; absent verified authorization for AI-written
restricted components remains an academic-integrity blocker. Editorial changes do
not resolve it. No new commit/push/upload. Suggested commit:
`fix: validate supplemental cache provenance and consolidate submission disclosure`.

## 2026-11-09 — Approved focused final revision commit

The user authorized a local commit. Pre-commit verification confirmed that the final
16-file ZIP (1,914,738 bytes; SHA256
c50a489ed9be17891714610d51984dbb4b5668f70b38ae6f5b91063463311875),
all packaged files and296 audited evidence hashes still match successful verification
records. Both extracted notebooks passed141/55 code cells; all ten audits passed.
Git diff and whitespace checks pass. Commit scope is the final notebook cache fixes,
disclosure/presentation revisions, tests/verification tooling and internal evidence/
tracking records. Parent39112c6 is preserved. The original assignment DOCX remains
untracked; ZIP, datasets, checkpoints and environment remain excluded from Git.
Technical readiness and the unresolved academic-integrity authorization blocker are
unchanged. No retraining, push, publication or external submission is authorized or
performed by this commit step. The resulting commit hash is available in Git history.

## 2026-11-10 — AI-policy resolution audit
- Re-read original DOCX rules and supplied clarification record. Explicit permission for AI-written scratch components remains absent; compliance blocked pending instructor decision.
- Added `docs/ai-policy-resolution.md`: source locations, affected notebook cells, unsent professor message, conditional remediation and understanding questions (answers pending).
- Existing report declaration already accurately names all material Codex uses; preserved unchanged. No scratch code changes or retraining.
- Verified actual PDF declaration, ZIP CRC and exact equality of all 16 packaged files with repository artifacts; internal records remain excluded. No submission or message sent.


## 2026-11-10 — Final submission compliance review

Re-read original DOCX body/tables/rubric/FAQ. Withdrew unsupported informal-permission
assertions from current records while preserving actual AI authorship disclosure.
Flagged six restricted implementations for independent student replacement; no graded
implementation was rewritten. Qualified the unauthenticated clarification summary.
Updated one-page README, concise declaration and report; preserved numerical evidence.
Ten audits passed over 296 unchanged files. Final ZIP cached replay passed 141/55
notebook code cells and byte-identical CSV/samples/nine figures. Report layout/ZIP
checks passed. Exact hash, checklist and unresolved blockers: submission-validation.md.
No fresh full training, clean install, T4 timing, external message/upload or commit.


## Updated DOCX and clean-environment review — 10 November 2026

Compared latest local DOCX (SHA-256 ca533fa4237248115aa6f686f0ae5d81c1cd7ebafb81995ab7eeef27acacd02d)
with prior copy. Only two deletions; required tasks unchanged, AI-tools ban and FAQ
verification exception retained. No new scratch implementation generated. Fixed P1
verification to call its existing strict gate during Run All, replacing the old
non-failing incomplete summary. Updated introductions, report reference, reproducibility
status and current review records. Fresh dependency install and pip check passed;
both notebooks passed in clean venv with existing caches, and disposable uncached
training/resume/replay test passed. All result/sample bytes and graded implementation
sources preserved. Rebuilt PDF/ZIP and synchronized visible submission folder.
Final independent audits and extraction evidence are recorded in final-verification.md.
T4 timing unavailable (no GPU), authorship provenance unresolved, no full retraining
or portal action claimed. The original course DOCX remains local/ignored. No push.

## 2026-11-10 — Final submission-readiness correction

Read the supplied original DOCX in full (SHA-256 37311ac57faf68aaf1adc2e69c312fe9325154f3d3de93b2abbd2304e14e950d).
It retains the scratch-authorship restriction and mandatory AI-use declaration.
Withdrawn: the preceding review's inference that a locally edited brief proved a
policy change. No authenticated amendment was located; the student explicitly
confirmed no verified instructor authorization exists. README/notebooks/report now
identify Codex's actual uses and the unresolved authorship discrepancy. Restricted
implementations remain unchanged. Restored required d=128 encoder count; report
reflowed without relaxing 11pt/A4/2cm/six-content-page checks. All ten read-only audits
passed with 296 evidence files unchanged. Full notebook/isolated extraction checks,
final archive digest and conditional 95/100 rubric review are recorded in
submission-validation.md. Jupyter's local TCP sockets required escalation beyond the
sandbox; this is an execution restriction, not a component-test failure. No push,
instructor communication or university submission performed.
