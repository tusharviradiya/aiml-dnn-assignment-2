# External examiner evaluation — DNN Programming Assignment 2

Review date: 9 November 2026. Student: Viradiya Tushar Rajeshbhai, 2026aj05073.

**Estimated technical mark: 96/100; defensible examiner range: 93–98/100, conditional on acceptance of the reported instructor clarifications and AI authorization. An unconditional awarded mark cannot responsibly be predicted: the submission explicitly declares AI-written scratch implementations despite the original written prohibition.** This is a substantive policy conflict, not an ordinary one- or two-mark deduction. The technical score below must not be read as confirmation that the submission is eligible for those marks.

## Basis and limits of examination

The controlling source was the original `DNN Programming Assignment – RNN, LSTM, GRU and Transformer.docx`, including its rubric, FAQ, report requirements and integrity rules. I inspected both notebooks' source and saved outputs, the actual PDF and LaTeX source, metric tables, histories, predictions, saved attention arrays, samples, scripts, requirements, README and the existing submission ZIP. Progress/readiness documents were not accepted as proof of correctness.

`docs/instructor-clarifications.md` records permission to choose sizes/seeds and create the hand example. No original instructor-authored email was located in the supplied files. The assessment provisionally accepts that recorded clarification; it is not independent authentication. The original FAQ independently permits d=64 and two LM layers on CPU, so the reduced LM is not automatically noncompliant.

Execution checks ran against temporary copies under `/tmp/dnn-professor-review`, using the existing environment and reading the local datasets/checkpoints. This kept potentially writing notebook setup code away from submission files. Only this requested evaluation document was created in the project. No experiments, reports, metrics or submission archive were changed.

The following were actually rerun successfully, rather than inferred from log documents:

| Check | Evidence verified during this review |
|---|---|
| `scripts/test_verification.py` | Re-executed scratch component verifiers; recurrent and Transformer completion gates pass; deliberate invalid fixtures are rejected. |
| `scripts/test_cache_fingerprints.py` | Reviewed cache reuse passes; configuration/training changes invalidate fingerprints. |
| `scripts/audit_har.py` | All nine recurrent HAR checkpoints reproduce predictions, accuracy/F1, normalization, selection and parameter counts. |
| `scripts/audit_adding.py` | All 36 checkpoints reproduce predictions, MSE, solved status and selected epoch; all 12 summary groups reconcile. |
| `scripts/audit_task5.py` | All 24 width-study checkpoints, six forget-bias checkpoints and 18 before/after gradient probes reproduce; paired bias initialization is checked. |
| `scripts/audit_problem2.py` | Nine encoder HAR checkpoints and four LM checkpoints reconcile; validation loss/BPC, all 2,000 generated characters including the no-mask sample, attention maps and perturbation diagnostics reproduce. |
| Independent archive/PDF inspection | ZIP CRC passes; archived files match their working counterparts; 3,245,412-byte archive excludes datasets/checkpoints/environment. PDF has seven A4 pages: six content pages plus the excluded declaration/references page. Extracted body text fits the prescribed margins. |

These audit programs belong to the submission, so their passing is not alone an external proof. Their logic and the underlying model/training source were also inspected. In particular, I checked the GRU reset placement, attention masking, pre-LN order, parameter formulas, split/normalization code, checkpoint selection and training loops. Saved notebook execution counts are sequential and contain no error outputs. I did **not** retrain all experiments from fresh initialization, reinstall into a clean environment, independently rerun the entire notebooks, or remeasure historical timings. Checkpoint replay supports inference/metric reproducibility; it does not independently prove the exact historical training process or runtimes. No portal submission receipt was available.

## Detailed marking table

The rubric gives only task totals. Subtask weights below are examiner allocations, not additional official rules. Small deductions for depth and communication are judgment calls; where a requirement is satisfied, poor benchmark performance alone is not penalized.

