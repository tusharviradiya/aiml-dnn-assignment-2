# Final local submission validation — 2026-11-09

**Locally verified technically; academic-integrity authorization blocked/unverified; portal steps external.**

Archive: `2026aj05073_DNN_Assignment.zip` at repository root.
Size: **1,914,738 bytes** (1.91 MB decimal; below25,000,000).
SHA256: `c50a489ed9be17891714610d51984dbb4b5668f70b38ae6f5b91063463311875`. Correct outer folder: `2026aj05073_DNN_Assignment/`.
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
  reproducibility-audit.md. Graded model equations unchanged; only three recurrent
  class docstrings were consolidated, verified against the original executable AST.
- Both root notebooks executed top to bottom with cached-only guards:141 P1 and55
  P2 code cells, sequential counts, saved outputs, no errors. Supplemental report
  experiments and all report figures are part of this workflow.
- Fresh extraction of **this exact archive** ran both notebooks with no copied helper
  files or preexisting metrics directories. A local-only relative data symlink reused
  datasets/checkpoints; Adam guard rejects training. CSV, primary sample file and all
  nine included figures regenerate byte-identically. No Git directory is needed.
- Ten independent audits passed; before/after hashes cover296 evidence
  files. Verification cannot replace the data it checks. Definition-only loaders do
  not execute experiment/setup cells or download missing data.
- `scripts/test_verification.py` — exit0
- `scripts/test_cache_fingerprints.py` — exit0
- `scripts/test_supplement_cache.py` — exit0; all ten historical supplements match
  reviewed compatibility bindings;23 negative controls reject protocol/config/source/
  data/baseline changes, unknown legacy records, partial caches and corruption.
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
- Git diff checked. Exact generated sample bytes are unchanged. Prior commit39112c6
  remains intact; the user authorized a local commit of this focused revision.
  No push/upload performed.

Disclosure/presentation: no informal-permission narrative remains in submitted report,
notebook sources or saved text outputs. The complete report-end Codex/Codex CLI
declaration explicitly includes AI-written scratch cells/Transformer components,
experiment code/execution, tests/debugging, plots, analysis/report drafting and audits/
packaging. The generator and generated LaTeX agree. Fixed compressed words and spacing;
rendered revised pages3/4/7 inspected, with original figure dimensions retained.

Cache compatibility uses resolved full protocol, scoped executable-source and data
fingerprints and runtime settings. LM contracts include the originating baseline's
key, selected epoch/loss, source identity and checkpoint SHA256. Historical metadata
is left byte-identical; reconstructed legacy bindings and their provenance limits
are in review-evidence/supplement-cache-bindings.json. Historical baseline hashes were
not recorded at training; current observed hashes and independently matching initial
validation losses are retrospective evidence, not proof of historical file identity.
Future runs persist complete contracts at creation. Mismatches stop before reuse or
overwrite and require a distinct experiment name.

## Scope and remaining work

This is **cached replay**, not a fresh full-training reproduction. Earlier actual
training produced82 baseline runs and10 supplemental runs; no models were retrained
for this release. Fresh notebook execution trains missing experiments automatically;
hardware timings/serialization hashes can differ. Full fresh training, fresh network
setup, clean dependency installation and GPU/T4 behavior were not repeated. Historical
optimizer/RNG states do not exist; only future training saves them. Overfit diagnostic
CSV timing averages logged update intervals, not all1200 updates; notebook text states
that scope, and report model-speed comparisons do not use those values.
The extraction verifier confirmed reuse of the same raw context timing repeats before
comparing timing-derived figures exactly. No fresh benchmark observations were made;
fresh timings would require statistical comparison of repeats rather than PNG equality.

Student-reported informal AI permission is distinct from the email's size/seed/example
clarifications. No written exemption or personal understanding is certified. Keep the
concise accurate declaration and review the excluded internal understanding checklist.
Resolve any required course authorization clarification, then upload/download/open the
actual portal copy and retain confirmation. No portal verification is claimed.

Machine-readable local records: `.cache/submission-verification.json`,
`.cache/extracted-verification.json`, `.cache/readonly-audits.json` (not submitted).

## Files affected by the focused final revision

```text
docs/assignment-progress.md
docs/decisions.md
docs/development-log.md
docs/problem1-analysis.md
docs/report.tex
docs/reproducibility-audit.md
docs/review-evidence/supplement-cache-bindings.json
docs/submission-readiness.md
docs/submission-validation.md
problem1/problem1.ipynb
problem2/problem2.ipynb
report.pdf
scripts/build_report.py
scripts/review_checks.py
scripts/test_reproducibility.py
scripts/test_supplement_cache.py
scripts/validate_report.py
scripts/verify_extracted_submission.py
scripts/verify_readonly_audits.py
```

The ignored final ZIP was rebuilt. Original assignment DOCX, datasets, assessed
checkpoints, results.csv, required primary samples and existing figure bytes were
preserved. Original versions remain in Git39112c6 and the ignored local snapshot.
