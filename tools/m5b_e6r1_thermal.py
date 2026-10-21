"""Three keying waveforms on the unchanged E6 coupled thermal network."""
import functools,itertools,math
import numpy as np
from scipy.linalg import solve
from m5b_e6r1_common import *
from m5b_e6r1_morse import schedule,units
from m5b_e6r1_power import point,transition_packet,FIELDS
from m5b_e6_thermal import Network,NAMES,powers
from m5b_e6_stress import audio
from m5b_e6_power import operating

def word_period(text,wpm):return sum(n for n,m,k in units(text))*round(1200000/wpm)/1e6

def waveform(text,wpm,slot,cycle,pop,erp,architecture,edge=.008,steps=8,eta=None,absorbed=0,supply_scale=1.,beta=60.,periodic_word=False):
    if periodic_word:
        duration=word_period(text,wpm)
        assert abs(slot-duration)<1e-6 and abs(cycle-duration)<1e-6
        # Extract a middle word. Its edge ramps cross the arbitrary period
        # origin naturally, without inventing an RF shutdown every minute.
        full,loads,_=waveform(text,wpm,3*duration,3*duration,pop,erp,architecture,edge,steps,eta,absorbed,supply_scale,beta)
        seq=[];t=0.
        for dt,state in full:
            a=max(t,duration);b=min(t+dt,2*duration)
            if b>a+1e-10:seq.append((b-a,state))
            t+=dt
        energy={k:sum(dt*loads[s][k] for dt,s in seq) for k in FIELDS if k.endswith('_W')}
        assert abs(sum(dt for dt,s in seq)-duration)<1e-7
        return seq,loads,energy
    raw=schedule(text,wpm,slot,cycle);loads={};seq=[]
    def add(dt,key,z):
        if dt<1e-10:return
        loads[key]=z
        if seq and seq[-1][1]==key:seq[-1]=(seq[-1][0]+dt,key)
        else:seq.append((dt,key))
    if architecture=='A':
        for z in raw:
            key=z['state'];p=point(erp,pop,tone=key=='mark',architecture='A',eta=eta,absorbed=absorbed,supply_scale=supply_scale,beta=beta)
            if key=='off':
                p={k:0. for k in FIELDS};p['other_PCB_W']=p['DC_input_W']=p['controller_3V3_input_W']=.04
            add((z['end_us']-z['start_us'])/1e6,key,p)
    else:
        t=0.;space=point(erp,pop,alpha=0,architecture=architecture,supply_scale=supply_scale,beta=beta)
        packet=transition_packet(erp,pop,architecture,supply_scale)
        for row in raw:
            if row['state']!='mark':continue
            logical_a=row['start_us']/1e6;logical_b=row['end_us']/1e6
            a=max(0.,logical_a-edge/2);b=min(slot,logical_b+edge/2)
            assert a>=t-1e-8 and b-a>=2*edge
            add(a-t,'space',space)
            for rising in [True,False]:
                if not rising:add(b-a-2*edge,'flat',point(erp,pop,architecture=architecture,eta=eta,absorbed=absorbed,supply_scale=supply_scale,beta=beta))
                for i in range(steps):
                    x=(i+.5)/steps;alpha=.5-.5*math.cos(math.pi*x)
                    if not rising:alpha=1-alpha
                    z=point(erp,pop,alpha=round(alpha,10),architecture=architecture,eta=eta,absorbed=absorbed,supply_scale=supply_scale,beta=beta).copy()
                    # Explicit complete capacitor charge/release heat packet.
                    p=packet['pass_charge_heat_J'] if rising else 0.
                    other=packet['rise_other_heat_J'] if rising else packet['fall_other_heat_J']
                    inp=packet['rise_input_J'] if rising else 0.
                    stored=packet['storage_total_on_rise_J']*(1 if rising else -1)
                    z['pass_W']+=p/edge;z['other_PCB_W']+=other/edge
                    z['DC_input_W']+=inp/edge;z['RF_battery_input_W']+=inp/edge
                    z['storage_W']+=stored/edge
                    add(edge/steps,('rise' if rising else 'fall')+str(i),z)
            t=b
        add(slot-t,'space',space)
        off={k:0. for k in FIELDS};off['other_PCB_W']=off['DC_input_W']=off['controller_3V3_input_W']=.06
        add(cycle-slot,'off',off)
    assert abs(sum(dt for dt,k in seq)-cycle)<1e-6
    for z in loads.values():assert abs(z['DC_input_W']-sum(z[k] for k in ['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W','storage_W']))<1e-9
    energy={k:sum(dt*loads[s][k] for dt,s in seq) for k in FIELDS if k.endswith('_W')}
    assert abs(energy['DC_input_W']-sum(energy[k] for k in ['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W','storage_W']))<1e-8
    return seq,loads,energy

