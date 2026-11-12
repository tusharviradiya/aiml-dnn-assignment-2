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
 assert all(r['seconds']>0 for r in runtime['runs'].values())
assert all(runtime['runs'][p]['status']=='passed' for p in ('problem1','problem2'))
def read(p):return pd.read_csv(p)
def pm(m,s,scale=1):return f'{m*scale:.4f} $\\pm$ {s*scale:.4f}'
def table(n,title,heads,rows):
 return '\\begin{center}\\textbf{Table '+str(n)+'. '+title+'}\\par\\smallskip\n\\begin{tabular}{'+'l'*len(heads)+'}\\toprule\n'+' & '.join(heads)+r'\\\midrule'+'\n'+'\n'.join(' & '.join(map(str,row))+r'\\' for row in rows)+'\n\\bottomrule\\end{tabular}\\end{center}\n'
def fig(n,path,caption,height):
 return '\\begin{center}\\includegraphics[width=\\linewidth,height='+str(height)+'cm,keepaspectratio]{'+path+'}\\par Figure '+str(n)+'. '+caption+'\\end{center}\n'
def page(title):return '\\newpage\n\\section*{'+title+'}\n'
har=read(P1/'har_summary.csv');runs=read(P1/'har_runs.csv');adding=read(P1/'adding_summary.csv');sweep=read(P1/'har_hidden_sweep_summary.csv');forget=read(P1/'forget_bias_summary.csv')
best=har.sort_values(['validation_f1_mean','model'],ascending=[False,True]).iloc[0]
representative=runs[runs.model==best.model].sort_values(['val_macro_f1','seed'],ascending=[False,True]).iloc[0]
lm=read(P2/'lm_runs.csv');enc=read(P2/'har_summary.csv');scaling=read(P2/'context_scaling.csv')
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
normalization uses only the remaining training subjects. Figure 1 shows the splits.
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
s+=page('Problem 1: adding, width and individual ablation')
s+=r'''The prescribed adding generator uses two markers, one per half; assertions check
marker counts and exact target sums. Each length uses 10000/1000/1000 examples
with data seeds 0/1/2. All models use $h=64$, Adam $10^{-3}$, batch128,
five epochs and clipping1, with three model seeds. Validation MSE selects weights.
The theoretical constant-1 baseline is $1/6$; Table2 uses the measured baseline.
Solved means test MSE below0.05; Figure3 contains length and learning curves.
'''
rows=[]
for T in (50,100,200,400):
 g=adding[adding.seq_len==T].set_index('model')
 rows.append([T]+[pm(g.loc[m,'test_mse_mean'],g.loc[m,'test_mse_std']) for m in ('RNN','LSTM','GRU')]+['/'.join(str(int(g.loc[m,'solved'])) for m in ('RNN','LSTM','GRU'))])