| Task/subtask | Max | Award | Assessment and deduction |
|---|---:|---:|---|
| **P1.1 Data pipelines** | **5** | **5** | Complete. |
| HAR loading, prescribed subject split, training-only normalization | 3 | 3 | Correct nine-channel ordering, official shapes, four held-out training subjects per seed, no train/test subject overlap; statistics replay against raw training subsets. |
| Class balance | 1 | 1 | Actual split-specific figure exists and appears in PDF. |
| Adding generator and tests | 1 | 1 | Matches prescribed generator; marker counts, one per half and target identity are asserted for all required datasets. |
| **P1.2 Scratch recurrent cells** | **10** | **10** | Technically correct; eligibility subject to authorship policy below. |
| Vanilla RNN | 2 | 2 | Registered matrices and tanh recurrence; reference comparisons pass. |
| LSTM | 3 | 3 | Correct i/f/g/o order and separate cell/hidden state; nonzero-state forward and gradient checks. |
| GRU | 3 | 3 | Correct PyTorch r/z/n convention, including reset applied to the recurrent candidate projection and its bias. |
| Parameter derivation and reconciliation | 2 | 2 | Correct single-bias and two-bias formulas/counts; classifier head accounted for. |
| **P1.3 HAR classification** | **10** | **10** | Complete comparison; no accuracy-target penalty. |
| Protocol and nine runs | 4 | 4 | Last hidden state; common h=64, Adam 1e-3, batch 128, ten epochs, clipping and three seeds. |
| Metrics, spread, parameters and timing | 4 | 4 | Sample standard deviations and underlying predictions reconcile. Timing is clearly CPU training time. |
| Best-model confusion matrix | 2 | 2 | Validation-selected GRU seed 2, epoch 9; no selection of checkpoint by test accuracy. |
| **P1.4 Adding problem** | **10** | **10** | Required experiment grid and evidence complete despite failure to solve. |
| 4 lengths × 3 models × 3 seeds | 4 | 4 | All 36 actual checkpoints/prediction sets verified. |
| MSE and constant baseline | 2 | 2 | Correct empirical constant-1 baseline for each length, as well as theoretical context. |
| Solved-run accounting | 2 | 2 | Correct threshold MSE<0.05 and explicit 0/3 for every group. |
| T=200 learning curves and MSE-versus-length | 2 | 2 | Both required plots appear in PDF. |
| **P1.5 Gradients, ablations, analysis** | **15** | **14** | Experiments complete; investigation of universal adding failure is limited. |
| (a) Before/after hidden gradients at T=100 | 4 | 4 | Actual retained intermediate hidden states, log plot, three seeds; float64 unroll agrees with library predictions and parameter gradients. |
| (b) LSTM/GRU width sweep | 4 | 4 | All widths 16/32/64/128, three seeds; legitimate reuse of existing h=64 runs. |
| (c) Odd-ID forget-bias study | 3 | 3 | Effective initial bias 0 versus 1, paired other weights/shuffle, T=200; not merely changing one of two bias vectors without checking the sum. |
| (d) One-page interpretation and wearable choice | 4 | 3 | Good limitations and quantitative GRU h=32 recommendation. **−1:** five-epoch undertraining is plausible but not experimentally isolated; no rescue or small-batch overfit diagnostic establishes why every short-sequence gated run failed. This limits explanatory depth, not completion of P1.4. |
| **Problem 1 subtotal** | **50** | **49** | |
| **P2.1 Attention** | **10** | **10** | Complete, conditional on reported example clarification. |
| Scaled dot product and optional mask | 4 | 4 | Correct scale, boolean visibility semantics, softmax axis and weighted values; fully masked rows explicitly rejected. |
| Numerical tests | 4 | 4 | Reference agreement, normalized rows, future zeros and additional gradient tests pass. |
| Three-token hand example | 2 | 2 | Chosen zero Q/K gives uniform weights; causal and unmasked calculations agree with code. Trivial but valid under the reported clarification; random nonzero tests separately check scaling. |
| **P2.2 MHA and encoder** | **10** | **10** | Complete. |
| Q/K/V/O and reshaping | 3 | 3 | Correct head split/merge; restricted library implementations confined to checks. |
| Pre-LN residual/FFN/dropout block | 3 | 3 | Correct normalization placement, 4d FFN and dropout branches. |
| Sinusoidal positions | 2 | 2 | Correct formula and scalar agreement tests. |
| Parameter derivation | 2 | 2 | 49,152 matrix weights + 832 bias/norm parameters = 49,984 at d=64; d=128 reference count also checked in code. |
| **P2.3 HAR encoder classifier** | **10** | **9** | Complete operational comparison, limited causal interpretation. |
| Patch embedding, CLS and classification | 3 | 3 | Correct patch8 embedding and CLS classification; output/backward tests pass. |
| None/sinusoidal/learned positions | 3 | 3 | All nine runs and three-seed summaries verified. |
| Comparison to recurrent baseline and interpretation | 4 | 3 | Same subjects, statistics, optimizer and epoch budget. **−0.5:** parameter count, depth, patching and dropout differ simultaneously, so gain cannot be assigned specifically to attention. Report acknowledges this, but does not isolate it. **−0.5:** explanation omits that patch flattening preserves order within each eight-step patch even with “none”; patch-permutation invariance is tested in code but its implication is not developed in the report. |
| **P2.4 Character LM** | **10** | **10** | Complete under explicit CPU exception. |
| Data, vocabulary and causal training | 4 | 4 | Whole-text vocabulary, contiguous 90/10 split, context128, no target crossing, scratch blocks. |
| Validation loss, BPC and curve | 3 | 3 | 2.23495 nats and 3.22434 BPC independently replayed; learning curve included. |
| Three 500-character top-k samples and discussion | 3 | 3 | Temperatures 0.2/0.8/1.5, top-k20; exact continuations reproduce; weak quality disclosed. |
| **P2.5 Analysis and ablations** | **10** | **9** | All required studies exist; modest deductions for depth of evidence. |
| (a) Two heads and interpretation | 2.5 | 2 | Actual trained maps reproduce. **−0.5:** interpretation largely describes diagonal/nearby mass; it does little to explain concrete repeated-character or cross-word links in this sentence. Avoiding unsupported syntactic claims is correct. |
| (b) Heads 1/4/8 at fixed d | 2.5 | 2.5 | Common width, initialization and budget; parameter count fixed; single seed allowed by this subtask and limitation disclosed. |
| (c) Causal-mask removal | 2.5 | 2.5 | Training-loss collapse, failed generation and future-perturbation evidence; contaminated validation explicitly labelled. |
| (d) Context 64/128/256/512 cost | 2.5 | 2 | Valid full-model forward/backward method and positive measurements; correct quadratic-score explanation. **−0.5:** only aggregate repeat statistics and one memory peak per length retained; raw timing repetitions/profiler events are absent, limiting independent assessment of variability and reconstructed peaks. |
| **Problem 2 subtotal** | **50** | **48** | |
| **Technical task subtotal** | **100** | **97** | |
| Report/code presentation deduction | — | **−1** | Crowded raster plot labels at PDF size, combined multi-figure captions, skipped Figure 3 and nonsequential presentation (4–5, 7–8 before 6). These are communication defects, not missing experiments. Discretionary deduction; official rubric does not give a separate formatting tariff. |
| **Estimated technical total** | **100** | **96** | **Bonus: 0; neither stretch experiment attempted.** |