class Cycle:
    def __init__(self,net,loads,observer_tau=None,observer_node=2,extra_plate_W=0.):
        self.net=net;self.tau=observer_tau;self.node=observer_node
        self.loads={s:powers(z,solar_plate_W=extra_plate_W) for s,z in loads.items()};self.cache={}
        self.eqs={s:net.equilibrium(q) for s,q in self.loads.items()}
        if self.tau is not None:self.eqs={s:np.r_[q,q[self.node]] for s,q in self.eqs.items()}
    def transition(self,dt):
        f=self.net.transition(dt)
        if self.tau is None:return f
        n=self.net;decay=math.exp(-dt/self.tau);den=1-n.eig*self.tau
        weight=np.divide(np.exp(-n.eig*dt)-decay,den,out=np.full_like(den,dt/self.tau*decay),where=np.abs(den)>1e-8)
        r=(n.U[self.node,:]/n.root[self.node]*weight)@n.U.T*n.root
        out=np.zeros((13,13));out[:12,:12]=f;out[12,:12]=r;out[12,12]=decay
        return out
    def advance(self,x,state,dt):
        key=(round(dt,9),state)
        if key not in self.cache:
            f=self.transition(dt);eq=self.eqs[state];self.cache[key]=(f,eq-f@eq)
        f,u=self.cache[key];return f@x+u
    def run(self,seq,ambient=40,record=False):
        total=sum(t for t,s in seq);zero=np.zeros(len(next(iter(self.eqs.values()))));u=zero.copy()
        for dt,s in seq:u=self.advance(u,s,dt)
        start=solve(np.eye(len(zero))-self.transition(total),u)
        results=[];trace=[]
        for initial in [zero,start]:
            x=initial.copy();hi=x.copy();lo=x.copy();t=0
            for dt,s in seq:
                for a in sorted(set([dt,dt/2]+[v for v in [.0001,.001,.01,.05,.1] if v<dt]+list(np.arange(.5,dt,.5)))):
                    y=self.advance(x,s,a);hi=np.maximum(hi,y);lo=np.minimum(lo,y)
                    if record:trace.append([t+a,s,*list(y+ambient)])
                x=self.advance(x,s,dt);t+=dt
            results.append((hi+ambient,lo+ambient))
            if initial is zero:trace=[]
        residual=float(np.max(np.abs(x-start)));assert residual<1e-6
        return dict(first_max_C=dict(zip(NAMES,results[0][0][:12].tolist())),
            periodic_max_C=dict(zip(NAMES,results[1][0][:12].tolist())),periodic_min_C=dict(zip(NAMES,results[1][1][:12].tolist())),
            periodic_residual_C=residual),trace,start

@functools.lru_cache(maxsize=64)
def ripple(kind,cap,erp,pop,source_R=None):
    net=Network(kind=kind,capacity_scale=cap,source_R=source_R)
    return audio(net,operating(erp,pop,waveform=True,phases=256),256)['positive_ripple_C']['PA_junction']

