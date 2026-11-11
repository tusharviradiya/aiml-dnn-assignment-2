# Submission audit — 11 November 2026

Student ID: **2026aj05073**. Verified at **2026-11-11T04:09:25.862996+00:00**.
Authority: the supplied original assignment DOCX, read in full before changes;
SHA-256 `37311ac57faf68aaf1adc2e69c312fe9325154f3d3de93b2abbd2304e14e950d`.
No instructor-confirmation or changed-rule claim is inferred from local documents.

**The ZIP is structurally ready to upload.** Package integrity and cached notebook
execution passed. This does not certify full cache-free training reproducibility or
academic-policy acceptance. No report, implementation, result or saved notebook
output was changed. The report was not regenerated.

## PASS / WARNING / FAIL

| Status | Requirement | Actual finding |
|---|---|---|
| PASS | Exact archive/root and required files | `2026aj05073_DNN_Assignment.zip`, one prescribed root, 16 allowlisted files; reopened, CRC checked, extracted and compared to source bytes |
| PASS | Size and exclusions | 1,916,033 bytes, below 25 MB; no data, weights, environments, caches, internal scripts/metrics/docs or audit documents |
| PASS | Notebook validity and outputs | P1: 141 code cells; P2: 55; valid notebook schema, sequential saved counts, no saved error outputs; original bytes preserved |
| PASS | From-scratch numerical verification | Strict recurrent/attention/block gates, reference/gradient/mask tests, negative controls and parameter sums pass; no implementation rewritten |
| PASS | Dataset and experiment evidence | Fixed official channels/shapes/subject splits, train-only statistics, prescribed adding generator/data seeds, counts and matched configurations checked against checkpoints |
| PASS | CSV | Exact 12 columns, 92 unique records (75 P1, 17 P2), preserved canonical bytes, irrelevant fields blank and BPC = nats / ln(2) |
| PASS | Report and CSV consistency | Nine PDF tables, 31 data rows checked against recorded metrics; all displayed numbers agree at reported precision |
| PASS | Required figures and samples | Nine packaged report figures reproduce exactly; three labelled primary samples each have 500 new characters at temperatures 0.2/0.8/1.5 and match selected weights |
| PASS | PDF | Six assessed pages + excluded AI-use/reference page; A4/11pt source, PDF text margins at least 2 cm, embedded fonts, numbered/captioned/referenced tables and figures; current pages visually inspected |
| PASS | README | Environment, commands, assumptions, measured CPU runtimes, cache/training distinction and limitations present; Pandoc A4/11pt/2cm render is one page; no condensation needed |
| PASS | Extracted execution | Both complete workflows ran in an isolated extraction with copied historical data/checkpoints/measurements and an Adam-construction guard; 141/55 cells passed; no excluded helper dependency |
| PASS | Preservation | All 300 protected files, including original DOCX, report, notebooks/outputs, results, samples, metrics, figures and experiment caches, remain byte-identical; rebuilt ZIP bytes also match the previous valid archive |
| WARNING | Full fresh reproduction | Clean downloads, fresh dependency installation and complete assessed training sweeps were not repeated; cached replay is not fresh training |
| WARNING | Resume and inference limits | Historical optimizer/RNG states are missing; continued LM resets Adam; single-seed LM comparisons, weak samples and architectural comparison confounds remain disclosed |
| WARNING | Adding quality | All 36 baseline runs remain unsolved; longer T=50 validation-only pilots support a limited duration diagnosis, not new test results or T=200–400 success |
| WARNING | Variant and fixture | Referenced variant table and instructor hand fixture are absent; h64/d64/seeds0/1/2 and the self-created example remain explicit assumptions under the original missing-information clause |
| WARNING | Deadline and portal | Date/weekday wording is inconsistent and portal link is unfinished; authoritative deadline, upload, downloaded-copy check and receipt remain student actions |
| FAIL — requirement unmet | T4 runtime in README | T4 total runtime remains unmeasured; this CPU-only machine cannot supply it. Actual CPU times remain accurately labelled; no time is invented |
| FAIL — unresolved compliance | Original scratch-authorship restriction | Existing records disclose AI-written restricted components and broader assistance. No applicable instructor exemption is verified. Technical tests and disclosure do not establish authorship or permission |

The FAIL rows identify unresolved submission requirements, **not failing numerical
unit tests**. There are no remaining failed technical checks from this audit.

## Files changed and preserved

