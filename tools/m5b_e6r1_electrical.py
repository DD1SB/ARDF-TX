"""Reduced-order AM loop, source filter, edge spectrum and exact net proposal.

This independent small-signal model is NOT a transistor RF/SPICE qualification.
It exposes assumed pass/helper poles and load changes. No fabricated measured
S-parameters, spur suppression or guaranteed hot SOA is asserted.
"""
import itertools,math
import numpy as np
from scipy import signal
from m5b_e6r1_common import *
from m5b_e6r1_morse import schedule

def loop(K=10.,load=5.,Cout=100.33e-9,ft=1e6,pass_pole=8e5,helper_pole=3e6):
    s=np.poly1d([1.,0.]);A0=1e5;Aden=np.poly1d([A0/(2*np.pi*ft),1.])
    Pden=np.poly1d([load*Cout,1.])*np.poly1d([1/(2*np.pi*pass_pole),1.])*np.poly1d([1/(2*np.pi*helper_pole),1.])
    gsum=1/18000+1/10000;C=4.7e-9
    Lnum=A0*(K/18000+s*C*Pden);Lden=Aden*Pden*(gsum+s*C)
    den=Lden+Lnum;num=A0*K*(gsum+s*C)
    return np.poly1d(num),np.poly1d(den),np.poly1d(Lnum),np.poly1d(Lden)

def evaluate(**kw):
    num,den,ln,ld=loop(**kw);f=np.geomspace(10,1e8,4000);ss=2j*np.pi*f
    L=np.polyval(ln,ss)/np.polyval(ld,ss);phase=np.unwrap(np.angle(L))*180/np.pi
    cross=np.flatnonzero((np.abs(L[:-1])>=1)&(np.abs(L[1:])<1));pm=float(min(180+phase[i] for i in cross)) if len(cross) else None
    h=np.polyval(num,2j*np.pi*800)/np.polyval(den,2j*np.pi*800)
    sf=1/(1+2j*np.pi*800*47e-6)**2
    pre=2.8/abs(h*sf);top=4/2.8*(1+.8*pre);bottom=4/2.8*(1-.8*pre)
    poles=np.roots(den);stable=bool(np.max(poles.real)<0)
    return dict(**kw,stable=stable,phase_margin_deg=pm,AM800Hz_gain=float(abs(h)),
        AF_reconstruction_gain=float(abs(sf)),required_AF_preemphasis=pre,
        commanded_PWM_peak_V=float(top),commanded_PWM_trough_V=float(bottom),within_3V3=bool(top<3.3 and bottom>=0),
        maximum_pole_real_per_s=float(np.max(poles.real)))

def shaped_envelope(t,edge,wpm=12,slot=60,periodic=False):
    env=np.zeros(len(t))
    duration=3*slot if periodic else slot
    for z in schedule('MO',wpm,duration,duration):
        if z['state']!='mark':continue
        offset=slot if periodic else 0
        a=max(0,z['start_us']/1e6-edge/2)-offset;b=min(duration,z['end_us']/1e6+edge/2)-offset
        m=(t>=a)&(t<b);x=t[m]
        if edge==0:env[m]=1;continue
        v=np.ones(len(x));up=x<a+edge;down=x>b-edge
        v[up]=.5-.5*np.cos(np.pi*(x[up]-a)/edge)
        v[down]=.5-.5*np.cos(np.pi*(b-x[down])/edge)
        env[m]=np.maximum(env[m],v)
    return env

