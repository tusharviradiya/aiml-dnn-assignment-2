# Manual report review — 11 November 2026

The current `report.pdf` was inspected and **has not been rewritten or regenerated**.
The supplied original assignment DOCX controls this review. Its SHA-256 is
`37311ac57faf68aaf1adc2e69c312fe9325154f3d3de93b2abbd2304e14e950d`.

**No required numerical correction was found.** All nine PDF tables (31 data rows)
match the stored experimental evidence at their displayed precision. Six assessed
A4 pages plus one excluded AI-use/reference page, the 11-point document setting,
minimum 2 cm text margins, embedded fonts, captions and figure/table references pass.
The figures were reproduced by cached execution in a separate ZIP extraction.

These are manual review instructions, not new experimental results. `REQUIRED`
means an unresolved requirement/action; `CONDITIONAL` applies only if new evidence
or experiments exist; `OPTIONAL` is an editorial improvement. Unaffected sections
explicitly say **NO CHANGE NECESSARY**.

## Page-by-page findings

| PDF page and section | Existing evidence checked | Finding |
|---|---|---|
| 1 — P1 data, cell verification and HAR; Table 1, Figures 1–2 | Shapes/channels, subject split, train-only normalization, one/two-bias counts, accuracy/F1/sample std, parameter counts, CPU time, validation-selected confusion | **NO CHANGE NECESSARY.** RNN/LSTM/GRU accuracy remains 70.52/87.71/88.19%; these are actual results. |
| 2 — adding, width and odd-ID bias study; Tables 2–4, Figures 3–4 | Full 36-run five-epoch grid, actual constant-1 baseline by length, every solved count 0/3, width sweep and six paired forget-bias runs | **NO CHANGE NECESSARY** for the current experiments. Do not improve numbers or change budgets in prose without new runs. |
| 3 — gradients and one-page P1 analysis; Table 5, Figure 5 | Before/after T=100 gradients, explicit LSTM cell-path limitation, validation-only T=50 diagnostics and wearable recommendation | **NO CHANGE NECESSARY.** The 25-epoch validation MSE values 0.16463/0.01327/0.00189 are diagnostics, not test-grid replacements. |
| 4 — attention, encoder and HAR; Table 6, Figure 6 | Hand/code example, reference tests, d=128 weights 196608 and total 198272, actual d=64 total 49984, positional comparison and confounds | **NO CHANGE NECESSARY** to calculations or results. Missing instructor fixture remains a stated assumption, not an authenticated substitution. |
| 5 — causal LM and masking; Tables 7–8, Figure 7 | CPU exception, baseline versus continued variants, Adam reset, nats/BPC, contaminated no-mask loss, primary samples and diversity statistics | **NO CHANGE NECESSARY** to results. Primary four-head causal validation is 2.0269467236664482 nats / 2.924265986379717 BPC. |
| 6 — attention interpretation and scaling; Table 9, Figures 8–9 | Two-head observations, timing repeats, allocation traces, 21.56× measured time and 28.07× tensor-peak growth, 92-row accounting | **NO CHANGE NECESSARY.** CPU cost is not a T4 measurement; attention weights do not establish causation. |
| 7 — AI-use statement and references | Codex/CLI named, actual assistance and AI-written scratch components disclosed, authorship discrepancy and lack of verified exemption stated | **NO CHANGE NECESSARY** on current evidence. Disclosure is factual; it does not establish authorization. See required action R1 below. |

## REQUIRED manual actions

### R1 — Page 7, academic-policy review

- Existing text: “No verified instructor exemption is available. Academic compliance
  remains unresolved; disclosure alone does not authorize restricted work.”
- Why action is required: the original brief prohibits AI writing the scratch parts.
  Earlier development records identify AI-written components; passing numerical
  tests and describing them as student-authored do not establish independent authorship.
  No verified instructor authorization has been supplied in this session.
- **Replacement now: none. Preserve the current truthful declaration.** Obtain an
  applicable written instructor decision or approved remediation before claiming
  academic compliance. A wording change alone cannot resolve the restriction.
- This review has not removed references to preliminary implementations or any
  other real Codex assistance, and has not rewritten any restricted implementation.

### R2 — Reference [5] and submission deadline

- Existing text: the supplied date and weekday disagree; confirm the portal deadline.
- Why action is required: the brief contains proposed dates and an unfinished portal
  link. Local review cannot establish the authoritative course deadline.
- **Replacement now: none.** Confirm the actual portal deadline manually. Change
  this sentence only if the portal/instructor provides an authoritative correction.

## OPTIONAL editorial edits

### O1 — Pages 4–5, optimizer notation

- Existing: “Adam10⁻³” on pages 4–5 and “norm1 clipping” on page 5.
- Reason: spacing is dense and the learning-rate meaning is implicit.
- Exact replacements: **“Adam with learning rate 10⁻³”** and
  **“gradient clipping at norm 1.0.”**
