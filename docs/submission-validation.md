# Final local submission validation — 2026-11-09

**Locally verified technically; course authorization scope unresolved; portal steps external.**

Archive: `2026aj05073_DNN_Assignment.zip` at repository root.
Size: **1,909,232bytes** (1.91MB decimal; below25,000,000).
SHA256: `85e99a502cf4407056ed0c4b86823f7d4d2bba24fd3d96f4c8ef0b692fd2803c`. Correct outer folder: `2026aj05073_DNN_Assignment/`.
Exactly**16 files**; CRC and all file hashes pass. No internal docs, scripts,
metrics, manifests, reviews, permission records, checkpoints, datasets, environments
or Git metadata are included. The complete accurate report-end AI declaration remains.

## Exact ZIP contents (relative to the outer folder)

```text
README.md
problem1/figures/report_adding.png
problem1/figures/report_class-balance.png
problem1/figures/report_confusion.png
problem1/figures/report_gradients.png
problem1/figures/report_sweep-forget.png
problem1/problem1.ipynb
problem2/figures/report_attention-heads.png
problem2/figures/report_context.png
problem2/figures/report_lm-continued.png
problem2/figures/report_positions.png
problem2/generated_samples.txt
problem2/problem2.ipynb
report.pdf
requirements.txt
results.csv
```

Nine report images contain all required figure panels. Other notebook plots remain
saved inside notebooks and regenerate on execution; duplicate PNG files are excluded.

## Checks actually executed

- Original DOCX/rubric/email checked; full task-to-evidence checklist in
  reproducibility-audit.md. Restricted scratch model source unchanged.
- Both root notebooks executed top to bottom with cached-only guards:141 P1 and55
  P2 code cells, sequential counts, saved outputs, no errors. Supplemental report
  experiments and all report figures are part of this workflow.
- Fresh extraction of **this exact archive** ran both notebooks with no copied helper
  files or preexisting metrics directories. A local-only relative data symlink reused
  datasets/checkpoints; Adam guard rejects training. CSV, primary sample file and all
  nine included figures regenerate byte-identically. No Git directory is needed.
- Nine independent audits passed; before/after hashes cover295 evidence
  files. Verification cannot replace the data it checks. Definition-only loaders do
  not execute experiment/setup cells or download missing data.
- `scripts/test_verification.py` — exit0
- `scripts/test_cache_fingerprints.py` — exit0
- `scripts/test_reproducibility.py` — exit0
- `scripts/audit_har.py` — exit0
- `scripts/audit_adding.py` — exit0
- `scripts/audit_task5.py` — exit0
- `scripts/audit_problem2.py` — exit0
- `scripts/review_checks.py` — exit0
- `scripts/normalize_review_ledger.py` — exit0
- Recurrent/attention/block reference errors <1e-5, negative controls, backward
  agreement, train-only normalization, subject splits, adding markers/targets/state
  reset, checkpoint selection, metrics/counts and weighted losses are checked.
- All82 baseline ledger rows remain byte-identical. Exact12-column schema and92
  unique rows pass. Six adding diagnostics have no test metrics; original36 test
  runs remain unsolved. Four continued LM validations and all baseline/new samples
  independently replay from weights. Primary samples are exactly3×500 new chars.
- Future resume test restores optimizer moments and Python/NumPy/Torch/loader RNG,
  reproducing the next stochastic Adam update exactly. A disposable one-update
  diagnostic tests fresh execution/saving/replay; it adds no assessed result.
- Installed package versions exactly match requirements.txt. No clean install or
  download replay was performed. Paths in notebook code are relative.
- PDF: six A4 content pages + one excluded AI/reference page;11pt and2cm margins;
  bounding boxes/no overflow, all fonts embedded, Tables1–9/Figures1–9 captioned and
  explicitly referenced. Rendered pages checked for readability. Full hand arithmetic,
  d64 parameter derivation, primary sample discussion and limitations agree with evidence.
- Git diff checked. Exact generated sample trailing spaces are intentionally retained;
  removing them would alter measured samples. Local commit approval is recorded in development-log.md; no push/upload performed.

## Scope and remaining work

This is **cached replay**, not a fresh full-training reproduction. Earlier actual
training produced82 baseline runs and10 supplemental runs; no models were retrained
for this release. Fresh notebook execution trains missing experiments automatically;
hardware timings/serialization hashes can differ. Full fresh training, fresh network
setup, clean dependency installation and GPU/T4 behavior were not repeated. Historical
optimizer/RNG states do not exist; only future training saves them. Overfit diagnostic
CSV timing averages logged update intervals, not all1200 updates; notebook text states
that scope, and report model-speed comparisons do not use those values.

Student-reported informal AI permission is distinct from the email's size/seed/example
clarifications. No written exemption or personal understanding is certified. Keep the
concise accurate declaration and review the excluded internal understanding checklist.
Resolve any required course authorization clarification, then upload/download/open the
actual portal copy and retain confirmation. No portal verification is claimed.

Machine-readable local records: `.cache/submission-verification.json`,
`.cache/extracted-verification.json`, `.cache/readonly-audits.json` (not submitted).
