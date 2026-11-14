# Student understanding and final personal review

Current status, 13 November 2026: the student clarified that AI-written scratch
components are permitted. Codex implementation/execution/report assistance and
Claude review are disclosed. Technical verification does not independently prove
student authorship or understanding; no such proof is claimed. This current note
supersedes the historical CPU-era policy/reimplementation checklist, preserved in
`.cache/presentation-revision-2026-11-13/docs/understanding-checklist.md`.

There is no pending required scratch reimplementation or manual PDF correction.
The brief says there is no viva. These questions are useful personal review,
not an additional course requirement or a claim that the student answered them.

- Trace all recurrence/state shapes; explain the GRU reset placement and why
  PyTorch has two biases while the hand-counted cells use one.
- Explain subject-wise splitting and training-only normalization. Identify the
  actual held-out subjects for one seed.
- Read Table 3: why can the measured constant-1 baseline differ from 1/6?
  Why are the 50-epoch results follow-up experiments rather than an untouched
  holdout? Explain the solved counts and the null T=200 forget-bias result.
- Explain partial hidden-state gradients versus the LSTM cell-state path.
  Identify the fixed independent T=100 probe and checkpoint-selection rule.
- Recompute the three-token attention example and block count 12d²+13d.
  Explain pre-LN, causal mask direction and the future-token perturbation test.
- Explain why sinusoidal is selected by validation F1 although learned positions
  have higher observed test accuracy. Identify patching, size, depth and dropout
  differences before interpreting the GRU time/accuracy comparison.
- Trace the contiguous character split and next-token targets. Explain nats/ln2,
  Adam reset at continuation, temperature/top-k and the no-mask leakage result.
- Distinguish allocated tensor memory from reserved memory/RSS and training GPU
  time from wearable energy or inference latency. Explain why full-model scaling
  differs from a pure quadratic attention operation.
- Trace KV positions, offset masks and rebuilding after a context-window shift.
  Explain short-prefix speed gains and the reported 500-character slowdown.
- Distinguish the original 96.27-minute fresh GPU run from current cached replay.
  Review the AI disclosure and missing variant/hand-fixture assumptions honestly.

Final personal actions: confirm the portal deadline, upload
`2026aj05073_DNN_Assignment.zip`, download/open the uploaded copy and retain the
confirmation. The brief's date/weekday is inconsistent; the portal is authoritative.
See [the final review](../FINAL_SUBMISSION_REVIEW.md). No portal action was performed.