def spectrum(edge,dt=1/50000,vpa_cutoff_V=0.,feedthrough_dB=None,depth=.8):
    # One exact MO repetition at12WPM:28dit=2.8s. Avoid a window hiding
    # rectangular-edge leakage; periodically aligned FFT is the authority.
    duration=2.8;t=np.arange(round(duration/dt))*dt
    env=shaped_envelope(t,edge,slot=duration,periodic=True)
    a=env*(1+depth*np.sin(2*np.pi*800*t))
    gate=(a*4>=vpa_cutoff_V)&(env>0)
    a=a*gate
    feed=0. if feedthrough_dB is None else math.sqrt((10**1.9/1000)*10**(feedthrough_dB/10)/1.2589254117941673)
    a+=feed*gate
    y=np.fft.fft(a);f=np.fft.fftfreq(len(a),dt);power=np.abs(y)**2;total=power.sum()
    order=np.argsort(np.abs(f));cs=np.cumsum(power[order])/total
    bw=2*abs(f[order[np.searchsorted(cs,.99)]])
    fractions={str(hz):float(power[np.abs(f)>hz].sum()/total) for hz in [2000,3000,5000,10000]}
    return dict(edge_full_s=edge,edge_10_to_90_s=edge*(math.acos(-.8)-math.acos(.8))/math.pi,
        relative_99percent_BW_Hz=bw,outside_offset_power_fraction=fractions,
        drain_ready_threshold_V=vpa_cutoff_V,driver_feedthrough_dB_assumed=feedthrough_dB,
        AF_depth=depth,constructive_flat_RF_depth=depth/(1+feed),
        method='Ideal AM envelope DFT; no analyzer floor, no RFPA memory/feedthrough/harmonics. Not a national-mask test')

