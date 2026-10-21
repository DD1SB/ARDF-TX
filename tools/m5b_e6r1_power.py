"""E6-compatible terminal ledger plus native bleeder/bias and keying domains.

Flat MARK assumptions are unchanged. Spaces do not receive an RF-output-only
mute discount: C removes VPA, B hypothetically cold-switches normal domains.
Capacitor transition packets explicitly include stored/released energy.
"""
import functools,math
import numpy as np
from m5b_e6r1_common import *
from m5b_e6_power import native

FIELDS=['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W','DC_input_W',
        'RF_battery_input_W','controller_3V3_input_W','PA_DC_W','PA_RF_W',
        'converter_W','driver_W','bias_divider_W','VPA_bleeder_W','regulated_current_A','storage_W']

@functools.lru_cache(maxsize=2048)
def point(erp,pop='BUCK4S',alpha=1.,tone=True,architecture='C',eta=None,absorbed=0.,phases=128,supply_scale=1.,corrected=True,beta=60.):
    n=native();p=parts();eta=(.5 if erp>=.75 else .4) if eta is None else eta
    v0=4 if erp>=.75 else 4/1.8 if erp<=.3 else 4*math.sqrt(erp)
    bus=(n['reduced_buck_V'] if erp<.75 else n['full_buck_V']) if pop=='BUCK4S' else n['full_rail_V'];bus*=supply_scale
    internal=erp*10**.175;i0=internal/(eta*v0);ibias=.15;k=(i0-ibias)/v0
    assert alpha>=0 and alpha<=1 and k>0 and 0<=absorbed<=1
    beta_h=40.;vbe=.75;rf_in=10**1.9/1000
    converter_eta=.91 if pop=='BUCK4S' else .87
    driver=(.1463 if architecture=='A' or alpha>0 else 0.)
    # Atalpha0:pass command zero and RF clock disabled. Source+converter remain
    # active for C. This is an assumed residual budget, not measured leakage.
    if alpha==0:
        rail_idle=.020 if pop=='BOOST2S' else .008
        idle=0. if architecture=='B' else rail_idle
        pa=.001;pas=.002;helper=.001
        drv=bus*driver
        bias_power=(bus*bus/11000 if architecture=='C' else 0.)
        rail=drv+bias_power+pa+pas+helper
        conv=rail*(1/converter_eta-1)+idle
        logic=.10+(.02 if architecture in ['B','C'] else 0.)
        other=drv+bias_power+conv+logic
        dc=rail+conv+logic
        result=dict(zip(FIELDS,[pa,pas,helper,other,0.,dc,rail+conv,logic,pa,0.,conv,drv,bias_power,0.,(rail/bus),0.]))
        result['regulated_current_peak_A']=rail/bus
        return result
    angle=2*np.pi*(np.arange(phases)+.5)/phases
    depth=.8 if tone else 0.;v=alpha*v0*(1+depth*np.sin(angle));dv=alpha*v0*depth*2*np.pi*800*np.cos(angle)
    ipa=k*v+ibias*np.minimum(v/.2,1.)
    # The original A MARK/SPACE regime has Vmin>.2V, exactly retaining E6's
    # chosen bias. Low-voltage ohmic rolloff only affects new shaped tails.
    g_bleed=1/float(p['R513']['value'][:-1])/1000 if corrected else 0.
    irfb=v/n['feedback_ohm'];ibleed=v*g_bleed;icap=n['envelope_cap_F']*dv
    ic=ipa+irfb+ibleed+icap
    assert np.min(ic)>0, 'Unsupported pass-current reversal'
    ib=ic/beta;ireturn=vbe/n['base_return_ohm'];ih=ib+ireturn;ibh=ih/beta_h
    ie=ih+ibh;ve=ie*n['helper_emitter_ohm'];vb=ve+.75
    vc=bus-vbe-ih*n['base_series_ohm']
    assert np.min(vc-ve)>0 and np.max(v)<bus-.3
    # New coarse RF interlock forbids drive at a dead drain. Ideal threshold
    # .1V; offset/hysteresis and feedthrough are separately swept electrically.
    drive=(v>=.10) if architecture!='A' else np.ones(phases,dtype=bool)
    rf=internal*(v/v0)**2*drive*(1-absorbed)
    inp=rf_in*drive
    pa=v*ipa+inp-rf
    pas=(bus-v)*ic+vbe*ib
    helper=(vc-ve)*ih+.75*ibh
    res=vbe*ireturn+ih**2*n['base_series_ohm']+ie**2*n['helper_emitter_ohm']
    feedback=v*irfb;bleed=v*ibleed
    bias_power=bus*bus/11000 if corrected else 0.
    main=bus*(ic+ib+ireturn)+bias_power
    control=.10+(.02 if architecture in ['B','C'] else 0.);logic=control+3.3*ibh
    mmic=5*driver-inp;drv_R=n['driver_series_ohm']*driver**2
    ldo=(bus-driver*n['driver_series_ohm']-5)*driver
    driver_heat=mmic+drv_R+ldo
    rail=main+bus*driver
    conv=rail*(1/converter_eta-1)
    conv+=.020 if pop=='BOOST2S' else .008 # explicit prepared-converter idle allowance
    logic_heat=logic-vb*ibh
    rf_filter=rf*(1-10**(-.75/10));connector=rf-rf_filter
    other=res+feedback+bleed+bias_power+driver_heat+logic_heat+conv+rf_filter
    rfbatt=rail+conv;dc=rfbatt+logic;storage=v*icap
    arrays=[pa,pas,helper,other,connector,dc,rfbatt,logic,v*ipa,rf,conv,driver_heat,
            np.full(phases,bias_power),bleed,ic+ib+ireturn+driver+bias_power/bus,storage]
    error=dc-(pa+pas+helper+other+connector+storage)
    assert np.max(np.abs(error))<1e-10, np.max(np.abs(error))
    result={field:float(np.mean(a)) for field,a in zip(FIELDS,arrays)}
    result['regulated_current_peak_A']=float(np.max(arrays[14]))
    return result