- Recheck pagination/margins if you make these changes. Do not reduce the font or
  margins to fit. No numerical or training-configuration change is intended.

### O2 — Page 5, original versus continued LM setup

- Existing: “All comparisons use five full epochs, batch 64, seed 0, Adam10⁻³,
  dropout 0.1 and norm1 clipping.” Later text correctly explains continuation.
- Reason: the opening sentence can more clearly distinguish the two phases.
- Exact replacement:

  > The original head/mask comparisons use a five-epoch budget, batch 64, seed 0,
  > Adam with learning rate 10⁻³, dropout 0.1 and gradient clipping at norm 1.0.
  > Each continuation starts from its own validation-selected baseline checkpoint
  > and receives five additional epochs with Adam reset.

- Keep the existing explanation that restart and duration effects are not isolated,
  and that one seed cannot establish a ranking. This clarification is optional;
  the current later paragraphs already disclose these facts.

### O3 — Pages 2, 5–6, figure-panel readability

- Existing: compact multipanel Figures 3–4, 7 and 9.
- Reason: some legends/axis labels are small at printed A4 size.
- Replacement wording: none. If desired, rebalance the layout or enlarge labels
  using the same measured data. Keep all panels, captions, references and the
  six-content-page limit. No figure rewrite is required for correctness.

## CONDITIONAL edits after genuine new evidence

### C1 — Pages 2–3: if the student completes a new fair adding grid

Do not apply these edits based on the existing T=50 diagnostics. The executable
procedure and exact affected artifacts are in `SUBMISSION_AUDIT.md`.

- Page 2 setup: distinguish the original **five-epoch** grid from the new locked
  budget. For a completed 25-epoch grid, a truthful setup sentence is:

  > The original 36-run five-epoch grid is retained. A separate 25-epoch grid uses
  > the same data, three model seeds, architecture, optimizer and batch size;
  > its budget was fixed from validation evidence before inspecting its test results.

  Use this only if the actual run log supports every clause. Do not describe the
  prescribed test set as a new untouched holdout: it was evaluated previously.
- Table 2 and Figure 3: add/replace the displayed primary comparison with the actual
  three-seed mean/sample std, solved counts, MSE-versus-length and T=200 histories.
  Clearly label which budget each row/curve uses. There is no justified replacement
  numeric text until all new runs exist.
- Page 3 adding interpretation: revise conclusions from the new evidence while
  preserving the fact that the original five-epoch grid solved 0/36.
- Table 5: **keep the existing validation-only diagnostic values and labels.**
  Do not relabel those numbers as new grid test results.
- Figure 5 and gradient-ratio prose: recompute from the matching new T=100 selected
  checkpoints if discussing the new grid's gradients. Otherwise retain the old
  figure and label it explicitly as the original five-epoch gradient study.
- Table 4, Figure 4b and page 3 forget-bias prose change **only if** the paired
  six-run bias 0/1 study is also rerun under the new budget. Otherwise retain the
  original five-epoch labels and results; claim no new bias benefit.

### C2 — Page 6: if new experiment rows are appended

- Existing: “The 92 rows retain 82 baseline runs, 6 adding diagnostics and 4 LM continuations.”
- Reason: this count must describe the actual final CSV.
- Exact replacement for **only** 36 newly completed grid runs:

  > The 128 rows retain the original 82 baseline runs, 6 validation-only adding
  > diagnostics and 4 LM continuations, and add 36 separate adding-grid runs.

- If six new bias runs also exist, the total is **134**. Additional completed
  validation-only pilots add their actual row count to these totals. Do not insert
  planned runs into the ledger or report as completed runs.
- Update notebook/README run accounting and verification expectations consistently;
  preserve all original records and their identifiers.

### C3 — Page 7: if applicable instructor authorization is later verified

- Replace only the current permission/status sentences to match the exact scope
  of the evidence. Keep the real AI-use history and authorship qualification.
- Conditional template:

  > An instructor-issued authorization dated [date] permits [exact scope]. The AI
  > contributions described above remain disclosed.

- No professor name needs to be published to preserve the underlying written
  evidence. Do not claim blanket permission or independent authorship from a
  narrower authorization. Until such evidence exists, **no change is necessary**.

## Manual editing workflow

The declaration and report body are generated by `scripts/build_report.py` into
`docs/report.tex` and `report.pdf`. If you decide to make an edit, change the source
consistently and explicitly regenerate the PDF yourself. Then rerun report validation
and rebuild the ZIP. This audit did **not** run the report generator. If new records
or disclosure wording are introduced, update the relevant validator expectations
while keeping numerical, layout, provenance and baseline-preservation checks intact.

With no new experiments or instructor evidence, the existing report can remain
byte-for-byte unchanged. Structural readiness and academic-policy acceptance are
separate decisions.