Added:

- `SUBMISSION_AUDIT.md` — this audit, evidence, student plan and remaining actions.
- `REPORT_MANUAL_EDITS.md` — page-specific REQUIRED/CONDITIONAL/OPTIONAL review
  instructions, including explicit findings where no PDF change is necessary.

Updated:

- `docs/assignment-progress.md` — link to this current review and preservation status.

Rebuilt/reopened:

- `2026aj05073_DNN_Assignment.zip` — 16 prescribed files, unchanged valid payload
  and byte-identical archive hash. The two requested audit documents remain outside it.

No README condensation was necessary. `README.md`, `requirements.txt`, both
notebooks including outputs, all six restricted implementations, `results.csv`,
metrics, figures, samples, `docs/report.tex`, report generator and `report.pdf`
remain unchanged. The original instructor DOCX was only read.
Verification logs, renders and read-only check code are local in
`.cache/pre-submission-2026-11-11/`; these are not submission artifacts.

## Checks actually executed

Pinned environment reused: Python 3.14.4, four CPU threads, CUDA
available: **False**. All eight direct package pins match:
numpy 2.5.4, pandas 3.1.1, matplotlib 3.11.2, scikit-learn 1.9.1, torch 2.15.0+cpu, nbformat 5.11.1, nbclient 0.11.0, ipykernel 7.4.0. `pip check` passed. No new environment installation is claimed.

| Command | Result | Current log |
|---|---|---|
| `scripts/test_verification.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/test_verification.log` |
| `scripts/test_cache_fingerprints.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/test_cache_fingerprints.log` |
| `scripts/test_supplement_cache.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/test_supplement_cache.log` |
| `scripts/test_reproducibility.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/test_reproducibility.log` |
| `scripts/audit_har.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/audit_har.log` |
| `scripts/audit_adding.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/audit_adding.log` |
| `scripts/audit_task5.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/audit_task5.log` |
| `scripts/audit_problem2.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/audit_problem2.log` |
| `scripts/review_checks.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/review_checks.log` |
| `scripts/normalize_review_ledger.py` | PASS, exit 0 | `.cache/pre-submission-2026-11-11/normalize_review_ledger.log` |
| `scripts/validate_report.py` | PASS layout, evidence and declaration checks | `.cache/pre-submission-2026-11-11/report-validation.log` |
| Local read-only `check_report_tables.py` | PASS 9 tables / 31 rows, schema/BPC, CPU time totals, saved notebooks, version pins, d64/d128 counts | `.cache/pre-submission-2026-11-11/report-table-checks.log` |
| `scripts/package_submission.py` | PASS allowlist, size, CRC, safe root, extraction, source hashes | `.cache/pre-submission-2026-11-11/packaging.log` |
| `scripts/verify_extracted_submission.py` | PASS complete P1/P2 execution in disposable extraction | `.cache/pre-submission-2026-11-11/extraction.log` |
| `python -m pip check` | PASS no broken requirements | `.cache/pre-submission-2026-11-11/pip-check.log` |
| Pandoc README render + pdfinfo | PASS one A4 page | `.cache/pre-submission-2026-11-11/README.pdf` |
| PDF text/bounds, font extraction, image inventory and rendered-page review | PASS | `.cache/pre-submission-2026-11-11/report.txt`, `report-stext.xml`, `pdf-images.txt`, `report-page-*.png` |

The ten read-only audits hashed 296 evidence files before and
after execution, with no changes. Original notebook and report hashes also match the
start-of-review snapshot. A new audit assertion initially treated legitimate empty
CSV fields as non-finite values; the read-only check was corrected to ignore allowed
blanks and all final checks passed. No scientific data was changed to satisfy a test.

The reproducibility test includes disposable tiny training/resume fixtures and
checks restoration of optimizer and Python/NumPy/Torch/loader RNG state. These are
not assessed experiments and add no submission result rows.

### Execution scope and tests not run

- Full **extracted** notebooks ran using independently copied existing raw data,
  experiment checkpoints and saved measurements. No scripts/docs/preexisting metric
  folders were copied into the extracted submission. The training guard rejected
  optimizer construction, and the ZIP itself remains free of these verification inputs.
- `results.csv`, generated samples, all nine packaged figures and report content
  matched source bytes after the extracted run. Original saved notebooks were neither
  rerun in place nor resaved in this audit.
