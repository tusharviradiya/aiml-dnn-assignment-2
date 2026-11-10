# Strict rubric review — 10 November 2026

**Estimated technical score: 95/100, conditional on instructor acceptance of authorship.**
This is a review estimate, not an awarded mark. It supersedes older optimistic estimates.
The original rubric rewards method and evidence, so weak adding performance or LM loss
outside the sanity range does not automatically lose marks. The original discretionary
reproducibility/format deduction is up to ten; the allowance below is our estimate.

| Rubric item | Maximum | Estimated technical credit | Evidence and remaining reservation |
|---|---:|---:|---|
| P1.1 Data pipelines | 5 | 5 | Prescribed HAR shapes/channels, subject split, training-only normalization, balance plot; exact adding generator/assertions |
| P1.2 Scratch cells | 10 | 10* | Forward/backward reference agreement, registration and both bias-count conventions; authorship blocked |
| P1.3 HAR | 10 | 10 | Nine matched-budget runs; accuracy/F1 mean and sample std, counts, timings, validation-selected confusion |
| P1.4 Adding | 10 | 10 | All 36 runs, four lengths, seeds, baseline, solved counts and T=200 curves; no deduction solely for unsolved runs |
| P1.5 Gradients/ablations/analysis | 15 | 15 | 18 gradient probes, 24 sweep results (six reused), six paired forget-bias runs; quantitative one-page interpretation |
| P2.1 Attention | 10 | 9* | Mask/reference/gradient tests and nonuniform hand calculation; instructor fixture missing, substitute acceptance unverified |
| P2.2 Multi-head/block | 10 | 10* | Shapes, pre-LN/residual/4d FFN/positions; d=64 and required d=128 weight/bias/norm counts; authorship blocked |
| P2.3 HAR encoder | 10 | 9 | Three position choices × three seeds and P1 reuse; architecture/patching/dropout/size confound mechanism comparisons |
| P2.4 Character LM | 10 | 10 | CPU exception, split/targets, validation curve/nats/BPC, three reproducible labelled 500-character samples |
| P2.5 Analyses/ablations | 10 | 9 | Heads/mask/context studies and actual allocation traces; interpretation covers two heads on one sentence, no broad specialization claim |
| Subtotal | 100 | 97 | Method/evidence estimate; no invented official fixed deduction tariffs |
| Cross-cutting allowance | — | -2 | T4 total runtime remains missing; dense small figure panels and incomplete full-training reproducibility verification |
| Conditional technical estimate | 100 | **95** | Plausible examiner range 92–98; bonus 0 |

The starred 30 points concern explicitly restricted scratch work. Technical correctness
cannot establish eligibility for those marks. Development records identify AI-written
code, current source matches that baseline, and the student confirmed no verified
instructor exemption is available. Disclosure has been restored, but this does not
resolve the prohibition. An actual grade cannot be responsibly predicted under the
institute's integrity policy; it may be substantially lower than 95, including zero
if the applicable policy so determines. No specific institutional sanction is asserted.

All 92 rows are supported by preserved checkpoint/metric evidence and the ten read-only
audits. Final clean-extraction execution and packaging evidence are recorded in
[submission-validation.md](submission-validation.md). Full uncached training and T4
runtime were not measured in this audit. Historical optimizer/RNG states are unavailable;
continued LM training resets Adam. Single-seed LM evidence remains single-seed.
