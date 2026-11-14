"""Build a report from the completed local GPU experiment evidence."""
from pathlib import Path
import json, math, subprocess, shutil, sys
import numpy as np
import pandas as pd
P1=Path('problem1/metrics');P2=Path('problem2/metrics')
layout_fixture = '--layout-fixture' in sys.argv
runtime=json.loads(Path('gpu-runtime.json').read_text())
if layout_fixture:
 assert Path('FIXTURE_ONLY.txt').is_file(), 'Fixture builds require an explicitly marked fixture directory'
else:
 assert '1650' in runtime['gpu'], 'A measured GTX 1650 run is required'
 protocol=json.loads(Path('problem2/metrics/config.json').read_text())
 assert protocol['device']=='cuda' and protocol['lm']['d']==128 and protocol['lm']['layers']==4
 assert runtime.get('fresh_experiments') is True, 'Fresh-experiment provenance is required'
 assert all(r['seconds']>0 for r in runtime['runs'].values())
assert all(runtime['runs'][p]['status']=='passed' for p in ('problem1','problem2'))
def read(p):return pd.read_csv(p)
def pm(m,s,scale=1,precision=4):return f'{m*scale:.{precision}f} $\\pm$ {s*scale:.{precision}f}'
def scientific(value):
 mantissa,exponent=f'{value:.2e}'.split('e')
 return mantissa+r'\times10^{'+str(int(exponent))+'}'
def table(n,title,heads,rows):
 return '\\begin{center}\\textbf{Table '+str(n)+'. '+title+'}\\par\\smallskip\n\\begin{tabular}{'+'l'*len(heads)+'}\\toprule\n'+' & '.join(heads)+r'\\\midrule'+'\n'+'\n'.join(' & '.join(map(str,row))+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}\\end{center}\n'
def fig(n,path,caption,height):
 return '\\begin{center}\\includegraphics[width=\\linewidth,height='+str(height)+'cm,keepaspectratio]{'+path+'}\\par Figure '+str(n)+'. '+caption+'\\end{center}\n'
def page(title):return '\\newpage\n\\section*{'+title+'}\n'
har=read(P1/'har_summary.csv');runs=read(P1/'har_runs.csv');adding=read(P1/'adding_summary.csv');sweep=read(P1/'har_hidden_sweep_summary.csv');forget=read(P1/'forget_bias_summary.csv')
best=har.sort_values(['validation_f1_mean','model'],ascending=[False,True]).iloc[0]
representative=runs[runs.model==best.model].sort_values(['val_macro_f1','seed'],ascending=[False,True]).iloc[0]
lm=read(P2/'lm_runs.csv');enc=read(P2/'har_summary.csv');scaling=read(P2/'context_scaling.csv')
# Select the encoder using validation evidence, before comparing its test result.
encoder_history=read(P2/'har_history.csv')
encoder_validation=encoder_history.groupby(['position','seed']).val_f1.max().groupby('position').agg(['mean','std'])
selected_position=encoder_validation['mean'].sort_values(ascending=False).index[0]
selected_encoder=enc.set_index('model').loc['HAR-Transformer-'+selected_position]
cont={k:json.loads((P2/'supplement'/f'lm-{k}.json').read_text()) for k in ('h4-causal1','h1-causal1','h8-causal1','h4-causal0')}
s=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[margin=2cm]{geometry}
\usepackage{graphicx,booktabs,amsmath,amssymb,url}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\setlength{\tabcolsep}{4pt}\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}\Large DNN Programming Assignment 2\\\normalsize
Viradiya Tushar Rajeshbhai --- 2026aj05073\end{center}
\section*{Problem 1: data, verification and HAR classification}
UCI HAR uses the prescribed nine inertial channels, 128 steps, six activities,
7352 source-training windows and 2947 official test windows. The 21 source-training
subjects and nine test subjects are disjoint. For each seed 0/1/2, four training
subjects are selected by the prescribed NumPy choice for validation. Channel
normalization uses only the remaining training subjects. Figure 1 shows the splits;
Figure 2 shows the validation-selected confusion matrix.
All classifiers use last-state classification, $h=64$, one recurrent layer,
Adam $10^{-3}$, batch 128, ten epochs and norm-1 clipping. Validation macro-F1
selects checkpoints; reported spreads are sample standard deviations.

