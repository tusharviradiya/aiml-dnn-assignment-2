"""Build the six-page assignment report plus excluded AI-use/reference page.

Requires local pdflatex; reads measured CSVs and existing figures, never trains.
"""
from pathlib import Path
import re
import shutil
import subprocess
import pandas as pd

ROOT=Path('.')
P1=ROOT/'problem1'/'metrics'
P2=ROOT/'problem2'/'metrics'
DEST=ROOT/'docs'/'report.tex'
BUILD=ROOT/'.cache'/'report'
BUILD.mkdir(parents=True,exist_ok=True)

def esc(text):
    mapping={'&':r'\&','%':r'\%','_':r'\_','#':r'\#','$':r'\$'}
    return ''.join(mapping.get(c,c) for c in str(text))

def pm(mean,std,scale=1,places=2):
    return f'${mean*scale:.{places}f}\\pm{std*scale:.{places}f}$'

def table(caption,headers,rows,align=None):
    align=align or 'l'+'r'*(len(headers)-1)
    lines=[r'\begin{center}',r'\textbf{'+esc(caption)+r'}\par\vspace{2pt}',
           r'\begin{tabular}{'+align+r'}\toprule',' & '.join(headers)+r'\\\midrule']
    lines+=[' & '.join(map(str,row))+r'\\' for row in rows]
    lines += [r'\bottomrule\end{tabular}\end{center}']
    return '\n'.join(lines)

def image(path,width=r'\linewidth',height=None):
    settings=f'width={width}'
    if height:settings+=f',height={height},keepaspectratio'
    return r'\includegraphics['+settings+']{'+path+'}'

def pair(left,right,caption,lheight=None,rheight=None):
    return ('\\begin{center}\n\\begin{minipage}[c]{.485\\linewidth}\\centering\n'+image(left,height=lheight)+
            '\n\\end{minipage}\\hfill\\begin{minipage}[c]{.485\\linewidth}\\centering\n'+image(right,height=rheight)+
            '\n\\end{minipage}\\par\\vspace{2pt}\n'+caption+'\n\\end{center}\n')

