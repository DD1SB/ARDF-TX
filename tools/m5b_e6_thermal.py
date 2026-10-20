"""Passive coupled Cauer thermal scenarios, with exact periodic state solution.

Manufacturer steady Rjc plus bounded assumed local capacities; NOT measured Zth.
The source copper/via/interface resistance is from the existing native-ground
FVM, re-evaluated for an electrically insulating interface. No solder-fill,
plastic-top, fan or unexplained heatsink-mass bypass is permitted.
"""
import csv
import math
import os
import itertools
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh, solve
from m5b_e6_common import *
from m5b_e6_power import operating

NAMES=['PA_junction','PA_source_case','PCB_source','bar','pass_junction','pass_case',
       'helper_junction','helper_case','shared_plate','fins','NTC','PCB_bottom']
CODES=dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
 ['.-','-...','-.-.','-..','.','..-.','--.','....','..','.---','-.-','.-..','--','-.','---','.--.','--.-','.-.','...','-',
  '..-','...-','.--','-..-','-.--','--..','-----','.----','..---','...--','....-','.....','-....','--...','---..','----.']))


@lru_cache(maxsize=4)
def source_storage(plating_um,cu_um):
    import pcbnew as p
    from m5b_e4r1_common import TOP_RECTS,via_specs
    b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'))
    expected={(round(x-20,5),round(y,5)):d for x,y,d,w,kind in via_specs()}
    vias=[];uncredited=[]
    for t in b.GetTracks():
        if not isinstance(t,p.PCB_VIA) or t.GetNetname()!='GND':continue
        x,y=p.ToMM(t.GetPosition().x),p.ToMM(t.GetPosition().y)
        if 85<=x<=99 and 47<=y<=63:
            key=(round(x,5),round(y,5))
            if key not in expected:
                uncredited.append(dict(x_mm=x,y_mm=y));continue
            drill=p.ToMM(t.GetDrillValue());assert abs(drill-expected[key])<1e-6
            vias.append(dict(x_mm=x,y_mm=y,drill_mm=drill))
    assert len(vias)==98, ('native source thermal vias',len(vias))
    # Rectangles are disjoint in this manufacturer-derived source model.
    top_area=sum((r[2]-r[0])*(r[3]-r[1]) for r in TOP_RECTS)
    holes=sum(math.pi*(v['drill_mm']/2)**2 for v in vias)
    top_area-=holes;bottom_area=14*16-holes
    cp_vol=8960*385 # kg/m3 * J/kgK
    via_volume=sum(math.pi*v['drill_mm']*.001*plating_um*1e-6*.0016 for v in vias)
    return dict(via_count=len(vias),plating_um=plating_um,copper_um=cu_um,
                top_area_less_holes_mm2=top_area,bottom_area_less_holes_mm2=bottom_area,
                via_copper_J_K=via_volume*cp_vol,top_copper_J_K=top_area*1e-6*cu_um*1e-6*cp_vol,
                bottom_copper_J_K=bottom_area*1e-6*cu_um*1e-6*cp_vol,
                copper_density_kg_m3=8960,copper_cp_J_kgK=385,
                uncredited_neighbor_vias=uncredited,native_source_sha256=sha(HW/'RF2M.kicad_pcb'))


def morse(text,wpm):
    unit=1.2/wpm;out=[]
    for wi,word in enumerate(text.upper().split()):
        for ci,char in enumerate(word):
            if ci:out.append((3*unit,False))
            for i,mark in enumerate(CODES[char]):
                if i:out.append((unit,False))
                out.append((unit*(3 if mark=='-' else 1),True))
        if wi<len(text.split())-1:out.append((7*unit,False))
    out.append((7*unit,False))
    return out


def schedule(slot,cycle,code,wpm=12,callsign='DD1SB',include_id=True):
    word=code+(' '+callsign if include_id else '')
    sequence=morse(word,wpm);out=[];time=0.
    while time<slot-1e-8:
        for dt,mark in sequence:
            dt=min(dt,slot-time)
            if dt<=1e-8:break
            out.append((round(dt,9),'mark' if mark else 'space'));time+=dt
            if time>=slot-1e-8:break
    if cycle>slot:out.append((cycle-slot,'off'))
    return out


