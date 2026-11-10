> Historical review record. Current verification and policy status are in [submission-validation.md](submission-validation.md). Prior authorship or permission assertions are not evidence of instructor authorization.

# Requirement-to-evidence audit — updated 2026-11-10

Current release status and executed checks: `submission-validation.md`. Authorship
compliance is blocked; technical evidence below is not a claim of student authorship.

Controlling sources: original DOCX and its100-point rubric, an unauthenticated local clarification summary,
and the CPU exception in the original FAQ. Progress records are claims checked against
code, artifacts and checkpoint replay. The prior release is preserved in Git2689b65;
pre-change notebooks/PDF/ZIP/samples are also retained in ignored
`data/reproducibility-baseline-2026-11-09/`. This internal file is excluded from submission.

## Requirement-to-evidence checklist

| Requirement | Marks | Concrete deliverable/evidence |
|---|---:|---|
| P1 data: official shapes/channels/labels; subject split; train-only normalization; balance |5|P1 Tasks1/3 assert cells; Figure1; independent nine-checkpoint audit |
| Exact adding generator and two-marker/target tests |included|P1 Task1 assert cells; fixed independent target sum in diagnostic code |
| RNN/LSTM/GRU equations, registration, shapes, weight-copy, forward <1e-5 |10|P1 Task2; all reference checks and negative controls; original model source hashes unchanged |
| Single/two-bias counts d9/h64 |included|Report page1; actual4800/19200/14400 vs single4736/18944/14208; backward tests |
| Last-state HAR; common h/Adam/lr/batch/epochs;3 seeds; mean/sample std/F1/params/time |10|P1 Task3;9 rows; Table1; validation-selected Figure2 confusion matrix |
| Adding4 lengths ×3 models ×3 seeds; constant baseline; solved counts; T200 curves |10|P1 Task4;36 rows; Table2; Figure3; all36 unsuccessful results preserved |
| T100 hidden gradients before/after; width16/32/64/128; odd-ID forget-bias0/1 T200 |15|P1 Task5;18 probes/24 sweep points/6 paired bias runs; Tables3–4, Figures4–5 |
| One-page interpretation and wearable recommendation |included|Report page3: quantitative trade-offs and limited inference; Table5 clearly validation-only |
| Attention optional/causal mask; row sums/reference/zero future; hand example |10|P2 Tasks1–2 assert cells; report page4 explicit nonuniform Q/K/V and scalar exp calculation |
| QKVO heads/pre-LN/FFN4d/residual/dropout/sinusoidal positions; weight+bias/norm counts |10|P2 reference/backward/assert cells;49152+832=49984 atd64; derivation report page4 |
| HAR patch8+CLS comparison and none/sinusoidal/learned |10|P2 TaskA;9 runs; Table6/Figure6; fixed-weight patch-order probe; confounds explicit |
| 65-char whole-text vocab; contiguous90/10 no shuffle; next-token context128 |10|P2 TaskB; boundary oracle and weighted-loss fixture; d64/two-layer CPU exception |
| LM learning curve/nats/BPC;3 labelled500-char samples at.2/.8/1.5 |included|Table7/Figure7; primary continued four-head checkpoint printed with config/SHA; required sample file |
| Two heads/sentence; heads1/4/8 fixed-width; no-mask train/generation; contexts64/128/256/512 |10|P2 analysis cells; Tables7–9/Figures7–9; raw timing repeats and allocation traces retained internally |
| No forbidden framework scratch layers/no pretrained weights/only named datasets |cross-cutting|AST/source inspection; library layers only reference tests or permitted P1 experiment layers |
| Exact12 CSV columns; per-run saving; irrelevant fields empty; fixed seeds/relative paths |cross-cutting|92 unique rows; original82 bytes unchanged; direct notebook assertions and independent audits |
| Restart & Run All, saved outputs; assert cells following tested components; shape comments |cross-cutting|Both required notebooks include baseline and supplemental experiments, all code inline |
| A4/11pt/≥2cm/≤6 assessed pages; numbered/captioned/cited required figures/tables |cross-cutting|PDF validator plus rendered-page inspection; AI statement/references on excluded seventh page |
| README≤1 page; pinned dependencies/settings/runtime/limitations |cross-cutting|One-page rendered README; measured CPU time; T4 runtime explicitly unmeasured |
| Prescribed ZIP name/root;≤25MB; required files only; no data/weights/env |cross-cutting|Explicit allowlist in internal packager; fresh extraction/CRC/hash checks |
| Portal upload/download/open confirmation |external|Not performed; cannot infer success from local ZIP |
| AI-use declaration |integrity|Concise complete report-end declaration includes AI-written scratch code; written scratch-code authorship rule remains unmet |
| Optional bonus |0 claimed|Not attempted |

