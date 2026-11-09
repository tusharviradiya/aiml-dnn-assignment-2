# Submission readiness after instructor clarification

**Technical readiness: PASS after examiner-led review. Overall unconditional submission clearance: FAIL / authorization unresolved.** This is not a finding of misconduct: the supplied written rules prohibit AI-written scratch code, while the user reports verbal permission. We cannot certify that exception from the supplied evidence.

Chosen settings: P1 h=64 for RNN/LSTM/GRU baselines; P2 d=64, main heads4, ablation heads1/4/8; seeds0/1/2 for three-seed runs. Confirmed deadline: Saturday14 November2026. The original brief states11:59PM IST; the email changes the weekday/date clarification, not that time. Portal upload is not performed.

## Marking rubric audit

| Requirement | Marks | Result | Evidence / limitation |
|---|---:|---|---|
| P1.1 Data pipelines | 5 | PASS | Official shapes7352/2947×128×9; nine ordered channels; labels1–6;21/9 subject separation; four held-out training subjects/seed; frozen training-only statistics; Figure1; exact adding generator with marker/target assertions |
| P1.2 Scratch recurrent cells | 10 | PASS technical | Only registered tensors/matrix operations; tanh RNN, i/f/g/o LSTM, r/z/n GRU and reset/bias compatibility; all outputs <1e-5; hand/actual counts reconciled; gradient tests. Authorship authorization separately unresolved |
| P1.3 HAR classification | 10 | PASS | Same h64, Adam1e-3, batch128,10 epochs, three seeds each, last hidden state; sample mean/std accuracy/F1, counts/training time; validation-selected confusion matrix |
| P1.4 Adding experiments | 10 | PASS | T50/100/200/400×three models×three seeds, exact10000/1000/1000 sizes/data seeds; MSE/constant baseline/solved<.05 counts; T200 learning curves and MSE-vs-length. All36 unsolved honestly retained |
| P1.5 Gradients/ablations/analysis | 15 | PASS | T100 actual hidden gradients before/after; log plots; LSTM/GRU16/32/64/128; odd-ID initial forget-bias0/1 T200; paired other weights/shuffle; one-page analysis and wearable recommendation with size/time caveats |
| P2.1 Attention | 10 | PASS technical | Row sums1, SDPA max error3.576279e-7, exact future zeros; explicit3×2 Q/K/V hand calculation and code agreement. Email permits self-created example; random nonzero inputs also test scaling |
| P2.2 Multi-head/block | 10 | PASS technical | Own Q/K/V/O head reshaping; pre-LN, residuals, dropout, FFN4d, sinusoidal positions; reference errors<1e-5; d64 weights49152 plus biases/norm832 =49984 actual parameters |
| P2.3 HAR encoder | 10 | PASS | Patch8+CLS, d64/two blocks, none/sinusoidal/learned×three seeds; same subjects/normalization/budgets; recurrent comparison reports accuracy/counts/CPU time and architecture differences |
| P2.4 Character LM | 10 | PASS | Official Shakespeare65-character whole-text vocab; contiguous90/10, no shuffling/boundary targets; context128, d64/two layers under CPU exception; selected validation2.234945nats/3.224344BPC; learning curve; exactly500 new characters at0.2/0.8/1.5 with top-k20 and discussion |
| P2.5 Analysis/ablations | 10 | PASS | Two heads on sentence, interpretation; heads1/4/8 at fixed width/budget; no-mask train-loss/generation/leakage demonstration; measured contexts64/128/256/512 time/live-tensor memory and O(T²d) discussion |
| Optional cache/LSTM bonus | up to5 | NOT ATTEMPTED | Optional; no bonus claimed |

Technical rubric coverage is100 points, not an awarded score or integrity approval.

## Cross-cutting requirements