- No complete uncached assessed sweep, fresh network download, fresh dependency
  install, new T4 measurement, long adding rerun, new LM continuation, bonus model
  or report rebuild was executed. No causal claim about the effect of Adam reset,
  attention specialization, or wearable energy is established by these checks.
- Jupyter requires local TCP sockets; execution used the approved escalated kernel
  path because the sandbox blocks those sockets. The extraction and training guard
  kept the original report/notebooks/results intact.

## Verified result accounting

The exact `results.csv` header is:

```text
problem,model,seed,seq_len,test_acc,macro_f1,test_mse,params,sec_per_epoch,val_loss_nats,bits_per_char,notes
```

| Group | Ledger rows | Notes |
|---|---:|---|
| Original P1 recurrent HAR | 9 | Three models × three seeds |
| Original P1 adding | 36 | Three models × four lengths × three seeds |
| Additional P1 HAR width sweep | 18 | Full sweep has 24 points; six h64 points reuse original HAR runs |
| Original odd-ID P1 forget-bias study | 6 | Bias0/1 × three seeds at T200 |
| Original P2 HAR | 9 | No/sinusoidal/learned positions × three seeds |
| Original P2 LM head/mask study | 4 | Causal heads1/4/8 and unmasked heads4 |
| Validation-only adding diagnostics | 6 | Three overfit checks + three longer pilots; test metrics empty |
| Continued P2 LM variants | 4 | Five extra epochs, common Adam reset rule |
| Total | **92** | Original82 + additional10; no values replaced |

HAR remains approximately 70.52% RNN, 87.71% LSTM and 88.19% GRU. The primary
continued four-head causal LM remains 2.0269467236664482 validation nats /
2.924265986379717 BPC; no-mask losses are explicitly contaminated by future tokens.
All reported mean/sample std, parameter totals and recorded timing aggregates agree.
Measured baseline training totals 44.7 CPU minutes, LM continuation 9.13 additional
training minutes, and adding diagnostics approximately 123 seconds wall time. Those
quantities exclude other execution/validation overhead and are **not T4 runtimes**.

## Why the original adding grid is unsolved

Evidence supports a limited explanation, not a fabricated fix:

1. All 36 five-epoch test MSE values are at or near the constant-1 baseline. Across
   those saved runs, mean predictions are roughly 0.964–1.056 and within-run
   prediction standard deviations roughly 0.0055–0.0277. This is consistent with
   learning a low-variation prediction near the target mean instead of reliably
   adding marked values. It does not itself locate a coding defect.
2. Independent tests/checkpoint replay verify the prescribed generator, markers and
   targets, state reset, finite gradients, parameter updates and metric calculation.
   All three models can fit 32 examples below MSE0.05. That small-set test is a
   pipeline sanity check and does not establish generalization.
3. With identical data/initialization/shuffle/batch/optimizer, the T50 seed0
   validation-only pilots reproduce their original first five epochs. Continuing
   to 25 epochs yields validation MSE0.16462985 (RNN), 0.01327108 (LSTM) and
   0.00189044 (GRU). Test data were not evaluated in these pilots. This supports
   insufficient duration for the gated T50 runs under this protocol.
4. It does **not** demonstrate that every short-sequence run will solve, that
   25 epochs suffice at T200/T400, or that all vanilla-RNN failures have the same
   cause. Existing hidden-gradient attenuation is supporting diagnostic evidence,
   not proof of a general memory ranking; LSTM has a separate cell-state path.

No original test result was replaced by a diagnostic. The original brief explicitly
accepts outcomes outside the approximate sanity range when method and analysis are sound.

## STUDENT-EXECUTABLE fair-rerun plan — not executed

No replacement experimental or from-scratch code is supplied here. Use the existing
notebook infrastructure where suitable; any necessary adaptation must be performed
by the student, preserving the restricted components and all historical evidence.
A rerun is optional for this audit and cannot resolve the AI-authorization issue.

### 1. Preserve the baseline and choose the budget before new test inspection

- Preserve the current 92-row CSV, notebooks, histories, figures, report and original
  checkpoints as a labelled baseline. Work in a separate student-controlled copy or
  new experiment namespace; do not enable a force-rerun switch against old paths.
- A minimal evidence-backed choice is **25 fixed epochs for every model/length/seed**,
  chosen now from the already observed T50 validation-only evidence. Record that
  rationale and the complete protocol before running the new grid. This is a budget
  choice, not a promise that all runs will solve.
