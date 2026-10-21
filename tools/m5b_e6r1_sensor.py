"""Source-region observer, window-comparator corners, and bounded fault latency.

The observer is not a junction sensor. Bond lag and joint resistance are
independent unknowns, swept instead of claimed as manufacturer data.
"""
import math,itertools
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
from m5b_e6r1_common import *
from m5b_e6r1_thermal import Cycle,waveform,word_period
from m5b_e6r1_power import point
from m5b_e6_thermal import Network,NAMES
from m5b_e6_power import operating
from m5b_e6_stress import audio
from m5b_e6_faults import absorbed

def ntc_R(temp,r25=10000.,beta=3434.):return r25*math.exp(beta*(1/(temp+273.15)-1/298.15))
def sensor_V(temp):
    r=ntc_R(temp);return 3.3*r/(33000+r)
def divider_temperature(v,r25=10000.,beta=3434.):
    r=33000*v/(3.3-v)
    return 1/(1/298.15+math.log(r/r25)/beta)-273.15

def with_joint(source_R,cap,joint):
    n=Network(source_R=source_R,capacity_scale=cap)
    old=next(e['K_W'] for e in n.edges if e['a']=='PA_source_case' and e['b']=='PCB_source')
    delta=1/joint-1/old
    for a,b,sign in [(1,1,1),(2,2,1),(1,2,-1),(2,1,-1)]:n.G[a,b]+=sign*delta
    n.eig,n.U=eigh(n.G/n.root[:,None]/n.root[None,:]);n.transition_cache={}
    return n

def healthy_headroom():
    rows=[]
    period=word_period('MO',8)
    seq,loads,_=waveform('MO',8,period,period,'BUCK4S',1.,'C',periodic_word=True)
    nominal=divider_temperature(3.3*10/201)
    for kind,tau in itertools.product(['nominal','conservative','poor_joint'],[.01,.05,.1,.3,.6,1.]):
        result,trace,_=Cycle(Network(kind=kind),loads,tau).run(seq,record=True)
        peak=float(max(z[-1] for z in trace))
        rows.append(dict(thermal_case=kind,tau_s=tau,healthy_sensor_peak_C=peak,
            nominal_hot_trip_C=nominal,healthy_trip_expected=bool(peak>=nominal),
            PA_cycle_mean_peak_C=result['periodic_max_C']['PA_junction']))
    return rows

def evaluate(n,tau,threshold,mode='stuck_HIGH',observer_node=2,delay=.001):
    period=word_period('MO',8)
    seq,healthy,energy=waveform('MO',8,period,period,'BUCK4S',1.,'C',periodic_word=True)
    observer=Cycle(n,healthy,tau,observer_node)
    _,trace,_=observer.run(seq,record=True)
    hot=max(trace,key=lambda z:z[2]);x=np.array(hot[2:])-40
    if mode=='stuck_HIGH':
        faults={'full':point(1.,architecture='C',eta=.4,absorbed=1.)};sequence=[(10.,'full')]
    else:
        sequence,faults,_=waveform('MO',8,period,period,'BUCK4S',1.,'C',eta=.4,absorbed=1.,periodic_word=True)
        sequence*=math.ceil(60/period)
    f=Cycle(n,faults,tau,observer_node)
    a=audio(n,absorbed(operating(1.,eta=.4,waveform=True,phases=256),1.),256)['positive_ripple_C']['PA_junction']
    peak=float(x[0]+40+a);trip=None;time=0.;records=[]
    for dt,state in sequence:
        points=sorted(set([dt]+[v for v in [.00001,.0001,.001,.005,.01,.05,.1,.3,.5,1,2,5] if v<dt]))
        previous=0.
        for t in points:
            y=f.advance(x,state,t);sensor=40+y[12]
            if sensor>=threshold:
                if 40+x[12]>=threshold:when=0.
                else:when=brentq(lambda tt:40+f.advance(x,state,tt)[12]-threshold,previous,t,xtol=1e-9)
                shut=f.advance(x,state,when+delay)
                # Full positive AM ripple and all VPA cap energy in the smallest
                # die capacity are added conservatively through actuation delay.
                cap_energy=.5*100.33e-9*7.2**2
                peak=max(peak,float(shut[0]+40+a+cap_energy/n.C[0]))
                trip=dict(seconds=time+when,action_complete_s=time+when+delay,
                          sensor_at_trip_C=40+f.advance(x,state,when)[12],source_copper_at_action_C=40+shut[2],
                          junction_cycle_mean_at_action_C=40+shut[0])
                break
            peak=max(peak,float(40+y[0]+a));previous=t
        if trip:break
        x=f.advance(x,state,dt);time+=dt
        records.append([time,40+x[0]+a,40+x[2],40+x[12]])
    if trip is None:
        periodic,_,_=f.run(sequence)
        peak=max(peak,periodic['periodic_max_C']['PA_junction']+a)
    return dict(tau_s=tau,threshold_C=threshold,mode=mode,observer_node=NAMES[observer_node],
        peak_junction_upper_C=peak,trip=trip,PA_125C_met=peak<=125,PA_110C_met=peak<=110,
        maximum_actuation_delay_s=delay,AM_positive_upper_C=a,samples=records)

