> Historical experiment analysis retained for provenance. Current primary model, notebook workflow and submission scope are defined in [reproducibility-audit.md](reproducibility-audit.md) and [submission-validation.md](submission-validation.md). Baseline numbers below remain baseline results; they are not automatically primary-model results.

# Problem 1 — analysis for the report

Figure 6 shows early hidden-gradient attenuation at T=100. After training, the t=1/t=100 mean-norm ratios are about3.6×10⁻²² (RNN),1.2×10⁻¹¹ (LSTM) and6.5×10⁻⁵ (GRU). Predictions and parameter gradients match the library graph. Gating retains stronger early hidden signals here, but these derivatives also depend on loss and trajectory; dL/dh_t does not cover LSTM's separate cell-memory path or prove a general memory ranking.

Table 2 and Figures 4–5 preserve36 unsolved five-epoch test runs. T=400's lower MSE also occurs for constant prediction, not better memory. New Table5 reports independent T=50 diagnostics. All models fit32 training examples below0.05; memorization is not generalization. With unchanged data, initialization, shuffle, optimizer and batch, the25-epoch pilots exactly replay their first five baseline epochs, then reach validation MSE0.16463/0.01327/0.00189 (RNN/LSTM/GRU). This isolates duration as a gated short-sequence limitation. It neither explains T=200–400 nor establishes a new test ranking: no pilot test data were accessed. Finite gradients, target identity, state reset and parameter updates pass.

The paired odd-ID study changes only initial effective forget bias. Table 4/Figure 8 give test MSE0.16840±0.00045 (bias0) versus0.16849±0.00039 (bias1), neither solved. This difference is small relative to seed spread; no reliable benefit or harm follows under five epochs.

On HAR, Table 1 gives70.52±4.91% (RNN),87.71±0.29% (LSTM),88.19±1.04% (GRU); Figure 2 shows sitting/standing confusion. Table 3/Figure 7 show GRU h32→128 raises accuracy87.41→89.04% while parameters grow4326→54150. LSTM h128 reaches88.28% with71942 parameters. CPU training favors LSTM over comparable GRU widths on this backend; it does not measure deployment energy.

For a memory-constrained wearable, these measurements favor prototyping GRU h32:71% fewer parameters than h64 for0.78 points lower accuracy, and better accuracy than LSTM h32. Float32 weights occupy16.9KiB before activations/runtime. Device latency and energy remain unmeasured; three seeds and short budgets limit certainty.