- If you want further tuning, use training and validation data only, compare the same
  predeclared candidate budgets (for example5/10/25/50) across all models and lengths,
  and fix one common final budget by a stated validation rule and compute limit.
  Log all pilots, including unsuccessful ones. Do not adjust budgets per model/seed
  or extend only runs whose test results disappoint.
- The existing `run_adding` evaluates test data at completion. **Do not use it as a
  validation-only budget-search routine.** Existing validation-only diagnostic helpers
  support separate requests; any student adaptation must keep test construction and
  evaluation out of the pilot phase and use new compatible cache identities.
- The prescribed test set has already been evaluated in the baseline. Call the result
  a validation-guided rerun on that same prescribed test set, not a new untouched
  holdout. Avoid making further choices from the new test results or claiming that
  prior test exposure has been undone.

### 2. Execute one complete matched grid

- Use the exact existing `make_adding` generator. For each T50/100/200/400, retain
  10000 training sequences with data seed0, 1000 validation with data seed1 and
  1000 test with data seed2. Data seeds and model seeds serve different purposes.
- Run **RNN/LSTM/GRU × T50/100/200/400 × model seeds0/1/2 =36 new final runs**.
  Retain h64, last-state regression head, Adam lr0.001, batch128, norm1 clipping,
  the same initialization rules and recorded CPU/device environment. Change the
  duration only for the proposed comparison. Do not change model sizes or data.
- Start each run from its recorded random seed with fresh optimizer/loader RNG;
  historical final `.pt` weights lack the optimizer/RNG states for an equivalent
  resume. Loading old weights and resetting Adam would be a different continuation
  protocol and must not be called a duration-only fresh-grid rerun.
- Train for the common fixed budget. Select the lowest-validation-MSE checkpoint
  with the same earliest-tie rule. Do not select checkpoints using test MSE.
- Once the protocol is locked, evaluate that selected checkpoint on the prescribed
  test set. Keep every completed run, failed/unsolved outcomes included. Solved still
  means **test MSE<0.05**. Compute mean and **sample** std over all three seeds.
- Give new configurations new run IDs, checkpoint/cache paths and truthful notes
  recording the exact budget. Do not make old checkpoints look compatible with new
  training via aliases. Save histories, timing, state and final CSV records for the
  actual new runs; do not create rows for planned runs.

### 3. Optional aligned gradient/bias follow-ups

- New T100 checkpoints allow inexpensive recomputation of the same before/after
  hidden-gradient probe, without another training sweep. Preserve the original
  18 probes/1800 rows separately; name the new evidence by the new run/budget.
- To study the odd-ID ablation at the new duration, complete **six separate T200 LSTM
  runs** (effective initial forget bias0/1 × seeds0/1/2) under the same new budget,
  holding other weights and data shuffle paired. Do not rerun only one bias or only
  favorable seeds. Otherwise retain the existing five-epoch ablation as explicitly
  labelled baseline evidence and claim no longer-budget ablation result.

### 4. Exact records, figures and report sections affected

| Artifact | If the new grid is completed | What remains preserved |
|---|---|---|
| `results.csv` | Append36 final-grid records with new run identity, actual test MSE, count/time/config notes. Exactly128 rows if these are the only new runs. Six new bias runs would give134; any new completed pilot rows add their actual count. | Original92 records, especially the 36 baseline-adding rows with `run_id=7d60ee6ede81051e`, modelsRNN/LSTM/GRU, lengths50/100/200/400 and seeds0/1/2. They occupy current data rows10–45 (file lines11–46). |
| `problem1/metrics/adding_runs.csv`, `adding_history.csv`, `adding_predictions.csv`, `adding_summary.csv`, `adding_config.json` | Save corresponding new-run records, histories, predictions and configuration in a separate namespace; derive the displayed primary summaries from the chosen, complete grid. | Keep the original5-epoch metric files and their connection to original checkpoints. |
| `problem1/figures/adding_mse_vs_length.png`, `adding_curves_t200.png`, `report_adding.png` | Regenerate the selected comparison from actual new means/std and T200 train/validation histories; clearly label budgets if showing both. | Keep the original figures in the baseline record; never use pilot validation values as test MSE. |
| PDF page2 Table2/Figure3, setup and solved-count statements; page3 adding analysis | Update only after all new results exist. Report actual new values and conclusions; preserve the historical0/36 outcome. | P1 HAR Table1/Figures1–2 and width Table3/Figure4a stay unchanged. |
| `hidden_gradients.csv`, `hidden_gradient_norms.png`, `report_gradients.png`; PDF page3 Figure5 and ratio prose | Change only if new-gradient evidence is generated from matching new T100 checkpoints. | Otherwise keep old gradient evidence and explicitly label it5-epoch baseline. It has no separate ledger run rows. |
| `forget_bias_*` metrics, `forget_bias_ablation.png`, right panel of `report_sweep-forget.png`; PDF Table4/Figure4b/page3 bias prose | Change only after the separate six-run new-budget study exists; append six corresponding new CSV rows. | The original six bias rows (current file lines65–70) and five-epoch conclusions remain historical evidence. |
| PDF page3 Table5 | No change from a new test grid alone. New pilots must be separately labelled if added. | Existing overfit/validation-only values and empty test fields stay diagnostics. |
| README/notebook budgets, runtime/row accounting; PDF page6 ledger-count sentence | Describe the actual added run count, budget, measured runtime and fresh-versus-cache mode. | Do not update counts/timing for runs not actually executed. |
| P2 notebooks/metrics, Tables6–9, Figures6–9 and generated samples | No scientific change needed for a P1 rerun. | Retain the verified primary LM, its selected checkpoint and samples. |

