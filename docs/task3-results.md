# Task 3 — HAR evidence and interpretation

Configuration: one recurrent layer, hidden size 64, final hidden-state classifier, batch 128, Adam 1e-3, 10 epochs, norm-1 clipping, no dropout. Three paired chosen seeds 0/1/2. Source/data/config fingerprint: 878cc93e6862a042. These results use the official subject-disjoint test split.

Table 1. Means ± sample standard deviations across three seeds. Accuracy is percent; macro-F1 is on [0,1]. Training times are measured on this CPU with four PyTorch threads, excluding validation/evaluation.

| Model | Test accuracy (%) | Macro-F1 | Parameters | Seconds/epoch |
|---|---:|---:|---:|---:|
| RNN | 70.52 ± 4.91 | 0.6814 ± 0.0495 | 5190 | 0.677 ± 0.012 |
| LSTM | 87.71 ± 0.29 | 0.8768 ± 0.0023 | 19590 | 1.182 ± 0.040 |
| GRU | 88.19 ± 1.04 | 0.8819 ± 0.0104 | 14790 | 2.279 ± 0.022 |

Table 1 shows a large improvement from either gated model over the vanilla RNN under this budget. GRU's mean accuracy is slightly higher than LSTM's, but three runs do not establish a statistically reliable advantage. GRU has fewer parameters, while LSTM trains faster on this particular CPU/backend; these times do not measure wearable inference speed or energy. RNN's larger seed variability suggests less stable performance here.

Figure 2 (`problem1/figures/har_confusion_matrix.png`) uses GRU seed 2, epoch 9. Architecture selection used mean validation macro-F1; run and epoch selection also used validation only. This representative run achieves 87.14% test accuracy, rather than the best observed GRU test accuracy. Sitting/standing account for 204 cross-confusions (88 sitting→standing and 116 standing→sitting), a prominent error pattern.

Figure 3 (`problem1/figures/har_learning_curves.png`) plots training and validation losses averaged over all seeds. Gated models reduce training loss more consistently; RNN validation loss fluctuates and remains higher. This observation does not by itself prove a vanishing-gradient mechanism: Task 5 gradient evidence is still required.

Evidence: results.csv plus problem1/metrics/har_{runs,summary,history,predictions}.csv and har_config.json. No test-driven tuning was performed. Remaining limitations: a short fixed epoch budget and CPU-specific timings. No T4 runtime or battery-power measurements are claimed.