The scratch cells match library outputs within $10^{-5}$; assert cells also verify
backward gradients and nonzero initial states. For $g=1,4,3$ gates, the single-bias
count is $gh(d+h+1)$ and PyTorch's two-bias count is $gh(d+h+2)$.
At $d=9,h=64$, RNN/LSTM/GRU counts are 4736/18944/14208 versus
4800/19200/14400. Classifier heads add $6h+6$.
'''
s+=table(1,'HAR: three seeds; GTX 1650 training time',['Model','Acc. (\\%)','Macro-F1','Params','s/epoch'],[[r.model,pm(r.accuracy_mean,r.accuracy_std,100),pm(r.macro_f1_mean,r.macro_f1_std),int(r.params),f'{r.seconds_per_epoch_mean:.3f}'] for r in har.itertuples()])
s+=fig(1,'problem1/figures/report_class-balance.png','Class balance by subject split and official test set.',2.6)
s+=fig(2,'problem1/figures/report_confusion.png',f'Validation-selected {best.model}, seed {int(representative.seed)}, epoch {int(representative.best_epoch)}. Table 1 compares all architectures.',3.6)
s+='Table2 keeps the same HAR budget and subject splits while varying hidden width.\n'
s+=table(2,'HAR hidden-size sweep',['h','LSTM acc. (\\%)','Params','GRU acc. (\\%)','Params'],[[h,pm((g:=sweep[sweep.hidden_size==h].set_index('model')).loc['LSTM','accuracy_mean'],g.loc['LSTM','accuracy_std'],100),int(g.loc['LSTM','params']),pm(g.loc['GRU','accuracy_mean'],g.loc['GRU','accuracy_std'],100),int(g.loc['GRU','params'])] for h in (16,32,64,128)])
s+=page('Problem 1: adding, width and individual ablation')
s+=r'''The prescribed adding generator uses two markers, one per half; assertions check
marker counts and exact target sums. Each length uses 10000/1000/1000 examples
with data seeds 0/1/2. All models use $h=64$, Adam $10^{-3}$, batch128,
50 epochs and clipping1, with three model seeds. Validation MSE selects weights.
The theoretical constant-1 baseline is $1/6$; Table3 uses the measured baseline.
Solved means test MSE below0.05; Figure3 contains length and learning curves.
'''
rows=[]
for T in (50,100,200,400):
 g=adding[adding.seq_len==T].set_index('model')
 rows.append([T]+[pm(g.loc[m,'test_mse_mean'],g.loc[m,'test_mse_std'],precision=6) for m in ('RNN','LSTM','GRU')]+[f'{g.iloc[0].baseline_mse:.4f}']+['/'.join(str(int(g.loc[m,'solved'])) for m in ('RNN','LSTM','GRU'))])
s+=table(3,'Adding MSE; solved R/L/G counts out of three',['T','RNN','LSTM','GRU','Constant1','Solved'],rows)
s+=fig(3,'problem1/figures/report_adding.png','Test MSE against length; T=200 curves: solid training, dashed validation.',5.1)
s+='ID ends in3, so the required individual experiment compares initial LSTM forget bias0/1 at T=200 (Table4); other initial weights and shuffle seeds are paired. Figure4 shows this and the hidden-size study (Table2).\n'
s+=table(4,'Forget-bias ablation, three seeds',['Bias','MSE','Solved'],[[int(r.forget_bias),pm(r.test_mse_mean,r.test_mse_std,precision=6),f'{int(r.solved)}/3'] for r in forget.itertuples()])
s+=fig(4,'problem1/figures/report_sweep-forget.png','Hidden-size trade-offs and initial forget-bias comparison.',4.3)
s+=page('Problem 1: gradient evidence and one-page analysis')
s+=fig(5,'problem1/figures/report_gradients.png','Actual hidden-state gradient norms at T=100 before/after training; logarithmic scale, three-seed means.',5.8)
s+=r'''A fixed independent seed3 probe contains32 examples. Float64 custom unrolls
retain each hidden state and verify agreement with library predictions and parameter
gradients. LSTM retains a separate cell-state graph. Small early hidden gradients
indicate weak direct credit assignment to early states, but do not alone measure
all memory carried through an LSTM cell state. Figure5 should therefore be read
alongside the predictive evidence in Table3, not as proof that gates solve every task.
'''
grad=read(P1/'hidden_gradients.csv')
for m in ('RNN','LSTM','GRU'):
 g=grad[(grad.model==m)&(grad.phase=='after')].groupby('t').norm.mean()
 s+=f'{m}: mean post-training first/last hidden-gradient norms are ${scientific(g.iloc[0])}$/${scientific(g.iloc[-1])}$. '
s+='\n\n'
solved=int(adding.solved.sum())
s+=f'Table3 records {solved}/36 solved runs under a common 50-epoch budget. Validation-only T=50 pilots motivated this frozen follow-up budget after the earlier five-epoch grid solved none. Earlier test results were already observed; this is not a new untouched holdout. Validation MSE selects each checkpoint. GRU solves all lengths; LSTM becomes unstable at T=100 and stalls at T=200/400; RNN solves only one short run. This is finite-budget evidence, not architectural impossibility.\n\n'
fraw=read(P1/'forget_bias_runs.csv').pivot(index='seed',columns='forget_bias',values='test_mse')
delta=fraw[1]-fraw[0]
s+=f'Table4: neither initial forget bias solves T=200. Paired bias1-minus-bias0 MSE differences are '+', '.join(f'{v:.5f}' for v in delta)+f' (mean {delta.mean():.5f}, sample std {delta.std(ddof=1):.5f}). Negative favors bias1; no benefit is observed here. Baseline-level losses limit conclusions about forgetting or a universal ranking.\n\n'
hmap=har.set_index('model')
s+=f"Table1: GRU uses {100*(1-hmap.loc['GRU','params']/hmap.loc['LSTM','params']):.1f} percent fewer parameters than LSTM, with {100*(hmap.loc['GRU','accuracy_mean']-hmap.loc['LSTM','accuracy_mean']):.2f} percentage-point accuracy difference. Mean training seconds/epoch are {hmap.loc['RNN','seconds_per_epoch_mean']:.3f}/{hmap.loc['LSTM','seconds_per_epoch_mean']:.3f}/{hmap.loc['GRU','seconds_per_epoch_mean']:.3f} for RNN/LSTM/GRU. A smaller or faster model is useful only if its measured accuracy is acceptable.\n"
s+=f'For a wearable prototype I would start with {best.model}, selected by the highest mean validation F1 ({best.validation_f1_mean:.4f}), then consider smaller widths in Table2 if memory is constrained. Table1 supplies its accuracy, parameters and training cost; GPU training times do not measure wearable inference latency or energy. Deployment needs on-device validation.\n'
minutes=sum(r['seconds'] for r in runtime['runs'].values())/60
s+=f'Local NVIDIA GeForce GTX1650 (4 GB): independently fresh P1/final P2 workflows took {minutes:.2f} minutes before this presentation revision, including tests, training, evaluation, plots and CPU diagnostics; setup, downloads and an earlier P2 optimization attempt are excluded. Current cached verification is separate. T4 timing was not measured. The KV-cache bonus is included.\n'
s+=r"""\par\textbf{AI-use disclosure.} OpenAI Codex assisted with scratch implementations,
training, testing, execution, plots, analysis and report preparation. Claude supplied
an external review. The current assignment permits AI assistance for scratch components.
"""
s+=page('Problem 2: scratch Transformer and HAR encoder')
s+=r'''Attention is $A=\mathrm{softmax}(QK^T/\sqrt{d_k}+M)$, $O=AV$.
Assertions verify row sums, shapes, zero future weights, gradients and agreement
with PyTorch SDPA within $10^{-5}$. Framework attention/encoder layers are used
only in tests. Fully masked rows are rejected. A nonuniform hand example substitutes
for the absent instructor fixture: $Q=[(1,0);(0,1);(1,1)]$,
$K=[(1,0);(0,1);(1,-1)]$, $V=[(1,0);(0,2);(3,4)]$.
For $a=1/\sqrt2$, score rows are $(a,0,a),(0,a,-a),(a,a,0)$.
Exponentiate and divide each row by its sum; outputs are
$(1.6044,2.0000),(0.7041,1.7121),(0.9944,1.5933)$, agreeing with code.