def main():
    guard();rows=[];plots=[]
    for pop,erp,a,mode,code,wpm,amb in itertools.product(['BUCK4S','BOOST2S'],[.25,.5,1.],['A','B','C'],['Classic','Sprint','MO'],['MOE','MOI','MOS','MOH','MO5'],[8,10,12,15],[25,40]):
        if mode=='MO' and code!='MOE':continue
        if wpm not in [8,12,15]:continue
        if mode!='MO' and wpm!=12 and code!='MO5':continue
        if mode=='MO':code='MO'
        slot,period=(60,300) if mode=='Classic' else (12,60) if mode=='Sprint' else (word_period(code,wpm),word_period(code,wpm))
        seq,loads,energy=waveform(code,wpm,slot,period,pop,erp,a,periodic_word=(mode=='MO'))
        net=Network();out,trace,start=Cycle(net,loads).run(seq,amb,record=(pop=='BUCK4S' and erp==1 and wpm==12 and code in ['MO5','MO'] and amb==40))
        rp=ripple('conservative',1.,erp,pop)
        peak=out['periodic_max_C']['PA_junction']+rp
        rows.append(dict(population=pop,ERP_W=erp,architecture=a,mode=mode,code=code,WPM=wpm,ambient_C=amb,cycle_s=period,
            energy_J=energy,AM_ripple_positive_C=rp,PA_peak_with_AM_C=peak,
            meets_operating_limits=peak<=110 and out['periodic_max_C']['pass_case']<=60 and out['periodic_max_C']['helper_case']<=80,**out))
        if trace:plots.append(dict(architecture=a,mode=mode,trace=trace))
    sensitivities=[]
    for a,kind,cap,mode in itertools.product(['A','B','C'],['nominal','conservative','poor_joint'],[.1,1.,3.],['Classic','Sprint','MO','CW30']):
        slot,period=(60,300) if mode=='Classic' else (12,60) if mode=='Sprint' else (30,300) if mode=='CW30' else (word_period('MO',8),word_period('MO',8))
        if mode=='CW30':
            loads={'space':point(1.,tone=False,architecture='A'),'off':{k:0 for k in FIELDS}};loads['off']['other_PCB_W']=.04
            seq=[(30,'space'),(270,'off')];energy={}
        else:seq,loads,energy=waveform('MO5' if mode!='MO' else 'MO',8,slot,period,'BUCK4S',1.,a,periodic_word=(mode=='MO'))
        net=Network(kind=kind,capacity_scale=cap);out,_,_=Cycle(net,loads).run(seq)
        rp=ripple(kind,cap,1.,'BUCK4S')
        sensitivities.append(dict(architecture=a,thermal_case=kind,capacity_scale=cap,mode=mode,AM_ripple_positive_C=rp,PA_peak_with_AM_C=out['periodic_max_C']['PA_junction']+rp,**out))
    save('thermal-results.json',dict(status='MODEL_COMPARISON_NOT_PHYSICAL_QUALIFICATION',
        boundary=Network().config,rows=rows,sensitivities=sensitivities,
        A_B_C='Same E6 mechanical/boundary network; only power waveforms/domain states differ',
        AM_ripple='Original E6 PA waveform is unchanged at full MARK; frequency-domain upper addition used at plateau. No false junction safety from cooler mass.',physical='NOT_RUN'))
    save('plot-traces.json',plots)
    for z in rows:
        if z['population']=='BUCK4S' and z['ERP_W']==1 and z['ambient_C']==40 and z['WPM']==12 and z['code'] in ['MO5','MO']:
            print(z['architecture'],z['mode'],round(z['first_max_C']['PA_junction'],2),round(z['PA_peak_with_AM_C'],2),round(z['periodic_max_C']['pass_case'],2),'heatJ',round(sum(z['energy_J'][k] for k in FIELDS[:4]),3),flush=True)

if __name__=='__main__':main()
