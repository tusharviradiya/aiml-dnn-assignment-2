# Final submission review — 13 November 2026

**Verdict: READY TO SUBMIT.** No outstanding technical fix or report correction. This review is an evidence-based self-assessment, not a promised grade or institutional approval.

Student: Viradiya Tushar Rajeshbhai, **2026aj05073**. Authority: the current root DOCX identified by the student; no separate assignment PDF exists locally. The supplied variant table and instructor hand example are absent, so the report explicitly discloses the permitted missing-information assumptions. Local GTX 1650 timing replaces unmeasured T4 timing transparently. AI-written scratch components are permitted according to the student's clarification; actual Codex and Claude assistance is disclosed without claiming independent implementation by the student.

## Rubric and evidence

These conservative ranges total **93–100/100**, with an estimated **3–5 optional bonus points assessed separately**. Qualitative marking, missing-fixture acceptance and the instructor's bonus/capping policy remain uncertain. No deduction is automatically assigned for approximate sanity-range misses, a valid null ablation or the single LM seed.

| Task | Max | Estimate | Verified evidence / possible qualitative limitation |
|---|---:|---:|---|
| P1.1 Pipelines | 5 | 5 | Exact nine-channel HAR order/shapes; disjoint subjects; seeded four-subject validation; training-only normalization; class balance; exact adding generator and marker/target asserts. |
| P1.2 Scratch cells | 10 | 10 | RNN/LSTM/GRU tensor implementations; library-output and backward checks; nonzero states; 4736/18944/14208 versus 4800/19200/14400 bias-count reconciliation. |
| P1.3 HAR | 10 | 9–10 | Nine matched ten-epoch runs, seeds 0/1/2; accuracy/F1 mean and sample std; parameters/time; validation-selected GRU/seed-2 confusion matrix. Interpretation is concise. |
| P1.4 Adding | 10 | 9–10 | All 36 fifty-epoch runs, four lengths; measured/theoretical constant baseline, solved table, T=200 train/validation curves. GRU 12/12, LSTM 5/12, RNN 1/12 solved; failures are preserved and explained. |
| P1.5 Gradients/ablations/analysis | 15 | 13–15 | Eighteen before/after T=100 gradient probes independently reproduced; 24 width runs; six paired required T=200 forget-bias runs; one-page analysis and wearable trade-off. Null ablation limits mechanistic conclusions; no unsupported positive effect claimed. |
| P2.1 Scratch attention | 10 | 9–10 | SDPA output/gradient, shape, row-sum, causal future-zero and future-perturbation tests; three-token hand calculation agrees. Self-created fixture substitutes for missing instructor fixture. |
| P2.2 MHA/encoder | 10 | 10 | Scratch Q/K/V/O and reshaping, pre-LN/residual/dropout/4d FFN/sinusoidal positions; 196608+1664=198272 at d=128 and 49152+832=49984 at d=64. |
| P2.3 HAR encoder | 10 | 9–10 | Nine runs/three positions/seeds; same HAR splits/stats; explicit validation-selected sinusoidal versus GRU accuracy/size/time comparison. Patching, depth/size and dropout confounds disclosed. |
| P2.4 Character LM | 10 | 10 | Full 65-character dataset, contiguous 90/10 split, d128/four layers/four heads/context128; learning curves; 1.744418 nats = 2.516664 BPC; three labelled 500-character samples and temperature/top-k discussion. |
| P2.5 Analysis/ablations | 10 | 9–10 | Indexed two-head heatmaps; matched 1/4/8-head and no-mask studies; generation leakage diagnostic; measured time/memory at 64/128/256/512 with scope and quadratic-growth explanation. Single seed limits head ranking; one sentence limits attention interpretation. |
| Optional KV cache | +5 | +3–5 | Exact scratch-model generation cache; offsets/chunks/reset/rolling-window tests; unchanged weights; four workloads, three warmups, ten alternating synchronized paired trials. Speed ratios 1.301/1.211/1.245/0.981; long-window slowdown reported honestly. |

Potential remaining deductions are qualitative judgment about concise analysis, figure density, assumption acceptance and how much insight is obtained from the null ablation—not a missing mandatory experiment. Bonus credit is not guaranteed by implementation alone.

## Corrections and review decisions

- Corrected the two stale five-epoch descriptions to 50; preserved legitimate diagnostic and LM baseline five-epoch text. Corrected the chronology: the revised budget was frozen before follow-up training after earlier test results had already been observed; validation selects checkpoints.
- Selected the encoder by **mean best validation F1** (sinusoidal 0.931429), not by highest test accuracy. Its test accuracy is **90.3970% versus GRU 88.0783%**, +2.3187 percentage points; **105222 versus 14790 parameters**, 7.1144 times; **0.283642 versus 1.418827 s/epoch** locally. Learned-position test accuracy 91.5847% remains visible but does not determine selection.
- Moved the hidden-width table to page 1, renumbered Tables 2/3 and all references, enlarged Figures 3–5 and 7, improved legends and actual-setting ticks, replaced head-loss bars with differences from four heads, and fixed caption/sample quotes and gradient-number typography. Measured minimum annotation sizes for these four revised plots are 8.80/9.03/9.00/8.28 pt (gradients/adding/width-bias/LM) at final printed scale.
- Preserved the required odd-ID T=200 ablation. Neither setting solves it, so the analysis states the limited null result; no supplementary T=100 run was requested or substituted.
- Rejected two inaccurate review claims: README already specifies six assessed pages plus references only, and the AI statement on page 3 has no right-margin overflow. Page 7 is references, not an excluded general supplementary page.
- Kept the **96.27-minute historical fresh-run measurement** immutable. The revised notebooks have a separate presentation manifest and guarded cached replay. This revision does not claim fresh training or a new T4 measurement.

