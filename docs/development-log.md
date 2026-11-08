# Development log

## 2026-11-08 — P1.1 implementation (in progress)

Inspected the existing repository: only the source assignment was present, with no commits and no AGENTS.md. Created the Task 1 notebook, inline assertions, execution script, tracking documents, ignore rules and results schema. No restricted model implementations added.

Errors: an initial file-search command had an invalid argument and was corrected with a directory scan; `python` was unavailable, so Python 3 was used. Sandbox DNS blocked pip and the official dataset download; retried with explicit network approval. Dependency installation and real-data execution are pending. No commit hash exists; no commit or push performed.

## 2026-11-08 — P1.1 validation completed

Installed pinned dependencies in ignored `.venv`; Python 3.14.4 and PyTorch 2.15.0+cpu. Downloaded the official archive. The sandboxed Jupyter launch stalled before cells ran; interrupted it and executed with approved local-kernel access. The first real run found an extra `__MACOSX/UCI HAR Dataset` directory; fixed discovery to require actual training labels. The subsequent full notebook execution exited 0 and saved all outputs.

Verified shapes 7352×128×9 and 2947×128×9; all nine channel positions; labels; 21/9 non-overlapping subjects; three four-subject validation splits; training-only channel statistics; finite normalized values; constant-channel rejection; class-balance image; all 12 prescribed adding datasets; reproducibility. Split train/validation counts: seed 0 = 5886/1466, seed 1 = 5905/1447, seed 2 = 6017/1335. Constant-1 test MSE at T=50/100/200/400: 0.175392/0.169709/0.167942/0.152720. These are data baselines, not trained-model results.

Task 1 marked Completed with documented provisional seeds. Student-specific rerun remains pending the missing variant table. Results CSV remains header-only. User approved the Task 1 commit on 2026-11-08. Commit message: `feat(problem1): implement and validate Task 1 data pipelines`. No push requested or performed. The commit hash is available through `git log` after creation.