## Design and provenance

The primary language model is **four-head causal, selected additional epoch5**,
validation2.0269467236664482nats /2.924265986379717BPC. Its checkpoint SHA256 is
`310136e793bb0f86d3a6fb0ae9579ca1b696be71d406cdd26c69c2e05af04849`.
The required sample file now corresponds to this checkpoint. Baseline samples remain
internally in the historical snapshot and metrics. Baseline five-epoch head/mask
ablations retain identical initialization; continuation variants start from their own
selected weights and all restart Adam. Five extra epochs and optimizer restart are
joint changes, not an isolated estimate of either effect. Heatmaps and context costs
are explicitly from the five-epoch baseline, not the primary continued checkpoint.

All report experiments and figures are generated by the two submitted notebooks.
No docs/scripts/metrics directories are needed at extraction. Metric histories and
measurement records are generated on execution; matching ignored local caches allow
replay. A clean run trains missing experiments and measures new hardware-dependent
times. Replay does not constitute fresh training or a new timing measurement.
Historical optimizer/RNG states are absent. Future runs save separate model/optimizer,
selection/history, Python/NumPy/Torch/CUDA and loader-generator resume states; a stochastic
Adam next-update test verifies restoration. No historical states were invented.

Verification loads definitions without executing setup/experiment cells. It compares
saved evidence instead of replacing it. The audit harness hashes artifacts before and
after all checks. Notebook execution and figure generation are explicit mutations,
separate from read-only audits. Idempotent cached logging preserves existing CSV bytes.
Exact reviewed source/config aliases are embedded in required notebooks; changed
training definitions/config/data invalidate reuse. Checkpoint paths derive from
saved configs/current experiment cache, not literal historical IDs in helper scripts.

## Scope of conclusions

Small-batch fitting detects trainability, not generalization. T50 single-seed gated
validation improves with25 epochs; this is not a revised test result or evidence for
T400 memory. The assessed36-run grid remains unsolved. Patch flattening retains
within-patch offset order; absence of global positions makes CLS invariant to whole
patch permutations. HAR architecture/size/depth/dropout/patching differences prevent
attention-only attribution. Unmasked LM inputs reveal future targets, contaminating
validation and making generation behavior a necessary diagnostic. Attention links are
observations, not causal explanations; profiler peaks measure additional live tensor
bytes under one workload, not RSS, energy or reserved GPU memory.

Execution results and final artifact details are recorded in submission-validation.md.

## Focused final revision: supplemental compatibility and disclosure

Supersedes the earlier broad claim that all supplemental cache compatibility was
already guarded. The final review found adding lookup preceding requested budget
resolution and continuation lookup lacking baseline identity. Both are corrected.
Complete contracts cover requested settings plus source/data/runtime; LM includes
baseline key/hash/selected epoch/loss. The23 negative controls in the added cache
test reject stale evidence before evaluation, logging or training. All ten existing
supplements pass reviewed legacy bindings. Full evidence and provenance limits are
in review-evidence/supplement-cache-bindings.json; no historical metadata is rewritten.
Current observed baseline hashes are retrospective, not proof of training-time identity.

Only three recurrent class docstrings changed in graded implementation cells; exact
executable-AST comparison against39112c6 passes. Full disclosure is consolidated at
report end; no informal-permission narrative remains in submitted sources/outputs.
No verified exemption exists; independent student reimplementation remains required.
Root and final extracted notebooks pass141/55 code cells; ten audits leave296 checked
files unchanged. Exact final artifact details are in submission-validation.md.
