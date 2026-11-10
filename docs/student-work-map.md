# Final scratch-component map

| Notebook | One-based cell | Completed component (student reports manual implementation) |
|---|---:|---|
| problem1/problem1.ipynb | 26 | MyRNNCell |
| problem1/problem1.ipynb | 29 | MyLSTMCell |
| problem1/problem1.ipynb | 32 | MyGRUCell |
| problem2/problem2.ipynb | 8 | scaled_dot_product_attention |
| problem2/problem2.ipynb | 17 | MyMultiHeadAttention |
| problem2/problem2.ipynb | 23 | MyEncoderBlock |


The student reports completing the final six scratch implementations manually.
All six definitions are present; strict reference, gradient, mask and parameter tests
pass. This review preserves scratch implementations and experiment definitions. The
P1 verification cell now calls its existing strict gate during Run All; the preserved
model-baseline comparison also passes. Consequently, technical
verification does not independently verify the reported authorship or demonstrate a
replacement of earlier AI-written drafts. Earlier AI assistance remains disclosed.
No pending implementation placeholder is asserted for these completed components.

The assignment restricts AI use to explanations, debugging and plot tidying and
requires student-authored scratch components. Earlier AI-written drafts and broader
pipeline, experiment and report assistance remain a policy concern; this review
cannot certify institutional acceptance. No informal permission or unauthenticated
instructor clarification is relied upon.

Settings h=64, d=64, seeds 0/1/2 and the self-created hand example are stated
assumptions under the DOCX missing-information clause. Its referenced variant table
and instructor fixture were not supplied. The two-layer d=64 CPU LM exception is
explicit in the DOCX. Portal deadline wording has an inconsistent weekday.

Clean dependency installation and `pip check` passed. Cached checkpoint replay
is not fresh full training. Historical optimizer/RNG states are missing; continuations reset Adam.
T4 runtime is unmeasured, leaving that README requirement unmet. Original adding
runs remain unsolved (0/36); LM comparisons are single-seed. Results are preserved.
Portal upload, downloaded-copy inspection and receipt retention are outstanding.