class Network:
    def __init__(self,kind='conservative',sink_R=5.5,mass_g=214,capacity_scale=1.,sensor_tau=5.,source_R=None,source_split=.6):
        fvm=json.loads((OUT/'E6-source-path-FVM.json').read_text())['cases']
        d=next(x for x in fvm if x['name']==('nominal' if kind=='nominal' else 'poor_pressure' if kind=='poor_joint' else 'conservative'))
        rsource=d['source_to_bar_K_W'] if source_R is None else source_R
        nominal=kind=='nominal'
        # Silicon .0001..0.01 J/K, case/source .001..0.1 J/K and local board
        # .003..0.3 J/K are deliberately broad physical sensitivity assumptions.
        # Aluminium mass/cp is separate and never assigned to a junction.
        storage=source_storage(d['plating_um'],d['copper_um'])
        caps=np.array([.001,.025,0,15*44*6.2/1000*2.7*.9,.003,.5,.001,.2,
                       mass_g*.9*.505,mass_g*.9*.495,.001,0])
        caps[[0,1,4,5,6,7]]*=capacity_scale
        # Known Cu/barrel storage is never scaled away with unknown package/FR4
        # capacity. Splitting the FVM path is a Cauer approximation, not a fitted
        # manufacturer Zth curve; its split fraction is explicitly exposed.
        caps[2]=storage['top_copper_J_K']+storage['via_copper_J_K']/2+.003*capacity_scale
        caps[11]=storage['bottom_copper_J_K']+storage['via_copper_J_K']/2+.05*capacity_scale
        self.C=caps;self.G=np.zeros((len(caps),len(caps)))
        self.edges=[]
        def edge(a,b,r):
            assert r>0
            g=1/r;self.G[a,a]+=g;self.G[b,b]+=g;self.G[a,b]-=g;self.G[b,a]-=g
            self.edges.append(dict(a=NAMES[a],b=NAMES[b],K_W=r))
        edge(0,1,3.)
        edge(1,2,.25 if nominal else (1.5 if kind=='poor_joint' else 1.))
        assert 0<source_split<1
        edge(2,11,source_split*rsource+(0 if nominal else 1.))
        edge(11,3,(1-source_split)*rsource)
        edge(3,8,.25 if nominal else .7)
        edge(4,5,2.5)
        edge(5,8,.6 if nominal else (2.0 if kind=='poor_joint' else 1.2))
        edge(6,7,10.)
        edge(7,8,1.2 if nominal else 2.)
        # Catalogue total sink rating is preserved: spread+fin/air sum = sink_R.
        spread=.15 if nominal else .35
        assert sink_R>spread
        edge(8,9,spread);self.G[9,9]+=1/(sink_R-spread)
        edge(5,10,sensor_tau/.001)
        self.root=np.sqrt(caps)
        self.eig,self.U=eigh(self.G/self.root[:,None]/self.root[None,:])
        assert self.eig.min()>0
        self.transition_cache={}
        self.sink_R=sink_R
        self.config=dict(kind=kind,sink_K_W=sink_R,mass_g=mass_g,capacity_scale=capacity_scale,
                         sensor_tau_s=sensor_tau,capacities_J_K=dict(zip(NAMES,caps.tolist())),
                         edges=self.edges,source_to_bar_FVM_K_W=rsource,known_Cu_via_storage=storage,
                         FVM_path_split_fraction=source_split,split_limitation='Approximate allocation of a DC FVM impedance; not a measured transient ladder')

    def transition(self,dt):
        dt=round(dt,9)
        if dt not in self.transition_cache:
            self.transition_cache[dt]=((self.U*np.exp(-self.eig*dt))@self.U.T)*self.root[None,:]/self.root[:,None]
        return self.transition_cache[dt]

    def equilibrium(self,p):return solve(self.G,p,assume_a='pos')

    def advance(self,x,p,dt):
        eq=self.equilibrium(p)
        return eq+self.transition(dt)@(x-eq)

    def response(self,p,dt):
        eq=self.equilibrium(p)
        return eq-self.transition(dt)@eq


def powers(z,coupled=.25,solar_plate_W=0.):
    q=np.zeros(len(NAMES));q[0]=z['PA_W'];q[4]=z['pass_W'];q[6]=z['helper_W']
    q[8]=z.get('other_PCB_W',0)*coupled+solar_plate_W
    return q


