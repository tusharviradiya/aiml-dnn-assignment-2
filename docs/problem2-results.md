> Historical experiment analysis retained for provenance. Current primary model, notebook workflow and submission scope are defined in [reproducibility-audit.md](reproducibility-audit.md) and [submission-validation.md](submission-validation.md). Baseline numbers below remain baseline results; they are not automatically primary-model results.

> Baseline training results are preserved below; new continuation results are in research-review.md. Figure numbers here refer to notebook plots; the final PDF uses consecutive report numbering. Context measurements below were refreshed with raw evidence.

# Problem 2 results and analysis

All 13 runs and110 epochs completed. Full notebook execution and cache restart passed; independent checkpoint/sample replay passed. The instructor clarification permits our own three-token example; its strict tests pass. AI-assisted code follows professor permission reported by the user.

## Component evidence and parameter derivation

Attention max absolute error3.576279e-7 versus functional SDPA; multi-head1.804112e-16 versus nn.MultiheadAttention; encoder8.881784e-16 versus the pre-LN reference; sinusoidal5.960464e-8 versus scalar math. Input gradients match within8.881784e-16. Row sums, future zeros, finite gradients, invalid masks and dimensions, and whole-block/LM causality assertions pass. No library attention/Transformer is used in model implementations. The chosen hand example agrees by hand/code; the chosen example satisfies the clarified instruction.

Block matrices contribute4d²+2d(4d)=12d²; attention biases4d, FF biases5d, two LayerNorm scale/bias vectors4d add13d. At d=128:196608+1664=198272 total, verified against actual parameters. At d=64:49152+832=49984. HAR has2×49984 + (72×64+64) embedding +64 CLS +128 final norm +(64×6+6) head =105222; learned positions add17×64=1088, giving106310. LM has2×49984 +65×64 embedding +128 final norm +(64×65+65) untied output =108481.

## HAR: Table 5 and Figure 9

Same full dataset, three seeds/splits, training-only normalization, batch 128, Adam1e-3 and10 epochs as P1. Transformer uses8-step patches, CLS, d=64/two blocks/four heads/dropout0.1; these architecture differences matter when interpreting time and accuracy. Checkpoints select validation macro-F1 only.

| Model | Test accuracy (%) | Macro-F1 | Parameters | CPU sec/epoch |
|---|---:|---:|---:|---:|
| HAR-Transformer-learned | 91.20 ± 0.53 | 0.9121 ± 0.0057 | 106310 | 1.521 |
| HAR-Transformer-none | 90.54 ± 1.82 | 0.9045 ± 0.0182 | 105222 | 1.419 |
| HAR-Transformer-sinusoidal | 90.61 ± 1.02 | 0.9062 ± 0.0106 | 105222 | 1.544 |
| P1 validation-selected GRU h=64 | 88.19 ± 1.04 | 0.8819 ± 0.0104 | 14790 | 2.279 |

Table 5: means±sample std over three seeds; CPU training time excludes evaluation. Figure 9 (`problem2/figures/har_positions.png`) plots the positional variants. Mean validation macro-F1 chooses **sinusoidal** (0.927613), not learned (0.914417); none reaches0.924655. Learned has the highest observed test mean, but test scores do not select the model. The selected sinusoidal encoder gains2.42 percentage points over P1 GRU h=64, using7.11× as many parameters and a measured 0.68× CPU seconds/epoch on this backend. Patching reduces tokens from128 to17 including CLS; this is not evidence that attention is generally faster.

Position-free and sinusoidal test means differ by just0.068 percentage points, smaller than their between-seed variation. Absence of global positional information leaves within-patch order and sensor distributions available. Learned-position performance does not establish a consistent benefit across unseen subjects, especially given its lower validation mean.

## Language-model experiments

Table 6 and Figures10–12 use the same contiguous90/10 split, seed 0, context 128, d=64/two layers (explicit CPU exception), five epochs, batch=64, Adam1e-3, dropout0.1 and norm1 clipping. No shuffling and no split-boundary targets. Validation selects the minimum-loss checkpoint. Vocabulary65 comes from the whole1115394-character source. All models have108481 parameters, with exactly matched parameter initialization; only head reshaping or masking changes.

| Heads / mask | Validation nats | BPC | CPU sec/epoch |
|---|---:|---:|---:|

| 4 / causal | 2.234945 | 3.224344 | 22.091 |
| 1 / causal | 2.202787 | 3.177949 | 16.018 |
| 8 / causal | 2.255983 | 3.254695 | 32.616 |
| 4 / none (LEAKAGE) | 0.317695 | 0.458337 | 24.997 |

Table 6: measured validation loss and BPC=nats/ln2, one seed. The four-head causal model improved from2.55856 to2.23495 validation nats over five epochs; its curve is still descending. The smaller CPU model and limited budget explain a plausible shortfall from the larger/longer-trained model's approximate1.5–1.8 range; these experiments do not isolate either effect. One-head validation loss is lowest here; do not generalize a single-seed ranking. Increasing heads leaves matrix counts unchanged but increases the number of stored T×T softmax maps at fixed batch/context, contributing to backend timing differences. Figures10–12 are panels of `problem2/figures/lm_ablations.png`.