## Validation performed

1. Both current notebooks passed Restart/Run All using matching local caches with `DNN_VERIFY_CACHED_ONLY=1` and Adam construction blocked: **141 + 58 code cells**, contiguous counts, saved outputs, no errors. Missing caches cannot silently initiate training.
2. Strict recurrent and Transformer component gates plus negative-control verification passed (`test_verification.py`). Cache fingerprint controls passed; **23 stale/source/data/baseline/protocol/integrity controls** rejected incompatible supplemental caches. No new assignment training ran.
3. Independent GPU audits reproduced all nine recurrent HAR checkpoints and 36 adding checkpoints, every first-five-epoch trajectory, all 24 width records, six paired bias records, 18 hidden-gradient probes, nine encoder checkpoints, four LM baselines, samples, attention, context evidence and KV logits/output hashes/raw-trial statistics. Supplemental continuation compatibility and BPC arithmetic passed; no forbidden library layer appears in model definitions (library comparisons occur only in tests, as the FAQ permits).
4. `verify_presentation_revision.py` compares against the preserved verified ZIP and original fresh source hashes. The only changed executable cells are the exact Markdown-fingerprint compatibility entry in P1 and the report renderer in P2. All model/training/test code, configs, datasets, checkpoints, CSV, samples, requirements and raw measurements are unchanged. Cached outputs were refreshed; original fresh outputs remain in the backup.
5. PDF checks passed: A4, 11 pt body, at least 2 cm margins, six assessed pages including AI disclosure plus one references-only page, embedded fonts, no overfull boxes, nine numbered/captioned/referenced figures and nine tables. Required evidence and all labelled samples are present. Revised pages were rendered and visually inspected; README renders to one A4 page at 11 pt/2 cm.
6. Final ZIP allowlist, CRC, individual hashes, 25 MB limit and exact student folder/name passed. **Both notebooks also passed from its isolated extraction**, with copied local test datasets/checkpoints/measurements and no internal helpers. Results CSV, samples and all nine packaged PNGs reproduced byte-for-byte; original timing repeats replayed exactly. This portability check is separate from fresh training and clean dependency installation.

## Changed files

- Submission files: `README.md`, `report.pdf`, both notebooks; P1 `report_adding.png`, `report_sweep-forget.png`, `report_gradients.png`; P2 `report_lm-continued.png`, `report_context.png` (legend enlargement). The other four report PNGs, `results.csv`, `requirements.txt` and `generated_samples.txt` are unchanged.
- Report/review sources: `scripts/build_gpu_report.py`, `docs/report.tex`, `REPORT_MANUAL_EDITS.md`, this review, `SUBMISSION_AUDIT.md`, `docs/submission-validation.md`, `docs/final-verification.md`, `docs/understanding-checklist.md`.
- Provenance/check tools: `docs/presentation-revision.json`, `scripts/verify_presentation_revision.py`, `scripts/replay_presentation_revision.py`, `scripts/validate_gpu_submission.py`. Generated internal `problem1/metrics/cache_aliases.json` gains only the exact reviewed Markdown-only alias. Test records are under `.cache/presentation-*` and excluded from the ZIP.
- Rebuilt `2026aj05073_DNN_Assignment.zip`. Internal reviews/helpers/provenance, datasets/checkpoints/environments and the original assignment brief are excluded from it.

## Submission and personal actions

Archive: **2026aj05073_DNN_Assignment.zip**, **1,893,436 bytes**, **16 files** under `2026aj05073_DNN_Assignment/`.

SHA-256: `ffff31c5ebcd06578282917e85a7d7acfa7de86f5cd387e555951f6efcc858f3`.

No technical blocker or pending manual PDF edit remains. The user selected no new experiments. T4 timing remains unmeasured and the unavailable variant/hand-fixture assumptions remain explicit; the report does not invent instructor confirmations. AI disclosure reflects actual assistance, not a demonstration of the student's independent understanding.

The student should review the submission and disclosure, confirm the actual portal deadline (the brief's date/weekday is inconsistent and its dates are marked proposed), upload this exact ZIP, download/open the uploaded copy and keep the receipt. No portal action was performed. The earlier verified ZIP and evidence remain in `.cache/presentation-revision-2026-11-13/`; `gpu-runtime.json` retains the original fresh measurement.
