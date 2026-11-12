"""Verify the rendered one-page README and embedded PDF fonts."""
from pathlib import Path
import subprocess
out=Path('.cache/improvement-run/README-check.pdf')
subprocess.run(['pandoc','README.md','-o',str(out),'-V','fontsize=11pt','-V','geometry:margin=2cm','-V','papersize=a4'],check=True)
info=subprocess.check_output(['pdfinfo',str(out)],text=True)
assert 'Pages:           1' in info and '(A4)' in info
fonts=subprocess.check_output(['pdffonts','report.pdf'],text=True)
assert all('yes' in line for line in fonts.splitlines()[2:])
print('PASS README renders as one A4 page at11pt/2cm; report fonts embedded')