Q/K/V/O projections reshape into heads. Pre-LayerNorm blocks use residuals,
ReLU FFN width$4d$ and dropout. Sinusoidal positions use
$PE_{p,2i}=\sin(p/10000^{2i/d})$ and cosine for odd components.
Matrix weights per block are $4d^2+2dd_{ff}$:196608 at $d=128,d_{ff}=512$.
Biases and LayerNorm add $13d=1664$, total198272, checked by summing parameters.
For the HAR encoder, $d=64$:16384+32768=49152 weights, plus832 gives49984.

TaskA uses 8-step patches, a CLS token, $d=64$, two blocks/four heads,
dropout0.1, batch128 and ten epochs under the same subject splits. Table5 and
Figure6 compare no, sinusoidal and learned positions. Recurrent baselines are in
Table1; patching, dropout and parameter counts confound architecture-only conclusions.
'''
s+=table(5,'HAR encoder, three seeds',['Position','Val F1','Test acc. (\\%)','Test F1','Params','s/epoch'],[[r.model.removeprefix('HAR-Transformer-'),f'{encoder_validation.loc[r.model.removeprefix("HAR-Transformer-"),"mean"]:.4f}',pm(r.acc_mean,r.acc_std,100),pm(r.f1_mean,r.f1_std),int(r.params),f'{r.seconds:.3f}'] for r in enc.itertuples()])
s+=f'The highest mean validation F1 ({encoder_validation.loc[selected_position,"mean"]:.4f}) selects {selected_position}, rather than choosing by test accuracy. Against the validation-selected {best.model} in Table1, it achieves {100*selected_encoder.acc_mean:.2f} versus {100*best.accuracy_mean:.2f} percent test accuracy (+{100*(selected_encoder.acc_mean-best.accuracy_mean):.2f} percentage points), using {int(selected_encoder.params)} versus {int(best.params)} parameters ({selected_encoder.params/best.params:.2f} times). Mean local training time is {selected_encoder.seconds:.3f} versus {best.seconds_per_epoch_mean:.3f} s/epoch. Patching shortens attention to17 tokens versus128 recurrent steps; size and dropout also differ, so these timings do not isolate architecture or measure energy.\n'
s+=fig(6,'problem2/figures/report_positions.png','Position ablation; error bars are sample standard deviations.',3.3)
s+=r'''Removing positions makes attention invariant to permutations of whole patches,
verified by reversing patch order. It does not remove order within each flattened
8-step patch. Thus a strong no-position result would not prove temporal order irrelevant.
Sizes/seeds are disclosed assumptions where the variant table is missing.
'''
s+=page('Problem 2: causal language model and ablations')
s+=r'''Tiny Shakespeare uses its full65-character vocabulary; the first90 percent
trains and last10 percent validates, without shuffled text. The standard GPU model
uses $d=128$, four layers, context128, four heads, batch64, dropout0.1,
Adam $10^{-3}$ and five epochs. Heads1/4/8 and mask removal have matched budgets.
Four additional five-epoch continuations reset Adam consistently from each selected
baseline. This deliberate restart protocol does not isolate duration from restart effects.
'''
rows=[]
for r in lm.itertuples():
 c=json.loads(r.notes);after=cont[f'h{c["heads"]}-causal{int(c["causal"])}']
 rows.append([c['heads'],'causal' if c['causal'] else 'unmasked',f'{r.val_loss_nats:.4f}',f'{after["best_val_loss"]:.4f}',f'{after["bits_per_char"]:.4f}'])
s+=table(6,'LM validation; BPC = nats / ln2',['Heads','Mask','Base nats','Continued nats','BPC'],rows)
s+=fig(7,'problem2/figures/report_lm-continued.png','Validation learning; head-loss difference from four heads (one seed); mask-removal training loss.',5)
s+=r'''Uniform prediction costs $\ln65=4.17439$ nats. Table6 and Figure7 provide
learning evidence; one seed does not establish a reliable head-count ranking.
Unmasked training exposes the next-character target through future input tokens:
its validation loss is contaminated and is not autoregressive quality. Causal-prefix
invariance and an unmasked counterexample are tested on the trained weights.
The primary LM is the continued four-head causal checkpoint. All samples contain
500 new characters after \texttt{ROMEO:\textbackslash n}, top-k20, sampling seed700.
'''
from collections import Counter
samples=json.loads((P2/'supplement'/'continued-samples.json').read_text())
rows=[]
for a in samples:
 if a['causal']:
  count=Counter(a['sample']);entropy=-sum(v/500*math.log2(v/500) for v in count.values())
  rows.append([a['temperature'],len(count),f'{entropy:.3f}'])
unmasked_stats=read(P2/'sample_statistics.csv').query("model=='unmasked'").iloc[0]
rows.append(['unmasked,0.8',int(unmasked_stats.distinct_characters),f'{unmasked_stats.empirical_char_entropy_bits:.3f}'])
s+=table(7,'Sample diversity: continued main model; unmasked baseline',['Temperature/model','Distinct characters','Empirical entropy'],rows)
s+=f'The baseline unmasked draw at0.8 has {100*unmasked_stats.newline_fraction:.1f} percent newlines and {100*unmasked_stats.repeated_adjacent_fraction:.1f} percent identical adjacent characters (Table7). Compare this generation evidence with its contaminated validation loss in Table6.\n'

s+="Table7 describes individual draws, not model predictive entropy. Temperature0.2 concentrates probability on likely characters; 0.8 permits more variation; 1.5 flattens the distribution. Higher character diversity is not evidence of coherent language. At0.2, repeated `shall' fragments dominate; 0.8 contains speaker-like `POMPENEy' but malformed `lannio'; 1.5 varies punctuation and case while misspelling `wildrak'. The full labelled samples are in generated\\_samples.txt.\n"
s+=page('Problem 2: attention interpretation and context scaling')
s+=fig(8,'problem2/figures/report_attention-heads.png',"Baseline first-layer heads1/2 on ``To be, or not to be.'' Rows are queries, columns are keys.",4)
diag=json.loads((P2/'mask_diagnostic.json').read_text())
s+=f'Figure8 mean diagonal weights are {diag["diagonal_attention_means"][0]:.4f} and {diag["diagonal_attention_means"][1]:.4f}. Future weights are zero; heads distribute weight differently over visible character positions. This single input does not establish semantic specialization or causal importance.\n'
s+=table(8,'GTX 1650 full-model context benchmark',['Context','Time(ms), mean $\\pm$ std','Peak tensor MiB'],[[int(r.context),pm(r.mean_seconds,r.std_seconds,1000),f'{r.peak_incremental_bytes/2**20:.3f}'] for r in scaling.itertuples()])
s+=fig(9,'problem2/figures/report_context.png','Measured time and incremental allocated tensor memory versus context.',3.3)
s+=f'Table8/Figure9: batch8/FP32, eval-mode forward plus backward, two warmups and five synchronized timings. Peak allocated tensor memory subtracts the model/input baseline. From64 to512, time grows {scaling.mean_seconds.iloc[-1]/scaling.mean_seconds.iloc[0]:.2f} times and memory {scaling.peak_incremental_bytes.iloc[-1]/scaling.peak_incremental_bytes.iloc[0]:.2f} times. Attention scores grow64 times; projections and FFNs add linear work, so full-model ratios differ.\n'
kv=json.loads((P2/'kv_benchmark.json').read_text())
krows=[]
for r in kv['trials']:
 if r['cached']:
  unc=next(a for a in kv['trials'] if not a['cached'] and a['prompt_length']==r['prompt_length'] and a['new_characters']==r['new_characters'])
  krows.append([f"{r['prompt_length']}+{r['new_characters']}",f"{unc['mean_seconds']:.3f}",f"{r['mean_seconds']:.3f}",f"{r['speedup']:.2f}"])
s+=table(9,'Bonus: total greedy generation latency on GTX1650',['Prompt+new','Uncached(s)','Cached(s)','Speed ratio'],krows)
s+='Table9 uses selected continued weights, batch1/FP32, three warmups and ten alternating paired synchronized trials, including prefill. Ratio = uncached/cached mean latency. Logits pass absolute/relative tolerances $10^{-5}$; greedy outputs match exactly. Rebuilding after window shifts preserves original positions and context. Short-prefix speed-ups do not extend to the500-character rolling case, which is slower. Raw trials are in CSV notes.\n'
s+=page('References')
s+=r'''
[1] Course assignment: DNN Programming Assignment--2, RNN, LSTM, GRU and Transformer;
current root DOCX identified by the student. Missing variant table and hand fixture
are handled as explicit assumptions under its missing-information clause.

