# Final submission validation — 10 November 2026

Verified at 2026-11-10T16:36:15.841011+00:00. This record supersedes prior readiness/policy estimates.

**Technical status:** packaging and both complete notebook workflows PASS with
historical caches. Full clean-download/full-training reproducibility is NOT verified.
**Academic status:** BLOCKED / not compliant with the original scratch-authorship
rule. The student confirmed no verified instructor authorization is available.
**Conditional technical estimate:** 95/100 (plausible range 92–98); actual institutional
integrity-policy outcome cannot be predicted. [Full rubric review](professor-evaluation.md).

## Assignment source and authorization

Read the supplied original `DNN Programming Assignment – RNN, LSTM, GRU and Transformer.docx`
in full before editing. SHA-256:
`37311ac57faf68aaf1adc2e69c312fe9325154f3d3de93b2abbd2304e14e950d`.
Extracted instructions are retained locally in `.cache/final-audit/assignment.txt`.
The original requires student-authored scratch parts, prohibits AI writing them,
and requires a report-end AI-use statement naming the tool and scope. That statement
and references do not count toward the six-content-page limit.

No newer instructor-approved amendment was verified. Public searches of the exact
assignment/instructor found no official amendment; no connected document sessions
were available. The private course portal/mailbox was not accessible. Local edited
briefs (`ca533fa4...` / `4d3f7c56...`) and local permission summaries are not authority.
The student explicitly answered “No verified instructor authorization is available.”
The earlier claim that the AI prohibition/declaration was removed is withdrawn.

Development records identify AI-written MyRNNCell, MyLSTMCell, MyGRUCell,
scaled_dot_product_attention, MyMultiHeadAttention and MyEncoderBlock. Those six
restricted definitions remain unchanged (AST hashes verified before/after). The prior
manual-completion statement is recorded as unverified, not certified. Correctness is
separate from authorship. Disclosure alone cannot resolve prohibited AI use.

## Corrections completed

- Restored truthful OpenAI Codex/Codex CLI tool-and-scope disclosures in README, both
  notebook introductions and the report-end AI-use statement. Removed unsupported
  claims of instructor permission or amended rules; synchronized progress records.
- Corrected an unsupported instructor-clarification comment to an explicit assumption.
  This changed a source fingerprint; the cache test caught the mismatch. Two exact
  aliases were added only after proving the setup AST identical and validating the
  original source/config/data bindings. Negative controls still reject training,
  configuration and data changes. Evidence: `.cache/final-audit/comment-alias-evidence.json`.
- Restored the required d=128/d_ff=512 block calculation: 196608 matrix weights plus
  1664 bias/norm parameters = 198272. Actual module sums also verify d=64: 49152+832=49984.
- Reflowed the report without reducing the body font, margins or required content.
  The initial extra calculation crossed the bottom margin; compacted redundant prose
  and reran the unchanged geometric margin check successfully.
- Saved successful notebook outputs and rebuilt the exact prescribed ZIP. Extraction
  verification now copies raw datasets/checkpoints/measurements into an isolated
  extraction, without symlinks or excluded repository helpers.

All model/training operations and the original result/sample bytes are preserved.
Only the permission comment and reviewed cache-alias metadata changed in code cells.
No assessed model was retrained; the reproducibility test uses disposable tiny fixtures.

## Executed tests and evidence

Environment: Python 3.14.4, PyTorch 2.15.0+cpu, four CPU threads, no CUDA device.
All eight direct package pins match requirements.txt; `pip check` passed. This audit
reused the pinned environment installed in the preceding review; it did not perform
another fresh installation. Metadata/counts: `.cache/final-audit/environment-counts.json`.

