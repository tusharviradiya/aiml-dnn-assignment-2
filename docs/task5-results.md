# Task 5 — measured results

Gradient evidence: hidden_gradients.csv contains 1800 records from 18 probes (three models × three seeds × before/after), each T=100. Figure 6 shows log-scale means over seeds; actual hidden graph nodes retain gradients. Outputs and parameter gradients agree with library references. Raw zero values, if any, remain in CSV; display floor is 1e-300.

Table 3. HAR sweep means/sample standard deviations, three seeds. All widths use ten epochs and the prior matched protocol. Six width64 results were reused; eighteen new runs were trained.

| Model | h | Accuracy (%) | Macro-F1 | Params | CPU sec/epoch |
|---|---:|---:|---:|---:|---:|
| GRU | 16 | 78.57 ± 2.23 | 0.7761 ± 0.0219 | 1398 | 1.122 |
| GRU | 32 | 87.41 ± 0.73 | 0.8741 ± 0.0064 | 4326 | 1.591 |
| GRU | 64 | 88.19 ± 1.04 | 0.8819 ± 0.0104 | 14790 | 2.279 |
| GRU | 128 | 89.04 ± 0.70 | 0.8891 ± 0.0092 | 54150 | 4.181 |
| LSTM | 16 | 75.55 ± 6.53 | 0.7434 ± 0.0755 | 1830 | 0.298 |
| LSTM | 32 | 84.80 ± 1.12 | 0.8467 ± 0.0112 | 5702 | 0.538 |
| LSTM | 64 | 87.71 ± 0.29 | 0.8768 ± 0.0023 | 19590 | 1.182 |
| LSTM | 128 | 88.28 ± 0.43 | 0.8833 ± 0.0038 | 71942 | 2.997 |

Figure 7 shows the sweep with sample-std error bars.

Table 4. Odd-ID effective initial forget-bias comparison, LSTM T=200, five epochs, three paired seeds.

| Bias | Test MSE | Solved / 3 |
|---|---:|---:|
| 0 | 0.168401 ± 0.000449 | 0 |
| 1 | 0.168494 ± 0.000390 | 0 |

Figure 8 shows validation curves and test MSE error bars. Initial recurrent forget bias is zero in both branches; input forget bias is 0 or 1. Other weights and shuffle orders are paired. Biases remain trainable, so these are initialization interventions. Both branches remain unsolved.

Evidence: hidden_gradients.csv, har_hidden_sweep_{runs,summary,history,predictions}.csv, forget_bias_{runs,summary,history,predictions}.csv and task5_config.json. See problem1-analysis.md for the concise report analysis, including memory interpretation, failures, trade-offs and the conditional wearable recommendation.
