"""Consistent terminal-power ledger for the native E5 drain modulator.

Assumed RF transfer and transistor gain are sensitivity parameters, not measured
device characteristics. Carrier efficiency includes quiescent current. The
separate dynamic-efficiency M2 model is retained only as an explicitly different
stress family, never combined with the E5 efficiency and an added bias twice.
"""
import csv
import itertools
import math
from m5b_e6_common import *


def native():
    p = parts()
    def r(ref): return number(p[ref]['value'])
    assert p['Q401']['mpn'] == 'D45H11' and p['Q402']['mpn'] == 'BD139'
    assert p['Q501']['mpn'] == 'PD54008L-E'
    assert p['U402']['pins'] == {'1':'AF_DC','2':'GND','3':'LEVEL_DC','4':'AM_COMMAND','5':'V3V3','6':'KEY'}
    assert p['Q401']['pins'] == {'1':'PASS_BASE','2':'VPA','3':'VMOD'}
    assert p['Q402']['pins'] == {'1':'MOD_BASE','2':'MOD_SINK','3':'MOD_E'}
    assert p['Q501']['pins']['S'] == 'GND'
    return dict(feedback_gain=1+r('R511')/r('R512'), feedback_ohm=r('R511')+r('R512'),
                base_return_ohm=r('R505'), base_series_ohm=r('R506'), helper_emitter_ohm=r('R507'),
                driver_series_ohm=r('R413'), current_shunt_ohm=r('R309'),
                full_rail_V=1.229*(1+r('R401')/r('R402')), full_buck_V=.596*(1+r('R301')/r('R302')+r('R301')/r('R303')), reduced_buck_V=.596*(1+r('R301')/r('R302')),
                rail_basis='E5 native converter populations; legacy 13.5 V M2 full rail is superseded',
                envelope_cap_F=number(p['C506']['value'])+number(p['C634']['value']))


def operating(erp, population='BUCK4S', m=.8, tone=True, eta=None,
              bias=.15, beta=60., driver=.1463, filter_db=.75,
              phases=1440, model='E5_carrier_efficiency', waveform=False, supply_scale=1.):
    n=native()
    eta = (.5 if erp >= .75 else .4) if eta is None else eta
    # E5 full 4 V centre / reduced 2.222 V centre, with intermediate PWM profiles.
    v0 = 4. if erp >= .75 else (4/1.8 if erp <= .30 else 4*math.sqrt(erp))
    bus = (n['reduced_buck_V'] if erp < .75 else n['full_buck_V']) if population=='BUCK4S' else n['full_rail_V']
    bus *= supply_scale
    pc=erp*10**.1; internal=pc*10**(filter_db/10)
    if model=='E5_carrier_efficiency':
        i0=internal/(v0*eta); slope=(i0-bias)/v0
    else:
        # Original M2 dynamic efficiency explicitly excludes the added bias.
        slope=internal/(eta*v0*v0);i0=slope*v0+bias
    assert slope>0
    rows=[]
    for i in range(phases if tone else 1):
        angle=2*math.pi*(i+.5)/phases if tone else 0.
        depth=m if tone else 0.
        v=v0*(1+depth*math.sin(angle));dv=v0*depth*2*math.pi*800*math.cos(angle)
        ipa=slope*v+bias
        irfb=v/n['feedback_ohm'];icap=n['envelope_cap_F']*dv
        ic=ipa+irfb+icap
        assert ic>0, 'Envelope model requires unsupported negative pass current'
        ib=ic/beta;vbe=.75
        ireturn=vbe/n['base_return_ohm'];ih=ib+ireturn
        bh=40.;ibh=ih/bh;ie=ih+ibh
        ve=ie*n['helper_emitter_ohm'];vb=ve+.75
        vc=bus-vbe-ih*n['base_series_ohm']
        assert vc>ve and v<bus-.3, 'Headroom failure'
        rf=internal*(v/v0)**2
        rfdrive=10**(19/10)/1000
        heat_pa=v*ipa+rfdrive-rf
        heat_pass=(bus-v)*ic+vbe*ib
        heat_helper=(vc-ve)*ih+.75*ibh
        base_resistors=vbe*ireturn+ih*ih*n['base_series_ohm']+ie*ie*n['helper_emitter_ohm']
        feedback=v*irfb
        main_rail=bus*(ic+ib+ireturn)
        balance=main_rail+vb*ibh-(v*ipa+v*icap+feedback+heat_pass+heat_helper+base_resistors)
        assert abs(balance)<1e-11, balance
        v_after_r=bus-driver*n['driver_series_ohm']
        ldo1=(v_after_r-5.456)*driver;ldo2=(5.456-5)*driver
        assert ldo1>0
        driver_R=n['driver_series_ohm']*driver**2
        mmic=5*driver-rfdrive
        control=.10
        # The native logic/opamp rail comes through J101 V3V3, not the RF
        # converter/current shunt. Keep these supply domains separate. The
        # fixed logic allowance excludes the helper base-drive contribution.
        rail_input=main_rail+bus*driver
        logic_input=control+3.3*ibh
        logic_heat=logic_input-vb*ibh
        conv_eta=.87 if population=='BOOST2S' else .91
        conv_heat=rail_input*(1/conv_eta-1)
        rf_filter=rf-rf/10**(filter_db/10)
        pcb_other=base_resistors+feedback+driver_R+ldo1+ldo2+mmic+logic_heat+conv_heat+rf_filter
        rf_battery=rail_input/conv_eta
        battery=rf_battery+logic_input
        heat_total=heat_pa+heat_pass+heat_helper+pcb_other
        assert abs(battery-(heat_total+rf/10**(filter_db/10)+v*icap))<1e-9
        rows.append(dict(PA_W=heat_pa,pass_W=heat_pass,helper_W=heat_helper,
                         other_PCB_W=pcb_other,PA_DC_W=v*ipa,PA_RF_W=rf,
                         connector_RF_W=rf/10**(filter_db/10),DC_input_W=battery,
                         RF_battery_input_W=rf_battery,controller_3V3_input_W=logic_input,
                         base_resistors_W=base_resistors,MMIC_W=mmic,driver_regulators_W=driver_R+ldo1+ldo2,
                         converter_W=conv_heat,control_W=logic_heat,
                         regulated_current_A=ic+ib+ireturn+driver,
                         VPA_V=v,PA_current_A=ipa,helper_current_A=ih,
                         pass_VCE_V=bus-v,pass_IC_A=ic,helper_VCE_V=vc-ve,
                         envelope_storage_W=v*icap,
                         terminal_energy_balance_W=balance))
    mean={k:sum(x[k] for x in rows)/len(rows) for k in rows[0]}
    maxima={k:max(x[k] for x in rows) for k in rows[0]}
    minima={k:min(x[k] for x in rows) for k in rows[0]}
    result=dict(ERP_W=erp,population=population,tone=tone,m=m if tone else 0,
                V0_V=v0,upstream_V=bus,carrier_efficiency_assumed=eta,
                bias_A=bias,pass_beta_assumed=beta,driver_A=driver,model=model,
                filter_loss_db=filter_db,antenna_feed_gain_dBd=-1,
                mean=mean,maximum=maxima,minimum=minima,
                current_trip_nominal_A=1.797,
                below_nominal_current_trip=maxima['regulated_current_A']<1.797,
                qualification='CALCULATED_ASSUMPTIONS_NOT_MEASURED')
    if waveform:result['waveform']=rows
    return result


