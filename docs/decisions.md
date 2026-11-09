# Decisions and assumptions

## 2026-11-08 — Task 1

- Use the existing repository root as the development/submission-content root. Create the StudentID-named outer folder during final packaging once the ID is known. Do not create a second repository.
- Keep modular functions in the notebook so the required submitted notebook is self-contained; assertions immediately follow their functions. A separate script executes the actual notebook and preserves outputs.
- Download only the assignment's official UCI HAR archive; support nested ZIP extraction and reject escaping archive paths. Cache ignored raw data locally.
- Preserve the required nine-channel order. Validate original labels 1–6 and expose labels 0–5 for later PyTorch classification.
- Use sorted unique training subjects and the exact prescribed RNG choice. Seeds 0/1/2 are provisional because the variants table is absent. This is an explicit assumption, not a claimed assigned variant.
- Fit per-channel population mean/std over training windows and timesteps only, in float64; return normalized float32 arrays. Refit per split seed. Apply identical frozen statistics to validation/test; reject constant channels.
- Copy the supplied adding generator unchanged. Keep dataset seeds 0/1/2 and sizes 10000/1000/1000 fixed for every length, independently of eventual model seeds.
- Use CPU PyTorch 2.x for Task 1: no model training or GPU is needed. Python is the available 3.14.4. Notebook tooling is infrastructure, not an additional modeling framework. Pin tested dependencies after installation.
- `results.csv` remains header-only because data validation is not a model experiment. Do not invent metrics or T4 timings.
- AI assistance implemented Task 1 at the user's request. No restricted scratch-model code is written. Disclose this assistance in the final report; the assignment's listed AI allowances are narrower than this data-pipeline assistance, so instructor acceptance is not established.
- Do not generate placeholder report/results or mark future tasks complete. Problem 2 implementation waits for instruction.

- Real archive inspection revealed a macOS metadata directory with the same dataset name. Select dataset roots by the presence of `train/y_train.txt`, rather than directory name alone.

## 2026-11-08 — Task 2 preparation

- Preserve all Task 1 source cells and append Task 2 within the same self-contained notebook. No scratch recurrent computations or parameter setup are supplied by AI; the student writes both constructor and forward.
- Use four direct parameters per custom cell with PyTorch-compatible names (without `_l0`) and two bias vectors. This makes arbitrary reference-weight copying unambiguous. Derive single-bias counts separately; custom counts must equal the two-bias totals.
- PyTorch GRU reset acts on the projected recurrent candidate including its bias. Single-bias candidate parameterization cannot in general represent two arbitrary PyTorch candidate biases. Do not sum them for equivalence.
- Reference verification uses single-layer unidirectional sequence layers, packed LSTM i/f/g/o and GRU r/z/n ordering, nonzero random initial states/biases, batch sizes 1/4, lengths 1/7, dimensions 3/5 and 9/64, seeds 13/29 and float32/float64. These verification seeds are independent of the missing experiment variant. Compare every hidden step, every LSTM cell state and the full sequence with strict max absolute error <1e-5.
- Catch only NotImplementedError for pending student work. Shape/numerical failures must fail execution. The strict completion function reruns verification and cannot accept skipped placeholders. Run All success is explicitly distinct from Task 2 completion.
- Equation references were checked against the installed PyTorch class documentation. AI assistance on interfaces/tests/explanations must be disclosed; no model experiments or results CSV changes are warranted.

## 2026-11-08 — Autonomous permitted work

- User explicitly confirmed no clarification authorizes AI-written experiment code. Keep all new experiment pipelines student-authored; continue interfaces, tests, explanations and debugging. This supersedes the earlier instruction to wait at each task boundary, but does not authorize graded implementations.
- Record unchanged recurrent placeholders as an academic-integrity dependency; do not repeatedly stop/retry the same NotImplementedError. Add independent constructor diagnostics and prepare P2 test infrastructure.
- P2 boolean attention masks use True=allowed (functional SDPA convention); reference MultiheadAttention/Transformer masks invert this. Fully masked queries are outside the declared contract.
- P2 reference contract: biased projections, pre-LayerNorm with eps=1e-5, ReLU feed-forward width 4d, dropout on feed-forward activation and both residual branch outputs. ReLU is a permissible unspecified choice. Use no internal attention dropout for deterministic reference checks. Encoder total at d=128 is 198272 including biases and norm parameters; matrix weights alone are 196608.
- The three-token uniform-score diagnostic is illustrative only, not a replacement claim for the missing instructor example. Test verifiers using library oracles exclusively inside tests; no reference implementation may be used for actual P2 tasks.
- Targeted execution saves Task 2/P2 outputs without rerunning Task 1. Infrastructure success and pending student checks are separately reported. No results rows, samples or report are fabricated to fill missing deliverables.

## 2026-11-09 — Updated professor permission and variant assumptions

