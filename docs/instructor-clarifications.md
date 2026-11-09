# Instructor clarifications supplied by the user

The instructor email confirms the due date as **Saturday, 14 November 2026** and changes two requirements:

1. Ignore the variants table and related FAQ. Choose one common P1 baseline hidden size, choose P2 width divisible by head count, and choose any three seeds for three-seed experiments. State h, d and seeds on the report title page and README. Recompute counts for those sizes.
2. Construct our own three-token example with small Q/K/V matrices. Show the chosen matrices, hand calculation and code agreement in the report; no external fixture is required.

Applied choices: **h=64; d=64; seeds 0,1,2**. Main attention uses four heads, with one/eight-head ablations also dividing64. The original CPU exception permits two LM layers. The original odd-ID forget-bias experiment is retained; removing the size/seed lookup does not invalidate this completed ablation.

Chosen hand example: Q=K=[[0,0],[0,0],[0,0]], V=[[1,0],[0,2],[3,4]]. Scaled scores are zero; exp(0)/(3exp(0))=1/3 for each unmasked weight. Each output is (4/3,2). Causal row outputs are (1,0),(1/2,1),(4/3,2). Independent random nonzero inputs also verify scaling and reference agreement.

AI-policy evidence: this email does not change AI authorship or disclosure rules. The original brief prohibits AI-written from-scratch code and requires disclosure of every AI use. Earlier the user reported full AI permission. During the final audit the user reported verbal permission from Samsir and an instruction not to mention AI assistance in the parts originally designated manual. No instructor-authored evidence resolving this conflict has been supplied. The declaration accurately retains actual AI assistance, including scratch implementations. Technical correctness and disclosure do not independently establish authorization. No claim of proven misconduct or confirmed exemption is made.
