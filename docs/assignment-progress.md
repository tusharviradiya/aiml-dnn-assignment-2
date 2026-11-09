# Assignment progress

Updated after instructor clarification. Status values: Not Started, In Progress, Completed, Blocked.

**All rubric tasks have verified supporting evidence; estimated quality is assessed separately in professor-evaluation.md, not an awarded grade.** h=64, d=64, seeds0/1/2 are chosen settings. All82 experiment rows remain unchanged. P2 attention hand/code tests pass. Examiner-led diagnostics, LM continuations, component/audit checks and both full notebooks passed. Final report/archive validation is recorded in submission-readiness.md. Academic-integrity authorization is not independently verified; technical completion is not unconditional submission clearance.

| Task | Marks | Status | Verified acceptance evidence |
|---|---:|---|---|
| P1.1 Data | 5 | Completed | Official HAR, ordered nine channels, subject split, training-only normalization/class balance; exact adding generator and marker/target assertions |
| P1.2 Cells | 10 | Completed | Tensor-only RNN/LSTM/GRU; eight cases each; max errors1.19e-7/2.38e-7/2.38e-7; correct single/two-bias counts; backward checks |
| P1.3 HAR | 10 | Completed | Nine equal-budget runs, three seeds/model, accuracy/F1 sample mean/std, counts/timing, validation-selected confusion matrix |
| P1.4 Adding | 10 | Completed | 36 full-data runs, four lengths, MSE/baselines, solved counts, learning curves; all unsolved honestly reported |
| P1.5 Gradients/ablations/analysis | 15 | Completed | 18 verified gradient probes;24 width-sweep points;6 paired forget-bias runs; one-page analysis and wearable trade-off |
| P2.1 Attention | 10 | Completed | Row sums/reference<1e-5/causal zeros; uniform and nonuniform3×2 Q/K/V scalar hand calculations agree with code; own example allowed by clarification |
| P2.2 MHA/block | 10 | Completed | Tensor attention, pre-LN/residual/dropout/4d FFN, sinusoidal positions; d64 count49152+832=49984 verified |
| P2.3 HAR encoder | 10 | Completed | CLS/patch8 classifier, three positional options×three seeds, accuracy/params/time against P1 |
| P2.4 Character LM | 10 | Completed | Whole-text65-character vocabulary, contiguous90/10 split, CPU two-layer configuration, validation nats/BPC/curves, three500-character top-k samples |
| P2.5 Analysis/ablations | 10 | Completed | Two head maps/interpreted; heads1/4/8; no-mask losses/generation/future perturbation; four contexts timing/tensor-memory/scaling |
| Optional bonus | up to5 | Not Started | Optional; no claim |
| Clarified report/ZIP | — | Completed | Seven-page PDF (six assessed), archive CRC/manifest/size checks, both extracted notebooks and all four experiment audits passed; final documentation/presentation rebuild preserves executed notebook and audit sources |
| Integrity authorization | — | Blocked | Actual AI-written scratch code disclosed; original prohibition conflicts with user-reported verbal permission; supplied email does not resolve it |
| Portal submission | — | Not Started | Due Saturday14 November2026; upload/download/open and confirmation remain external |

## Instructor clarification applied

See instructor-clarifications.md. Sizes/seeds are legitimate choices and our self-created example is sufficient when tests pass. No assigned-value lookup or external hand fixture is required. Report/README list all chosen values; d64 matrices49152, biases/norm832, total49984.

## Verification and reproducibility

No models are retrained for clarification changes. Model/training-loop ASTs match the committed version; exact cache aliases only cover comment/requirement text changes. Full execution is guarded: creating an Adam optimizer aborts verification on a cache miss. Raw data/checkpoints remain local, outside submission. Final verification records and rubric review are in submission-readiness.md.

## Integrity review

Original brief requires student-authored scratch implementations and declaration of every AI use. Codex actually wrote scratch cells, attention/block components and substantial pipelines/report material. This is explicitly declared. User reports Samsir verbally allowed AI and said not to mention it for manual parts; no instructor-written waiver is supplied. We retain truthful disclosure and cannot certify an exception from the supplied documents alone. Other integrity checks (permitted datasets, no pretrained weights, framework-reference isolation, measured results) pass.

## Examiner-led supplemental review

Baseline82 experiments preserved. Six adding diagnostics Completed: all cells overfit32 examples; common25-epoch T50 validation pilots reproduce baseline first five epochs, then gated models generalize below0.05 without accessing test data. Four equal-budget LM continuations Completed; both notebooks and all baseline/supplemental tests passed. Final PDF/archive checked after synchronization. See review-evidence/protocol.md; this work does not change the restricted scratch code or resolve integrity authorization.

## Current reproducibility release — supersedes prior packaging/workflow claims

- Self-contained supplemental adding/LM experiment sections and report graphics:
  Completed; P1 has141 executed code cells, P2 has55, with no saved errors.
- Primary LM/sample alignment: Completed; continuedh4 causal2.0269467nats /2.924266BPC;
  required file regenerated from the recorded selected checkpoint. Baseline preserved.
- Future optimizer/RNG resume-state saving: Completed; exact next stochastic Adam
  update/loader sequence restoration test passes. Historical states remain absent.
- Read-only audit immutability and minimal extraction execution: Completed after
  actual nine-audit and packaged-notebook checks; see submission-validation.md.
- Course authorization scope and external portal steps remain unverified; no change
  to student-reported status. No new scratch implementation or full retraining.