## Findings that materially affect interpretation

### Correct mathematics and code

The implemented recurrences and attention equations are sound on inspection and testing. The recurrent count formula is g·h(d+h+1) for one bias and g·h(d+h+2) for two; at d=9,h=64 it gives 4,736/4,800, 18,944/19,200 and 14,208/14,400. The general encoder count is 12d²+13d, including biases and two LayerNorms. No forbidden framework attention or Transformer layer was found in the experimental model implementation; library oracle use in tests is permitted.

Do not mistake verification scaffolding containing placeholder *negative controls* for unfinished submitted models. Completion gates actually passed. Similarly, using library RNN/LSTM/GRU for P1 experiments is explicitly allowed.

### Results are supported, but scientific conclusions are narrow

Replayed HAR means are RNN 70.52%, LSTM 87.71%, GRU 88.19%. The report does not conceal RNN instability. Transformer HAR means are roughly 90.54–91.20%, but the validation-selected sinusoidal model, rather than the highest test mean, is the defensible main comparison.

All 36 adding runs are unsolved. At T=400 the empirical constant baseline is 0.15272, below every model mean; the lower absolute MSE at that length is not improved memory. The report correctly recognizes this. The five-epoch budget is legal and the rubric explicitly allows results outside sanity ranges. A large automatic deduction for these values would be unfair. Nevertheless, this experiment does not demonstrate successful long-memory learning by gated models, and its diagnosis remains incomplete.

The gradient probes are real derivatives, not a product-of-Jacobian surrogate. However, dL/dh_t is loss-, parameter- and trajectory-dependent; LSTM cell-state memory is a separate path. The report correctly qualifies this. Float64 probing improves visibility of tiny gradients but should not be mistaken for the float32 training computation.

The main LM remains weak at 2.23495 nats, although clearly better than ln(65)≈4.17439. The loss is still improving at epoch five. The reported no-mask loss of 0.31769 is leakage, not superior language modeling: the future input exposes the next-token target. Its generated text is 98.4% newlines. This is a particularly strong, correctly interpreted ablation.

The context experiment measures evaluation-mode forward **and backward**, using a surrogate squared-logit loss, not training-mode cross-entropy or generation latency. CPU memory means reconstructed additional live tensor allocation, not total RSS or GPU reserved memory. The report states the main distinctions correctly. Score-element counts illustrate one attention matrix's B·H·T² storage, not total memory across all layers and intermediates.

### Report, reproducibility and submission

The six-content-page limit is met: the seventh page contains the excluded declaration/references. A4 and margin evidence agree with the source's 11pt/2cm settings; raster figure text is smaller and harder to read than body text. All required figure categories and tables are present. The missing Figure 3 is a numbering defect, not evidence that a required experiment is absent.