## Mask ablation and generation

Figure 12 shows unmasked final training loss0.59362 versus causal2.26579. Unmasked apparent validation loss0.317695 is contaminated: input token at t+1 exposes the target for position t. It cannot be interpreted as a valid autoregressive BPC despite the arithmetic value in Table 6/results.csv. Changing future input tokens leaves the trained causal prefix logits exactly unchanged, but changes unmasked prefix logits by max7.15354 (`mask_diagnostic.json`).

With the same prefix/top-k20/seed 700 at temperature0.8, the unmasked continuation is98.4% newlines, with only 4 distinct characters. Its low training loss fails to yield useful generation because future targets are unavailable when sampling. All 500 characters are saved in `no_mask_sample.txt`.

The main model generates exactly500 new characters each at temperatures0.2/0.8/1.5 with top-k20, seed 700 and prompt`ROMEO:\n`. The prompt is not counted in500. `generated_samples.txt` labels the three samples; `samples.json` preserves exact strings/settings. Table 7 reports empirical sample diversity (not model entropy):

| Temperature | Distinct characters | Empirical character entropy (bits) |
|---|---:|---:|
| 0.2 | 14 | 2.920 |
| 0.8 | 31 | 4.167 |
| 1.5 | 44 | 4.688 |

Table 7: statistics of the single saved500-character draw per temperature. At0.2, repeated `the`/`and` fragments dominate. At0.8, wordlike fragments, line breaks and speaker-like formatting become more varied but spelling remains weak. At1.5, mixed case and punctuation increase and coherence declines. These are observations about the saved draws, not significant quality differences established over repeated samples.

## Attention heatmaps

Figure 13a/b (`attention_heads.png`) show layer1 heads1/2 on `To be, or not to be.`. Both favor current/nearby characters, with different off-diagonal patterns. Mean diagonal mass is0.3616/0.3736; mean first-token mass0.0721/0.0747. The first row has only one visible key. Every future weight is zero. One short character sentence does not establish syntactic head specialization or causal explanations; the saved matrices in `attention_heads.npz` support only these measured patterns.

## Context scaling: Table 8 and Figure 14

Fixed trained four-head model, batch 8, float32, eval/dropout off; two warmups and five forward+backward timing repeats. CPU profiler memory is peak additional live tensor allocation relative to existing model/input baseline, not RSS or reserved allocator memory. Model quality is not evaluated at these longer contexts.

| Context | Mean ± sample std (ms) | Peak additional tensors (MiB) | One score tensor elements |
|---|---:|---:|---:|
| 64 | 8.709 ± 0.402 | 5.228 | 131072 |
| 128 | 14.602 ± 0.810 | 12.714 | 524288 |
| 256 | 45.767 ± 0.897 | 41.331 | 2097152 |
| 512 | 187.750 ± 6.799 | 146.753 | 8388608 |

Table 8: measured full-model cost; Figure 14 (`context_scaling.png`) plots time and memory, including an anchored quadratic reference. An8× context increase gives64× as many score elements, 21.56× measured time and 28.07× additional tensor peak. Each score product/weighted sum has O(T²d) work; FFN/embeddings add linear-T cost, so the total need not scale exactly64×. Hardware/cache/thread/allocation overhead also affects short-context time. CPU results do not establish T4 runtime or wearable inference energy.

## Verification and remaining work

Full Restart & Run All passed twice (initial training, then13 cache hits). The baseline ledger has82 rows, including69 P1 and13 P2 runs; the final ledger additionally contains10 explicitly labelled diagnostics/continuations. Independent audit reproduces nine HAR checkpoints/26523 predictions, all four LM validation losses, all 2000 generated characters, statistics and perturbation evidence; verifies sample standard deviations, selected epochs, counts, source fingerprints and absence of forbidden framework layers in model code. All four image files visually inspected. Total P2 training-only CPU time613.14 seconds (10.22 min), excluding validation/generation/profiling/setup. No T4 measurement.

The instructor email permits chosen h/d/seeds and a self-created three-token example. We choose h=64, d=64 and seeds0/1/2. Hand/code agreement passes. The mathematical reference remains Vaswani et al. The email confirms Saturday14 November2026 as the due date. It does not address AI authorship; the original written prohibition needs the separately user-reported permission to apply. Optional bonus is unattempted; portal submission remains external.

## Supplemental examiner-led evidence

See research-review.md and review-evidence/: equal five-epoch LM continuations, new actual samples, concrete indexed head links and trained patch-order probe. All five raw timings and three full memory traces per context are retained under problem2/metrics/context_raw_*.json. Original baseline learning failures and generation are retained; no claimed causal architectural improvement.