def run_cycle(net,sequence,loads,ambient=40.,samples=.5):
    duration=sum(x[0] for x in sequence)
    u=np.zeros(len(NAMES))
    for dt,state in sequence:u=net.advance(u,loads[state],dt)
    periodic=solve(np.eye(len(NAMES))-net.transition(duration),u)
    def trace(initial,record):
        x=initial.copy();lo=x.copy();hi=x.copy();t=0;records=[]
        for dt,state in sequence:
            eq=net.equilibrium(loads[state])
            # Local RC peaks and slower coupling are sampled independently of
            # Morse length; dt convergence is tested separately.
            points=sorted(set([dt]+[q for q in [.0001,.001,.01,.05,.1,dt/2] if 0<q<dt]+
                              list(np.arange(samples,dt,samples))))
            for a in points:
                y=eq+net.transition(float(a))@(x-eq);lo=np.minimum(lo,y);hi=np.maximum(hi,y)
                if record:records.append([round(t+a,6),state,*[float(v+ambient) for v in y]])
            x=eq+net.transition(dt)@(x-eq);t+=dt
        return x,lo,hi,records
    x0=np.zeros(len(NAMES));first_end,first_lo,first_hi,first_trace=trace(x0,True)
    end,lo,hi,period_trace=trace(periodic,True)
    assert np.max(np.abs(end-periodic))<1e-7
    hot=max(period_trace,key=lambda row:row[2])
    hot_state=np.array(hot[2:])-ambient
    shutdown=[dict(seconds=t,temperatures_C=dict(zip(NAMES,(ambient+net.transition(t)@hot_state).tolist()))) for t in [0,1,5,30,60,240,600]]
    summary=dict(first_cycle_max_C=dict(zip(NAMES,(ambient+first_hi).tolist())),
                 periodic_min_C=dict(zip(NAMES,(ambient+lo).tolist())),periodic_max_C=dict(zip(NAMES,(ambient+hi).tolist())),
                 period_s=duration,ambient_C=ambient,mean_heat_W=float(sum(dt*sum(loads[state]) for dt,state in sequence)/duration),
                 tone_fraction_of_slot=sum(dt for dt,s in sequence if s=='mark')/sum(dt for dt,s in sequence if s!='off'),
                 periodic_residual_C=float(np.max(np.abs(end-periodic))),shutdown_from_PA_hottest_sample=shutdown,
                 shutdown_cycle_position_s=hot[0])
    return summary,first_trace,period_trace