s=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=2cm]{geometry}
\usepackage{graphicx,booktabs,amsmath,amssymb,array,url}
\usepackage{hyperref}
\hypersetup{colorlinks=true,urlcolor=blue,linkcolor=black,pdftitle={DNN Programming Assignment 2},pdfauthor={Viradiya Tushar Rajeshbhai}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{1em}
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.08}
\newcommand{\topic}[1]{\vspace{4pt}{\large\bfseries #1}\par}
\begin{document}
\begin{center}
{\Large\bfseries DNN Programming Assignment 2}\par
Viradiya Tushar Rajeshbhai \quad Student ID: 2026aj05073
\end{center}
\topic{Problem 1: data, verification and HAR classification}
UCI HAR uses nine channels in the prescribed order: body acceleration xyz,
body gyroscope xyz, total acceleration xyz. Shapes are $7352\times128\times9$
(training source) and $2947\times128\times9$ (test), with labels remapped 1--6 to 0--5.
The 21 training and 9 test subjects are disjoint. For each seed, NumPy's prescribed
choice holds out four training subjects; normalization uses that seed's training
portion only. Figure 1 shows class balance; constant channels are rejected.

The variants table is absent: $h=64$ and seeds 0/1/2 are provisional.
All recurrent classifiers use the last hidden state, one library layer, no dropout,
Adam $10^{-3}$, batch 128, 10 epochs and norm-1 clipping. Best checkpoints use
validation macro-F1 (earliest tie). All reported spread is sample std over three seeds;
timing is training-only CPU, four threads, not T4. Test data never select checkpoints.

Scratch cells use registered matrices, tanh RNN, LSTM i/f/g/o gates and GRU r/z/n
gates, including PyTorch's reset on the recurrent candidate bias. Eight forward cases
per cell cover two dtypes, two seeds and nonzero states. Maximum errors are
$1.19\cdot10^{-7}$ (RNN), $2.38\cdot10^{-7}$ (LSTM/GRU), below $10^{-5}$;
backward errors are at most $2.22\cdot10^{-16}$.
For $g=1,4,3$ gates, single-bias count is $gh(d+h+1)$; PyTorch/custom
count is $gh(d+h+2)$. At $d=9,h=64$, these are 4736/4800,
18944/19200 and 14208/14400. Classifier heads add $6h+6$ parameters.
'''
har=pd.read_csv(P1/'har_summary.csv').set_index('model')
rows=[]
for model in ('RNN','LSTM','GRU'):
 r=har.loc[model];rows.append([model,pm(r.accuracy_mean,r.accuracy_std,100),pm(r.macro_f1_mean,r.macro_f1_std,1,4),str(int(r.params)),f'{r.seconds_per_epoch_mean:.3f}'])
s+=table('Table 1. HAR recurrent comparison',['Model',r'Accuracy (\%)','Macro-F1','Parameters','sec/epoch'],rows)
s+='\n'+image('problem1/figures/har_class_balance.png',height='4cm')+'\n'
s+=r'''\par Figure 1. Class balance for all three subject splits and the test set.
\begin{center}
\begin{minipage}{.43\linewidth}\centering
'''+image('problem1/figures/har_confusion_matrix.png',height='5.2cm')+r'''
\end{minipage}\hfill\begin{minipage}{.53\linewidth}
Figure 2. Validation-selected GRU, seed 2, epoch 9. Sitting/standing account for
204 cross-errors (88+116). Mean validation macro-F1 selects GRU (0.9104),
then seed 2; it is not the highest-test-score run. Table 1 shows the strong
classification gain from gating. The custom cells are checked against library
layers; library recurrent layers are used only in permitted experiments.
\end{minipage}\end{center}
\newpage
\topic{Problem 1: adding problem, width and individual ablations}
The supplied generator is unchanged: two markers, one per half; targets equal their
marked-value sum. All $T\in\{50,100,200,400\}$ use 10000/1000/1000 train/validation/test
examples with data seeds 0/1/2. Models use $h=64$, batch128, Adam $10^{-3}$,
clipping1 and five epochs; lowest validation MSE selects a checkpoint. Model seeds
are 0/1/2. Solved means test MSE $<0.05$. Table 2 and Figures 4--5 show no solved
run (0/3 in every model/length group). The short budget was fixed before testing.
'''
adding=pd.read_csv(P1/'adding_summary.csv')
rows=[]
for T in (50,100,200,400):
 g=adding[adding.seq_len==T].set_index('model')
 rows.append([str(T)]+[pm(g.loc[m,'test_mse_mean'],g.loc[m,'test_mse_std'],places=4) for m in ('RNN','LSTM','GRU')]+[f'{g.iloc[0].baseline_mse:.4f}'])
s+=table('Table 2. Adding test MSE; every group solved 0/3',['T','RNN','LSTM','GRU','Constant 1'],rows)
s+=pair('problem1/figures/adding_mse_vs_length.png','problem1/figures/adding_curves_t200.png',
         'Figures 4--5. Test MSE versus length (left); T=200 learning curves (right).',lheight='3cm',rheight='3cm')
s+=r'''\vspace{-4pt}Table 3/Figure 7 retain the same 10-epoch HAR protocol; six $h=64$ runs are reused.
ID ends in 3 (odd): Table 4/Figure 8 compare initial LSTM effective forget bias 0/1 at
T=200, five epochs, three paired seeds; the other weights and shuffle are identical.
'''
sweep=pd.read_csv(P1/'har_hidden_sweep_summary.csv')
rows=[]
for h in (16,32,64,128):
    group=sweep[sweep.hidden_size==h].set_index('model')
    row=[str(h)]
    for model in ('LSTM','GRU'):
        r=group.loc[model]
        row += [pm(r.accuracy_mean,r.accuracy_std,100),str(int(r.params)),f'{r.sec_per_epoch:.2f}']
    rows.append(row)
s+=table('Table 3. HAR sweep: LSTM (left), GRU (right)',
         ['h',r'LSTM acc. (\%)','Params','sec',r'GRU acc. (\%)','Params','sec'],rows)

forget=pd.read_csv(P1/'forget_bias_summary.csv')
s+=table('Table 4. Initial forget-bias ablation',['Bias','Test MSE','Solved'],[[int(r.forget_bias),pm(r.test_mse_mean,r.test_mse_std,places=5),'0/3'] for r in forget.itertuples(index=False)])
s+=pair('problem1/figures/har_hidden_sweep.png','problem1/figures/forget_bias_ablation.png',
         'Figures 7--8. Width trade-offs (left); initial forget-bias comparison (right).',lheight='2.8cm',rheight='2.8cm')
s+=r'''\newpage
\topic{Problem 1: gradient evidence and one-page analysis}
'''+image('problem1/figures/hidden_gradient_norms.png',height='5cm')+r'''
\par Figure 6. At T=100, mean batch L2 norms of actual $\partial L/\partial h_t$;
log scale, before/after training, three-seed means. A fixed independent 32-example
probe uses seed3. Float64 custom unrolls reproduce library predictions and all
recurrent parameter gradients. LSTM retains a separate cell-state graph.
'''
analysis=Path('docs/problem1-analysis.md').read_text().split('\n\n',1)[1]
replacements={'Figure 6':'Figure 6','‖':r'$\Vert$','∂':r'$\partial$','×':r'$\times$','⁻²²':r'$^{-22}$','⁻¹¹':r'$^{-11}$','⁻⁵':r'$^{-5}$','±':r'$\pm$','≈':r'$\approx$','’':"'",'–':'--','dL/dh_t':r'$dL/dh_t$'}
analysis=esc(analysis)
for old,new in replacements.items():analysis=analysis.replace(old,new)
s+='\n'+analysis+'\n'
s+=r'''\newpage
\topic{Problem 2: scratch Transformer and HAR encoder}
Custom scaled dot-product attention computes
\[ A=\operatorname{softmax}(QK^\top/\sqrt{d_k}+M),\qquad O=AV, \]
where forbidden logits are $-\infty$. Boolean True means visible. Every query needs
at least one visible key; fully masked rows are rejected. Row sums, future zeros,
shapes and random output equivalence pass. Maximum SDPA reference error is
$3.58\cdot10^{-7}$ and input-gradient error $8.88\cdot10^{-16}$.
Only tests use framework attention/Transformer implementations.

For the \textbf{illustrative, not instructor-supplied} three-token check, $Q=K=0$
with width2 and $V=[(1,0),(0,2),(3,4)]$. Unmasked rows have weights $(1/3,1/3,1/3)$
and output $(4/3,2)$. Causal rows have weights $(1,0,0),(1/2,1/2,0),(1/3,1/3,1/3)$
and outputs $(1,0),(1/2,1),(4/3,2)$, verified by code. The instructor's specified fixture
is absent; the paper [1] gives the equation, not this numerical example.

Multi-head attention has separate biased Q/K/V/O projections and head reshaping.
The block uses pre-LayerNorm (eps$=10^{-5}$), residual branches, ReLU FFN width$4d$,
and dropout0.1 on activated FFN and branch outputs. Tests turn dropout off: MHA and
block errors are $1.80\cdot10^{-16}$ and $8.88\cdot10^{-16}$. Sinusoidal
$PE_{p,2i}=\sin(p/10000^{2i/d})$, $PE_{p,2i+1}=\cos(p/10000^{2i/d})$
matches scalar calculations within $5.96\cdot10^{-8}$; causal perturbation and
parameter-gradient checks pass.

Block matrix count is $4d^2+2d\,d_{ff}=12d^2$. Attention biases add$4d$, FFN biases
$5d$, and two LayerNorms $4d$: total$12d^2+13d$. At d128 this is196608+1664=198272,
matching actual parameters. At d64 it is49984. Two blocks, patch embedding, CLS,
final norm and6-class head give105222; learned positions add1088. The untied
65-character language model has108481 parameters, including embeddings/head.

Task A uses8-step patches (72 values), a d64 embedding, CLS, two blocks/four heads,
then normalized CLS classification. Nine runs compare none/sinusoidal/learned positions,
using the exact P1 subjects, frozen training statistics, batch128, Adam$10^{-3}$,
clipping1 and10 epochs. Architecture, dropout and patching differ from recurrent models.
'''
phar=pd.read_csv(P2/'har_summary.csv')
rows=[]
for r in phar.itertuples(index=False):rows.append([r.model.removeprefix('HAR-Transformer-'),pm(r.acc_mean,r.acc_std,100),pm(r.f1_mean,r.f1_std,places=4),r.params,f'{r.seconds:.3f}'])
rows.append(['P1 GRU',pm(har.loc['GRU','accuracy_mean'],har.loc['GRU','accuracy_std'],100),pm(har.loc['GRU','macro_f1_mean'],har.loc['GRU','macro_f1_std'],places=4),'14790','2.279'])
s+=table('Table 5. HAR positional comparison, three seeds',['Positions/model',r'Accuracy (\%)','Macro-F1','Params','sec/epoch'],rows)
s+=image('problem2/figures/har_positions.png',height='3.8cm')+r'''
\par Figure 9. HAR accuracy with sample std. Mean validation F1 chooses sinusoidal
(0.9276), not learned (0.9144), despite learned's higher test mean. The selected encoder
improves accuracy by2.42 points over GRU, using7.11$\times$ the parameters.
Patching reduces128 steps to17 tokens including CLS; backend time is not wearable energy.
\newpage
\topic{Problem 2: causal language modeling, heads and masking}
Tiny Shakespeare has1115394 characters and65 distinct characters. The whole-text
vocabulary is sorted; first90\% (1003854) train, last10\% (111540) validation.
Contiguous nonoverlapping128-step next-character blocks are not shuffled; fewer
than128 trailing transitions per split are omitted. No targets cross the split boundary.
CPU uses the assignment FAQ exception: d64, two layers (rather than d128/four),
context128/four heads. All comparisons use five full epochs, batch64, seed0,
Adam$10^{-3}$, dropout0.1 and norm1 clipping. Minimum validation loss selects checkpoints.
Head/mask variants start with identical parameter values; all have108481 parameters.
'''
lm=pd.read_csv(P2/'lm_runs.csv')
rows=[]
for r in lm.itertuples(index=False):
 import json
 c=json.loads(r.notes);rows.append([str(c['heads']), 'causal' if c['causal'] else 'none: leakage',f'{r.val_loss_nats:.5f}',f'{r.bits_per_char:.5f}',f'{r.sec_per_epoch:.2f}'])
s+=table('Table 6. LM validation; BPC = nats / ln 2',['Heads','Mask','Nats','BPC','sec/epoch'],rows)
s+=image('problem2/figures/lm_ablations.png',height='5cm')+r'''
\par Figures 10--12. Learning curve (left), fixed-width head ablation (middle),
and mask-removal training loss (right). Uniform baseline is $\ln65=4.17439$ nats.
Main validation loss falls2.55856 to2.23495 at epoch5 and is still improving.
The smaller CPU model/short budget plausibly explain weak results; neither effect is
isolated. The one-head run wins here, but one seed cannot establish a general ranking.
More heads retain the same matrices while storing more $T\times T$ softmax maps.

Without the mask, token t+1 exposes the target at t. Final training loss collapses to
0.59362 versus causal2.26579. Apparent validation0.31769 nats/0.45834 BPC is
\textbf{contaminated}, not autoregressive quality. Changing future tokens leaves the
trained causal prefix logits unchanged (max0), but changes unmasked logits by7.15354.
At generation the missing future targets expose the failure:98.4\% of its500 characters
are newlines and only4 characters are distinct (temperature0.8).

Three labelled500-new-character continuations are saved in generated\_samples.txt:
prompt \texttt{ROMEO:\textbackslash n}, top-k20, seed700, temperatures0.2/0.8/1.5.
Table7 describes these draws, not predictive model entropy or repeated-sample significance.
'''
stats=pd.read_csv(P2/'sample_statistics.csv').query("model=='causal'")
s+=table('Table 7. Main-model sample diversity',['Temperature','Distinct chars','Empirical entropy (bits)'],[[f'{r.temperature:.1f}',r.distinct_characters,f'{r.empirical_char_entropy_bits:.3f}'] for r in stats.itertuples(index=False)])
s+=r'''At0.2, repeated high-probability \texttt{the}/\texttt{and} fragments dominate.
At0.8, wordlike variation and speaker-like line breaks increase, but spelling remains
weak. At1.5, case/punctuation become more varied and coherence declines.
All remain weak samples; no fluent Shakespeare claim is supported.
\newpage
\topic{Problem 2: attention interpretation and context scaling}
'''+image('problem2/figures/attention_heads.png',height='6cm')+r'''
\par Figures 13a--b. Trained layer1, heads1/2 on ``To be, or not to be.''
Rows are queries and columns keys. Both favor current/nearby characters with different
off-diagonal patterns. Mean diagonal mass0.3616/0.3736; first-token mass0.0721/0.0747.
Future entries are exactly zero; first row has only one visible key. One short
character sentence does not prove syntactic specialization or causal explanation.

Measure the same causal model at batch8, float32, eval/dropout off, contexts64/128/256/512.
Two warmups precede five timed forward+backward repeats. CPU memory reconstructs
peak additional live tensor bytes from raw profiler allocation/free events, relative
to existing model/input baseline; it excludes interpreter/model weights and allocator
reservation. It is neither process RSS nor reserved GPU memory.
'''
scaling=pd.read_csv(P2/'context_scaling.csv')
s+=table('Table 8. Full-model context cost on CPU',['Context',r'Time (ms), mean $\pm$ std','Peak tensor MiB','Score elements'],[[r.context,pm(r.mean_seconds,r.std_seconds,1000,3),f'{r.peak_incremental_bytes/2**20:.3f}',r.attention_score_elements] for r in scaling.itertuples(index=False)])
s+=image('problem2/figures/context_scaling.png',height='4.5cm')+r'''
\par Figures 14a--b. Time and incremental tensor peak versus context; dashed line
is an anchored quadratic memory reference. With8$\times$ context, score elements
increase64$\times$, measured time28.29$\times$, tensor peak28.07$\times$.
Attention products cost$O(T^2d)$; embeddings/FFN add linear-T work, so full-model
ratios need not equal64. Short-length timing includes overhead and cache effects.
Long-context quality and T4/device latency are not evaluated.

All assertions pass; full notebooks execute top to bottom with outputs. Independent
checkpoint audits reproduce HAR predictions, adding errors, LM losses, samples,
gradients and selection. The82-row ledger preserves69 P1 and13 P2 runs. The instructor
hand fixture and variants table remain missing; the illustrative example and provisional
settings are disclosed. Optional bonus is not attempted. Method and evidence, rather
than reaching approximate sanity ranges, determine these conclusions.
\newpage
\topic{AI-use statement and references (excluded from six-page limit)}
OpenAI Codex was used for assignment review, project setup, data pipelines, tests,
custom RNN, LSTM, GRU and Transformer implementations, experiment pipelines,
debugging, execution, plots, result audits, analysis drafting, report generation and
submission packaging. This includes AI-written from-scratch code. The user reported
on9 November2026 that the professor permits full AI assistance, superseding the
narrower AI restriction in the supplied assignment. This is reported authorization,
not independent verification or a claim that the original document changed.
The student is responsible for reviewing the work and confirming that authorization.

No pretrained weights or external datasets were used. Reference framework layers
occur only in verification for restricted components; permitted library recurrent
layers run P1 experiments. Experimental values are measured; failed adding runs
and weak language samples are reported without fabricated success. Subject-specific
variants remain provisional because the table is absent. The user-proposed paper [1]
does not supply the missing worked numerical instructor fixture found in the brief.

[1] A. Vaswani et al. \emph{Attention Is All You Need}.2017.
Sections3.2.1,3.2.2,3.5 and Table1: attention, head projections, positions and complexity.
\url{https://arxiv.org/abs/1706.03762}.
The assignment's pre-LN requirement is followed; the original paper uses post-LN.

[2] UCI Machine Learning Repository. \emph{Human Activity Recognition Using Smartphones}.
Official nine-channel sensor windows and subject IDs.
\url{https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones}.

[3] A. Karpathy. \emph{char-rnn: Tiny Shakespeare input.txt}.
\url{https://github.com/karpathy/char-rnn/tree/master/data/tinyshakespeare}.

[4] PyTorch reference documentation and installed class documentation:
RNN, LSTM, GRU, functional scaled\_dot\_product\_attention,
MultiheadAttention and TransformerEncoderLayer (verification only).
\url{https://pytorch.org/docs/stable/nn.html}.

[5] Course assignment: \emph{DNN Programming Assignment--2: RNN, LSTM, GRU and
Transformer}, supplied DOCX. Source of dataset/split/generator instructions,
marking criteria and CPU exception. Portal link, variants table, instructor hand
fixture and final deadline confirmation were not supplied.

Reproducibility: Python3.14.4, PyTorch2.15.0+cpu and exact package pins in
requirements.txt; four CPU threads. P2 training-only time10.22min; P1 adding25.27min;
these exclude validation/setup and do not estimate T4 runtime. Checkpoints/raw data
are intentionally excluded from the submission and regenerated by the notebooks.
\end{document}
'''
# Normal textual spacing; TeX math remains intact.
s=re.sub(r'\b(Table|Figure|Figures|layer|heads|head|batch|seed|context|epoch|top-k)(?=\d)',r'\1 ',s)
for a,b in {'With8':'With 8','increase64':'increase 64','time28':'time 28','peak28':'peak 28','on9':'on 9','November2026':'November 2026','The82':'The 82','preserves69':'preserves 69','and13':'and 13','all500':'all 500','at0.2':'at 0.2','At0.2':'At 0.2','At0.8':'At 0.8','At1.5':'At 1.5','parameters.22':'parameters. 22','has1115394':'has 1115394','and65':'and 65','first90':'first 90','last10':'last 10','to17':'to 17','reduces128':'reduces 128','using7.11':'using 7.11','by2.42':'by 2.42'}.items():s=s.replace(a,b)
for a,b in {
'clipping1':'clipping 1','width2':'width 2','dropout0.1':'dropout 0.1','d128':'$d=128$',
'd64':'$d=64$','is196608':'is 196608','is49984':'is 49984','and6-class':'and 6-class',
'give105222':'give 105222','add1088':'add 1088','has108481':'has 108481','uses8-step':'uses 8-step',
'and10 epochs':'and 10 epochs','nonoverlapping128':'nonoverlapping 128','than128':'than 128',
'have108481':'have 108481','falls2.55856':'falls 2.55856','to2.23495':'to 2.23495',
'causal2.26579':'causal 2.26579','validation0.31769':'validation 0.31769','max0':'max 0',
'by7.15354':'by 7.15354','its500':'its 500','only4':'only 4','temperature0.8':'temperature 0.8',
'labelled500':'labelled 500','temperatures0.2':'temperatures 0.2','mass0.3616':'mass 0.3616',
'mass0.0721':'mass 0.0721','contexts64':'contexts 64','equal64':'equal 64','Sections3':'Sections 3',
'Python3':'Python 3','PyTorch2':'PyTorch 2','time10':'time 10','adding25':'adding 25',
'contribute4d':'contribute 4d','add$4d$':'add $4d$','total$12d':'total $12d','width$4d$':'width $4d$',
'cost$O':'cost $O','This is196608':'This is 196608'}.items():s=s.replace(a,b)
DEST.write_text(s)
for _ in range(2):
    result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={BUILD}',str(DEST)],capture_output=True,text=True)
    (BUILD/'build-output.txt').write_text(result.stdout+result.stderr)
    if result.returncode:
        raise RuntimeError('Report build failed; see .cache/report/build-output.txt\n'+result.stdout[-3500:])
shutil.copyfile(BUILD/'report.pdf',ROOT/'report.pdf')
print('Built report.pdf from measured metrics and docs/report.tex')
