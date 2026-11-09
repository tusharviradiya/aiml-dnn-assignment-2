"""Generate supplemental evidence/plots from actual selected checkpoints."""
from pathlib import Path
import json, math
import nbformat
import numpy as np
import pandas as pd
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research_review import lm_scope, OUT, CACHE


def generate_samples():
    scope=lm_scope();main=torch.load(CACHE/'lm-h4-causal1.pt',weights_only=True)
    chars=main['chars'];stoi={c:i for i,c in enumerate(chars)}
    scope.update(chars=chars,stoi=stoi)
    n=nbformat.read('problem2/problem2.ipynb',4)
    source=next(c.source for c in n.cells if c.source.startswith('def load_language'))
    exec(source,scope)
    samples=[]
    for causal in (True,False):
        saved=torch.load(CACHE/f'lm-h4-causal{int(causal)}.pt',weights_only=True)
        model=scope['CharacterTransformer'](len(chars),saved['config'])
        model.load_state_dict(saved['state_dict']);model.eval()
        for temperature in ((.2,.8,1.5) if causal else (.8,)):
            sample=scope['generate_characters'](model,'ROMEO:\n',temperature,500,20,700)
            assert len(sample)==500
            samples.append(dict(causal=causal,temperature=temperature,sample=sample,prompt='ROMEO:\n',top_k=20,seed=700))
    (OUT/'continued-samples.json').write_text(json.dumps(samples,indent=2)+'\n')
    (OUT/'continued-generated_samples.txt').write_text('\n\n'.join(f'Temperature {s["temperature"]}; causal={s["causal"]}; 500 NEW characters; prompt ROMEO:\\n; top-k20; seed700\n{s["sample"]}' for s in samples))


