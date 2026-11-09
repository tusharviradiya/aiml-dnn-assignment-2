# Examiner reassessment — DNN Assignment 2

Review date:9 November2026; Viradiya Tushar Rajeshbhai,2026aj05073.

**Conditional technical estimate:98/100 (plausible examiner range96–99). Prior estimate96/100 (93–98). These are judgments, not awarded marks or guarantees. Eligibility under the AI policy remains unresolved.** The complete earlier evaluation is preserved in baseline-2026-11-09/docs/professor-evaluation.md; commit817a025 anchors the baseline artifacts.

## Evidence and scope

The original DOCX and100-point rubric were read, including the CPU exception, every required figure, exact CSV schema, report format and integrity clauses. User-supplied instructor clarification permits chosen h64/d64/seeds0/1/2 and a self-created attention example. No instructor-authored AI-policy waiver was located; the reported verbal permission is not independently authenticated.

Both actual notebook sources/outputs, raw datasets, checkpoint structures, histories, prediction tables, figures, PDF and ZIP were inspected. Passing progress text was not accepted as proof. Existing component tests/negative controls, cache tests, four baseline checkpoint audits and complete notebooks were rerun; supplemental validation/sample/memory checks also ran. Final extraction replays existing local data/checkpoints; it is not a clean install, network download or fresh retraining of the original82 runs. Six adding diagnostics and four LM continuations were actually trained during this review. No test data were used for their selection.

## Rubric reassessment

Official rubric specifies task totals; finer deductions below are examiner judgments.

| Task | Max | Estimate | Verified evidence / remaining deduction |
|---|---:|---:|---|
| P1.1 Data |5|5|Official shapes/order/labels; four-subject holdouts and frozen training statistics; balance plot; supplied generator and independent target/marker checks.|
| P1.2 Cells |10|10 technical|All three reference forward/state/gradient tests pass; two-bias/single-bias derivations/counts correct. Source unchanged from baseline. Authorship eligibility unresolved.|
| P1.3 HAR |10|10|Nine equal-budget runs, three-seed accuracy/F1/counts/CPU time, validation-selected confusion matrix replay.|
| P1.4 Adding |10|10|All36 required tests/results/four lengths/solved counts/baselines/curves preserved and replayed; performance alone is not penalized.|
| P1.5 Analysis/ablations |15|15|Actual gradient probes, width/paired-bias studies and wearable trade-off. New overfit/pilot evidence recovers the earlier diagnostic-depth deduction, with explicit limits on T200–400.|
| P2.1 Attention |10|10 technical|Reference/row-sum/causal tests plus nonuniform QKV scalar hand oracle pass; original masked example retained. Authorship eligibility unresolved.|
| P2.2 MHA/block |10|10 technical|Pre-LN/residual/dropout/FFN/positions/reference tests and49152+832=49984 count; unchanged scratch source. Authorship eligibility unresolved.|
| P2.3 HAR encoder |10|9|All nine runs and operational comparison verified. Ordered within-patch offsets versus whole-patch invariance now explained and tested. Retain1-point discretionary deduction for limited controlled architectural comparison: depth/count/patching/dropout differ, and the new synthetic fixed-weight probe does not measure classification consequences. No attention-specific superiority claim is made.|
| P2.4 LM |10|10|Split/targets/masking/token-weighted loss/selected checkpoint/samples verified; equal additional-budget continuation documented. Main loss improves2.234945 to2.026947; weak language quality/one seed/restart confound remain explicit.|
| P2.5 Analyses |10|9.5|Heads/mask studies preserved; raw five timing repeats and12 memory-event traces reconstruct peaks. Indexed head links are more concrete. Retain0.5 for interpretation limited to two heads/one short character sentence without intervention.|
| Technical task subtotal |100|98.5|Conditional on authorship acceptance.|
| Presentation adjustment |—|−0.5|Sequential figures/subpanels and larger labels improve readability; dense six-page evidence still needs careful reading at final size. Discretionary rather than an official separate tariff.|
| Estimated total |100|98|Bonus0; not attempted.|

The estimate changes because specific evidence gaps were filled, not because additional effort automatically earns marks. Deductions overlap with subjective examiner preferences; the range reflects that uncertainty. There is no promise of full marks or freedom from integrity risk.

## Before and after under comparable conditions

- **Adding T50 seed0:** original first-five-epoch train/validation trajectories are exactly replayed in each25-epoch pilot. Best validation drops to0.013271 (LSTM) and0.001890 (GRU), while RNN remains0.164630. All three overfit32 examples. This isolates duration as a limitation for gated short-sequence training with the fixed protocol. It does not demonstrate revised test performance, a three-seed improvement or long-memory success atT400. Original36 unsolved results remain visible.
- **LM:** four-head selected validation2.234945→2.026947 nats; architecture/data/batch/lr unchanged, five extra epochs and Adam reset. All four variants get the same continuation rule. This is a within-variant comparison, not an isolated duration effect or fresh matched initialization. Original five-epoch head/mask ablations remain the causal-comparison evidence; continued unmasked validation is contaminated.
- **HAR:** no new accuracy claim. Positional mechanism and the limits of the existing2.42-point encoder/GRU operational gap are clearer. Model count/depth/patch/dropout confounds remain.
- **Measurement/report:** historical aggregate timings are preserved; new raw repeats/traces add auditability. Numbering is consecutive, matrix arithmetic nontrivial, captions explicit and figures regenerated for final sizing. Context remeasurement is not claimed to be a speed improvement.

## Integrity and external conditions

Complete AI disclosure remains in the PDF, including AI-written restricted scratch components and this review's analysis/experiment assistance. No independent student derivation or reasoning is invented. Technical success and truthful disclosure do not establish instructor permission. If original restrictions are enforced,30 directly affected scratch-task marks and potentially broader institutional consequences remain exposed; this is not a prediction of penalty or a misconduct finding.

The assignment FAQ states no formal viva; earlier review language suggesting one was a formal requirement is corrected. Understanding preparation and any necessary student-authored remediation are separately flagged in understanding-checklist.md. No clean dependency installation, GPU/T4 timing, wearable energy, external similarity/originality certification, portal upload/download or receipt is claimed.

**Readiness: locally verified technically; awaiting resolution of authorship authorization and external portal submission steps.** See submission-readiness.md for the final archive/check evidence. No commit, push, publication or submission was performed during this review.
