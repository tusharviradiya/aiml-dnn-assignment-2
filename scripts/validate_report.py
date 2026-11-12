"""Validate the current GPU report and its measured evidence."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("validate_gpu_submission.py")), run_name="__main__")