def figures():
    dest=OUT/'figures';dest.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':12,'axes.titlesize':12,'axes.labelsize':12,'legend.fontsize':10,
                         'xtick.labelsize':11,'ytick.labelsize':11,'savefig.dpi':220})
    def save(fig,name):
        fig.tight_layout(pad=.35);fig.savefig(dest/f'{name}.png',bbox_inches='tight');plt.close(fig)
    # Compact, readable data/setup figures at their final report widths.
    root=next(p.parent for p in Path('data/har').rglob('y_train.txt') if '__MACOSX' not in str(p))
    labels=np.loadtxt(root/'y_train.txt',dtype=int)-1
    subjects=np.loadtxt(root/'subject_train.txt',dtype=int)
    test=np.loadtxt(root.parent/'test/y_test.txt',dtype=int)-1
    fig,axes=plt.subplots(1,3,figsize=(7,1.65),sharey=True)
    for seed,ax in enumerate(axes):
        held=np.random.default_rng(seed).choice(np.unique(subjects),4,replace=False)
        valid=np.isin(subjects,held)
        for offset,data,label in ((-.25,labels[~valid],'Train'),(0,labels[valid],'Val'),(.25,test,'Test')):
            ax.bar(np.arange(6)+offset,np.bincount(data,minlength=6),width=.25,label=label)
        ax.set_xticks(range(6),['W','Up','Dn','Sit','Std','Lay'],fontsize=9)
        ax.set_title(f'Seed {seed}');ax.tick_params(axis='y',labelsize=9)
    axes[0].set_ylabel('Windows');axes[-1].legend(fontsize=7)
    save(fig,'class-balance')
    from sklearn.metrics import confusion_matrix
    preds=pd.read_csv('problem1/metrics/har_predictions.csv').query("model=='GRU' and seed==2")
    matrix=confusion_matrix(preds.true,preds.predicted)
    fig,ax=plt.subplots(figsize=(3.1,2.5));ax.imshow(matrix,cmap='Blues')
    ax.set_xticks(range(6),['W','Up','Dn','Sit','Std','Lay'],fontsize=9)
    ax.set_yticks(range(6),['W','Up','Dn','Sit','Std','Lay'],fontsize=9)
    for i in range(6):
        for j in range(6):ax.text(j,i,str(matrix[i,j]),ha='center',va='center',fontsize=9,color='white' if matrix[i,j]>300 else 'black')
    ax.set_xlabel('Predicted');ax.set_ylabel('True');save(fig,'confusion')
    gradients=pd.read_csv('problem1/metrics/hidden_gradients.csv')
    fig,axes=plt.subplots(1,2,figsize=(7,2.1),sharey=True)
    for phase,ax in zip(('before','after'),axes):
        for kind,g in gradients[gradients.phase==phase].groupby('model'):
            g=g.groupby('t').norm.mean();ax.semilogy(g.index,np.maximum(g.values,1e-300),label=kind)
        ax.set_xlabel(f'{phase.capitalize()}: time step');ax.legend(fontsize=8)
    axes[0].set_ylabel('Mean hidden-gradient norm');save(fig,'gradients')
    har=pd.read_csv('problem2/metrics/har_summary.csv')
    fig,ax=plt.subplots(figsize=(6.2,1.75));ax.errorbar(range(3),100*har.acc_mean,yerr=100*har.acc_std,fmt='o',capsize=4)
    ax.set_xticks(range(3),har.model.str.removeprefix('HAR-Transformer-'));ax.set_ylabel('HAR accuracy (%)')
    save(fig,'positions')
    # Supplemental diagnostics: a fair same-budget T50 pilot, not a new grid.
    fig,axes=plt.subplots(1,2,figsize=(7,2.1))
    for kind in ('RNN','LSTM','GRU'):
        over=json.loads((OUT/f'adding-{kind}-overfit.json').read_text())
        pilot=json.loads((OUT/f'adding-{kind}-validation-pilot.json').read_text())
        axes[0].plot([h['epoch'] for h in over['history']],[h['train32_mse'] for h in over['history']],label=kind)
        axes[1].plot([h['epoch'] for h in pilot['history']],[h['val_mse'] for h in pilot['history']],label=kind)
    for ax in axes:
        ax.axhline(.05,color='k',ls='--',lw=.7);ax.set_ylim(bottom=0);ax.set_ylabel('MSE');ax.legend()
    axes[0].set_xlabel('Updates (same 32 examples)');axes[1].set_xlabel('Epochs (validation only)')
    save(fig,'adding-diagnostics')
    # Attention: preserve actual weights, label every key/query with its index.
    saved=np.load('problem2/metrics/attention_heads.npz');weights=saved['weights'];sentence=str(saved['sentence'])
    records=[]
    for head,w in enumerate(weights):
        for query in (16,17,18):
            visible=np.argsort(w[query,:query+1])[::-1][:4]
            records.append(dict(head=head+1,query=query,character=sentence[query],links=[dict(key=int(k),character=sentence[k],weight=float(w[query,k])) for k in visible]))
    (OUT/'attention-links.json').write_text(json.dumps(records,indent=2)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(7,2.3))
    labels=[f'{i}:{c if c!=" " else "·"}' for i,c in enumerate(sentence)]
    for i,ax in enumerate(axes):
        im=ax.imshow(weights[i],vmin=0,vmax=1,cmap='viridis',aspect='auto');ax.set_xticks(range(len(sentence)),labels,rotation=90,fontsize=8.5)
        rows=[0,3,6,9,12,15,17,19]
        ax.set_yticks(rows,[labels[j] for j in rows],fontsize=8.5);ax.set_title(f'(a) Head 1' if i==0 else '(b) Head 2')
        fig.colorbar(im,ax=ax,fraction=.035,pad=.02,ticks=[0,.5,1]).ax.tick_params(labelsize=8)
        ax.set_xlabel('Key index:character');ax.set_ylabel('Query')
    save(fig,'attention-heads')
    # Final-size plots use compact panels without redundant figure titles.
    adding=pd.read_csv('problem1/metrics/adding_summary.csv')
    hist=pd.read_csv('problem1/metrics/adding_history.csv')
    fig,axes=plt.subplots(1,2,figsize=(7,2.0))
    for kind,g in adding.groupby('model'):
        g=g.sort_values('seq_len');axes[0].errorbar(g.seq_len,g.test_mse_mean,yerr=g.test_mse_std,marker='.',label=kind)
        h=hist[(hist.model==kind)&(hist.seq_len==200)].groupby('epoch')[['train_mse','val_mse']].mean()
        line=axes[1].plot(h.index,h.train_mse,label=kind)[0]
        axes[1].plot(h.index,h.val_mse,'--',color=line.get_color())
    g=adding[adding.model=='RNN'].sort_values('seq_len');axes[0].plot(g.seq_len,g.baseline_mse,'k--',label='Constant 1')
    axes[0].set_xlabel('(a) Sequence length');axes[0].set_ylabel('Test MSE');axes[0].legend(fontsize=8)
    axes[1].set_xlabel('(b) Epoch, T=200');axes[1].set_ylabel('Train/validation MSE');axes[1].legend(fontsize=8)
    save(fig,'adding')
    sweep=pd.read_csv('problem1/metrics/har_hidden_sweep_summary.csv');forget=pd.read_csv('problem1/metrics/forget_bias_summary.csv')
    fig,axes=plt.subplots(1,2,figsize=(7,1.8))
    for kind,g in sweep.groupby('model'):axes[0].errorbar(g.hidden_size,100*g.accuracy_mean,yerr=100*g.accuracy_std,marker='.',label=kind)
    axes[0].set_xlabel('(a) HAR hidden width');axes[0].set_ylabel('Accuracy (%)');axes[0].legend(fontsize=8)
    axes[1].errorbar(forget.forget_bias,forget.test_mse_mean,yerr=forget.test_mse_std,marker='o',capsize=3)
    axes[1].set_xticks([0,1]);axes[1].set_xlabel('(b) Initial forget bias');axes[1].set_ylabel('Test MSE')
    save(fig,'sweep-forget')
    scaling=pd.read_csv('problem2/metrics/context_scaling.csv')
    fig,axes=plt.subplots(1,2,figsize=(7,2.15))
    axes[0].errorbar(scaling.context,1000*scaling.mean_seconds,yerr=1000*scaling.std_seconds,marker='.',capsize=3)
    axes[0].set_ylabel('Forward + backward ms')
    axes[1].plot(scaling.context,scaling.peak_incremental_bytes/2**20,'.-',label='Measured')
    axes[1].plot(scaling.context,scaling.peak_incremental_bytes.iloc[0]*(scaling.context/64)**2/2**20,'--',label='Quadratic reference')
    axes[1].set_ylabel('Additional tensor MiB');axes[1].legend(fontsize=8)
    for i,ax in enumerate(axes):
        ax.set_xlabel('(a) Context' if i==0 else '(b) Context');ax.set_xticks(scaling.context)
    save(fig,'context')
    if (OUT/'lm-h4-causal1.json').exists():
        fig,axes=plt.subplots(1,3,figsize=(7,2.0))
        for heads in (1,4,8):
            data=json.loads((OUT/f'lm-h{heads}-causal1.json').read_text())
            axes[0].plot([5]+list(range(6,11)),[data['before']]+[r['val_loss'] for r in data['history']],label=str(heads))
        axes[0].set_xlabel('(a) Total epochs');axes[0].set_ylabel('Validation nats');axes[0].legend(title='Heads',fontsize=7)
        axes[1].bar([1,4,8],[json.loads((OUT/f'lm-h{h}-causal1.json').read_text())['best_val_loss'] for h in (1,4,8)])
        axes[1].set_xticks([1,4,8]);axes[1].set_xlabel('(b) Heads');axes[1].set_ylabel('Selected nats')
        for causal in (True,False):
            d=json.loads((OUT/f'lm-h4-causal{int(causal)}.json').read_text())
            axes[2].plot(range(6,11),[r['train_loss'] for r in d['history']],label='Causal' if causal else 'No mask')
        axes[2].set_xlabel('(c) Total epochs');axes[2].set_ylabel('Training nats');axes[2].legend(fontsize=7)
        save(fig,'lm-continued')


if __name__=='__main__':
    generate_samples();figures()
