# Task 4 — Adding results

All 36 full-data runs completed: three models × four lengths × three model seeds. Training/validation/test sizes 10000/1000/1000 use fixed data seeds 0/1/2. Shared settings: chosen h=64, model seeds 0/1/2, batch 128, Adam 1e-3, norm-1 clipping and five epochs. Select minimum validation MSE, ties earliest.

Table 2. Test MSE mean ± sample std. Every group has **0 solved runs out of 3** (threshold MSE <0.05).

| T | RNN | LSTM | GRU | Constant-1 empirical baseline |
|---|---:|---:|---:|---:|
| 50 | 0.174303 ± 0.000505 | 0.174341 ± 0.000304 | 0.171701 ± 0.002500 | 0.175392 |
| 100 | 0.169953 ± 0.000536 | 0.169969 ± 0.000769 | 0.169283 ± 0.000823 | 0.169709 |
| 200 | 0.168615 ± 0.000770 | 0.168417 ± 0.000481 | 0.168546 ± 0.000325 | 0.167942 |
| 400 | 0.154511 ± 0.000280 | 0.153823 ± 0.000541 | 0.153454 ± 0.000343 | 0.152720 |

Figure 4 (`problem1/figures/adding_mse_vs_length.png`) compares models with sample-std error bars, theoretical baseline 1/6 and solved threshold. Table 2 gives empirical baselines: the lower T=400 MSE is also present for constant prediction, so it does not indicate better memory.

Figure 5 (`problem1/figures/adding_curves_t200.png`) shows mean training/validation curves. Training approaches roughly 0.17 and plateaus. These experiments do not demonstrate successful retention/addition of marked values, or a reliable gated-model advantage. The short five-epoch CPU budget is a material limitation, fixed before test evaluation. No test-driven extension or success claim is made; Task 5 gradients/ablations are still required.

Evidence: results.csv plus problem1/metrics/adding_{runs,summary,history,predictions}.csv and adding_config.json. Independent checkpoint replay reproduced predictions/metrics and verified checkpoint selection, counts and statistics. Datasets/checkpoints remain ignored.

Training-only CPU time: 25.3 minutes, excluding evaluation/setup/audit. T=400 LSTM took about 42–45 sec/epoch. No T4 timing is claimed.