def main():
    guard();out=[];curves=[];power_cache={}
    for pop,erp,mode,code in itertools.product(['BUCK4S','BOOST2S'],[.25,.3,.5,1.],['Classic','Sprint_slow','Sprint_fast','Beacon'],['MOE','MOI','MOS','MOH','MO5']):
        if mode=='Beacon' and code!='MOE':continue
        slot,cycle,wpm=(60,300,12) if mode=='Classic' else (12,60,12) if mode=='Sprint_slow' else (12,60,20) if mode=='Sprint_fast' else (60,60,12)
        if mode=='Beacon':code='MO'
        seq=schedule(slot,cycle,code,wpm,include_id=(mode!='Beacon'))
        key=(pop,erp)
        if key not in power_cache:
            power_cache[key]=(operating(erp,pop,tone=True)['mean'],operating(erp,pop,tone=False)['mean'])
        zmark,zspace=power_cache[key]
        loads={'mark':powers(zmark),'space':powers(zspace),'off':powers(dict(PA_W=0,pass_W=0,helper_W=0,other_PCB_W=.04))}
        net=Network();summary,a,b=run_cycle(net,seq,loads)
        out.append(dict(population=pop,ERP_W=erp,mode=mode,code=code,WPM=wpm,model='conservative5.5K/W',**summary))
        if pop=='BUCK4S' and erp==1 and code in ['MO5','MO']:
            curves.append((mode,a,b))
    sensitivity=[]
    for sink,cap,mass,eta,beta,other,amb in [
        (2.2,1,214,.5,60,.25,40),(4.,1,214,.5,60,.25,40),(5.5,1,214,.5,60,.25,40),
        (8.,1,214,.5,60,1.,40),(12.,1,214,.5,60,1.,40),
        (5.5,.1,214,.5,60,.25,40),(5.5,3.,214,.5,60,.25,40),
        (5.5,1,100,.5,60,.25,40),(5.5,1,400,.5,60,.25,40),
        (5.5,1,214,.4,20,1.,40),(5.5,1,214,.45,40,.25,40),
        (5.5,1,214,.5,60,.25,25),(5.5,1,214,.5,60,.25,45),(5.5,1,214,.5,60,.25,55)]:
        for mode,slot,cycle in [('Classic',60,300),('Sprint',12,60),('Beacon',60,60),('Service_CW_30s',30,300)]:
            net=Network(sink_R=sink,capacity_scale=cap,mass_g=mass)
            z=operating(1.,eta=eta,beta=beta)['mean'];zs=operating(1.,eta=eta,beta=beta,tone=False)['mean']
            loads={'mark':powers(z,other),'space':powers(zs,other),'off':powers(dict(PA_W=0,pass_W=0,helper_W=0,other_PCB_W=.04),other)}
            seq=[(slot,'space'),(cycle-slot,'off')] if mode.startswith('Service') else schedule(slot,cycle,'MO5' if mode!='Beacon' else 'MO',include_id=False)
            summary,a,b=run_cycle(net,seq,loads,ambient=amb)
            sensitivity.append(dict(mode=mode,sink_K_W=sink,capacity_scale=cap,mass_g=mass,eta=eta,beta=beta,other_PCB_coupling=other,**summary))
    save('transient-results.json',dict(status='CALCULATED_UNVALIDATED_RC_SCENARIOS',network=Network().config,scenarios=out,sensitivities=sensitivity,
        WPM_basis='Classic12WPM; Sprint slow12/fast20 explicit analysis settings, not claimed target firmware integration or event rule requirements; PARIS1.2/WPM. MOE/I/S/H/5 plus representative DD1SB CW-ID.',
        source_impedance_basis='E6-source-path-FVM.json; actual native source geometry must remain unchanged',
        capacitance_basis='Silicon/die/case/local-copper capacities are assumptions swept0.1..3x, not manufacturer transient Zth. Aluminium900J/kgK and214g indexed mass split between base/fins.',
        AM_basis='800Hz cycle-averaged powers. Separate zero-junction-storage ripple upper bound and stress/solar/sensor scenarios are required before disposition.',
        physical='NOT_RUN'))
    fields=['population','ERP_W','mode','code','WPM','ambient_C','mean_heat_W','PA_first_C','PA_periodic_C','pass_case_C','helper_case_C','sink_C','NTC_C']
    with (OUT/'transient-summary.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
        for z in out:
            w.writerow({**{k:z[k] for k in fields[:7]},'PA_first_C':z['first_cycle_max_C']['PA_junction'],'PA_periodic_C':z['periodic_max_C']['PA_junction'],
                        'pass_case_C':z['periodic_max_C']['pass_case'],'helper_case_C':z['periodic_max_C']['helper_case'],'sink_C':z['periodic_max_C']['shared_plate'],'NTC_C':z['periodic_max_C']['NTC']})
    os.environ.setdefault('MPLCONFIGDIR','/tmp/m5b-e6-matplotlib')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(2,2,figsize=(12,7),layout='constrained')
    for mode,a,b in curves:
        k={'Classic':0,'Sprint_slow':1,'Sprint_fast':2,'Beacon':3}[mode];axis=ax.flat[k]
        data=np.array([[v[0],*v[2:]] for v in b])
        for name in ['PA_junction','pass_case','helper_case','shared_plate','NTC']:
            axis.plot(data[:,0],data[:,1+NAMES.index(name)],label=name)
        first=np.array([[v[0],*v[2:]] for v in a]);axis.plot(first[:,0],first[:,1],':',label='PA first cycle')
        axis.set(title=mode+' 1W ERP / 40°C / assumed5.5K/W',xlabel='time / s',ylabel='temperature / °C');axis.grid();axis.legend(fontsize=7)
    fig.savefig(OUT/'transient-responses.pdf');fig.savefig(OUT/'transient-responses.png',dpi=150);plt.close(fig)
    for z in out:
        if z['population']=='BUCK4S' and z['ERP_W']==1 and z['code'] in ['MO5','MO']:
            print(z['mode'],{k:round(z['periodic_max_C'][k],2) for k in ['PA_junction','pass_case','helper_case','shared_plate']})


if __name__=='__main__':main()