`results.csv` has the prescribed schema and 82 experiment rows: 69 P1 and 13 P2. Width64 and default comparison runs are reused rather than double-counted. Generated samples have the requested lengths. Exact package versions are pinned. The archive opens, has the required student-ID naming/root and contains `report.pdf`; its size is well below 25 MB. Portal upload/download and receipt are not evidenced, so this review does not certify submission.

README honestly states CPU timings and that T4 time was not measured. Thus the literal requested T4-runtime item is unfulfilled; inventing a T4 estimate would be worse. No separate deduction is charged given the permitted CPU route and explicit disclosure. A fresh dependency installation and complete training replay remain unverified; the official up-to-10 reproducibility deduction is **not** imposed merely because those checks were outside this review. Historical timing values cannot be authenticated through replaying predictions.

## Academic-integrity and clarification conditions

The PDF's own declaration says Codex wrote the custom recurrent and Transformer implementations, tests, pipelines and substantial analysis/report content. The original brief permits AI explanations, debugging and plot tidying, but prohibits AI-written from-scratch parts and requires those components to be the student's own code. This is direct evidence of a conflict with the written requirement; successful tests and disclosure do not resolve it.

The files report verbal instructor permission, but do not supply instructor-authored evidence overriding that prohibition. I cannot authenticate that permission, decide an institutional misconduct case, or invent its penalty. There is no basis here to allege fabricated results or undisclosed copying from classmates/public repositories; no external similarity comparison was performed. A viva remains relevant to individual understanding and authorship.

The appropriate score scenarios are:

| Scenario | Realistic interpretation |
|---|---|
| Clarifications and AI-written scratch code explicitly accepted by instructor | **96/100 central technical estimate; 93–98 range.** |
| Original prohibition enforced and only the three directly affected scratch-component rubric rows receive zero | Those rows total 30 marks (P1.2, P2.1, P2.2): mechanically **66/100** after the same other deductions. This is an illustration, **not** a prescribed or predicted institutional penalty. Other rows may also be affected. |
| Referred under the institute's integrity policy | Mark could be withheld or the assignment rejected/zeroed if that policy permits. Neither the probability nor sanction can be determined from these files. |

Therefore, “I will realistically get 96” is too strong. “My technical evidence supports approximately 96, but eligibility is unresolved” is the defensible conclusion. Also preserve the original size/seed/example clarification: the local summary alone does not prove its authority. No numerical variant penalty is invented without authenticated controlling instructions.

## Improvements ranked by potential mark gain

| Rank | Specific action | Potential effect |
|---:|---|---|
| 1 | Obtain instructor-authored confirmation covering AI-written **scratch code**, its scope, and the submission's actual disclosed use; retain the size/seed/example clarification too. If permission is denied, follow the instructor's required remediation honestly. Do not conceal assistance or relabel AI code as independently authored. | Largest eligibility effect: potentially preserves 30 directly exposed rubric marks or avoids a wider policy consequence. Not an ordinary bonus. |
| 2 | Diagnose adding failure with a small-batch overfit check and a validation-selected longer-budget pilot at T=50/100; if adopted, rerun fair comparisons with the same revised budget for every model. Include a concrete finding distinguishing optimization failure from long-memory difficulty. | About **+1** recoverable under P1.5; strengthens central learning outcome. Solving alone does not automatically earn extra marks. |
| 3 | Explain why “no positions” still retains within-patch order, and distinguish patch-order invariance from time-step-order invariance. Add a parameter/depth/patching-controlled diagnostic if making an architectural superiority claim. | Up to **+1** under P2.3; part recoverable by clearer interpretation without retraining. |
| 4 | Enlarge graph labels at final PDF size, reduce wasted space, fix figure numbering/order, and give each panel an unambiguous caption/reference. Preserve six content pages and required evidence. | About **+1** presentation recovery. |
| 5 | Interpret specific attention links with labelled character indices; retain raw context timing repeats and profiler allocation events, and repeat memory measurements. Explain what the attention score count covers. | Up to **+1** combined under P2.5. |
| 6 | If time and permitted scope allow, implement and measure the optional KV cache, checking cached versus uncached generation agreement and timing comparable workloads. | **Up to +5 bonus**, subject to course cap/scaling rules; not currently earned. |
| 7 | Add LM seeds/longer training, hardware inference latency/energy and richer generated-text analysis. | Improves confidence and viva defense; little guaranteed ordinary-mark gain because required experiments already receive substantial credit. |

Gains overlap and are not promises. The current submission has strong technical coverage and unusually checkable evidence. Its most consequential unresolved issue is whether the declared authorship process is authorized under the assignment rules.
