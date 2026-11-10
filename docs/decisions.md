> Historical review record: authorship/completion judgments below predate the student’s final manual-implementation statement and are superseded by `ai-policy-resolution.md` and `final-verification.md`. Earlier AI assistance remains disclosed; no historical permission or clarification assertion establishes authorization.

> Chronological internal record. Earlier decisions/claims may be superseded. Current requirements and evidence are in reproducibility-audit.md and submission-validation.md; the clarification source is unverified and the written authorship restriction controls. Unsupported informal-permission claims below are withdrawn; see student-work-map.md.

# Decisions and assumptions

## 2026-11-08 — Task 1

- Use the existing repository root as the development/submission-content root. Create the StudentID-named outer folder during final packaging once the ID is known. Do not create a second repository.
- Keep modular functions in the notebook so the required submitted notebook is self-contained; assertions immediately follow their functions. A separate script executes the actual notebook and preserves outputs.
- Download only the assignment's official UCI HAR archive; support nested ZIP extraction and reject escaping archive paths. Cache ignored raw data locally.
- Preserve the required nine-channel order. Validate original labels 1–6 and expose labels 0–5 for later PyTorch classification.
- Use sorted unique training subjects and the exact prescribed RNG choice. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. This is an explicit assumption, not a claimed assigned variant.
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
- Reference verification uses single-layer unidirectional sequence layers, packed LSTM i/f/g/o and GRU r/z/n ordering, nonzero random initial states/biases, batch sizes 1/4, lengths 1/7, dimensions 3/5 and 9/64, seeds 13/29 and float32/float64. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Compare every hidden step, every LSTM cell state and the full sequence with strict max absolute error <1e-5.
- Catch only NotImplementedError for pending student work. Shape/numerical failures must fail execution. The strict completion function reruns verification and cannot accept skipped placeholders. Run All success is explicitly distinct from Task 2 completion.
- Equation references were checked against the installed PyTorch class documentation. AI assistance on interfaces/tests/explanations must be disclosed; no model experiments or results CSV changes are warranted.

## 2026-11-08 — Autonomous permitted work

- User explicitly confirmed no clarification authorizes AI-written experiment code. Keep all new experiment pipelines student-authored; continue interfaces, tests, explanations and debugging. This supersedes the earlier instruction to wait at each task boundary, but does not authorize graded implementations.
- Record unchanged recurrent placeholders as an academic-integrity dependency; do not repeatedly stop/retry the same NotImplementedError. Add independent constructor diagnostics and prepare P2 test infrastructure.
- P2 boolean attention masks use True=allowed (functional SDPA convention); reference MultiheadAttention/Transformer masks invert this. Fully masked queries are outside the declared contract.
- P2 reference contract: biased projections, pre-LayerNorm with eps=1e-5, ReLU feed-forward width 4d, dropout on feed-forward activation and both residual branch outputs. ReLU is a permissible unspecified choice. Use no internal attention dropout for deterministic reference checks. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Test verifiers using library oracles exclusively inside tests; no reference implementation may be used for actual P2 tasks.
- Targeted execution saves Task 2/P2 outputs without rerunning Task 1. Infrastructure success and pending student checks are separately reported. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. That earlier authorization inference is withdrawn. The written student-authorship rule remains controlling. Disclose AI-generated code and debugging in the final report.
- Student ID supplied: `2026aj05073` (email domain omitted from repository documentation). Last digit 3 selects the odd-ID ablation: LSTM forget-gate bias initialized to 0 versus 1 at T=200. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. The adding-dataset seeds are fixed independently. Keep the assignment's explicit Transformer configuration d=128, four heads, four layers unless using its documented CPU exception. These are assumptions, not assigned variant values.
- Implement recurrent equations directly with registered tensors and matrix operations. Retain both biases for exact PyTorch compatibility, packed LSTM i/f/g/o and GRU r/z/n order, and reset the GRU recurrent candidate projection including its bias. Initialize uniformly within ±1/sqrt(h). Add backward-gradient checks as well as required output equivalence.

