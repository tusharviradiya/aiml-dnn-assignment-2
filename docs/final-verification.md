# Final verification — 10 November 2026

The final ZIP is technically verified as detailed below. Unconditional submission
readiness is not certified: authorship provenance remains unresolved and total T4
runtime is unmeasured. No portal upload was performed.

## Corrections and preservation

Updated README, both notebook introductions/assumptions, report generator and PDF
page 7. The declaration records the student's report of final manual implementation,
earlier AI-written scratch drafts and actual broader development assistance. Removed
claims that final implementation is pending and unsupported instructor authorization.
Settings and the self-created hand example are explicit assumptions under the supplied
DOCX's missing-information clause. Current status documents supersede earlier reviews;
historical technical records are marked as historical. No required AI disclosure was removed.

Every notebook code cell is byte-identical to its pre-review source (141 P1; 55 P2).
The 92-row results.csv is byte-identical to the pre-review file. Saved outputs were
regenerated through full cached-only execution with Adam construction blocked.
Historical timings and failed adding runs were preserved, not replaced by invented results.
The visible submission folder is synchronized with the ZIP.

## Authorship evidence and limits

The student states that the final six components were implemented manually. They are
present and technically complete: MyRNNCell, MyLSTMCell, MyGRUCell,
scaled_dot_product_attention, MyMultiHeadAttention and MyEncoderBlock.
All notebook code cells also match Git HEAD
`7996b4446fefa0cccbbcd240900a23af9cca7f63` exactly. The existing older-baseline model
comparison passes (recurrent AST comparison ignores docstrings; other recorded
components use source hashes). Thus this workspace does not independently evidence
a replacement of the earlier implementations previously recorded as AI-written.
Passing tests cannot resolve that discrepancy. The report attributes the manual-work
statement to the student rather than claiming an independent authorship finding.
Earlier AI drafts and broader AI-generated pipeline/report assistance remain relevant
under the assignment's restrictive AI-use rules. No policy exemption is asserted.

## Checks

- Both notebooks executed top to bottom with saved, sequential execution counts and
  no error outputs: 141 and 55 code cells respectively. The deliberate `_probe`
  pending output is a negative-control test, not an unfinished required component.
- All three recurrent cells pass constructor, full-sequence reference, state,
  parameter-count and input/state/parameter-gradient checks.
- Attention passes row sums, causal future zeros, functional-reference comparison,
  uniform/nonuniform hand calculations and invalid-mask checks. Multi-head, pre-LN
  encoder, sinusoidal positions, gradients and whole-block causality checks pass.
- Ten audit commands: test_verification.py, test_cache_fingerprints.py,
  test_supplement_cache.py, test_reproducibility.py, audit_har.py, audit_adding.py,
  audit_task5.py, audit_problem2.py, review_checks.py and normalize_review_ledger.py.
  The final read-only run hashes evidence before/after and requires no changes.
- report.pdf: six assessed pages plus one excluded AI/reference page; A4, 11 pt,
  2 cm margins, embedded fonts, numbered/cited figures and tables, no overflow.
  Page 7 was also rendered and visually inspected.
- ZIP: prescribed filename/root, 16 files, required notebooks/README/requirements/
  PDF/CSV/samples and figure folders, valid CRC and all file hashes; no datasets,
  checkpoints or virtual environment. README is 423 words.
- Fresh ZIP extraction executes both self-contained notebooks without internal
  scripts/docs, explicitly reusing local data/checkpoints. Results, samples and
  included figures must reproduce exactly, including replayed timing records.

Notebook kernels require local sockets, blocked in the sandbox. The blocked attempts
were stopped; successful runs used approved elevated execution. An initial read-only
snapshot overlapped documentation edits and correctly detected changes; the final
snapshot run occurs after edits and notebook execution.

## Remaining limitations

Cached replay verifies portability and evidence consistency, not a fresh download,
clean dependency install or full retraining. Historical optimizer/RNG state is absent;
LM continuations reset Adam. T4 runtime has not been measured, so that explicit README
requirement remains unmet. The 36 original adding runs remain unsolved; LM ablations
are single-seed. The missing variant table/instructor fixture are addressed by stated
assumptions, not authenticated clarification. Portal upload, downloading/opening the
uploaded ZIP, deadline confirmation and receipt retention remain external steps.

Machine-readable evidence and detailed logs: `.cache/final-review/`,
`.cache/readonly-audits.json`, `.cache/submission-verification.json` and
`.cache/extracted-verification.json` (local review files, excluded from the ZIP).

Final archive: `2026aj05073_DNN_Assignment.zip` — 1915589 bytes (1.916 MB), 16 files.

SHA-256: `d425895cf34b304c1b15b23b9032e3666fff08b97c894525029d0df06290ce42`.