The current packager/audits intentionally check the present92-row evidence contract.
If the student genuinely adds runs, the ledger-count and expected-record checks in
`scripts/package_submission.py`, `scripts/review_checks.py`,
`scripts/normalize_review_ledger.py` and report/README checks must be updated to
validate the actual revised evidence while retaining baseline-preservation checks.
Do not bypass validation just to package a different row count. No such change is
needed or made for the current submission.

## Manual report review and remaining student actions

1. Read `REPORT_MANUAL_EDITS.md`. No required numerical PDF edit was found; optional
   spacing/layout refinements and conditional new-run changes are itemized there.
   The existing seven-page PDF remains untouched.
2. Resolve the original AI-authorship restriction with an applicable written
   instructor decision or approved remediation. Preserve the complete truthful
   declaration. A user statement or edit to local rules is not instructor permission.
3. Confirm the missing variant/example assumptions and actual portal deadline if
   authoritative course information becomes available. No change is justified by
   unsupported local claims.
4. Provide a genuinely measured T4 total only if you actually perform that measurement;
   otherwise retain the explicit “unmeasured” limitation. No automatic full training
   or optional improvement rerun was performed in this audit.
5. If you manually change the report or run new experiments, repeat the corresponding
   validations and rebuild the ZIP. Otherwise the current structurally verified
   archive needs no scientific modification.
6. Upload yourself, download the uploaded ZIP and check it opens, and keep the portal
   receipt. This agent did not push to GitHub or submit to the university portal.

## Final archive and contents

Exact file: `/home/tushar/Desktop/aiml-dnn-assignment-2/2026aj05073_DNN_Assignment.zip`.
Size: **1,916,033 bytes** (1.916 MB).
SHA-256: `9213e812367aa97e1a5cfe6bd436d93260f987338cb91cccd136e100ac7d92cb`.
Single root: `2026aj05073_DNN_Assignment/`. Members:

| File under required root | Bytes |
|---|---:|
| `README.md` | 3,627 |
| `problem1/figures/report_adding.png` | 98,230 |
| `problem1/figures/report_class-balance.png` | 40,708 |
| `problem1/figures/report_confusion.png` | 48,728 |
| `problem1/figures/report_gradients.png` | 93,363 |
| `problem1/figures/report_sweep-forget.png` | 60,786 |
| `problem1/problem1.ipynb` | 743,713 |
| `problem2/figures/report_attention-heads.png` | 88,061 |
| `problem2/figures/report_context.png` | 88,417 |
| `problem2/figures/report_lm-continued.png` | 86,579 |
| `problem2/figures/report_positions.png` | 25,469 |
| `problem2/generated_samples.txt` | 1,959 |
| `problem2/problem2.ipynb` | 365,326 |
| `report.pdf` | 733,347 |
| `requirements.txt` | 190 |
| `results.csv` | 36,355 |

Both requested audit documents are separate local deliverables, excluded from the
assignment's prescribed archive. Machine evidence and source hashes are in
`.cache/pre-submission-2026-11-11/verification.json`. Structural upload readiness is
PASS; unconditional academic-compliance or fresh-training reproducibility is not claimed.
