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
REVIEW=P2/'supplement'
ADDING_REVIEW=P1/'supplement'
import json
continued={name:json.loads((REVIEW/f'lm-{name}.json').read_text()) for name in ('h4-causal1','h1-causal1','h8-causal1','h4-causal0')}
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
    return r'\includegraphics['+settings+']{'+path+r'}\par'

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
\setlength{\parskip}{2pt}
\setlength{\emergencystretch}{1em}
\setlength{\tabcolsep}{5pt}
\setlength{\topsep}{3pt}
\renewcommand{\arraystretch}{1.08}
\newcommand{\topic}[1]{\vspace{4pt}{\large\bfseries #1}\par}
\begin{document}
\begin{center}
{\Large\bfseries DNN Programming Assignment 2}\par
Viradiya Tushar Rajeshbhai \quad Student ID: 2026aj05073\par
Chosen settings: $h=64$, $d=64$; seeds $0,1,2$.
\end{center}
\topic{Problem 1: data, verification and HAR classification}
UCI HAR uses nine channels in the prescribed order: body acceleration xyz,
body gyroscope xyz, total acceleration xyz. Shapes are $7352\times128\times9$
(training source) and $2947\times128\times9$ (test), with labels remapped 1--6 to 0--5.
The 21 training and 9 test subjects are disjoint. For each seed, NumPy's prescribed
choice holds out four training subjects; normalization uses that seed's training
portion only. Figure 1 shows class balance; constant channels are rejected.

Sizes/seeds are explicit assumptions under the missing-information clause [5].
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
s+='\n'+image('problem1/figures/report_class-balance.png',height='4cm')+'\n'
s+=r'''\par Figure 1. Class balance for all three subject splits and the test set.
\begin{center}
\begin{minipage}{.43\linewidth}\centering
'''+image('problem1/figures/report_confusion.png',height='5.2cm')+r'''
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
are 0/1/2. Solved means test MSE $<0.05$. Table 2 and Figure 3a--b show no solved
run (0/3 in every model/length group). The short budget was fixed before testing.
'''
adding=pd.read_csv(P1/'adding_summary.csv')
rows=[]
for T in (50,100,200,400):
 g=adding[adding.seq_len==T].set_index('model')
 rows.append([str(T)]+[pm(g.loc[m,'test_mse_mean'],g.loc[m,'test_mse_std'],places=4) for m in ('RNN','LSTM','GRU')]+[f'{g.iloc[0].baseline_mse:.4f}'])
s+=table('Table 2. Adding test MSE; every group solved 0/3',['T','RNN','LSTM','GRU','Constant 1'],rows)
s+=image('problem1/figures/report_adding.png',height='3.4cm')+'\nFigure 3a--b. (a) Test MSE versus length; (b) T=200 train (solid)/validation (dashed) curves.\n'
s+=r'''\vspace{-4pt}Table 3/Figure 4a retain the same 10-epoch HAR protocol; six $h=64$ runs are reused.
ID ends in 3 (odd): Table 4/Figure 4b compare initial LSTM effective forget bias 0/1 at
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
s+=image('problem1/figures/report_sweep-forget.png',height='3cm')+'\nFigure 4a--b. (a) HAR width trade-offs; (b) initial forget-bias comparison.\n'
s+=r'''\newpage
\topic{Problem 1: gradient evidence and one-page analysis}
'''+image('problem1/figures/report_gradients.png',height='4cm')+r'''
\par Figure 5. At T=100, mean batch L2 norms of actual $\partial L/\partial h_t$;
log scale, before/after training, three-seed means. A fixed independent 32-example
probe uses seed3. Float64 custom unrolls reproduce library predictions and all
recurrent parameter gradients. LSTM retains a separate cell-state graph.
'''
diagnostic_rows=[]
for kind in ('RNN','LSTM','GRU'):
    pilot=json.loads((ADDING_REVIEW/f'adding-{kind}-validation-pilot.json').read_text())
    over=json.loads((ADDING_REVIEW/f'adding-{kind}-overfit.json').read_text())
    first5=min(h['val_mse'] for h in pilot['history'][:5])
    diagnostic_rows.append([kind,f'{over["final_train32_mse"]:.3g}',f'{first5:.5f}',f'{pilot["best_val_mse"]:.5f}'])
s+=table('Table 5. T=50 diagnostic, seed0; test data never evaluated',
         ['Model','32-example train MSE','Val, 5 epochs','Val, 25 epochs'],diagnostic_rows)
analysis='\n'.join(line for line in Path('docs/problem1-analysis.md').read_text().splitlines() if not line.startswith(('#','>'))).strip()
replacements={'Figure 6':'Figure 5','Figures 4–5':'Figure 3a–b','Figure 7':'Figure 4a','Figure 8':'Figure 4b','‖':r'$\Vert$','∂':r'$\partial$','×':r'$\times$','⁻²²':r'$^{-22}$','⁻¹¹':r'$^{-11}$','⁻⁵':r'$^{-5}$','±':r'$\pm$','≈':r'$\approx$','’':"'",'–':'--','dL/dh\\_t':r'$dL/dh_t$','→':r'$\to$'}
analysis=re.sub(r'(?<=[a-zA-Z])(?=\d)',' ',analysis).replace('),', '), ').replace('0.16463/0.01327/0.00189','0.16463, 0.01327, 0.00189')
analysis=esc(analysis)
for old,new in replacements.items():analysis=analysis.replace(old,new)
analysis=re.sub(r'\bh (16|32|64|128)\b',r'$h=\1$',analysis)
analysis=analysis.replace('Float 32','Float32').replace('16.9KiB','16.9 KiB')
s+='\n'+analysis+'\n'
s+=r'''\newpage
\topic{Problem 2: scratch Transformer and HAR encoder}
Custom scaled dot-product attention computes
\[ A=\operatorname{softmax}(QK^\top/\sqrt{d_k}+M),\qquad O=AV, \]
where forbidden logits are $-\infty$. Boolean True means visible. Fully masked rows are rejected. Row-sum, shape, causality and reference tests pass. Maximum SDPA reference error is
$3.58\cdot10^{-7}$ and input-gradient error $8.88\cdot10^{-16}$.
Only tests use framework attention/Transformer implementations.

Our nonuniform three-token example uses $Q=[(1,0);(0,1);(1,1)]$,
$K=[(1,0);(0,1);(1,-1)]$, $V=[(1,0);(0,2);(3,4)]$.
Let $a=1/\sqrt2$, $E=e^a$. Scaled score rows are $(a,0,a),(0,a,-a),(a,a,0)$.
Exponentiating and normalizing gives
\[
 A=\begin{bmatrix} E/(2E+1)&1/(2E+1)&E/(2E+1)\\
 1/Z&E/Z&E^{-1}/Z\\ E/(2E+1)&E/(2E+1)&1/(2E+1)\end{bmatrix},\quad Z=1+E+E^{-1}.
\]
Each output is $(A_{i1}+3A_{i3},2A_{i2}+4A_{i3})$;
numerically $(1.6044,2.0000),(0.7041,1.7121),(0.9944,1.5933)$.
Scalar arithmetic and code agree below $10^{-5}$. The earlier uniform/masked
example and random reference tests remain in the notebook.

Biased Q/K/V/O projections split/merge heads. Blocks use pre-LayerNorm
(eps$=10^{-5}$), residuals, ReLU FFN width$4d$, dropout0.1 on FFN activation
and branch outputs. With dropout off, MHA/block reference errors are $1.80\cdot10^{-16}$ and $8.88\cdot10^{-16}$. Sinusoidal
$PE_{p,2i}=\sin(p/10000^{2i/d})$, $PE_{p,2i+1}=\cos(p/10000^{2i/d})$
matches scalar tests within $5.96\cdot10^{-8}$; backward/causality tests pass.

At our $d=64$, $d_{ff}=256$, block matrices contribute
$4(64)^2+2(64)(256)=16384+32768=49152$ weights.
Attention biases add $4(64)=256$; FFN biases $256+64=320$;
two LayerNorms add $4(64)=256$. Total $49152+256+320+256=49984$,
matching actual parameters. The general formula is $12d^2+13d$.
Two blocks, patch embedding, CLS, final norm and6-class head give105222;
learned positions add 1088. The untied 65-character LM has 108481 parameters.

Encoders in Figure6 use 8-step patches (72 values), a d64 embedding, CLS, two blocks/four heads,
then normalized CLS classification. Table6 compares nine runs with none/sinusoidal/learned positions,
using the exact P1 subjects, frozen training statistics, batch128, Adam$10^{-3}$,
clipping1 and10 epochs. Architecture, dropout and patching differ from recurrent models.
'''
phar=pd.read_csv(P2/'har_summary.csv')
rows=[]
for r in phar.itertuples(index=False):rows.append([r.model.removeprefix('HAR-Transformer-'),pm(r.acc_mean,r.acc_std,100),pm(r.f1_mean,r.f1_std,places=4),r.params,f'{r.seconds:.3f}'])
rows.append(['P1 GRU',pm(har.loc['GRU','accuracy_mean'],har.loc['GRU','accuracy_std'],100),pm(har.loc['GRU','macro_f1_mean'],har.loc['GRU','macro_f1_std'],places=4),'14790','2.279'])
s+=table('Table 6. HAR positional comparison, three seeds',['Positions/model',r'Accuracy (\%)','Macro-F1','Params','sec/epoch'],rows)
s+=image('problem2/figures/report_positions.png',height='3cm')+r'''
\par Figure 6. HAR accuracy with sample std. Mean validation F1 chooses sinusoidal
(0.9276), not learned (0.9144), despite learned's higher test mean. The selected encoder
improves accuracy by2.42 points over GRU, using7.11$\times$ the parameters.
Flattening preserves the eight ordered offsets inside each patch, even without positions.
The trained no-position probe is invariant to whole-patch reversal (max logit change
$1.91\cdot10^{-6}$), but within-patch reversal changes logits by5.52. Depth, size,
patching and dropout confound attention-specific attribution. CPU time is not energy.
\newpage
\topic{Problem 2: causal language modeling, heads and masking}
Tiny Shakespeare has1115394 characters and65 distinct characters. Sorted vocabulary uses the whole text; contiguous90/10 split gives1003854/111540
training/validation characters.
Contiguous nonoverlapping128-step next-character blocks are not shuffled; fewer
than128 trailing transitions per split are omitted. No targets cross the split boundary.
CPU uses the assignment FAQ exception: d64, two layers (rather than d128/four),
context128/four heads. All comparisons use five full epochs, batch64, seed0,
Adam$10^{-3}$, dropout0.1 and norm1 clipping. Minimum validation loss selects checkpoints; Figure7 shows continued learning.
Head/mask variants start with identical parameter values; all have108481 parameters.
'''
lm=pd.read_csv(P2/'lm_runs.csv')
rows=[]
for r in lm.itertuples(index=False):
 import json
 c=json.loads(r.notes); after=continued[f'h{c["heads"]}-causal{int(c["causal"])}'];rows.append([str(c['heads']), 'causal' if c['causal'] else 'leakage',f'{r.val_loss_nats:.5f}',f'{after["best_val_loss"]:.5f}',f'{after["bits_per_char"]:.5f}'])
s+=table('Table 7. LM validation; BPC = nats / ln 2',['Heads','Mask','5-epoch nats','Continued nats','Continued BPC'],rows)
s+=image('problem2/figures/report_lm-continued.png',height='4cm')+r'''
\par Figure 7a--c. (a) Continued validation curves; (b) selected causal losses;
(c) mask-removal training loss. Original five-epoch curves remain in the notebook. Uniform baseline is $\ln65=4.17439$ nats.
Five additional epochs improve causal validation (Table7). All variants restart Adam
because old optimizer states are absent; duration and restart effects are not isolated.
Original ablations have matched initialization; continuations start from their own
validation-selected weights under a common rule. One seed cannot establish a ranking.
Heads share the same matrix counts but store different numbers of softmax maps.

In the original five-epoch mask ablation, input $t+1$ exposes the target at $t$. Training loss falls to
0.59362 versus causal2.26579. Apparent validation0.31769 nats/0.45834 BPC is
\textbf{contaminated}, not autoregressive quality. Changing future tokens leaves the
trained causal prefix logits unchanged (max0), but changes unmasked logits by7.15354.
Its original generation exposes failure:98.4\% of its500 characters
are newlines and only4 characters are distinct (temperature0.8).

The primary LM is the continued four-head causal checkpoint (Table7), selected at
additional epoch5. Its three 500-character draws are in
\path{problem2/generated_samples.txt}:
prompt \texttt{ROMEO:\textbackslash n}, top-k20, seed700, temperatures0.2/0.8/1.5.
Table8 describes single draws, not predictive entropy.
'''
from collections import Counter
samples=json.loads((REVIEW/'continued-samples.json').read_text())
stats=[]
for sample in [x for x in samples if x['causal']]:
    counts=Counter(sample['sample']); entropy=-sum(n/500*__import__('math').log2(n/500) for n in counts.values())
    stats.append([sample['temperature'],len(counts),f'{entropy:.3f}'])
s+=table('Table 8. Continued main-model sample diversity',['Temperature','Distinct chars','Empirical entropy (bits)'],stats)
s+=r'''At0.2, ``the he''/``and the'' recur; ``halll'' shows spelling failure despite common words.
At0.8, ``That pray here you sliang'' has clause-like shape but malformed words and
no coherent continuation. At1.5, ``LRIENCUS:'' resembles a speaker cue, surrounded
by broken words such as ``caingmiely''. Increased case/punctuation variety is not
improved coherence. All three samples remain weak despite lower validation loss.
\newpage
\topic{Problem 2: attention interpretation and context scaling}
'''+image('problem2/figures/report_attention-heads.png',height='5.5cm')+r'''
\par Figure 8a--b. Five-epoch baseline layer1, heads1/2 on ``To be, or not to be.''
In Figure8, rows are queries, columns keys. Both favor current/nearby characters with different
off-diagonal patterns (mean diagonal mass0.3616/0.3736).
At query17 (b), head1 assigns0.6783 to itself and0.0460 to key3 (earlier b);
head1's query18 (e) places0.3480 on key17 (b), linking the local be pair.
For query18, head2 places0.2982 on key17 and0.1891 on the preceding space;
query17 attends0.5991 to itself and0.1213 to that space. Such weights describe
this input and do not establish semantic importance or a causal mechanism.
Future entries are exactly zero. This single sentence does not establish specialization.

Figure9 and Table9 measure baseline cost: batch8, float32, dropout off, contexts64/128/256/512.
Two warmups precede five timed forward+backward repeats; all raw times and three
independent allocation-event traces per length are retained internally; the notebook
replays matching measurements or measures a fresh run. CPU memory reconstructs
peak additional live tensor bytes from raw profiler allocation/free events, relative
to existing model/input baseline; it excludes interpreter/model weights and allocator
reservation. It is neither process RSS nor reserved GPU memory.
'''
scaling=pd.read_csv(P2/'context_scaling.csv')
s+=table('Table 9. Full-model context cost on CPU',['Context',r'Time (ms), mean $\pm$ std','Peak tensor MiB','Score elements'],[[r.context,pm(r.mean_seconds,r.std_seconds,1000,3),f'{r.peak_incremental_bytes/2**20:.3f}',r.attention_score_elements] for r in scaling.itertuples(index=False)])
s+=image('problem2/figures/report_context.png',height='4.5cm')+r'''
\par Figure 9a--b. Time and incremental tensor peak versus context; dashed line
is an anchored quadratic memory reference. With8$\times$ context, score elements
increase64$\times$, measured time28.29$\times$, tensor peak28.07$\times$.
Attention products cost$O(T^2d)$; embeddings/FFN add linear-T work, so full-model
ratios need not equal64. Short-length timing includes overhead and cache effects.
Long-context quality and T4/device latency are not evaluated.

The92 rows retain 82 baseline runs, 6 adding diagnostics and 4 LM continuations.
Both notebooks reproduce these results; cached replay is not fresh training. No bonus claimed.
\newpage
\topic{AI-use statement and references (excluded from six-page limit)}
The student reports manually implementing the final RNN, LSTM and GRU cells and
Transformer scratch components (attention, multi-head attention and encoder).
OpenAI Codex (including Codex CLI) assisted during development with earlier
AI-written from-scratch drafts, requirements review, data pipelines, training and
experiment code, tests, debugging, execution, plots, analysis/report drafting,
reproducibility audits and packaging. This review changed documentation and outputs,
not implementation code. All six components pass technical checks. Current code
matches the preserved baseline, so this review cannot independently verify the
reported manual implementation or resolve the authorship discrepancy. Earlier AI
assistance remains disclosed; policy acceptance is not established by passing tests.

[1] A. Vaswani et al. \emph{Attention Is All You Need}. 2017.
Sections 3.2.1, 3.2.2, 3.5 and Table1: attention, head projections, positions and complexity.
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
marking criteria, CPU exception and permission to state reasonable assumptions for
missing information. The referenced variant table and instructor hand example were
not supplied; chosen sizes/seeds and self-created examples are assumptions, not
verified instructor clarifications. The DOCX gives 14 November 2026, 11:59 PM IST, with an inconsistent
weekday label. Confirm the deadline on the course portal; its link is not supplied.

Reproducibility: Python3.14.4, PyTorch2.15.0+cpu and exact package pins in
requirements.txt; four CPU threads. Original P2 training-only time 10.22 min; P1 adding 25.27 min;
these exclude validation/setup and do not estimate T4 runtime. Checkpoints/raw data
are intentionally excluded from the submission and regenerated by the notebooks.
\end{document}
'''
s=s.replace('time28.29',f'time {scaling.mean_seconds.iloc[-1]/scaling.mean_seconds.iloc[0]:.2f}')
s=re.sub(r'\b(query|key|assigns|places|attends|itselfand|and|batch|float|contiguous|loss|failure:)(?=\d)',r'\1 ',s)
# Normal textual spacing; TeX math remains intact.
s=re.sub(r'\b(Table|Figure|Figures|layer|heads|head|batch|seed|context|epoch|top-k)(?=\d)',r'\1 ',s)
for a,b in {'With8':'With 8','increase64':'increase 64','time28':'time 28','peak28':'peak 28','on9':'on 9','November2026':'November 2026','The82':'The 82','The92':'The 92','all82':'all 82','plus6':'plus 6','and4':'and 4','by5.52':'by 5.52','gives1003854':'gives 1003854','preserves69':'preserves 69','and13':'and 13','all500':'all 500','at0.2':'at 0.2','At0.2':'At 0.2','At0.8':'At 0.8','At1.5':'At 1.5','parameters.22':'parameters. 22','has1115394':'has 1115394','and65':'and 65','first90':'first 90','last10':'last 10','to17':'to 17','reduces128':'reduces 128','using7.11':'using 7.11','by2.42':'by 2.42'}.items():s=s.replace(a,b)
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
