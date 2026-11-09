# Student authorship and understanding

The supplied FAQ answers “Will there be a viva?” with “No”. This checklist is preparation for understanding and any later instructor questions, not a claim that a viva is required. AI-produced explanations here are not evidence that the student independently derived or demonstrated them.

## Authorship requirement still unresolved

The written rules require student-authored RNN/LSTM/GRU cells, attention, multi-head attention and encoder block. Existing versions are disclosed as AI-written. No instructor-authored waiver is available. Do not relabel these implementations as independently written. If the instructor rejects the reported exception, follow their remediation instructions; no purported student rewrite has been generated during this audit.

## Questions to answer from the actual submission

- Trace input/state/output shapes through each recurrence; explain LSTM's separate cell path, GRU reset placement and the two-bias parameter-count difference.
- Show why training-only normalization and subject holdouts prevent leakage; reproduce one held-subject list.
- Explain why fitting32 examples is not learning addition in general. Interpret the exact replay of the first five pilot epochs and the gated improvement by epoch25. Explain why this says nothing definitive about T400.
- Derive the nonuniform three-token attention weights from the stated Q/K/V; explain the square-root scale and the boolean mask convention.
- Derive12d²+13d per block and identify each bias/norm term. Explain pre-LN versus post-LN.
- Explain why flattening8 steps retains ordered offsets but no-position CLS is invariant to whole-patch permutations.
- Identify why attention cannot be credited alone for the HAR gain when depth, parameter count, dropout and patching differ.
- Trace the contiguous character split and one next-token block, including the final omitted tail. Show why the unmasked t+1 input leaks the target at t.
- Distinguish the matched-initialization five-epoch head ablation from the five-additional-epoch continuation with Adam reset. Identify the remaining single-seed limitation.
- Read a concrete query/key link by index. Explain why an attention weight alone does not establish a causal explanation.
- Reconstruct one memory peak from signed allocation events and distinguish it from RSS/reserved GPU memory. Explain the timed squared-logit forward/backward workload versus generation latency.
- Distinguish checkpoint replay, actual supplemental training, clean dependency installation and portal submission; state which were actually verified.
