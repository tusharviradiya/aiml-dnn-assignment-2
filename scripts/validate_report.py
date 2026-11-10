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
          'References (excluded from six-page limit)')
for page,title in zip(pages,expected):assert title in page
assert 'Viradiya Tushar Rajeshbhai' in pages[0] and '2026aj05073' in pages[0]
assert re.search(r'h\s*=\s*64', pages[0]) and re.search(r'd\s*=\s*64', pages[0])
assert re.search(r'seeds\s+0,\s*1,\s*2',pages[0])
body='\n'.join(pages[:6])
for n in range(1,10):assert f'Table {n}' in body
for n in range(1,10):
    assert re.search(rf'Figure\s+{n}(?=\D|$)',body),n
normalized=re.sub(r'(?<=\w)-\n\s*(?=\w)','',body)
for label in ('Figure','Table'):
    for number in range(1,10):
        assert len(re.findall(rf'{label}\s+{number}(?=\D|$)',normalized))>=2,(label,number)
# Every numbered item has both a caption and a prose reference or explicit
# explanation adjoining it; final visual inspection checks panel readability.
for term in ('2.23495','2.92427','105222','108481','0.59362','0.31769','0/3','nonuniform','contaminated','0.01327','0.00189'):
    assert term in body,term
assert 'post-LN' in pages[-1]
assert 'AI-use statement' not in pages[-1]
for term in ('untied65','use8-step','32:71'):
    assert term not in body,term
assert 'primary LM' in pages[4]
assert all(str(number) in body for number in (16384,32768,49152,49984))
assert 'provisional' not in '\n'.join(pages).lower()
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
print('PASS A4/11pt/2cm margins, six content pages + one reference page; all required evidence and no overflow')

fonts=subprocess.check_output(['pdffonts','report.pdf'],text=True)
for line in fonts.splitlines()[2:]:
    if line.strip(): assert 'yes' in line, 'PDF font not embedded'
print('PASS: all PDF fonts embedded')
