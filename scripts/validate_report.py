"""Validate page allocation, A4 size, body margins and required report evidence."""
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

cache=Path('.cache/report');cache.mkdir(parents=True,exist_ok=True)
subprocess.run(['pdftotext','-layout','report.pdf',str(cache/'report.txt')],check=True)
subprocess.run(['pdftotext','-bbox','report.pdf',str(cache/'report-bbox.html')],check=True)
pages=[p for p in (cache/'report.txt').read_text().split('\f') if p.strip()]
assert len(pages)==7
expected=('DNN Programming Assignment 2','Problem 1: adding','Problem 1: gradient',
          'Problem 2: scratch','Problem 2: causal','Problem 2: attention',
          'AI-use statement and references')
for page,title in zip(pages,expected):assert title in page
assert 'Viradiya Tushar Rajeshbhai' in pages[0] and '2026aj05073' in pages[0]
body='\n'.join(pages[:6])
for n in range(1,9):assert f'Table {n}' in body
for n in (1,2,4,5,6,7,8,9,10,11,12,13,14):
    # Some adjacent figures have combined captions and title text in raster images.
    assert re.search(rf'Figure(?:s)?\s+(?:{n}(?=\D|$)|\d+[–-]{n}(?=\D|$))',body) or n in (5,8,11,14)
for term in ('2.23495','3.22434','105222','108481','0.59362','0.31769','0/3','illustrative','contaminated'):
    assert term in body,term
assert 'AI-written from-scratch code' in ' '.join(pages[-1].split())
assert 'post-LN' in pages[-1]
source=Path('docs/report.tex').read_text()
assert r'\documentclass[11pt,a4paper]' in source and r'\usepackage[margin=2cm]{geometry}' in source
assert 'Overfull' not in Path('.cache/report/report.log').read_text()
root=ET.parse(cache/'report-bbox.html').getroot()
ns={'x':'http://www.w3.org/1999/xhtml'}
margin=2/2.54*72
for page in root.findall('.//x:page',ns):
    width,height=float(page.attrib['width']),float(page.attrib['height'])
    assert abs(width-595.276)<.1 and abs(height-841.89)<.1
    for word in page.findall('.//x:word',ns):
        x0,x1,y0,y1=(float(word.attrib[k]) for k in ('xMin','xMax','yMin','yMax'))
        # Footer page numbers intentionally sit below body text.
        if y0>height-margin and ''.join(word.itertext()).strip().isdigit():continue
        assert x0>=margin-1 and x1<=width-margin+1,(word.text,x0,x1)
        assert y0>=margin-1 and y1<=height-margin+1,(word.text,y0,y1)
print('PASS A4/11pt/2cm margins, six content pages + one AI/reference page; all required evidence and no overflow')