- The user reports that their professor permits completing the full assignment with AI assistance. Proceed on that reported authorization, including scratch cells and experiment code. This supersedes the earlier student-only restrictions in this log and work map; it is a user-reported exception, not a claim that the original document changed. Disclose AI-generated code and debugging in the final report.
- Student ID supplied: `2026aj05073` (email domain omitted from repository documentation). Last digit 3 selects the odd-ID ablation: LSTM forget-gate bias initialized to 0 versus 1 at T=200. For a two-bias cell set the effective forget bias deliberately (avoid accidentally setting both to 1).
- The referenced Individualisation/variants table is absent from the DOCX. Until supplied, use provisional recurrent hidden size 64 and split/model seeds 0/1/2. The adding-dataset seeds are fixed independently. Keep the assignment's explicit Transformer configuration d=128, four heads, four layers unless using its documented CPU exception. These are assumptions, not assigned variant values.
- Implement recurrent equations directly with registered tensors and matrix operations. Retain both biases for exact PyTorch compatibility, packed LSTM i/f/g/o and GRU r/z/n order, and reset the GRU recurrent candidate projection including its bias. Initialize uniformly within ±1/sqrt(h). Add backward-gradient checks as well as required output equivalence.

## 2026-11-09 — HAR experiment protocol

- Task 3 uses permitted library recurrent layers with one layer, no dropout, h=64, final hidden state and a six-class linear head. Batch 128, Adam 1e-3, 10 epochs, gradient clipping norm 1.0 for all models; no early stopping. Settings were fixed before test evaluation. Provisional seeds 0/1/2 use corresponding subject splits.
- Select each run's checkpoint by highest validation macro-F1 (earliest epoch on ties). Select best architecture by mean validation macro-F1, then representative seed by validation macro-F1 (lower seed on ties). Test data never select models/checkpoints.
- CPU execution with four threads; seconds/epoch measures training only, excluding validation/test and persistence. CUDA synchronization is included if subsequently run on GPU. Do not claim these times are T4 times.
- Independent seeded DataLoader generator ensures the same shuffle sequence across architectures for each seed, independent of parameter initialization draws. Compute mean/std anew from that seed's training portion only.
- Fingerprint Task 3 source, full experiment config and raw inputs/labels/subjects for cache reuse. Store checkpoints and detailed JSON in ignored data/experiments; atomic CSV upsert records each completed run immediately. Track compact metrics, history and predictions as evidence. Full reruns reuse matching cache unless FORCE_HAR_RERUN is true.
- Preserve results.csv schema and other tasks' rows; notes identify task/config/run fingerprint. No val_loss_nats is populated for HAR (reserved for the language-model metric here). Report sample std with ddof=1.
- Bound the quick verification runners at the Task 3 header so checker tests cannot accidentally launch training.

## 2026-11-09 — Adding experiment protocol

- Use library recurrent layers for Task 4, h=64 and final hidden-state scalar linear head. Fixed five-epoch CPU budget, batch 128, Adam 1e-3 and norm-1 clipping for every model/length/seed; select lowest validation MSE, ties earliest. Do not extend budget based on test results. Low solved counts will be reported honestly and discussed as a limitation.
- Generated training/validation/test data exactly follow assignment sizes 10000/1000/1000 and data seeds 0/1/2. Independently seed model/shuffle with 0/1/2. Targets are not normalized. Evaluate MSE in float64 from float32 model predictions to avoid batch-weighting artifacts.
- Keep measured constant-1 baselines by length as well as analytical 1/6. Define solved strictly as test MSE <0.05; aggregate with sample std ddof=1.
- Use Task 4 source/config fingerprint, length-specific filenames and length in notes to preserve all 36 rows in the shared atomic logger. Local checkpoints/JSON remain ignored. Track histories, predictions and compact summaries.
- Add a targeted Task 4 runner using earlier setup/generator/logger definitions without rerunning HAR or rewriting earlier notebook cells. Appending new sections changes the existing HAR notebook-wide source fingerprint on future full executions, which correctly invalidates its old cache; such a full execution may retrain HAR and log a distinct fingerprint. Current Task 3 evidence is preserved.

## 2026-11-09 — Task 5 protocol

- T=100 gradients use all three model seeds, paired initial and validation-selected Task 4 checkpoints, and an independent fixed 32-example adding probe generated with seed 3. Compute in float64 for dynamic range. Unroll verified custom cells with copied library weights and retain actual hidden nodes; compare predictions and recurrent parameter gradients to the fused library graph. Plot batch-mean L2 norm at each step on log scale; store exact values including zeros (display floor 1e-300 only). LSTM hidden and cell nodes are distinct, so hidden gradients alone do not measure the entire cell-memory path. Changes in loss scale also affect gradients.
- HAR width sweep uses three seeds for both LSTM/GRU at 16/32/64/128. Reuse the six existing width-64 runs; train 18 new widths with identical Task 3 settings and subject splits. Parameterize existing run helpers with explicit configuration/cache/run-ID overrides, preserving defaults rather than duplicating training loops.
- Odd-ID LSTM T=200 ablation compares effective initial forget bias 0 versus 1 across three paired seeds with the same five-epoch Task 4 budget. Set bias_ih forget slice to requested value and bias_hh forget slice to zero; all other initial weights and shuffle sequences are paired. Initial bias is not held fixed during optimization.
- Source/config fingerprint covers Task 5 code plus the generalized training helpers. Cache artifacts remain local and ignored. Additional experiment rows use existing exact schema and configuration notes; sweep width64 is reused without duplicate ledger rows.
- Training/validation selection remains independent of test results. No increase in budget is made to force solved adding runs. Scope performance conclusions to this short budget and measured CPU backend; wearable recommendation must distinguish model-size evidence from unmeasured energy/inference latency.