| Requirement | Result | Evidence |
|---|---|---|
| Python3.10+, PyTorch2.x, permitted libraries | PASS | Python3.14.4/torch2.15.0+cpu; only PyTorch/NumPy/pandas/Matplotlib/sklearn for modeling; standard library plus notebook/PDF tooling for execution/report |
| Allowed datasets; no pretrained weights | PASS | Official HAR and Shakespeare; exact synthetic generator; no other training data/weights |
| Framework restrictions | PASS technical | Library recurrent layers only in permitted comparisons/reference tests; no framework attention/Transformer inside custom implementation; AST audit |
| Reproducibility | PASS | Python/NumPy/Torch seeds, paired splits/shuffles, training-only normalization, matching budgets and validation-only checkpoint selection |
| Tests and saved notebooks | PASS | Assert cells around implemented components/data; strict negative controls/backward checks; full notebook runs saved; optimizer guard prevents retraining during clarification verification |
| Relative paths | PASS | Notebook/project paths relative to root or problem directory; no user-specific absolute source paths |
| results.csv | PASS | Exact12-column schema;92 actual runs (82 baseline,6 adding diagnostics,4 LM continuations); task-inapplicable values blank; per-run persistence; no duplicate rows; prior measurements unchanged |
| Report settings/format | PASS | h64/d64/seeds0/1/2 on title page and README; explicit count derivations; six content A4 pages,11pt,≥2cm margins; numbered/cited required figures/tables; separate AI/reference page |
| Samples | PASS | Three labelled500-new-character strings, recorded prompts/temperature/top-k/seed; independently reproduced; no-mask diagnostic separate |
| README | PASS with hardware limitation | One-page-sized instructions, environment, settings, limitations; baseline CPU training44.7min plus9.13min measured LM training and123.4sec adding diagnostic wall time. T4 runtime not measured, explicitly stated under permitted CPU workflow |
| ZIP | PASS | Exact2026aj05073_DNN_Assignment.zip and outer folder; all required files; below25MB; CRC and every manifest hash verified. Extracted notebooks and audits passed; final documentation-only rebuild preserves their tested source |
| Portal submission | NOT PERFORMED | User must upload, download/open uploaded copy, retain confirmation; portal URL not supplied |

## Academic-integrity audit

- **Disclosure accuracy: PASS.** OpenAI Codex assistance includes requirements review, data pipelines, graded scratch cells/Transformer components, tests/debugging, experiments, plot generation, analysis/report drafting, packaging and clarification edits. The declaration explicitly includes AI-written scratch code. It does not claim independent student authorship.
- **Authorization: NOT VERIFIED (blocks unconditional clearance).** Original brief: from-scratch parts must be student-authored and AI may not write them; every use must be declared. The new email changes only sizes/seeds/example. User reports Samsir verbally allowed AI and said to omit AI assistance for manual parts. No instructor-authored waiver resolving the original writing/disclosure rule is supplied. Verbal permission might exist, but this review cannot verify its scope. Merely disclosing assistance does not establish that it was allowed.
- **Requested omission: not applied.** Removing known scratch-code assistance would make the declaration incomplete under the supplied written rule. Accurate disclosure is retained; no unsupported exemption or misleading authorship claim is added.
- **Data/results integrity: PASS.** No fabricated experiments, pretrained weights or unapproved datasets; failed learning outcomes, single-seed LM limitations, CPU-only timing and profiler memory scope are explicit. Automated checks cannot prove originality against every other submission; no such certification is claimed.

No further model training is needed for these clarification changes. Technical artifacts can be delivered, but the student must resolve the authorization conflict and complete portal submission before claiming unconditional compliance.

## Final execution evidence — 2026-11-09

Fresh extraction passed all ten commands: component verification, cache fingerprint tests, both complete notebook runners, HAR/adding/Task5/Problem2 audits, canonical ledger normalization and supplemental review checks. Execution reused local datasets/checkpoints with an optimizer guard that aborts if training would start. All82 original experiment rows and ordering are byte-for-byte preserved;10 supplemental rows are separately labelled. No fresh download or uncached training is claimed. The final package is freshly extracted and both notebooks, baseline audits and review_checks are executed with local caches; no fresh installation/network/training replay is claimed. Local machine-readable records are `.cache/extracted-verification.json`, `.cache/submission-verification.json` and `.cache/final-source-verification.json`; archive file hashes are included in its manifest.

## Examiner-led improvements

See research-review.md and professor-evaluation.md for the independent claims/evidence assessment. Actual extra training: six adding diagnostics and four equal-budget LM continuations. All restricted scratch source hashes match the baseline. The chosen four-head causal LM improves2.234945→2.026947nats (3.224344→2.924266BPC), with an explicit Adam-restart confound. T50 gated validation improves under a longer fixed protocol; original36 unsuccessful test runs remain. Twelve raw memory traces and all timing repeats are retained; indexed head links and whole-patch/within-patch distinction are verified. Final figures are consecutively numbered with labelled panels; report pages3–6 rendered and inspected.

Conditional estimated technical mark98/100 (96–99 range), previously96/100; not a guaranteed or awarded score. No formal viva is required by the supplied FAQ; understanding/student-authorship conditions are listed separately. No bonus, clean-install verification, T4 runtime, parameter-matched HAR accuracy or portal submission is claimed.