s+=table(2,'Adding MSE; solved R/L/G counts out of three',['T','RNN','LSTM','GRU','Solved'],rows)
s+=fig(3,'problem1/figures/report_adding.png','Test MSE against length; T=200 train/validation curves.',2.8)
s+='The hidden-size sweep keeps the HAR budget fixed (Table3). ID ends in3, so the individual experiment compares initial LSTM forget bias0/1 at T=200 (Table4); other initial weights and shuffle seeds are paired. Figure4 shows both studies.\n'
s+=table(3,'HAR hidden-size sweep',['h','LSTM acc. (\\%)','Params','GRU acc. (\\%)','Params'],[[h,pm((g:=sweep[sweep.hidden_size==h].set_index('model')).loc['LSTM','accuracy_mean'],g.loc['LSTM','accuracy_std'],100),int(g.loc['LSTM','params']),pm(g.loc['GRU','accuracy_mean'],g.loc['GRU','accuracy_std'],100),int(g.loc['GRU','params'])] for h in (16,32,64,128)])
s+=table(4,'Forget-bias ablation, three seeds',['Bias','MSE','Solved'],[[int(r.forget_bias),pm(r.test_mse_mean,r.test_mse_std),f'{int(r.solved)}/3'] for r in forget.itertuples()])
s+=fig(4,'problem1/figures/report_sweep-forget.png','Hidden-size trade-offs and initial forget-bias comparison.',2.6)
s+=page('Problem 1: gradient evidence and one-page analysis')
s+=fig(5,'problem1/figures/report_gradients.png','Actual hidden-state gradient norms at T=100 before/after training; logarithmic scale, three-seed means.',4)
s+=r'''A fixed independent seed3 probe contains32 examples. Float64 custom unrolls
retain each hidden state and verify agreement with library predictions and parameter
gradients. LSTM retains a separate cell-state graph. Small early hidden gradients
indicate weak direct credit assignment to early states, but do not alone measure
all memory carried through an LSTM cell state. Figure5 should therefore be read
alongside the predictive evidence in Table2, not as proof that gates solve every task.
'''
grad=read(P1/'hidden_gradients.csv')
for m in ('RNN','LSTM','GRU'):
 g=grad[(grad.model==m)&(grad.phase=='after')].groupby('t').norm.mean()
 s+=f'{m}: mean post-training first/last hidden-gradient norms are ${g.iloc[0]:.2e}$/${g.iloc[-1]:.2e}$. '
s+='\n\n'
solved=int(adding.solved.sum())
s+=f'Table2 records {solved}/36 solved runs at the fixed five-epoch budget. Failure near the constant baseline indicates little useful marker-dependent prediction. It does not establish that the architecture cannot solve the task with another budget. Long sequences increase the credit-assignment distance and computation; three seeds expose instability rather than hiding failed runs.\n\n'
rows=[]
for m in ('RNN','LSTM','GRU'):
 a=json.loads((P1/'supplement'/f'adding-{m}-overfit.json').read_text());b=json.loads((P1/'supplement'/f'adding-{m}-validation-pilot.json').read_text())
 rows.append([m,f'{a["final_train32_mse"]:.5f}',f'{min(h["val_mse"] for h in b["history"][:5]):.5f}',f'{b["best_val_mse"]:.5f}'])
