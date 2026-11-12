from pathlib import Path
import shutil,json
s=Path('.cache/improvement-p2-final')
r=json.loads((s/'gpu-runtime.json').read_text());assert r['runs']['problem2']['status']=='passed' and r['fresh_experiments']
shutil.copytree(s/'problem2','problem2',dirs_exist_ok=True)
shutil.copytree(s/'problem1/figures','problem1/figures',dirs_exist_ok=True)
for name in ('experiments','measurements'):shutil.copytree(s/'data'/name,Path('data')/name,dirs_exist_ok=True)
for name in ('results.csv','gpu-runtime.json'):shutil.copy2(s/name,name)
p=Path('README.md');t=p.read_text();start=t.index('A successful fresh run took');end=t.index('\nSettings:',start)
t=t[:start]+f'''Successful fresh notebook executions took **{sum(v['seconds'] for v in r['runs'].values())/60:.2f} minutes** total:
P1 {r['runs']['problem1']['seconds']/60:.2f}, final P2 {r['runs']['problem2']['seconds']/60:.2f} minutes. This sums independent
fresh P1 and final P2 runs; an earlier P2 inference-optimization attempt is preserved
and excluded. Includes tests, training, evaluation, plots, CPU diagnostics and cache
benchmarks; excludes setup and staged downloads. T4 timing is unmeasured; actual
local GTX1650 timings are reported.
'''+t[end:]
p.write_text(t)
print('PASS final P2 promoted, independent fresh runtime scope disclosed')
