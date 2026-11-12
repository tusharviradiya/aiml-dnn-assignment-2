# Final CPU submission validation — 12 November 2026

The student explicitly chose finalization with verified CPU results, deferring GTX 1650 setup until suitable connectivity. This supersedes the earlier GPU migration objective for the current submission. No GPU timing or fresh GPU training is claimed.

Archive: `2026aj05073_DNN_Assignment.zip`. Size: 1,914,696 bytes. Files: 16.
SHA-256: `de4ad26c07d58e5e1a0b77476e1b791d33d7d05b05599c041434c3520d941851`.

## Current brief and disclosure

The student confirmed the current root DOCX (SHA-256 `4d3f7c56e29ae5111ddef3563db44e77538202d697c1f03d8f12305b455dcfa1`) permits AI-written scratch components. No independent instructor authentication is claimed. README, both notebook introductions and the report disclose actual Codex assistance. Earlier policy/readiness warnings based on a different brief are historical and superseded for this student-confirmed scope. All assessed model/training code and original numerical results are preserved.

The current brief excludes references alone from the six-page limit. The revised PDF has six assessed A4/11pt pages including AI-use disclosure, plus one references page; geometric margins, embedded fonts and absence of overflow pass. Pages 1 and 6 were visually inspected after rebuilding; unchanged figures and tables remain present. README renders to one A4 page at 11pt/2cm.

## Verification completed

- `scripts/verify_readonly_audits.py`: all ten audits pass with no protected evidence mutations. Numerical recurrent/attention/block reference and gradient checks, invalid-case controls, cache fingerprints, reproducibility fixtures, datasets/splits, experiment coverage and ledger checks pass. Evidence: `.cache/readonly-audits.json` and its ten logs.
- `scripts/validate_report.py`: report content/page allocation, figures/tables, parameter calculations, numerical evidence, disclosure, font and margin checks pass.
- `scripts/package_submission.py`: exact 16-file allowlist, correct archive/root name, CRC, size limit, extracted hashes and source-byte comparisons pass.
- `scripts/verify_extracted_submission.py`: both isolated packaged notebooks execute completely (141 and 55 code cells), using copied historical raw data/checkpoints/measurements and an Adam guard preventing training. No excluded helper dependency. CSV, samples and all packaged figures reproduce exactly. Evidence: `.cache/extracted-verification.json`.
- Existing pinned CPU environment passes `pip check`. This audit does not claim a fresh dependency installation or fresh full-training run.
- Current ZIP payload matches current source hashes. Both notebooks' code cells are identical to the verified CPU baseline. Only introductory disclosures changed.

An initial read-only wrapper detected a report rebuild that overlapped its snapshot; no numerical audit failed. The wrapper was rerun after freezing submission files and all ten audits then passed with zero mutations.

## Coverage and practical limits

All ten rubric tasks are covered: prescribed data pipelines and adding generator; scratch recurrent reference/count tests; three-seed HAR; complete 36-run adding grid; gradient, width and odd-ID forget-bias studies; attention hand/reference checks; multi-head/encoder/position tests and count reconciliation; HAR position ablation; causal character LM with BPC and three 500-character samples; attention/head/mask/context analyses. Results CSV has the exact 12 required columns and 92 supported rows. No bonus is claimed.

Measured baseline training is 44.7 CPU minutes; continuations add 9.13 CPU training minutes; adding diagnostics take 123 seconds wall time. These scopes exclude other setup/execution overhead. T4/GTX 1650 runtime remains unmeasured; CPU timing is explicitly substituted at the student's direction. Acceptance of that substitution has not been independently confirmed. All 36 original adding runs remain unsolved; LM comparisons are single-seed. Historical optimizer/RNG states are missing; future runs save resume snapshots. The missing variant table/hand fixture are handled as disclosed assumptions.

Datasets, checkpoints, environments, internal scripts, audit documents and partial CUDA downloads are excluded from the ZIP. CUDA downloads are stopped; retained chunks are only for possible future reuse. Full cache-free training and clean downloads are unverified in this final audit.

## Remaining student actions

Confirm name/ID and disclosed variant assumptions, check the authoritative portal deadline, upload the exact ZIP, download/open the uploaded copy and retain the confirmation receipt. The supplied deadline weekday/date conflict and unfinished portal link cannot be resolved locally. No university upload or external message was performed.

The chosen CPU submission is finalized and technically verified, with the timing substitution and reproducibility limits above disclosed. GPU migration is deferred and is not required to reopen this ZIP.
