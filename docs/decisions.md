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

## 2026-11-08 — Task 2 preparation

- Preserve all Task 1 source cells and append Task 2 within the same self-contained notebook. No scratch recurrent computations or parameter setup are supplied by AI; the student writes both constructor and forward.
- Use four direct parameters per custom cell with PyTorch-compatible names (without `_l0`) and two bias vectors. This makes arbitrary reference-weight copying unambiguous. Derive single-bias counts separately; custom counts must equal the two-bias totals.
- PyTorch GRU reset acts on the projected recurrent candidate including its bias. Single-bias candidate parameterization cannot in general represent two arbitrary PyTorch candidate biases. Do not sum them for equivalence.
- Reference verification uses single-layer unidirectional sequence layers, packed LSTM i/f/g/o and GRU r/z/n ordering, nonzero random initial states/biases, batch sizes 1/4, lengths 1/7, dimensions 3/5 and 9/64, seeds 13/29 and float32/float64. These verification seeds are independent of the missing experiment variant. Compare every hidden step, every LSTM cell state and the full sequence with strict max absolute error <1e-5.
- Catch only NotImplementedError for pending student work. Shape/numerical failures must fail execution. The strict completion function reruns verification and cannot accept skipped placeholders. Run All success is explicitly distinct from Task 2 completion.
- Equation references were checked against the installed PyTorch class documentation. AI assistance on interfaces/tests/explanations must be disclosed; no model experiments or results CSV changes are warranted.