| Command | Final result | Actual log |
|---|---|---|
| `scripts/test_verification.py` | PASS (exit 0) | `.cache/final-audit/test_verification.log` |
| `scripts/test_cache_fingerprints.py` | PASS (exit 0) | `.cache/final-audit/test_cache_fingerprints.log` |
| `scripts/test_supplement_cache.py` | PASS (exit 0) | `.cache/final-audit/test_supplement_cache.log` |
| `scripts/test_reproducibility.py` | PASS (exit 0) | `.cache/final-audit/test_reproducibility.log` |
| `scripts/audit_har.py` | PASS (exit 0) | `.cache/final-audit/audit_har.log` |
| `scripts/audit_adding.py` | PASS (exit 0) | `.cache/final-audit/audit_adding.log` |
| `scripts/audit_task5.py` | PASS (exit 0) | `.cache/final-audit/audit_task5.log` |
| `scripts/audit_problem2.py` | PASS (exit 0) | `.cache/final-audit/audit_problem2.log` |
| `scripts/review_checks.py` | PASS (exit 0) | `.cache/final-audit/review_checks.log` |
| `scripts/normalize_review_ledger.py` | PASS (exit 0) | `.cache/final-audit/normalize_review_ledger.log` |
| `scripts/execute_problem1.py` | PASS, 141 code cells; outputs saved | `.cache/final-audit/problem1.log` |
| `scripts/execute_problem2.py` | PASS, 55 code cells; outputs saved | `.cache/final-audit/problem2.log` |
| `scripts/validate_report.py` | PASS | `.cache/final-audit/report-validation.log` |
| `scripts/package_submission.py` | PASS CRC, paths, allowlist, manifest and size | `.cache/submission-verification.json` |
| `scripts/verify_extracted_submission.py` | PASS 141/55 code cells, no excluded helper dependency | `.cache/final-audit/extraction.log` |
| README Pandoc A4/11pt/2cm render + pdfinfo | PASS: one page | `.cache/final-audit/README.pdf` |

The post-correction read-only suite hashed 296 evidence files
before/after; none was created, removed or rewritten. Source/preserved-byte checks
also passed after execution. The initial Jupyter attempt was interrupted because the
sandbox denies local TCP sockets; approved local kernel execution passed. No final
component, experiment, report or package check remains failed.

**Execution scope:** both full repository notebooks and both notebooks in the fresh
ZIP extraction ran top to bottom with `DNN_VERIFY_CACHED_ONLY=1` and Adam construction
blocked. Extraction staged independent copies of existing HAR/Shakespeare data,
experiment checkpoints and original timing measurements; none is in the ZIP. No
scripts, docs or preexisting metric folders were copied into the extracted submission.
CSV, generated samples and all nine packaged figures reproduced byte-for-byte; the
report matched the source. This is cached replay, not a cache-free training run.
The archive retains the successfully executed repository notebooks; the extracted
execution retains its own verification outputs locally.

## All 92 result records and required evidence

- 82 baseline rows: P1 HAR 9, adding 36, additional HAR sweep 18 (six h=64 runs reused),
  forget-bias study 6; P2 HAR 9 and LM head/mask variants 4.
- 10 additional rows: six validation-only adding diagnostics (test fields empty),
  four five-extra-epoch LM continuations. These are labelled separately in the CSV.
- Exact 12-column CSV schema, unique run keys, relevant/empty fields, selected
  checkpoints, counts, histories, predictions, mean/sample std and nats/ln(2) BPC pass.
- Original baseline and supplemental ledger bytes agree with their preserved sources.
  Final results.csv SHA-256: `d6e51bc79775d45e2173884d9a0fcc65d9e06915b8c756c58731d28df10f1774`.
- Nine HAR baseline checkpoints, 36 adding checkpoints, all 24 sweep results, six
  forget-bias checkpoints and 18 hidden-gradient probes reconcile independently.
- All four baseline and four continued LM validations replay; parameter counts,
  masks, causality, character split/targets, scalar attention oracle and patch probes pass.
