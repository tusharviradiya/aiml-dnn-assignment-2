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