## 2026-11-09 — Problem 2 protocol

- User authorization for full AI assistance remains in force; custom implementation is AI-assisted and will be disclosed. Framework attention/Transformer calls are restricted to reference tests. Missing instructor hand example is still pending; do not call the illustrative diagnostic the official example.
- CPU-only LM uses the assignment FAQ exception d=64/two layers; main context 128/four heads retained. HAR also uses d=64/two layers, permissible model choice with patch 8 and CLS. All positional variants use 10 epochs, batch 128, Adam1e-3, dropout0.1, norm1 clipping and three matching P1 split seeds. Select highest validation macro-F1, earliest tie. P1 GRU h=64 selected by validation is the recurrent comparison; differences in architecture/patching/dropout are disclosed.
- LM budget fixed before results: five full epochs, batch 64, Adam1e-3, norm1 clipping, dropout0.1, seed 0. Whole-text sorted 65-character vocabulary; contiguous 90/10 split; no shuffling; nonoverlapping next-character blocks omit fewer than 128 trailing transitions per split. Select minimum validation nats, earliest tie. No train/validation boundary crossing. One seed for P2 LM ablations is an explicit limitation; P2 does not mandate three seeds.
- Heads 1/4/8 at fixed d=64 reuse the main four-head run, and no-mask model has same initialization and budget. Noncausal train/validation losses are leakage diagnostics, not autoregressive validation quality. Top-k20 and sampling seed 700 fixed; same prompt and 500 new characters at each requested temperature.
- Fingerprint only declared dependency cells plus complete config/data/software/device/thread metadata. Plot and analysis edits do not invalidate training. Atomic results.csv upsert preserves Problem 1 rows; checkpoints/raw data stay ignored.
- Context study measures full-model forward+backward at batch 8, dropout off, two warmups/five repeats, lengths64/128/256/512. CPU memory reconstructs peak additional live tensor bytes from raw profiler allocation events, excluding baseline model/input/interpreter and allocator reservation. CUDA uses peak allocated bytes above baseline. Report this scope, not GPU-reserved memory or host RSS.

- HAR validation mean selects sinusoidal although learned has the highest test mean. Report selected model90.61% versus P1 GRU88.19%, with 105222 versus 14790 parameters and patching differences; do not select the architecture by test accuracy.
- Attention-head interpretation is limited to measured diagonal/local patterns on one character sentence. Temperature discussion uses actual saved samples and labels empirical character entropy as sample statistics, not predictive model entropy. No-mask loss/BPC is explicitly contaminated and cannot rank autoregressive models; trained perturbation and generation provide direct failure evidence.
- User-proposed source https://arxiv.org/abs/1706.03762 was checked. Cite Eq 1/section 3.2.1 for attention and section 3.5 for positions, but no numerical three-token hand example was found. Keep the instructor-fixture requirement pending rather than inventing provenance. The original paper uses post-LN; retain the assignment's explicitly required pre-LN design.

## 2026-11-09 — Final report and submission packaging

- Use Viradiya Tushar Rajeshbhai, as supplied by the user, with student ID2026aj05073 in the title block. Produce six content pages on A4 at11pt with margins≥2cm, followed by a separate AI-use/reference page excluded by the assignment. No fabricated instructor example; explicitly list that remaining gap and missing-variant assumptions.
- Generate report from tracked LaTeX source and measured CSV/JSON evidence using existing local pdflatex. Figures retain their established numbers and are referenced in text/captions. Raw datasets/checkpoints/environment stay outside the ZIP.
- Replace P1 whole-notebook cache hashing with hashes of actual training/data/helper definitions, config and data. A tracked exact-fingerprint alias manifest maps the reviewed, independently replay-audited default implementations to their legacy run IDs. Subsequent source/config/data changes get a different fingerprint and cannot use the alias. Preserve original result rows/timings; do not relabel old runs as newly trained. Clean extraction without caches trains the same configurations under those IDs.

- Preserve the original measured82-row ledger and its ordering after cache-upsert verification. Keep full Run-All execution outputs in the final notebooks rather than targeted-run numbering. The portable69-row P1 snapshot is an audited provenance artifact and avoids a Git dependency in submitted verification scripts.
- Validate a fresh ZIP extraction by executing both notebooks and all audits with an explicitly reused local data/checkpoint symlink. That symlink is local-only and is not an archive member. This establishes extraction portability and integration without claiming an uncached network download/training test.
- Mark local report/package completion separately from external portal submission. No portal URL/upload permission is supplied; user must upload, download/open the uploaded file and keep confirmation. The optional bonus is unattempted.