## 2026-11-09 — HAR experiment protocol

- Task 3 uses permitted library recurrent layers with one layer, no dropout, h=64, final hidden state and a six-class linear head. Batch 128, Adam 1e-3, 10 epochs, gradient clipping norm 1.0 for all models; no early stopping. Settings were fixed before test evaluation. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Select best architecture by mean validation macro-F1, then representative seed by validation macro-F1 (lower seed on ties). Test data never select models/checkpoints.
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

- Custom implementation was AI-written and remains disclosed; course-policy authorization was not established. Framework attention/Transformer calls are restricted to reference tests. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. HAR also uses d=64/two layers, permissible model choice with patch 8 and CLS. All positional variants use 10 epochs, batch 128, Adam1e-3, dropout0.1, norm1 clipping and three matching P1 split seeds. Select highest validation macro-F1, earliest tie. P1 GRU h=64 selected by validation is the recurrent comparison; differences in architecture/patching/dropout are disclosed.
- LM budget fixed before results: five full epochs, batch 64, Adam1e-3, norm1 clipping, dropout0.1, seed 0. Whole-text sorted 65-character vocabulary; contiguous 90/10 split; no shuffling; nonoverlapping next-character blocks omit fewer than 128 trailing transitions per split. Select minimum validation nats, earliest tie. No train/validation boundary crossing. One seed for P2 LM ablations is an explicit limitation; P2 does not mandate three seeds.
- Heads 1/4/8 at fixed d=64 reuse the main four-head run, and no-mask model has same initialization and budget. Noncausal train/validation losses are leakage diagnostics, not autoregressive validation quality. Top-k20 and sampling seed 700 fixed; same prompt and 500 new characters at each requested temperature.
- Fingerprint only declared dependency cells plus complete config/data/software/device/thread metadata. Plot and analysis edits do not invalidate training. Atomic results.csv upsert preserves Problem 1 rows; checkpoints/raw data stay ignored.
- Context study measures full-model forward+backward at batch 8, dropout off, two warmups/five repeats, lengths64/128/256/512. CPU memory reconstructs peak additional live tensor bytes from raw profiler allocation events, excluding baseline model/input/interpreter and allocator reservation. CUDA uses peak allocated bytes above baseline. Report this scope, not GPU-reserved memory or host RSS.

- HAR validation mean selects sinusoidal although learned has the highest test mean. Report selected model90.61% versus P1 GRU88.19%, with 105222 versus 14790 parameters and patching differences; do not select the architecture by test accuracy.
- Attention-head interpretation is limited to measured diagonal/local patterns on one character sentence. Temperature discussion uses actual saved samples and labels empirical character entropy as sample statistics, not predictive model entropy. No-mask loss/BPC is explicitly contaminated and cannot rank autoregressive models; trained perturbation and generation provide direct failure evidence.
- User-proposed source https://arxiv.org/abs/1706.03762 was checked. Cite Eq 1/section 3.2.1 for attention and section 3.5 for positions, but no numerical three-token hand example was found. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. The original paper uses post-LN; retain the assignment's explicitly required pre-LN design.

## 2026-11-09 — Final report and submission packaging

- Use Viradiya Tushar Rajeshbhai, as supplied by the user, with student ID2026aj05073 in the title block. Produce six content pages on A4 at11pt with margins≥2cm, followed by a separate AI-use/reference page excluded by the assignment. Chosen h=64, d=64, seeds0/1/2 and the self-created example are assumptions under the DOCX missing-information clause; hand/code agreement is verified. Figures retain their established numbers and are referenced in text/captions. Raw datasets/checkpoints/environment stay outside the ZIP.
- Replace P1 whole-notebook cache hashing with hashes of actual training/data/helper definitions, config and data. A tracked exact-fingerprint alias manifest maps the reviewed, independently replay-audited default implementations to their legacy run IDs. Subsequent source/config/data changes get a different fingerprint and cannot use the alias. Preserve original result rows/timings; do not relabel old runs as newly trained. Clean extraction without caches trains the same configurations under those IDs.

