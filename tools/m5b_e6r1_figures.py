"""Publication figures from fresh numerical sources; all curves are unmeasured."""
import os,json
os.environ.setdefault('MPLCONFIGDIR','/tmp/m5b-e6-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from m5b_e6r1_common import *
from m5b_e6r1_thermal import waveform
from m5b_e6r1_electrical import shaped_envelope,spectrum
from m5b_e6_thermal import NAMES

def finish(fig,name):
    fig.get_layout_engine().set(rect=(0,.055,1,.945))
    fig.text(.5,.008,'Calculated sensitivity only · physical qualification NOT_RUN',ha='center',fontsize=8)
    fig.savefig(OUT/(name+'.pdf'),metadata={'CreationDate':None,'ModDate':None})
    fig.savefig(OUT/(name+'.png'),dpi=140)
    plt.close(fig)

def main():
    guard();plt.rcParams.update({'font.size':10,'axes.grid':True})
    t=np.arange(0,2.8,1/50000)
    env=shaped_envelope(t,.008,slot=2.8,periodic=True)
    logical=shaped_envelope(t,0,slot=2.8,periodic=True)
    fig,axes=plt.subplots(2,1,figsize=(10,6),layout='constrained')
    # Envelope bounds, not a fictitious 144MHz time-domain RF simulation.
    for ax,key,label in [(axes[0],np.ones(len(t)),'A: carrier retained in SPACE'),(axes[1],env,'C: shaped, modulated carrier')]:
        depth=.8*logical if ax is axes[0] else .8*np.ones(len(t))
        ax.fill_between(t,key*(1-depth),key*(1+depth),alpha=.45)
        ax.set(ylabel='RF voltage envelope / relative',title=label,xlim=(0,2.8))
    axes[1].set_xlabel('One continuous MO word at 12 WPM / s')
    finish(fig,'01-carrier-comparison')
    fig,axes=plt.subplots(2,1,figsize=(10,6),layout='constrained')
    for ax,a in zip(axes,['A','C']):
        seq,loads,_=waveform('MO',12,2.8,2.8,'BUCK4S',1.,a,periodic_word=True)
        times=[0];series={k:[] for k in ['PA_W','pass_W','helper_W','DC_input_W']}
        for dt,s in seq:
            for k in series:series[k].append(loads[s][k])
            times.append(times[-1]+dt)
        for k,v in series.items():ax.stairs(v,times,label=k)
        ax.set(title=f'{a}: 1 W ERP, BUCK4S, 800 Hz cycle-mean loads',ylabel='Power / W',xlim=(0,2.8));ax.legend(ncols=4)
    axes[1].set_xlabel('Continuous MO / s');finish(fig,'02-device-power')
    traces=json.loads((OUT/'plot-traces.json').read_text())
    for node,name,limit in [('PA_junction','03-PA-junction',110),('pass_case','04-pass-case',60)]:
        fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
        for ax,mode in zip(axes,['Classic','Sprint']):
            for z in traces:
                if z['mode']!=mode:continue
                v=z['trace'];ax.plot([r[0] for r in v],[r[NAMES.index(node)+2] for r in v],label=z['architecture'])
            ax.axhline(limit,color='red',ls='--',label=f'{limit}°C criterion')
            ax.set(title=mode+' periodic cycle, 1 W ERP, 40°C',xlabel='Time / s',ylabel=node+' / °C');ax.legend()
        finish(fig,name)
    fig,ax=plt.subplots(figsize=(10,4.5),layout='constrained')
    for z in traces:
        if z['mode']!='MO':continue
        for node,style in [('PA_junction','-'),('pass_case','--')]:
            ax.plot([r[0] for r in z['trace']],[r[NAMES.index(node)+2] for r in z['trace']],style,label=z['architecture']+' '+node)
    ax.axhline(60,color='red',ls=':',label='Q401 case limit');ax.set(title='Continuous 1 W ERP MO, 40°C, same restricted SK81 boundary',xlabel='One periodic word / s',ylabel='Temperature / °C');ax.legend(ncols=2)
    finish(fig,'05-continuous-MO')
    cases=json.loads((OUT/'sensor-fault-results.json').read_text())['cases']
    fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
    for joint in [1,5,10]:
        rows=sorted([r for r in cases if abs(r['source_to_bar_K_W']-11.846896331207134)<1e-7 and r['capacity_scale']==.1 and r['threshold_C']==87 and r['mode']=='stuck_HIGH' and r['source_solder_K_W']==joint],key=lambda r:r['tau_s'])
        ax.semilogx([r['tau_s'] for r in rows],[r['peak_junction_upper_C'] for r in rows],'o-',label=f'Solder/source joint {joint} K/W')
    ax.axhline(125,color='red',ls='--',label='125°C PA ceiling');ax.set(title='Source-region sensor fault test: fast local C, 87°C trip budget',xlabel='Assumed installed observer time constant / s',ylabel='PA upper estimate before interruption / °C');ax.legend()
    finish(fig,'06-local-fault-sensitivity')
    cool=json.loads((OUT/'cooling-comparison.json').read_text())['structures'];cost=json.loads((OUT/'cost-impact.json').read_text());d=cost['electronics_material_delta_EUR_per_unit']
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');x=np.arange(3)
    masses=[r['total_assembly_mass_g_estimate'] for r in cool]
    material=[[r['cooler_material_EUR_net_at7'][i]+d[i] for i in [0,1]] for r in cool]
    for ax,values,title,ylabel in [(axes[0],masses,'Supported assembly mass','Mass / g'),(axes[1],material,'Cooling + proposed electronics, quantity 7','EUR net / unit, estimates')]:
        mid=[sum(v)/2 for v in values];err=[(v[1]-v[0])/2 for v in values]
        ax.bar(x,mid,yerr=err,capsize=6);ax.set_xticks(x,[r['name'] for r in cool]);ax.set(title=title,ylabel=ylabel)
    finish(fig,'07-cooler-mass-cost')
    # Machine-readable basis of the spectrum panel, including feedthrough limits.
    fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
    for edge in [0,.005,.008,.012]:
        r=spectrum(edge);ax.semilogy([2000,3000,5000,10000],[r['outside_offset_power_fraction'][str(x)] for x in [2000,3000,5000,10000]],'o-',label=f'{edge*1000:g} ms full edge')
    ax.set(title='Ideal-envelope integrated far-offset energy; no RF-mask qualification',xlabel='Offset boundary / Hz',ylabel='Fraction outside ±offset');ax.legend();finish(fig,'08-ideal-keying-spectrum')
    print('8 figures exported as PDF and PNG; no native CAD render or manufacturing output')

if __name__=='__main__':main()
