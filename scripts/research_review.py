"""Compatibility entry point: supplemental experiments now live in required notebooks.

No duplicate training implementation or hard-coded historical experiment path.
The complete notebook replays existing matching runs and trains missing runs.
"""
import argparse
import subprocess
import sys
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('stage',choices=['adding','language'])
 stage=parser.parse_args().stage
 script='scripts/execute_problem1.py' if stage=='adding' else 'scripts/execute_problem2.py'
 subprocess.run([sys.executable,script],check=True)
