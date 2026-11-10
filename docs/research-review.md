> Historical review record. Current verification and policy status are in [submission-validation.md](submission-validation.md). Prior authorship or permission assertions are not evidence of instructor authorization.

> Historical experiment analysis retained for provenance. Current primary model, notebook workflow and submission scope are defined in [reproducibility-audit.md](reproducibility-audit.md) and [submission-validation.md](submission-validation.md). Baseline numbers below remain baseline results; they are not automatically primary-model results.

# Supplemental investigation — verified evidence

These experiments supplement the preserved82-run baseline; they do not silently replace it. Original metrics are in baseline-2026-11-09. The protocol was recorded in review-evidence/protocol.md before outcomes. Code is scripts/research_review.py; all selected checkpoints remain outside the submission.

## Adding diagnosis

Target identity was checked by an independent marker-times-value sum. Repeated forwards with intervening other sequences are identical: no hidden state leaks between batches. Gradients are finite and parameters update. The original36 checkpoints still reproduce their recorded test errors and validation-selected epochs.

All three models fit the fixed32-example training batch under1200 updates (final MSE RNN0.00000462, LSTM0.01597579, GRU0.00186863). These are training results, not evidence of generalization. The same data/model/optimizer/lr/batch/initialization/shuffle as the original T50 seed0 runs were then used for25 epochs. The first five train and validation losses match the original histories exactly. Best25-epoch validation MSE: RNN0.16462985, LSTM0.01327108, GRU0.00189044. Thus the gated short-sequence failure under five epochs is not a broken generator/loss or an inability to learn; duration matters here. The RNN fits a small set but still fails on independent validation, consistent with a learning/generalization limitation in this protocol.

This does not prove why T200–400 fails or measure a test improvement. No seed2/test data were generated in the diagnostics. There is no retuned36-run grid; the original common five-epoch results and their zero solved counts remain primary. Six extra rows have blank test metrics. Overfit sec_per_epoch is the mean of logged single-update intervals (not all1200 timings or full run wall time); the JSON separately records wall time. Pilot timings cover every epoch.

## LM continuation

Whole-text65-character vocabulary, first90%/last10% contiguous split, nonshuffled next-token blocks, no split-crossing targets and token-weighted loss were checked. No architecture/scratch code changes were made. All variants get five extra epochs, same batch64/lr1e-3/clip1/dropout0.1. Each resumes its own validation-selected five-epoch checkpoint and all restart Adam because old optimizer states are absent. Original matched-initialization comparisons are retained; continuation comparisons have equal additional budgets and the same resume rule, not identical starting weights. No causal attribution to duration alone is made.

| Variant | Baseline nats | Selected continued nats | Continued BPC | Extra epoch selected |
|---|---:|---:|---:|---:|
| h4-causal1 | 2.234945 | 2.026947 | 2.924266 | 5 |
| h1-causal1 | 2.202787 | 1.996096 | 2.879758 | 5 |
| h8-causal1 | 2.255983 | 2.072158 | 2.989491 | 5 |
| h4-causal0 | 0.317695 | 0.031937 | 0.046076 | 5 |

Unmasked losses are contaminated by future targets, not a better language model. Head rankings are one-seed observations. The causal four-head continuation is selected by its own validation loss and used for three500-character draws at0.2/0.8/1.5, top-k20, prompt ROMEO:newline, seed700. Original required samples remain intact; supplemental outputs are in review-evidence/continued-generated_samples.txt. Numerical quality still falls outside the approximate1.5–1.8-nat sanity range; this is disclosed rather than treated as a target to tune on test data.

## Interpretation and measurement

The fixed-weight trained no-position HAR probe distinguishes whole-patch reversal invariance from within-patch reversal sensitivity. Patching retains the eight ordered offsets in each token. It is not an arbitrary time-step bag. Width/depth/patch/dropout differences remain, so the2.42-point operational HAR gain is not assigned specifically to attention. No parameter-matched architecture comparison or deployment energy experiment was performed.

Attention maps retain the original actual five-epoch weights. Indexed links: head1 query17(b) attends0.6783 to itself and0.0460 to key3(b); query18(e) gives0.3480 to preceding b. Head2 query17 gives0.5991 to itself and0.1213 to the preceding space; query18 gives0.2982 to b and0.1891 to that space. These are descriptive links on one short input, not proof of semantic importance.

The nonuniform hand example uses Q=[(1,0),(0,1),(1,1)], K=[(1,0),(0,1),(1,-1)], V=[(1,0),(0,2),(3,4)]. Full scalar exponentials, weights and outputs are in the notebook/report and nonuniform-hand-example.json. Independent code agreement is checked without changing the scratch implementation.

New context measurements retain all five timings and three complete allocation-event traces per length; each peak is independently reconstructed from signed events. The workload remains eval-mode/dropout-off, squared-logit forward+backward at batch8, four CPU threads, two warmups. It is not next-token training throughput, generation latency, total RSS or reserved memory. Raw events permit reconstruction; historical aggregate-only measurements are preserved as baseline, not falsely reconstructed.

## Limits and integrity

Fresh supplemental training was executed; the old82 experiments are checkpoint replay, not freshly retrained. No clean dependency reinstall or T4 runtime was measured; no portal upload occurred. Scratch implementations remain unchanged and disclosure is complete. No instructor-authored authorization waiving the written AI restriction was located. Student understanding/authorship conditions are separately documented in understanding-checklist.md; the FAQ says no formal viva.

## Concrete continued-sample observations

At0.2, “the he” and “and the” recur, and “halll” is malformed. At0.8, “That pray here you sliang” resembles a clause but contains invented/misspelled words and does not sustain meaning. At1.5, “LRIENCUS:” resembles a speaker label while “caingmiely” and surrounding broken words show weak spelling and coherence. These are examples from single actual draws, not an evaluation of all possible outputs. The continued unmasked sample is inspected separately; low contaminated loss does not imply fluent generation.
