# Student-authored work and verification map

Updated 2026-11-08. AI prepares interfaces/tests/explanations, reviews student code,
debugs errors and tidies plots. The user confirmed no instructor clarification
permits AI-written experiment code: training pipelines remain student-authored.
No model experiments have run; this document is guidance, not results.

## Current independent work

| Component | Student action | Verification entry point |
|---|---|---|
| Recurrent constructor | Register/initialize four parameters in each existing cell | `verify_constructor(MyRNNCell, 'RNN')`, corresponding LSTM/GRU calls |
| Recurrent forward | Implement each cell's equations without library recurrent calls | `verify_cell(MyRNNCell, 'RNN')`, corresponding LSTM/GRU calls |
| Attention | Implement tensor-only scaling/masking/softmax/weighted values | `verify_attention(scaled_dot_product_attention)` |
| Multi-head | Four projections, split/merge heads, own attention | `verify_multihead(MyMultiHeadAttention)` |
| Encoder | Pre-LN residual branches, dropout, 4d FFN, own attention | `verify_encoder(MyEncoderBlock)` |
| Sinusoidal positions | Implement formula in notebook guidance | `verify_positions(sinusoidal_positions)` |
| P1 experiments | Student authors library-based recurrent training/evaluation code | Review for fairness, leakage, seeds, metrics before running |
| P2 experiments | Student authors data/model/training/generation code using custom components | Verify components first, then review split/mask/metrics and run |

P1 Tasks 3–5 permit library recurrent layers and are technically independent of
P1 Task 2. Their present blocker is missing **student-authored experiment code**,
not the custom recurrent cells. Problem 2 experiments additionally depend on
student-authored Transformer components. No need to repeatedly invoke unchanged
placeholders. Use targeted checks when student code changes.

## Experiment acceptance checklist for later code review

- HAR: use Task 1's channel order and training-only statistics. Refit split/statistics
  per seed; hold out four subjects. Fix variant width/seeds once the missing table
  is available; existing seeds 0/1/2 remain provisional.
- RNN/LSTM/GRU: last hidden state; same hidden width, batch size, Adam 1e-3 and epoch
  budget. Select checkpoints by validation data only. Log all three seeds, parameter
  counts, epoch time, accuracy and macro-F1. Use sample std (ddof=1). Choose the best
  architecture by validation evidence and document the confusion-matrix selection.
- Adding: four lengths × three models × three model seeds; dataset seeds remain
  fixed 0/1/2. Report MSE and solved counts (<0.05), T=200 curves and MSE vs length.
- Gradients: T=100; before/after training; actual intermediate hidden states must
  participate in the recurrent graph and retain gradients. A post-hoc view of a
  fused output tensor is not necessarily the internal recurrent state gradient.
- Sweep: LSTM/GRU hidden widths 16/32/64/128, comparable training budgets. Individual
  T=200 ablation depends on ID parity; do not guess the assigned branch.
- Transformer HAR: reuse identical splits; report accuracy/parameters/time;
  compare none/sinusoidal/learned positions. Keep all other choices controlled.
- Shakespeare: whole-text vocabulary (65); contiguous first 90%/last 10%; sequence
  windows must not cross the split. Next-token targets shift one character; causal
  mask must prevent access to future tokens. Context 128, d=128, 4 heads, 4 layers;
  CPU exception d=64/2 layers is allowed if explicitly documented.
- Language metrics: validation cross-entropy in nats; bits/character = loss/ln(2).
  Produce 500 newly sampled characters at each temperature 0.2/0.8/1.5 with a stated
  top-k; use eval/no-grad for generation. Keep outputs as evidence, not placeholders.
- Ablations: 1/4/8 heads at fixed d; no-mask loss/generation; context 64/128/256/512
  time and memory with the same measurement method/device. Synchronize GPU timing
  and distinguish allocated peak memory from CPU memory if applicable.
- Append a results.csv row after each actual completed run, using its exact schema.
  Keep irrelevant fields empty and identify ablation settings in notes. Do not
  populate results.csv with test-oracle outputs or untrained-model guesses.

## Reporting and integrity

Report remains blocked on measured evidence and student analysis. No report.pdf is
created merely to satisfy packaging. Required instructor hand example, variant table,
student identity and portal/deadline confirmation remain outstanding. The illustrative
attention fixture is explicitly not the missing instructor example.

Record AI use truthfully: Task 1 code was AI-assisted earlier; later interfaces,
verification tools, equation guidance, debugging and documentation are AI-assisted.
Do not describe AI-assisted code as wholly student-authored. Earlier Task 1 assistance
exceeds the narrowly listed AI uses; instructor acceptance has not been established.
