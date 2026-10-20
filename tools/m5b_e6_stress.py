"""Independent frequency-domain, fault and cooling-envelope scenarios."""
import itertools
import numpy as np
from scipy.linalg import solve
from m5b_e6_common import *
from m5b_e6_power import operating
from m5b_e6_thermal import Network,NAMES,powers,run_cycle,schedule


def audio(net,z,phases):
    wave=np.array([powers(row) for row in z['waveform']]);spectrum=np.fft.rfft(wave,axis=0)/phases
    result=np.zeros((phases,len(NAMES)))
    for k in range(1,6):
        response=solve(net.G+1j*2*np.pi*800*k*np.diag(net.C),spectrum[k])
        result+=2*np.real(np.exp(1j*2*np.pi*k*(np.arange(phases)+.5)/phases)[:,None]*response[None,:])
    return dict(positive_ripple_C=dict(zip(NAMES,np.max(result,axis=0).tolist())),
                peak_to_peak_C=dict(zip(NAMES,np.ptp(result,axis=0).tolist())),
                unmodelled_harmonic_power_W=float(np.max(np.abs(spectrum[6:]))))


def main():
    guard();ripple=[];fault=[];beacons=[];supplies=[]
    for capacity in [.1,1.,3.]:
        net=Network(capacity_scale=capacity)
        z=operating(1.,waveform=True,phases=256)
        a=audio(net,z,256);a['capacity_scale']=capacity
        # Independent upper bound: assume zero die storage and apply the PA
        # instantaneous junction-to-source Rjc drop; source ripple is separate.
        a['zero_die_storage_PA_positive_bound_C']=3*(z['maximum']['PA_W']-z['mean']['PA_W'])+a['positive_ripple_C']['PA_source_case']
        ripple.append(a)
    for e,pop,scale in itertools.product([.25,.3,.5,1.],['BUCK4S','BOOST2S'],[1.,1.03]):
        z=operating(e,pop,supply_scale=scale);s=operating(e,pop,tone=False,supply_scale=scale)
        supplies.append(dict(ERP_W=e,population=pop,supply_scale=scale,mark=z,space=s))
    for erp,pop,sink,ambient in itertools.product([.25,.3,.5,1.],['BOOST2S','BUCK4S'],[2.2,4.,5.5,8.,12.],[25.,40.]):
        net=Network(sink_R=sink);loads={s:powers(operating(erp,pop,tone=s=='mark')['mean']) for s in ['mark','space']}
        loads['off']=powers(dict(PA_W=0,pass_W=0,helper_W=0,other_PCB_W=.04))
        result,_,_=run_cycle(net,schedule(60,60,'MO',include_id=False),loads,ambient)
        beacons.append(dict(ERP_W=erp,population=pop,sink_K_W=sink,ambient_C=ambient,
                            pass_case_C=result['periodic_max_C']['pass_case'],PA_junction_C=result['periodic_max_C']['PA_junction'],
                            helper_case_C=result['periodic_max_C']['helper_case'],sink_C=result['periodic_max_C']['shared_plate'],
                            within_case_and_junction_limits=result['periodic_max_C']['pass_case']<=60 and result['periodic_max_C']['PA_junction']<=110 and result['periodic_max_C']['helper_case']<=80))
    for tau in [1.,5.,15.]:
        net=Network(sensor_tau=tau,capacity_scale=.1)
        mark=operating(1.)['mean'];space=operating(1.,tone=False)['mean']
        normal={'mark':powers(mark),'space':powers(space),'off':powers(dict(PA_W=0,pass_W=0,helper_W=0,other_PCB_W=.04))}
        # Start from the hotter constant slot load at periodic-average plate
        # temperature, not a cold heatsink. This is an imposed fault scenario.
        x=net.equilibrium(.2*normal['space']+.8*normal['off'])
        for dt in [.0001,.001,.01,.1,1.,5.,30.]:
            q=np.zeros(len(NAMES));q[0]=4.;q[4]=4.24;q[6]=1.1
            y=net.advance(x,q,dt)+40
            fault.append(dict(case='legacy_imposed_4W_PA_4p24W_pass_1p1W_helper_NOT_same_operating_point',sensor_tau_s=tau,duration_s=dt,
                              temperatures_C=dict(zip(NAMES,y.tolist())),PA_below125=bool(y[0]<125),pass_case_below60=bool(y[5]<60),
                              sensor_trip_detected=bool(y[10]>=65.85)))
        # Direct absorbed solar coupling 10W is intentionally adverse; no leaf
        # ignition claim. Shade/guard does not receive an invented cooling credit.
        q=normal['space'].copy();q[8]+=10
        times=np.arange(0,3601,1.)
        series=np.array([40+net.advance(x,q,float(t)) for t in times])
        hit=np.flatnonzero(series[:,10]>=65.85);stop=float(times[hit[0]]) if len(hit) else None
        if stop is not None:
            y=40+net.advance(x,q,stop)
            fault.append(dict(case='10W_solar_plus_continuous_carrier',sensor_tau_s=tau,trip_after_s=stop,
                              temperatures_at_trip_C=dict(zip(NAMES,y.tolist())),normal60C_pass_limit_exceeded=bool(y[5]>60),
                              implication='This installation is prohibited even if the later hardware trip operates'))
    save('stress-ripple-beacon.json',dict(status='CALCULATED_NOT_QUALIFIED',AM800Hz_ripple=ripple,supply_tolerance=supplies,
        beacon_envelopes=beacons,fault_and_sensor=fault,
        outdoor=dict(effective_sink_R_K_W={'unobstructed_vertical_catalogue_comparator':2.2,'horizontal_sensitivity':4.,'sideways_restricted_sensitivity':5.5,'partly_obstructed':8.,'severely_obstructed':12.},
                     ratings_are_not_guarantees=True,solar=dict(irradiance_W_m2=800,black_projected_m2=.0165,absorptivity_assumed=.8,absorbed_W=10.56),
                     accessible_guard_target_C=50,accessible_guard_stop_boundary_C=55,existing_pass_NTC_nominal_trip_C=65.85,
                     restriction='Shaded, ventilated protective base, raised >=15mm, no vegetation/soil touching fins. Avoid severe obstruction; continuous beacon requires its measured role-specific thermal envelope.',
                     fire_safety='No ignition-temperature or outdoor/fire qualification claim; case/guard solar temperature requires measurement independently of transmitter dissipation'),
        stress_disposition='Legacy4/4.24/1.1W allowances are imposed independent stresses. Fault interruption latency is unmeasured; sensor cannot protect rapid PA local faults. Initial powered qualification requires bounded pulses and an instrumented dummy load, not an automatic30s test entitlement.',physical='NOT_RUN'))
    print('Ripple (positive PA °C)',[round(x['positive_ripple_C']['PA_junction'],3) for x in ripple])
    print('Worst imposed-fault peak',max(x.get('temperatures_C',{}).get('PA_junction',0) for x in fault))


if __name__=='__main__':main()
