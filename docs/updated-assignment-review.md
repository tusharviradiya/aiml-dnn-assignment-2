> Superseded policy assessment: the latest DOCX removes the AI-use restriction and declaration requirement. See final-verification.md for current status. Earlier provenance disclosures remain historical evidence.

# Updated assignment review — 10 November 2026

Reviewed the supplied local DOCX against the previous copy and the current submission.
Current DOCX SHA-256: `ca533fa4237248115aa6f686f0ae5d81c1cd7ebafb81995ab7eeef27acacd02d`.
The assignment brief remains local, ignored by Git, and excluded from the ZIP.

## What changed in the document

Two deletions: the ground-rules sentence allowing library reference tests, and the
standalone “From-scratch parts” paragraph. No task, rubric item, artifact, format,
page limit or size limit was added or changed. The FAQ still explicitly allows
library implementations to check the student's code, and the AI-tools section
still forbids AI writing the scratch parts. The deleted paragraph therefore does
not authorize an AI rewrite or removal of earlier assistance disclosures.

## Required work

| Requirement | Verified submission evidence |
|---|---|
| P1 data pipelines | Prescribed HAR channels/shapes; subject-disjoint splits, training-only normalization; adding markers/targets/dtypes and reproducibility assertions |
| P1 scratch cells | RNN/LSTM/GRU present; library forward/state and gradient equivalence, registered parameter checks and both bias-count conventions |
| P1 HAR comparison | Three models × three seeds, matched budgets; mean/sample std, accuracy/F1, parameters, training timings and validation-selected confusion matrix |
| P1 adding grid | Three models × four lengths × three seeds; baseline, test MSE/sample std, solved counts and T=200 curves; all original runs remain unsolved |
| P1 gradient/sweep/ablation | Before/after T=100 gradients, LSTM/GRU sizes 16/32/64/128, three seeds and odd-ID forget-bias 0/1 study; trade-off analysis included |
| P2 attention | Mask and row-sum assertions, functional reference, uniform/nonuniform hand calculations, gradients and invalid-mask tests |
| P2 multi-head/encoder | Custom projected heads, pre-LN/residual/dropout/4d FFN, sinusoidal positions, shape/reference/causality tests; weights/bias/norm counts reconciled |
| P2 HAR | P1 splits reused; CLS and 8-step patches, no/sinusoidal/learned positions, three seeds; recurrent comparison and architectural differences disclosed |
| P2 character LM | 65-character vocabulary, contiguous 90/10 split, official d64/two-layer CPU exception; validation nats/BPC, three labelled 500-character samples |
| P2 ablations | Two causal heatmaps, 1/4/8 heads, no-mask loss/generation diagnostic, context 64/128/256/512 time/memory and quadratic attention explanation |
| Notebook execution | Both notebooks execute in a clean installed environment with saved outputs; final extraction requires no excluded helper scripts |
| Artifacts | Prescribed CSV schema, README, pinned requirements, PDF, figures and samples; six assessed PDF pages plus one excluded declaration/reference page; ZIP below 25 MB |

The only remaining implementation gap found was in verification: P1 defined but did
not invoke `require_task2_complete()` during Run All. Its existing test function is
now called unconditionally, so an unfinished component cannot produce a successful
Run All. No scratch implementation, training definition, result or sample was rewritten.
All other “pending” code is deliberate negative-control test infrastructure.

## Reproducibility work completed

Installed requirements.txt into a newly created venv using downloaded packages;
`pip check` passed. Both notebooks were then executed there with local experiment
caches and an Adam-construction guard that rejects accidental retraining. The clean
venv also passed the disposable uncached training/resume/validation-replay fixture.
The 92-row experiment CSV and generated samples remain byte-identical. Independent
checkpoint, gradient, cache-fingerprint, scalar attention, memory-trace, sample and
ledger audits pass. Final archive extraction repeats notebook execution and verifies
CSV, samples and included figures exactly.

## Remaining external or evidentiary limits

- No CUDA device is available; total T4 runtime cannot be measured here and remains
  explicitly unmeasured. CPU timings are not represented as T4 timings.
- Full assessed retraining was not repeated. Historical optimizer/RNG states remain
  absent; LM continuations reset Adam. Single-seed LM evidence remains single-seed.
- The student reports manual final implementations, but scratch code matches the
  preserved baseline previously recorded as AI-written. This review cannot establish
  authorship or institutional acceptance; earlier AI assistance remains disclosed.
- The referenced variant table and instructor hand fixture are still absent. The
  chosen values/example remain explicit assumptions under the DOCX ambiguity clause.
- The optional bonus is unattempted. Portal upload, download/open verification,
  deadline confirmation and receipt retention remain external steps.
