"""Validate the new GPU evidence and report without CPU-result-specific constants."""
from pathlib import Path
import json,math,re,subprocess,xml.etree.ElementTree as ET
import nbformat,pandas as pd,numpy as np
columns='problem,model,seed,seq_len,test_acc,macro_f1,test_mse,params,sec_per_epoch,val_loss_nats,bits_per_char,notes'.split(',')
df=pd.read_csv('results.csv');assert list(df.columns)==columns
assert len(df)==100 and not df.duplicated(['problem','model','seed','notes']).any()
for p in ('problem1','problem2'):
 nb=nbformat.read(f'{p}/{p}.ipynb',4);nbformat.validate(nb)
 cells=[c for c in nb.cells if c.cell_type=='code']
 assert [c.execution_count for c in cells]==list(range(1,len(cells)+1))
 assert not any(o.output_type=='error' for c in cells for o in c.outputs)
 print(p,len(cells),'executed cells')
a=pd.read_csv('problem1/metrics/adding_runs.csv')
assert len(a)==36 and set(zip(a.model,a.seq_len,a.seed))=={(m,t,s) for m in ('RNN','LSTM','GRU') for t in (50,100,200,400) for s in (0,1,2)}
h=pd.read_csv('problem1/metrics/har_runs.csv');assert len(h)==9
for summary_path,runs_path,metric,summary_metric,groups in [
 ('problem1/metrics/har_summary.csv','problem1/metrics/har_runs.csv','test_acc','accuracy',['model']),
 ('problem1/metrics/adding_summary.csv','problem1/metrics/adding_runs.csv','test_mse','test_mse',['model','seq_len'])]:
 summary=pd.read_csv(summary_path).set_index(groups);raw=pd.read_csv(runs_path)
 calculated=raw.groupby(groups)[metric].agg(['mean','std'])
 np.testing.assert_allclose(summary[summary_metric+'_mean'],calculated['mean'],atol=1e-12)
 np.testing.assert_allclose(summary[summary_metric+'_std'],calculated['std'],atol=1e-12)
lm=df[df.val_loss_nats.notna()];np.testing.assert_allclose(lm.bits_per_char,lm.val_loss_nats/math.log(2),atol=1e-12)
config=json.loads(Path('problem2/metrics/config.json').read_text());assert config['lm']['d']==128 and config['lm']['layers']==4
samples=json.loads(Path('problem2/metrics/supplement/continued-samples.json').read_text())
primary=[s for s in samples if s['causal']]
assert sorted(s['temperature'] for s in primary)==[.2,.8,1.5]
assert all(len(s['sample'])==500 for s in primary)
text=Path('problem2/generated_samples.txt').read_text()
assert all(s['sample'] in text for s in primary)
runtime=json.loads(Path('gpu-runtime.json').read_text());assert '1650' in runtime['gpu']
assert all(r['status']=='passed' and r['seconds']>0 for r in runtime['runs'].values())
scaling=pd.read_csv('problem2/metrics/context_scaling.csv');assert set(scaling.context)=={64,128,256,512}
assert scaling.device.eq('cuda').all() and (scaling.peak_incremental_bytes>0).all()
for row in scaling.itertuples():
 raw=json.loads(Path(f'problem2/metrics/context_raw_{row.context}.json').read_text())
 np.testing.assert_allclose(np.mean(raw['timing_seconds']),row.mean_seconds,atol=1e-12)
 assert int(np.median([r['peak_bytes'] for r in raw['memory_trials']]))==row.peak_incremental_bytes
cache=Path('.cache/report');cache.mkdir(parents=True,exist_ok=True)
subprocess.run(['pdftotext','-layout','report.pdf',str(cache/'report.txt')],check=True)
subprocess.run(['pdftotext','-bbox','report.pdf',str(cache/'report-bbox.html')],check=True)
pages=[p for p in (cache/'report.txt').read_text().split('\f') if p.strip()]
assert len(pages)==7 and 'References' in pages[-1]
assert 'AI-use disclosure' in '\n'.join(pages[:6])
body='\n'.join(pages[:6])
assert 'Viradiya Tushar Rajeshbhai' in body and '2026aj05073' in body
for label in ('Figure','Table'):
 for i in range(1,10):assert len(re.findall(rf'{label}\s*{i}(?=\D|$)',body))>=2,(label,i)
assert 'GTX 1650' in body and 'd = 128' in body
source=Path('docs/report.tex').read_text();assert r'\documentclass[11pt,a4paper]' in source and r'\usepackage[margin=2cm]{geometry}' in source
assert 'Overfull' not in (cache/'report.log').read_text()
root=ET.parse(cache/'report-bbox.html').getroot();ns={'x':'http://www.w3.org/1999/xhtml'};margin=2/2.54*72
for page in root.findall('.//x:page',ns):
 w,h=float(page.attrib['width']),float(page.attrib['height']);assert abs(w-595.276)<.1 and abs(h-841.89)<.1
 for word in page.findall('.//x:word',ns):
  x0,x1,y0,y1=(float(word.attrib[k]) for k in ('xMin','xMax','yMin','yMax'))
  if y0>h-margin and ''.join(word.itertext()).strip().isdigit():continue
  assert x0>=margin-1 and x1<=w-margin+1 and y0>=margin-1 and y1<=h-margin+1,(word.text,x0,x1,y0,y1)
print('PASS fresh GPU evidence, samples, aggregate calculations, measured timing, report geometry and references')
# Revised protocol and inference-only bonus evidence.
ac=json.loads(Path('problem1/metrics/adding_config.json').read_text());assert ac['epochs']==50
ah=pd.read_csv('problem1/metrics/adding_history.csv');assert len(ah)==36*ac['epochs']
fc=pd.read_csv('problem1/metrics/forget_bias_history.csv');assert len(fc)==6*ac['epochs']
kv=json.loads(Path('problem2/metrics/kv_benchmark.json').read_text());assert len(kv['trials'])==8
assert kv['request']['warmups']==3 and kv['request']['repeats']==10
assert kv['max_logit_error']<=1e-5
for r in kv['trials']:
 t=np.array(r['timing_seconds']);assert len(t)==10 and (t>0).all()
 np.testing.assert_allclose([r['mean_seconds'],r['std_seconds']],[t.mean(),t.std(ddof=1)],rtol=1e-12)
bonus=df[df.notes.str.contains('kv-cache-benchmark',regex=False,na=False)]
assert len(bonus)==8 and bonus.sec_per_epoch.isna().all() and bonus.val_loss_nats.isna().all()
print('PASS revised 50-epoch coverage and eight inference-only KV benchmark rows')
assert runtime['fresh_experiments'] is True
import hashlib
for problem in ('problem1','problem2'):
 nb=nbformat.read(f'{problem}/{problem}.ipynb',4)
 actual=hashlib.sha256('\n'.join(c.source for c in nb.cells if c.cell_type=='code').encode()).hexdigest()
 assert actual==runtime['source_hashes'][problem], 'Executed source differs from measured fresh workflow'
print('PASS fresh runtime bound to submitted notebook code hashes')