- Preserve the original measured82-row ledger and its ordering after cache-upsert verification. Keep full Run-All execution outputs in the final notebooks rather than targeted-run numbering. The portable69-row P1 snapshot is an audited provenance artifact and avoids a Git dependency in submitted verification scripts.
- Validate a fresh ZIP extraction by executing both notebooks and all audits with an explicitly reused local data/checkpoint symlink. That symlink is local-only and is not an archive member. This establishes extraction portability and integration without claiming an uncached network download/training test.
- Mark local report/package completion separately from external portal submission. No portal URL/upload permission is supplied; user must upload, download/open the uploaded file and keep confirmation. The optional bonus is unattempted.


## Current instructor clarification and integrity decision

- Choose h=64,d=64,seeds0/1/2; record on title page and README. Keep original matched experiments and results. Explicit chosen-width derivation49152+256+320+256=49984; verify actual custom block count.
- Our zero-Q/K three-token example is valid under the email and demonstrates softmax/averaging/masking. Show full matrices and hand arithmetic. Random nonzero tests separately verify scaling.
- The confirmed date is Saturday14 November2026. Original odd-ID forget-bias ablation remains a valid completed experiment; no size/seed lookup is required.
- Do not retrain for comment/markdown changes. Exact reviewed cache aliases preserve historical measured runs; verification rejects optimizer creation if a cache is absent.
- Keep AI-use declaration truthful and comprehensive. The original written authorship/disclosure rule remains controlling. Report technical PASS separately from authorization NOT VERIFIED; do not certify unconditional readiness or silently remove AI-written scratch-code disclosure.

## 2026-11-09 — Evidence-led improvements

- Preserve commit817a025 as the audited baseline. Supplemental runs append exact-schema rows and keep all82 original rows/metrics. Baseline required grid remains primary; T50 pilots do not become a post-hoc replacement36-run test grid.
- Diagnose adding with fixed small-batch training and common25-epoch validation-only pilots, seed0, unchanged lr/architecture. Exact first-five-epoch replay isolates duration for the gated short-sequence failure. RNN overfitting does not establish learned addition; longer-sequence generalization remains untested under the extra budget.
- Continue each LM variant for five extra epochs using the same resume/reset rule. Original weights-only checkpoints lack optimizer state: resetting Adam is necessary and disclosed; no claim that duration alone caused the gain. Selection uses validation only; unmasked losses remain leakage diagnostics. Keep original samples and add separately labelled continued samples.
- Do not modify restricted scratch implementations without further explicit authorization. A nonuniform hand-test oracle, documentation, diagnostics and plots are permitted changes. No verified institutional waiver exists.
- Preserve raw context timing repeats and three allocation-event traces per length. Report full-model CPU forward/backward with squared-logit loss, not inference latency, RSS or T4 estimates.
- Patch flattening retains ordered time offsets within each patch. No-position CLS is invariant to whole-patch permutation; that does not imply invariance to arbitrary step permutations. Retain the depth/width/patch/dropout confounds; do not attribute an architectural accuracy gain specifically to attention.

## 2026-11-09 — Minimal, self-contained reproducibility release

- Current evidence supersedes earlier mixed wording: a local summary describes
  size/seed/example changes, but the original email is absent. No verified
  authorship exemption exists. Keep complete concise disclosure at report end. Do not rewrite
  restricted model/cell implementations; their original model-source hashes remain checked.
- Choose the continued four-head causal LM as primary; replace required sample file
  with its actual three500-character draws. Preserve baseline samples/metrics internally.
  Keep baseline head/mask comparisons, heatmaps and context measurements explicitly
  distinct from continuation results, with a SHA/config/epoch provenance record.