def transition_packet(erp,pop,architecture,supply_scale=1.):
    n=native();z=point(erp,pop);bus=(n['reduced_buck_V'] if erp<.75 else n['full_buck_V']) if pop=='BUCK4S' else n['full_rail_V']
    bus*=supply_scale
    v0=4 if erp>=.75 else 4/1.8 if erp<=.3 else 4*math.sqrt(erp);peak=v0*1.8
    cap=n['envelope_cap_F'];charge=bus*cap*peak;stored=.5*cap*peak*peak
    conv_eta=.91 if pop=='BUCK4S' else .87
    reservoir=0.
    if architecture=='B':
        # Cold converter+driver domains: explicit baseline output reservoirs.
        reservoir=44e-6*bus**2+150e-6*5**2+9.4e-6*5.456**2
    inp=(charge+reservoir)/conv_eta
    # C reuses U305 to switch only the small MMIC-side capacitance, retaining
    # C409150uF upstream. Charge plus a conservative2ms powered warm-up interval.
    warm_driver=(101e-9*5**2+bus*.1463*.002) if architecture=='C' else 0.
    storage_total=stored+.5*reservoir
    inp+=warm_driver/conv_eta
    return dict(input_J=inp,stored_on_rise_J=stored,pass_charge_heat_J=charge-stored,
        other_heat_J=stored+reservoir+inp-charge-reservoir,
        rise_input_J=inp,rise_other_heat_J=.5*reservoir+inp-charge-reservoir,
        storage_total_on_rise_J=storage_total,fall_other_heat_J=storage_total,
        driver_precharge_allowance_J=warm_driver,
        VPA_capacitance_F=cap,cold_reservoir_charge_J=reservoir,
        interpretation='Complete rise/fall packet: C Vbus Vpeak input, halfCVpeak2 stored then released; no double counting of steady AM storage')

def main():
    guard();rows=[]
    for pop in ['BUCK4S','BOOST2S']:
        for e in [.25,.5,1.]:
            for a in ['A','B','C']:
                mark=point(e,pop,architecture=a)
                space=point(e,pop,tone=False,architecture='A') if a=='A' else point(e,pop,alpha=0,architecture=a)
                packet=transition_packet(e,pop,a)
                assert abs(packet['input_J']-packet['pass_charge_heat_J']-packet['other_heat_J'])<1e-10
                rows.append(dict(population=pop,ERP_W=e,architecture=a,mark=mark,space=space,transition=packet))
    save('power-budget.json',dict(status='CALCULATED_NOT_MEASURED',rows=rows,
        common_assumptions='E6 carrier efficiency,bias,beta,RFdrive and0.75dBfilter retained; corrected nativeR513bleeder andR606/RV501biasdivider, explicitconverteridle',
        B='Thermal lower-bound cold-key model; converter/driver startup not proved and not selected',
        C='Converter,synthesizer,bias remain prepared; U305 keys small downstream driver load with2ms precharge; VPA command and RF clock keyed; upstream150uF retained',
        current='R1 current includes bleeder andbiasdivider; controllerV3V3 remains separate',physical='NOT_RUN'))
    for r in rows:
        if r['population']=='BUCK4S':print(r['ERP_W'],r['architecture'],'mark',[round(r['mark'][k],4) for k in FIELDS[:4]],'space',[round(r['space'][k],4) for k in FIELDS[:4]])

if __name__=='__main__':main()