s+=table(5,'T=50 diagnostics on CPU; no test-set evaluation',['Model','Train32 MSE','Val,5 epochs','Val,25 epochs'],rows)
s+=r'''Table5 separates fitting32 examples from generalizing to independent validation
examples. These longer diagnostics support only a limited duration diagnosis at T=50;
they cannot be substituted for the prescribed test grid or claimed as T=400 success.
Table4 evaluates one paired initialization change rather than a new architecture.
The cell retention factor can improve the early optimization path, but its effect
must be judged from validation-selected test results and seed spread.
'''
s+=f'For a wearable prototype I would start with {best.model}, selected by the highest mean validation F1 ({best.validation_f1_mean:.4f}), then consider the smaller widths in Table3 if memory is constrained. Its mean test accuracy is {best.accuracy_mean*100:.2f} percent and it has {int(best.params)} parameters. Table1 supplies the measured training-cost trade-off; these GPU training times are not wearable inference latency or energy measurements. Deployment still needs on-device power, latency and accuracy validation.\n'
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
dropout0.1, batch128 and ten epochs under the same subject splits. Table6 and
Figure6 compare no, sinusoidal and learned positions. Recurrent baselines are in
Table1; patching, dropout and parameter counts confound architecture-only conclusions.
'''
s+=table(6,'HAR encoder, three seeds',['Position','Acc. (\\%)','Macro-F1','Params','s/epoch'],[[r.model.removeprefix('HAR-Transformer-'),pm(r.acc_mean,r.acc_std,100),pm(r.f1_mean,r.f1_std),int(r.params),f'{r.seconds:.3f}'] for r in enc.itertuples()])
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
s+=table(7,'LM validation; BPC = nats / ln2',['Heads','Mask','Base nats','Continued nats','BPC'],rows)
s+=fig(7,'problem2/figures/report_lm-continued.png','Validation learning, head ablation and mask-removal training loss.',4)
s+=r'''Uniform prediction costs $\ln65=4.17439$ nats. Table7 and Figure7 provide
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
s+=table(8,'Main-model sample diversity',['Temperature','Distinct characters','Empirical entropy'],rows)
s+='Table8 describes individual draws, not model predictive entropy. Temperature0.2 concentrates probability on likely characters;0.8 permits more variation;1.5 flattens the distribution. Higher character diversity is not evidence of coherent language. The full labelled samples are in generated\\_samples.txt.\n'
s+=page('Problem 2: attention interpretation and context scaling')
s+=fig(8,'problem2/figures/report_attention-heads.png','Baseline first-layer heads1/2 on ``To be, or not to be.'' Rows are queries, columns are keys.',4)
diag=json.loads((P2/'mask_diagnostic.json').read_text())
s+=f'The mean diagonal masses of the two heads in Figure8 are {diag["diagonal_attention_means"][0]:.4f} and {diag["diagonal_attention_means"][1]:.4f}. These quantify self-attention for this sentence; off-diagonal weights identify other accessible character positions. Future weights are zero. Different patterns in one sentence do not establish semantic specialization or causal importance.\n'
s+=table(9,'GTX 1650 full-model context benchmark',['Context','Time(ms), mean $\\pm$ std','Peak tensor MiB'],[[int(r.context),pm(r.mean_seconds,r.std_seconds,1000),f'{r.peak_incremental_bytes/2**20:.3f}'] for r in scaling.itertuples()])
s+=fig(9,'problem2/figures/report_context.png','Measured time and incremental allocated tensor memory versus context.',3.6)
s+=f'Table9/Figure9 use batch8, float32, evaluation-mode forward plus backward, two warmups and five synchronized timing repeats. CUDA peak allocated memory excludes the pre-existing model/input baseline and is not reserved memory. From64 to512 tokens, time grows {scaling.mean_seconds.iloc[-1]/scaling.mean_seconds.iloc[0]:.2f} times and additional tensor memory {scaling.peak_incremental_bytes.iloc[-1]/scaling.peak_incremental_bytes.iloc[0]:.2f} times. Attention score elements grow64 times; full-model cost need not exactly follow this ratio because projections and FFNs add linear work.\n'
minutes=sum(r['seconds'] for r in runtime['runs'].values())/60
s+=f'Execution used the local NVIDIA GTX1650, not a T4. Both complete notebook workflows took {minutes:.2f} minutes, excluding environment setup and dataset downloads; this includes tests, evaluation and plots as well as training. Some diagnostics use CPU. Local timing is a disclosed substitution for the requested T4 timing. No bonus is claimed.\n'
s+=r"""\par\textbf{AI-use disclosure.} OpenAI Codex assisted with scratch implementations,
training, testing, execution, plots, analysis and report preparation. The student
confirmed the root DOCX as the current brief permitting this assistance.
"""
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
s=s.replace('problem 1/','problem1/').replace('problem 2/','problem2/').replace('GTX 1650','GTX 1650').replace('T 4','T4')
if layout_fixture:
 s=s.replace(r'\begin{document}',r'\begin{document}\pagestyle{myheadings}\markright{LAYOUT FIXTURE ONLY --- historical CPU data; synthetic runtime}')
Path('docs/report.tex').write_text(s)
build=Path('.cache/report');build.mkdir(parents=True,exist_ok=True)
for _ in range(2):
 r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={build}','docs/report.tex'],capture_output=True,text=True)
 (build/'build-output.txt').write_text(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(r.stdout[-3000:])
shutil.copyfile(build/'report.pdf','report.pdf')
print('Built layout fixture only' if layout_fixture else 'Built GPU report from measured GTX 1650 evidence')