- Three labelled primary samples reproduce exactly: 500 new characters each,
  temperatures 0.2/0.8/1.5, top-k 20, seed 700, prompt `ROMEO:\n`. Their continued
  four-head causal checkpoint identity is recorded in the sample file/notebook.
  Baseline and unmasked diagnostics also reproduce. Primary LM: 2.0269467236664482
  validation nats / 2.924265986379717 BPC; no-mask loss is marked contaminated.
- All required figure panels are present in the PDF and notebook outputs: class
  balance, confusion, adding MSE/curves, gradients, widths/bias, LM curves, heads/mask,
  two attention heatmaps and time/memory against context. Five timing repeats and
  three allocation traces per context reconcile with the measured table.

## Report and README

Seven PDF pages: six content pages plus the excluded AI-use/reference page. Source
is A4/11pt/2cm; PDF page dimensions and actual text bounds satisfy the minimum
margins, no overfull boxes, all fonts embedded. All nine numbered tables and nine
numbered figures have captions and text references. Rendered pages 1–7 were visually
inspected; the one-page P1 analysis, hand example, parameter calculations, disclosures
and references remain present. README renders to one A4 page. Rendered previews are
local verification artifacts and are excluded from the archive.

## Remaining issues

1. **Academic compliance BLOCKED:** AI-written restricted implementations match the
   preserved baseline and have no verified instructor exemption. Broader AI assistance
   also exceeds the brief's narrow allowed-use list. An applicable written instructor
   decision or instructor-approved remediation is essential before claiming compliance.
2. **No fresh complete training verification:** only checkpoint replay and disposable
   uncached/resume fixtures were run. Historical optimizer/RNG states are unavailable;
   continued LM variants reset Adam. Fresh hardware timings need not match these CPU
   records. Clean network downloads were not retested.
3. **T4 total runtime unmeasured:** no GPU exists here; README explicitly leaves this
   requirement unmet. CPU minutes are not represented as T4 measurements.
4. Missing variant table and instructor numerical example remain explicit assumptions
   under the brief's missing-information clause; no authenticated amendment is claimed.
5. All original adding runs remain unsolved (0/36); longer T=50 gated validation pilots
   are diagnostics, not replacements for the test grid. LM evidence is single-seed,
   generated text remains weak, architectural comparison confounds are disclosed,
   and no optional bonus is claimed.
6. Portal date/weekday wording is inconsistent. Deadline confirmation, upload,
   downloaded-copy opening and receipt retention remain external steps. No GitHub
   push, instructor message or university submission was performed.

## Final archive

Exact filename: `2026aj05073_DNN_Assignment.zip`.
Exact absolute location: `/home/tushar/Desktop/aiml-dnn-assignment-2/2026aj05073_DNN_Assignment.zip`.
Size: **1,916,033 bytes** (1.916 MB), below 25,000,000 bytes.
Files: **16**, under the single required `2026aj05073_DNN_Assignment/` root.
SHA-256: `9213e812367aa97e1a5cfe6bd436d93260f987338cb91cccd136e100ac7d92cb`.
CRC, safe relative paths, all source/extracted/member SHA-256 values and file
consistency passed. Only the following prescribed files are included:

- `README.md`
- `problem1/figures/report_adding.png`
- `problem1/figures/report_class-balance.png`
- `problem1/figures/report_confusion.png`
- `problem1/figures/report_gradients.png`
- `problem1/figures/report_sweep-forget.png`
- `problem1/problem1.ipynb`
- `problem2/figures/report_attention-heads.png`
- `problem2/figures/report_context.png`
- `problem2/figures/report_lm-continued.png`
- `problem2/figures/report_positions.png`
- `problem2/generated_samples.txt`
- `problem2/problem2.ipynb`
- `report.pdf`
- `requirements.txt`
- `results.csv`

Datasets, checkpoints, environments, internal docs/scripts/metrics, the source DOCX,
Git files and verification records are excluded. Machine verification (local):
`.cache/final-audit/final-verification.json`. Packaging and cached execution are ready;
unconditional submission readiness is blocked by academic compliance and the stated
unverified requirements.
