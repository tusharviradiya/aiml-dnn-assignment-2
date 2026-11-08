# Decisions and assumptions

## 2026-11-08 — Task 1

- Use the existing repository root as the development/submission-content root. Create the StudentID-named outer folder during final packaging once the ID is known. Do not create a second repository.
- Keep modular functions in the notebook so the required submitted notebook is self-contained; assertions immediately follow their functions. A separate script executes the actual notebook and preserves outputs.
- Download only the assignment's official UCI HAR archive; support nested ZIP extraction and reject escaping archive paths. Cache ignored raw data locally.
- Preserve the required nine-channel order. Validate original labels 1–6 and expose labels 0–5 for later PyTorch classification.
- Use sorted unique training subjects and the exact prescribed RNG choice. Seeds 0/1/2 are provisional because the variants table is absent. This is an explicit assumption, not a claimed assigned variant.
- Fit per-channel population mean/std over training windows and timesteps only, in float64; return normalized float32 arrays. Refit per split seed. Apply identical frozen statistics to validation/test; reject constant channels.
- Copy the supplied adding generator unchanged. Keep dataset seeds 0/1/2 and sizes 10000/1000/1000 fixed for every length, independently of eventual model seeds.
- Use CPU PyTorch 2.x for Task 1: no model training or GPU is needed. Python is the available 3.14.4. Notebook tooling is infrastructure, not an additional modeling framework. Pin tested dependencies after installation.
- `results.csv` remains header-only because data validation is not a model experiment. Do not invent metrics or T4 timings.
- AI assistance implemented Task 1 at the user's request. No restricted scratch-model code is written. Disclose this assistance in the final report; the assignment's listed AI allowances are narrower than this data-pipeline assistance, so instructor acceptance is not established.
- Do not generate placeholder report/results or mark future tasks complete. Problem 2 implementation waits for instruction.

- Real archive inspection revealed a macOS metadata directory with the same dataset name. Select dataset roots by the presence of `train/y_train.txt`, rather than directory name alone.