- Embed all supplemental experiment and report-figure code in required notebooks;
  the ZIP has no internal docs/scripts/metrics/manifest. Reconstruct generated metrics
  on execution. Local replay needs ignored caches; a clean run trains missing runs.
- Save optimizer/model/history/selection and all RNG states for future epoch-boundary
  resume. Historical runs did not save them; never retrofit supposed historical states.
  Retain Adam reset for all historical continuations and its inference limitation.
- Independent verification must execute definitions only, without setup/write cells.
  Replace evidence writes with comparisons. Hash all checked artifacts before/after;
  do not build the PDF concurrently with that immutability check.
- Make cached ledger upserts byte-preserving when an existing row is identical.
  Embedded exact source/config aliases preserve independently audited historical
  caches after infrastructure changes; other source/config changes invalidate reuse.
- Keep only required root files, notebooks, figures and primary sample file in ZIP.
  Optional rebuild/audit tools and understanding checklist remain internal. PDF LaTeX
  rebuilding uses internal tooling; notebook result/figure reproduction is self-contained.

## 2026-11-09 — Final focused revision

- Original DOCX controls the six-content-page rule and required final AI-use statement.
  Keep a single complete report declaration naming Codex/Codex CLI and actual AI-written
  scratch code, experiments/tests/debugging, execution/plots, analysis/drafting and
  reproducibility/packaging. Remove repetitive informal-permission narrative from
  submitted technical material; retain permission history internally. This is editorial
  consolidation, not evidence of authorization. Treat the original restrictions as
  binding without an explicit applicable instructor exemption; integrity remains Blocked.
- Resolve requested supplemental settings before cache lookup. A weights checksum
  alone proves neither configuration nor data compatibility. Compare full protocol,
  scoped executable-source/data fingerprints, software/device/thread settings and,
  for continuations, baseline checkpoint identity/hash and selected epoch/loss.
  Mismatches raise a compatibility error rather than overwrite evidence; revised runs
  need distinct names. Prospective runs save complete contracts when created.
- Historical adding metadata lacks n_train, and continuation metadata lacks an original
  baseline hash. Reconstruct adding sizes only from the committed fixed training source
  and pre-outcome protocol. Bind exact preserved metadata/weights to that reviewed
  contract. For LM, record currently observed baseline hashes retrospectively, check
  source/config/key and independently reproduce each saved initial validation loss.
  A matching loss is supporting evidence, not proof of unique historical weights.
  Never retrofit these observations as contemporaneous provenance. Reviewed bindings
  are explicit in both self-contained notebooks, with detailed limits retained internally.
- Hash ASTs of relevant definitions while ignoring comments/docstrings; plot-only or
  disclosure edits should not invalidate experiment semantics. The historical binding
  itself is excluded from result-affecting source dependencies to avoid circular hashes.
  Changes to training/data/model/evaluation definitions must reject legacy reuse.
- No model changes or assessed retraining are justified by these cache-validation defects:
  inspected historical experiments match the fixed source/protocol and independent replay.
  Keep all92 existing rows and primary sample bytes. Verify future training only with
  disposable fixtures. Distinguish cached timing trace reuse from new hardware-dependent
  benchmark repeats; fresh timing studies require statistical analysis, not PNG equality.
- Preserve39112c6 and ignored pre-revision artifacts. Submit only the same16 required
  files; all cache helpers/assertions stay inside notebooks, with no excluded helper
  dependency. Internal review/provenance/permission files stay outside the ZIP.

## 2026-11-10 — Policy resolution requires instructor evidence
- Preserve current truthful disclosure and historical records. The supplied sizes/seeds/example clarification does not authorize AI-written scratch components. Seek explicit scope/remediation using the unsent draft in `ai-policy-resolution.md`; no replacement scratch implementation pending resolution.
- Understanding assessment is separate from authorship; answers remain unassessed. Existing package stays technically unchanged and cannot be certified course-compliant.
