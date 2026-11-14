# Report corrections — applied through the LaTeX builder

All changes below were applied in `scripts/build_gpu_report.py` or the notebook plot renderer, then used to rebuild `report.pdf`. No PDF binary editing or new training was used. Page numbers refer to the final seven-page PDF.

| Page | Before | Applied correction and reason |
|---|---|---|
| 1–2 | Hidden-width table occupied page 2; adding plots were small. | Move the width table to page 1 as Table 2; adding becomes Table 3. Update every reference and enlarge Figures 3–4. Width ticks now show 16/32/64/128, and length ticks show 50/100/200/400. |
| 2 | Figure 3 capped at 2.8 cm; Figure 4 at 2.6 cm. | Increase caps to 5.1 and 4.3 cm; increase legends. Preserve every plotted measurement and required T=200 curve/ablation. |
| 3 | Figure 5 capped at 4 cm; repeated prose listed solved counts already in the table. | Increase cap to 5.8 cm and replace repetition with a direct interpretation of failures by length. Retain the complete one-page analysis and AI statement. Render gradient values with scientific mathematical notation. |
| 3 | Forget-bias discussion did not explicitly state the inferential limit of both settings failing. | State: neither bias solves T=200; no benefit of bias 1 is observed under this protocol. Retain six measured runs and paired differences; do not substitute T=100 for the required T=200 experiment. |
| 3 | Runtime could be mistaken for a fresh execution of the presentation revision. | State that 96.27 minutes measures the preserved independently fresh P1/final P2 workflows before this revision. Current cached verification is separate. GTX 1650 is identified; T4 is unmeasured. |
| 4 | Encoder table had no validation-selection evidence or explicit numeric GRU comparison. | Add mean best validation F1. Select sinusoidal (0.9314), then compare 90.40% versus 88.08%, 105222 versus 14790 parameters, and 0.284 versus 1.419 s/epoch. Explain 17 patched/CLS tokens versus 128 recurrent steps, size and dropout differences. Learned positions remain reported, but their highest observed test accuracy does not select the comparison. |
| 5 | Figure 7(b) used nearly equal bars from zero. | Plot selected validation nats minus the four-head result, with a zero reference and a one-seed label. Absolute losses remain in Table 6; no significance claim is added. Enlarge Figure 7 and legends. Correct paired quotation marks around sample fragments. |
| 6 | Figure 8 sentence caption lost its closing quotation mark through Python string concatenation. | Preserve LaTeX opening/closing quotes around “To be, or not to be.” in the builder. |

Verified review claims requiring no correction:

- README already said six assessed pages including AI disclosure plus one references-only page. Only references receive the page-count exclusion.
- AI disclosure is on page 3, within the right margin. The reported page-7 overflow does not occur in this artifact; page 7 contains references only.
- The required odd-ID forget-bias experiment is T=200. A T=100 experiment would be supplementary, and the user selected no new training.
- Approximate accuracy ranges and the valid null ablation do not impose automatic mark deductions under the supplied rubric.

Companion notebook corrections: two stale five-epoch adding/forget-bias descriptions now say 50; the revised-budget chronology acknowledges that earlier test results had already been observed. Legitimate five-epoch baseline/diagnostic references are retained.

No manual report correction remains. Personal steps are to review the disclosed assumptions and AI statement, confirm the portal deadline, upload the verified ZIP, download/open that uploaded copy, and retain the confirmation. These actions have not been performed on the student's behalf.