def main():
    guard();threshold=3.3*10/(191+10);cold=3.3*191/(191+22.1)
    # Worst comparator offset8mV +half max25mV hysteresis, resistor/NTC corners.
    corners=[]
    for dv,r25,beta in itertools.product([-.0205,.0205],[9900,10100],[3380.,3468.]):
        corners.append(divider_temperature(threshold+dv,r25,beta))
    save('sensor-window.json',dict(sensor='Murata NCP15XH103F03RC,0402,10k1%,B25/50=3380K1%,B25/85typ3434K',
        pullup_ohm=33000,hot_reference_divider_ohm=[191000,10000],cold_reference_divider_ohm=[22100,191000],
        hot_nominal_C=divider_temperature(threshold),hot_input_threshold_V=threshold,
        cold_open_threshold_V=cold,hot_corner_C=[min(corners),max(corners)],
        comparator='TLV7034PWR pushpull; outputs1/7healthyHIGH,100kpulldowns;NAND->2N7002sinkHARD_OK_N;11GND4V3V3;8/14readiness',
        sensor_faults={'open':'HIGHwindowinhibit','short':'LOWwindowinhibit','unplugged':'HIGHwindowinhibit',
            'detached_but_electrically_intact':'NOT inherently detectable; coupling proof and bounded PA energy still needed',
            'plausible_stuck_resistance':'NOT inherently detectable by a simple window',
            'missing_or_unpowered_comparator':'Four100koutputpulldowns->TEMP_BAD=1 andRF_NOT_READY=1; inhibits withoutfirmware',
            'V3V3_loss':'Original brownout/default-off remains independent'},
        corner_limitation='B25/85typ is not a guaranteed tolerance curve;3380..3468K are explicit scenarios, not a guaranteed manufacturer bound. Ref/mounting drift need margin.87C uppertrip is a budget requiring qualification.',
        manufacturer_dissipation_mW_K_typ={'still_air_unmounted':1.,'specified_mounted_test_board':2.5},
        manufacturer_installed_time_constant='NOT_SPECIFIED; dissipation constants are not time constants',physical='NOT_RUN'))
    rows=[]
    source_cases=json.loads((HW/'review/M5B-E6/E6-source-path-FVM.json').read_text())['cases']
    poor=next(x['source_to_bar_K_W'] for x in source_cases if x['name']=='poor_pressure')
    for source_R,cap,joint in itertools.product([11.846896331207134,poor],[.1,1.],[1.,5.,10.]):
        n=with_joint(source_R,cap,joint)
        for tau,th,mode in itertools.product([.01,.05,.1,.3,.6,1.],[80.,87.],['MO','stuck_HIGH']):
            result=evaluate(n,tau,th,mode)
            result.update(source_to_bar_K_W=source_R,capacity_scale=cap,source_solder_K_W=joint)
            rows.append(result)
        print('Sensor fault cases completed',source_R,cap,joint,flush=True)
    save('sensor-fault-results.json',dict(status='CONDITIONAL_TRANSFER_FUNCTION_NOT_QUALIFIED',cases=rows,
        healthy_threshold_headroom=healthy_headroom(),
        note='Original E6 network retained except explicit solder-joint fault. Observer is measurement-only, with no fictitious cooling path. Healthy C MO hot start; same-point eta40/fullRFabsorption.',
        requirement='A passing row is conditional on its source-joint, sensor-node coupling, lag and threshold. No datasheet proves those installed values.',physical='NOT_RUN'))

if __name__=='__main__':main()