def main():
    guard();n=native();rows=[];cases=[]
    for pop,e,tone in itertools.product(['BOOST2S','BUCK4S'],[.25,.3,.5,1.],[False,True]):
        z=operating(e,pop,tone=tone);cases.append(z)
        rows.append(dict(population=pop,ERP_W=e,state='mark_80pct_AM' if tone else 'space_or_CW_carrier',
                         V0_V=z['V0_V'],upstream_V=z['upstream_V'],**z['mean'],
                         peak_rail_current_A=z['maximum']['regulated_current_A']))
    sensitivity=[]
    for eta,bias,beta in itertools.product([.35,.4,.45,.5,.6],[.05,.15,.2],[20,40,60,100]):
        z=operating(1.,eta=eta,bias=bias,beta=beta)
        sensitivity.append({k:z[k] for k in ['carrier_efficiency_assumed','bias_A','pass_beta_assumed','below_nominal_current_trip','mean','maximum']})
    m2=operating(1.,eta=.45,model='M2_dynamic_efficiency_plus_bias')
    save('power-audit.json',dict(status='CONSISTENT_MODEL_PHYSICAL_RF_TRANSFER_UNQUALIFIED',native_parameters=n,
        native_before_E6_sha256=sha(HW/'RF2M.kicad_pcb'),cases=cases,sensitivity=sensitivity,
        separate_M2_stress_family=m2,legacy_independent_heat_allowances_W={'PA':4,'pass':4.24,'helper':1.1},
        legacy_stress_disposition='Retained as an imposed simultaneous stress, not a derived valid operating point',
        model_uncertainties=['No measured 144MHz drain-current/RF-envelope transfer','Beta and bias sensitivity, not guaranteed hot gain curves',
                            'Full E5 rail is approximately9V; do not substitute M2 13.5V without an electrical ECO',
                            '50percent carrier efficiency already includes the chosen bias current',
                            'KEY changes AM tone/DC, not RF enable; no mark-space power-off discount',
                            'Current-trip rejected cases are reported, never clipped into successful RF output',
                            '0.5W PWM setting is a calculation candidate; physical calibration remains mandatory'],
        off_slot=dict(PA_W=0,pass_W=0,helper_W=0,RF_board_idle_W=.04,
                      condition='PREPARE=PA_PREPARE=SLOT=ARM=0, source/driver/bias/pass inhibited; native fail-off. Leakage allowance, not measured'),
        prepared_idle='No RF; converter/reservoir/analog overhead remains. No cooling credit for indefinite PREPARE.',
        physical='NOT_RUN'))
    with (OUT/'power-states.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    save('phase-A-completion.json',dict(PCB_modified=False,native_sha256=sha(HW/'RF2M.kicad_pcb'),
        power_source_sha256=sha(Path(__file__)),result='Power ledger complete before PCB changes; transient envelope is next',
        package_correction='PD54008L-E manufacturer Rev2 describes PowerFLAT5x5, not PowerSO10RF',physical='NOT_RUN'))
    for z in cases:
        if z['population']=='BUCK4S': print(z['ERP_W'],'MARK' if z['tone'] else 'SPACE',*[round(z['mean'][k],4) for k in ['PA_W','pass_W','helper_W','other_PCB_W']], 'peak_A',round(z['maximum']['regulated_current_A'],4))


if __name__=='__main__':main()
