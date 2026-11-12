# Frozen revision protocol

Before revised training: 50 epochs for all 36 adding and six paired forget-bias runs; h64, Adam0.001, batch128, clipping1, model seeds0/1/2 and original prescribed data. Select minimum validation MSE (earliest tie), evaluate test after training; no outcome-driven budget extension. Revision motivated by validation-only T50 pilots and external review. Earlier test results were already observed; no untouched-test claim is made.

KV bonus: inference-only existing four-head causal continued LM; greedy batch1 FP32; prompts8/32/64 with64 new characters and ROMEO newline with500 new characters. Three warmups, ten paired trials, alternating order, synchronized CUDA, prefill included. Rebuild caches when the original128-token window shifts. Save raw timings and correctness checks.

## Inference optimization follow-up
The first cache was numerically correct but approximately10% slower. Retain that full attempt at .cache/improvement-run. Remove redundant per-layer mask creation, and omit the all-visible mask for one appended query. Repeat P2 from fresh P2 training caches with identical training protocols. Keep the successful original fresh P1 execution; report the sum of those successful notebook executions, excluding the preserved earlier P2 attempt. Distinct-batch FP32 audit uses atol=rtol=1e-5 to account for shape-dependent GEMM rounding; raw absolute error is recorded in the audit.