[2] Vaswani et al., Attention Is All You Need (2017).
\url{https://arxiv.org/abs/1706.03762}. The assignment uses pre-LN, unlike the original post-LN block.

[3] UCI Human Activity Recognition Using Smartphones.
\url{https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones}.

[4] Karpathy, Tiny Shakespeare data.
\url{https://github.com/karpathy/char-rnn/tree/master/data/tinyshakespeare}.

[5] PyTorch reference documentation; recurrent and attention modules used for verification.
\url{https://pytorch.org/docs/stable/nn.html}.
\end{document}
'''
# Keep mathematical prose readable without concatenated numeric words.
import re
s=re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', s)
# Do not alter paths/URLs or commands; above prose normalization is restricted below by undoing known paths.
s=s.replace('a 4paper','a4paper').replace('problem 1/','problem1/').replace('problem 2/','problem2/').replace('GTX 1650','GTX 1650').replace('T 4','T4')
s=s.replace('2026aj 05073','2026aj05073')
if layout_fixture:
 s=s.replace(r'\begin{document}',r'\begin{document}\pagestyle{myheadings}\markright{LAYOUT FIXTURE ONLY --- historical CPU data; synthetic runtime}')
Path('docs/report.tex').write_text('\n'.join(line.rstrip() for line in s.splitlines())+'\n')
build=Path('.cache/report');build.mkdir(parents=True,exist_ok=True)
for _ in range(2):
 r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={build}','docs/report.tex'],capture_output=True,text=True)
 (build/'build-output.txt').write_text(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(r.stdout[-3000:])
shutil.copyfile(build/'report.pdf','report.pdf')
print('Built layout fixture only' if layout_fixture else 'Built GPU report from measured GTX 1650 evidence')
