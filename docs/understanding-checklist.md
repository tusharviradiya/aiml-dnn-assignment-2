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

## Internal viva-style exercises (not a required viva; excluded from ZIP)

Complete these independently; this document is preparation, not proof of understanding.

1. **Derivations:** write each recurrence and annotate every matrix/state shape.
   Recompute RNN/LSTM/GRU counts atd9/h64, showing both biases. Explain why merging
   candidate GRU biases changes PyTorch compatibility when the reset gate is not1.
2. **Attention arithmetic:** calculate all three QK rows, divide bysqrt2, normalize
   exponentials and multiply by V. Recalculate with the causal mask. Derive12d²+13d
   for the block and identify which terms change if projection biases are removed.
3. **Leakage debugging:** deliberately split HAR windows randomly, fit normalization
   on all subjects, or expose a future token. Explain why shape tests still pass;
   identify the stronger subject/statistics/future-perturbation test that catches each.
4. **Adding debugging:** move both markers into the first half, detach the hidden
   state, or forget optimizer.zero_grad. Predict which generator/gradient/overfit
   checks fail. Explain why passing a32-example fit cannot replace1000-example
   validation and why that validation cannot be called test performance.
5. **Checkpoint exercise:** identify primary LM config, baseline epoch, additional
   selected epoch and SHA in notebook output and sample header. Explain why resetting
   Adam loses first/second moments even when parameter values are unchanged.
6. **Resume exercise:** take one stochastic Adam step after saving; restore model,
   optimizer and every RNG, repeat, then omit loader RNG or dropout RNG and explain
   the mismatch. Historical selected-weight files cannot supply missing optimizer states.
7. **Interpretation:** trace one indexed attention link and propose an intervention
   needed to test its causal role. Show whole-patch invariance algebraically, and why
   reversing within-patch offsets instead changes the patch projection.
8. **Measurement exercise:** reconstruct one peak from signed memory events, separate
   O(T²d) attention products from linear FFN terms, and explain why this is not process
   RSS or wearable energy. Distinguish cached measurement replay from remeasurement.
9. **Authorship/reproduction:** accurately state actual AI contributions, the written
   rule and the scope of student-reported informal permission. Explain which commands
   trained models, replayed weights, checked evidence read-only, and executed extraction.
