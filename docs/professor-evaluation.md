# Conditional technical evaluation — final minimal release

Reassessed against the original100-mark rubric and current code/artifacts, not effort.
**Estimate: approximately97/100, plausible examiner range94–99.** This is not an
awarded mark, a guarantee or an authorship determination. The previous98 estimate
was optimistic while supplemental notebook integration and package scope remained
incomplete; correcting those issues does not justify automatic score inflation.
Historical evaluations remain in Git2689b65 and docs/baseline-2026-11-09/.

| Task | Available | Conditional estimate | Evidence / possible deduction |
|---|---:|---:|---|
| P1 data |5|5|Official data/splits/statistics; marker/target tests; balance plot |
| P1 scratch cells |10|10 technical|Forward/backward reference agreement, registered shapes, correct counts; authorship scope separate |
| P1 HAR |10|10|Common budgets,3 seeds, actual test mean/sample std/F1/count/time, validation-selected confusion |
| P1 adding |10|10|Complete36-run grid, baseline/solved table/T200 curves; poor performance alone is not a method deduction |
| P1 analysis/ablations |15|15|Actual hidden gradients, width/bias controls, evidence-grounded one-page analysis; diagnostic scope limited correctly |
| P2 attention |10|10 technical|Mask/reference/backward checks plus nonuniform explicit hand/code arithmetic |
| P2 multi-head/block |10|10 technical|Own tensor implementations, pre-LN/residual/FFN/positions; d64 derivation matches49984 |
| P2 HAR |10|8.5|Operational comparison valid; lack of matched parameter/depth/patch/dropout controls limits strength of attention-specific comparison |
| P2 LM |10|10|Complete data/targets/loss/curves/BPC/sample requirements; primary model/sample mapping explicit; weak quality and single seed limit conclusions, not automatic accuracy penalties |
| P2 analyses |10|9|Heads/mask/context studies complete; interpretation remains two heads on one sentence, without a causal intervention or repeat inputs |
| Total before discretionary presentation effects |100|97.5|Approximate97 after allowing for dense small-panel presentation; no official fixed tariff is invented |

All task coverage is present. The estimate's range allows different examiner judgments
about the stated confounds, dense six-page presentation, CPU-only measurement and
scope of analysis. Bonus0, not attempted. No deduction arithmetic predicts treatment
under institutional academic-integrity policy; if the original scratch-authorship
rule applies without an exception, outcomes could differ materially.

## Current verified improvements

- Both submitted notebooks include all report-used supplemental experiment and figure
  code; no excluded helper dependency. Minimal extraction runs141/55 code cells.
- Required samples now come from the primary continuedh4 causal checkpoint; baseline
  samples remain internal. All3×500 primary characters reproduce exactly from weights.
- Verification executes definitions only and compares evidence without writing it;
  all nine audits pass with before/after hashes. Exact92-row ledger retains82 original
  rows byte-for-byte. Future stochastic Adam resume restoration is tested; no missing
  historical optimizer/RNG states are invented.
- Final PDF remains six assessed A4/11pt/2cm pages plus an excluded declaration/reference
  page. Nine report figures cover all required panels; internal provenance is excluded
  from the16-file ZIP. These are reproducibility/presentation changes, not new training gains.

## Unchanged experimental outcomes and limitations

Adding original36 test runs remain unsolved. T50 seed0 gated validation improves at
25epochs (LSTM0.013271, GRU0.001890) while RNN remains0.164630; no revised test grid
or long-memory generalization is established. The primary LM remains2.026947nats /
2.924266BPC, versus its baseline2.234945nats /3.224344BPC; continuation adds five epochs
and resets Adam jointly. HAR scores are unchanged. Timings remain historical measured
CPU timings, not new T4 results. Full fresh training and dependency installation were
not repeated; cached extraction is accurately identified.

The student reports informal AI permission. The supplied email only changes sizes,
seeds and the example; no written scratch-code exemption is asserted. Complete,
concise disclosure remains at report end. No personal understanding, institutional
approval, originality certification or portal submission is claimed. The internal
understanding checklist is preparation only; the original FAQ says no formal viva.