def main():
    guard();p=parts()
    assert p['U402']['pins']['3']=='LEVEL_DC' and p['U305']['pins']['3']=='NORMAL_PERMIT'
    assert p['U601']['pins']['1']=='NORMAL_OFF' and p['C409']['pins']['1']=='VDRV_FILTER'
    assert p['C603']['pins']['1']=='VDRV_MMIC' and p['Q405']['pins']['3']=='MOD_COMMAND'
    rows=[]
    for K,load,ft,pp,hp in itertools.product([4.,10.,25.],[3.,8.],[8e5,1e6],[2.5e5,8e5],[5e5,3e6]):
        rows.append(evaluate(K=K,load=load,ft=ft,pass_pole=pp,helper_pole=hp))
    for K in [200.,1000.,3000.]:rows.append(evaluate(K=K,load=1/(1/1000+1/28000)))
    save('electrical-model.json',dict(model='Independent reduced-order small-signal loop, not manufacturer SPICE',cases=rows,
        nominal=evaluate(),spectra=[spectrum(v) for v in [0.,.005,.008,.012]],
        readiness_feedthrough_sensitivity=[spectrum(.008,vpa_cutoff_V=v,feedthrough_dB=db,depth=.75) for v,db in itertools.product([.02,.10,.20],[-40.,-20.,0.])],
        native_values={'R511_ohm':18000,'R512_ohm':10000,'C505_F':4.7e-9,'C506_plus_C634_F':100.33e-9},
        assumptions='A0=1e5,GBW0.8..1MHz,helper/pass poles are explicit transistor-stage sensitivity assumptions; not guaranteed hot corner models',
        limitations=['No nonlinear saturation, BJT storage-charge or SOA validation from this linear model',
            'Native C505 compensation remains a first-article loop acceptance item',
            'RFtransfer/clean PEP/800Hz AM distortion/feedthrough and harmonics require physical qualification',
            'Boundary shaping clips first/last edge inside SLOT; interior50percent edges retain logical Morse timing'],physical='NOT_RUN'))
    save('circuit-proposal.json',dict(status='PROPOSAL_ONLY_NO_NATIVE_EDIT',architecture='C',
        changes=[{'ref':'U402','pin':'3','from':'LEVEL_DC','to':'GND','reason':'KEYlow selects zero drain command'},
                 {'ref':'U305','pin':'3','from':'NORMAL_PERMIT','to':'DRIVER_ON','reason':'Only downstream101nF/MMIC load keyed; C409150uFstayscharged'},
                 {'ref':'U601','pin':'1','from':'NORMAL_OFF','to':'CLOCK_OFF','reason':'No RF drive into an unready drain/driver'},
                 {'ref':'R509','pin':'1','from':'NORMAL_OFF','to':'LOCAL_MOD_OFF','reason':'Space also clamps Q404/Q405; prevents zero-command offset/saturation from sustaining pass loss'},
                 {'ref':'AF_PWM','from':'continuous_sine','to':'reconstructed_sine_times_raised_cosine_key_envelope','reason':'Preserve70-80percentAMonflatMARK with calibrated AFpreemphasis'}],
        new_parts={
            'U970':dict(MPN='TLV7034PWR',package='TSSOP14',pins={'1':'TEMP_HOT_OK','2':'PA_TEMP_LOW','3':'PA_TEMP_S','4':'V3V3','5':'PA_TEMP_HIGH','6':'PA_TEMP_S','7':'TEMP_OPEN_OK','8':'VPA_READY','9':'VPA_READY_REF','10':'VPA_READY_S','11':'GND','12':'VDRV_READY_S','13':'VDRV_READY_REF','14':'DRIVER_READY'}),
            'U971':dict(MPN='SN74LVC2G00DCUR',package='VSSOP8',pins={'1':'TEMP_HOT_OK','2':'TEMP_OPEN_OK','3':'RF_NOT_READY','4':'GND','5':'VPA_READY','6':'DRIVER_READY','7':'TEMP_BAD','8':'V3V3'}),
            'U972':dict(MPN='SN74LVC2G32DCUR',package='VSSOP8',pins={'1':'NORMAL_OFF','2':'KEY_N','3':'CLOCK_OFF','4':'GND','5':'LOCAL_MOD_OFF','6':'RF_NOT_READY','7':'LOCAL_MOD_OFF','8':'V3V3'}),
            'U973':dict(MPN='SN74LVC1G04DBVR',package='SOT23-5',pins={'1':None,'2':'LOCAL_MOD_OFF','3':'GND','4':'DRIVER_ON','5':'V3V3'}),
            'Q970':dict(MPN='2N7002,215',package='SOT23',pins={'1':'TEMP_BAD','2':'GND','3':'HARD_OK_N'}),
            'RT970':dict(MPN='NCP15XH103F03RC',package='0402',location_proposed_mm=[92.,51.4],side='F.Cu',
                attachment='On a short source-ground wing beside Q501, thermally bonded; electrical sensing pad isolated from RF GND',
                warning='Coordinate is an analytical target, not collision/routing-approved; lag/source-joint correlation unqualified')},
        passive_proposal=dict(sensor_pullup_ohm=33000,hot_ref_top_bottom_ohm=[191000,10000],cold_ref_top_bottom_ohm=[22100,191000],
            VPA_divider_top_bottom_ohm=[100000,33000],VPA_reference_top_bottom_from_V3V3_ohm=[330000,2490],
            VDRV_divider_top_bottom_ohm=[10000,10000],VDRV_reference_top_bottom_from_V3V3_ohm=[10000,21500],
            comparator_output_pulldown_ohm=100000,new_IC_bypass_F=100e-9,
            TEMP_BAD_gate_pullup_ohm=100000,
            driver_enable_pulldown_ohm=100000,clock_off_pullup_ohm=100000),
        timing=dict(driver_prepare_before_RF_envelope_s=.002,chosen_edge_full_s=.008,
            emergency_actuation_budget_s=.001,normal_Morse_ARM_reacquire=False),
        safety='Pushpull comparator outputs pulledDOWN100k: missing/unpoweredU970meansTEMP_BAD andRF_NOT_READY;Q970hardwarewire-ORHARD_OK_N. LOCAL_MOD_OFF=existingNORMAL_OFF ORKEY_NpreservesRCdelay/fastkill; originalCLR/rearm,Q404/Q405/Q502,powerisolation/watchdogretained;SLOT/fault override shaping',
        firmware='M6-L2 files untouched. Future target firmware integration must identify RFhardware revision and implement AFprecomp/keylead; currently not functional contestfirmware',
        physical='NOT_RUN'))
    print('Loop cases',len(rows),'stable',sum(z['stable'] for z in rows),'minPM',min(z['phase_margin_deg'] for z in rows if z['phase_margin_deg'] is not None),flush=True)

if __name__=='__main__':main()
