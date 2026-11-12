# Final GTX 1650 submission validation — 12 November 2026

The GPU migration is complete. The verified CPU submission is preserved at `.cache/verified-cpu-final/2026aj05073_DNN_Assignment.zip` (SHA-256 `de4ad26c07d58e5e1a0b77476e1b791d33d7d05b05599c041434c3520d941851`), with CPU experiment caches also preserved. The root ZIP now contains the verified GPU submission.

Archive: `2026aj05073_DNN_Assignment.zip`; 1,876,278 bytes; 16 required files.
SHA-256: `fec6f47cfae3383ec484ad5386b833d8f87c4cc7eabee36a2b210ee432797641`.

## Environment and measured execution

NVIDIA GeForce GTX 1650, 4 GB; driver595.99.02; Python3.14.4; PyTorch2.11.0+cu128; CUDA12.8; four CPU threads. All CUDA wheels completed downloading; offline installation, `pip check`, and CUDA RNN/LSTM/GRU forward/backward smoke checks passed. Evidence: `.cache/gpu-install.log`, `.cache/gpu-smoke.log`, `gpu-environment.txt` and `requirements.txt`.

A clean successful execution trained all required experiments from fresh experiment caches: Problem1 274.883 seconds; Problem2 325.105 seconds; total 10.000 minutes. This includes numerical checks, training, evaluation, plotting and CPU diagnostics; it excludes package installation and already-staged raw dataset downloads. The complete record and notebook source hashes are in `gpu-runtime.json`. T4 runtime is unmeasured; actual GTX1650 timing is the disclosed user-authorized substitute. No independent instructor acceptance of that timing substitution is claimed.

The standard GPU LM now uses d128/four layers, context128, four heads. HAR encoder remains d64/two layers; recurrent h64; seeds0/1/2. No hyperparameter search or budget change was made in response to test scores.

## Corrections and provenance

The first GPU attempt completed main P1 training but stopped at an inappropriate 1e-12 equality assertion comparing a CPU diagnostic trajectory with CUDA training. The corrected notebook checks exact trajectory agreement only for the same backend, and retains protocol checks across CPU/CUDA. The full failed attempt is preserved in `.cache/gtx1650-attempt1/`. The reported final runtime comes from a subsequent clean successful run, with no experiment caches reused from that attempt.

The CUDA context benchmark now saves its raw timing and peak-memory evidence. Its device-matched allocation peak excludes the model/input baseline and is not reserved memory. The confusion figure selects architecture/seed using current validation F1 instead of historical hardcoded values. Report numerical tables, analyses, sample descriptions and CPU/GPU runtime labels reflect the verified fresh results. Report builder and validator now target the current GPU artifacts. Old CPU analyses are explicitly historical; an internal ledger helper was reconstructed from validated current P1 rows, not claimed as a pre-training provenance record.

## Verification completed

- Both full fresh notebooks passed:141/55 executed code cells, no saved error outputs; strict scratch forward/backward/reference/count/mask gates passed in the GPU environment.
- Independent CUDA replay reproduced all9 recurrent HAR checkpoints and36 adding checkpoints, train-only normalization, predictions, metrics, epoch selection, parameters and timing (`audit-recurrent.log`).
- Independent Task5 audit passed all24 width-sweep checkpoint/prediction records, six paired forget-bias runs, statistics and all18 gradient probes (`audit-task5.log`).
- Independent Transformer audit passed all9 HAR checkpoints, four baseline LM validation losses/BPC/history, contiguous text targets, matched ablation initialization/budgets, all2000 baseline/no-mask sample characters, attention maps and trained future-token perturbations (`audit-transformer.log`). Current P1 ledger rows bind to actual checkpoint metadata rather than stale copied CPU snapshots.
- `validate_gpu_submission.py` passed all92 CSV rows, required coverage, sample lengths/temperatures, aggregate means/sample std, BPC calculations, runtime/configuration, context evidence, seven-page A4/11pt/2cm report geometry, disclosure and numbered/referred figures/tables.
- Report contains six assessed pages including AI-use disclosure, plus references only on page7. All six content pages were visually inspected. README renders to one A4 page at11pt/2cm.
- ZIP CRC, exact16-file allowlist, root/name/size, source and extraction hashes pass. It excludes data, checkpoints, environments, scripts, internal metrics/audits and CUDA downloads.
- Both packaged notebooks passed from an isolated ZIP extraction, using independently copied raw data/checkpoints/measurements, no internal helpers and an Adam guard preventing training. The92-row CSV, three primary500-character samples and every packaged figure reproduce exactly. Evidence: `.cache/extracted-verification.json`; final archive hash matches this ZIP. The final report-only correction was checked separately: all notebook cell sources match the successful isolated replay, all other delivered files are byte-identical, and PDF identity, disclosure, GPU/runtime text and geometry pass.

## Verified results and remaining limits

GRU mean HAR accuracy:88.0783 percent (sample std0.6369 percentage points). All36 adding grid runs remain unsolved at the fixed five-epoch budget and are reported honestly. Continued four-head causal LM validation:1.744418 nats,2.5167 BPC. No-mask losses are contaminated, and its baseline generation is entirely newlines. LM ablations use one seed. Longer T50 CPU diagnostics are validation-only and do not substitute for the required test grid. No bonus is claimed. Future resume snapshots were saved during fresh runs; the common LM continuation protocol deliberately resets Adam.

The student confirmed the root DOCX (SHA-256 `4d3f7c56e29ae5111ddef3563db44e77538202d697c1f03d8f12305b455dcfa1`) as the current brief permitting AI-written scratch components. Actual AI assistance is disclosed; no independent authorship or instructor authentication is asserted. The missing variant table/hand fixture are handled as disclosed assumptions.

The assignment is technically ready as the user-authorized local GPU submission. The student confirmed the identity Viradiya Tushar Rajeshbhai, 2026aj05073, the use of local GTX1650 timing, and permission for AI-written scratch components. The final report explicitly includes the local GPU and AI-use disclosure. Remaining personal external steps: check the portal deadline, upload the exact ZIP, download/open the uploaded copy, and retain the receipt. Disclosed variant/fixture assumptions remain documented. The date/weekday conflict and incomplete portal link require the course portal. No portal upload or external message was performed.
