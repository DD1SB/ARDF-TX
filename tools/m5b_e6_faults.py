"""Fault loads tied to one native electrical operating point and real inhibits.

RF-absorption is a sensitivity, not a measured mismatched-load current curve.
It is bounded by input energy and the existing current monitor; no independent
10 W+10 W heat allowance is used as a design-acceptance operating point.
"""
import copy
import numpy as np
from m5b_e6_common import *
from m5b_e6_power import operating
from m5b_e6_thermal import Network,NAMES,powers,run_cycle,schedule
from m5b_e6_stress import audio


def absorbed(z,fraction):
    out=copy.deepcopy(z)
    for row in [out['mean'],out['minimum'],out['maximum'],*out.get('waveform',[])]:
        # For mean/waveform rows this conserves the same DC+RF-input energy.
        # Min/max fields are recomputed below when a waveform is present.
        original=row['PA_RF_W'];residual=original*(1-fraction)
        old_filter=original*(1-10**(-z['filter_loss_db']/10))
        new_filter=residual*(1-10**(-z['filter_loss_db']/10))
        row['PA_W']+=original*fraction;row['PA_RF_W']=residual
        row['connector_RF_W']=residual/10**(z['filter_loss_db']/10)
        row['other_PCB_W']+=new_filter-old_filter
    if out.get('waveform'):
        for field,fun in [('maximum',max),('minimum',min)]:
            out[field]={k:fun(x[k] for x in out['waveform']) for k in out['waveform'][0]}
    return out


def main():
    guard();p=parts()
    assert p['U201']['mpn']=='TPS3431SDRBR'
    assert p['R201']['value']=='10k' and p['R201']['pins']=={'1':'CWD','2':'V3V3'}
    fvm=json.loads((OUT/'E6-source-path-FVM.json').read_text())['cases']
    alternatives={z['name']:z['source_to_bar_K_W'] for z in json.loads((OUT/'source-interface-alternatives.json').read_text())['alternatives']}
    primary=next(z['source_to_bar_K_W'] for z in fvm if z['name']=='conservative')
    better=alternatives['KERATHERM_double_resistance_contact_allowance']
    grease=alternatives['E5_grease_conservative']
    rows=[];traces=[]
    for source_R in [primary,alternatives['KERATHERM_thicker_triple_resistance_allowance'],better,grease,6.]:
        for capacity in [.1,1.,3.]:
            net=Network(source_R=source_R,capacity_scale=capacity)
            mark=operating(1.,waveform=True,phases=256);space=operating(1.,tone=False)
            loads={'mark':powers(mark['mean']),'space':powers(space['mean']),'off':np.zeros(len(NAMES))}
            normal,_,trace=run_cycle(net,schedule(60,300,'MO5'),loads)
            hot=max(trace,key=lambda x:x[2]);x=np.array(hot[2:])-40
            crest=max(mark['waveform'],key=lambda z:z['VPA_V']);q=powers(crest)
            frozen=[]
            for t in [.001,.01,.05,.17,.20,.23]:
                y=40+net.advance(x,q,t)
                frozen.append(dict(seconds=t,temperatures_C=dict(zip(NAMES,y.tolist()))))
            reflections=[]
            for fraction in [.5,1.]:
                zm=absorbed(mark,fraction);zs=absorbed(space,fraction)
                q={'mark':powers(zm['mean']),'space':powers(zs['mean']),'off':loads['off']}
                result,_,rtrace=run_cycle(net,schedule(60,300,'MO5'),q)
                ripple=audio(net,zm,256)
                peak=result['periodic_max_C']['PA_junction']+ripple['positive_ripple_C']['PA_junction']
                balance=zm['mean']['DC_input_W']-sum(zm['mean'][k] for k in ['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W'])
                assert abs(balance)<1e-8
                reflections.append(dict(absorbed_fraction=fraction,PA_mean_W=zm['mean']['PA_W'],pass_mean_W=zm['mean']['pass_W'],
                    helper_mean_W=zm['mean']['helper_W'],peak_regulated_current_A=mark['maximum']['regulated_current_A'],
                    same_point_energy_balance_W=balance,periodic=result,ripple=ripple,PA_peak_with_periodic_audio_C=peak,
                    PA_125C_ceiling_met=peak<=125,PA_110C_target_met=peak<=110,
                    native_NTC_trip_expected=result['periodic_max_C']['NTC']>=65.85,
                    qualification='Bounded sensitivity; actual reflected-power absorption and drain-current shift require RF measurements'))
                if source_R>15 and capacity==1 and fraction==1:traces=rtrace
            rows.append(dict(source_to_bar_R_K_W=source_R,capacity_scale=capacity,
                known_Cu_via_storage=net.config['known_Cu_via_storage'],normal_peak_C=normal['periodic_max_C']['PA_junction'],
                held_AF_crest_230ms=frozen,RF_absorption=reflections))
    operating_sweep=[]
    for eta in [.4,.45,.5]:
        for source_R in [primary,better,grease,6.]:
            for capacity in [.1,1.,3.]:
                net=Network(source_R=source_R,capacity_scale=capacity)
                mark=operating(1.,eta=eta,waveform=True,phases=256);space=operating(1.,eta=eta,tone=False)
                for fraction in [.5,1.]:
                    zm=absorbed(mark,fraction);zs=absorbed(space,fraction)
                    q={'mark':powers(zm['mean']),'space':powers(zs['mean']),'off':np.zeros(len(NAMES))}
                    result,_,_=run_cycle(net,schedule(60,300,'MO5'),q)
                    ripple=audio(net,zm,256);peak=result['periodic_max_C']['PA_junction']+ripple['positive_ripple_C']['PA_junction']
                    operating_sweep.append(dict(eta_carrier_assumed=eta,source_to_bar_K_W=source_R,capacity_scale=capacity,
                        absorbed_fraction=fraction,peak_rail_current_A=mark['maximum']['regulated_current_A'],
                        nominal_current_trip_A=1.797,PA_mean_mark_W=zm['mean']['PA_W'],pass_mean_mark_W=zm['mean']['pass_W'],
                        PA_peak_with_audio_C=peak,pass_case_peak_C=result['periodic_max_C']['pass_case'],NTC_peak_C=result['periodic_max_C']['NTC'],
                        PA_125C_met=peak<=125,physical='NOT_RUN'))
    save('native-fault-envelope.json',dict(status='CALCULATED_SOURCE_PATH_AND_PROTECTION_CLOSURE_OPEN',
        native_inputs={'watchdog':p['U201'],'CWD':p['R201']},watchdog_interval_s=[.170,.230],
        assumptions=['The current stays at the nominal calibrated value under a changed RF load; this is a sensitivity, not a manufacturer curve',
                     'PA heat increases only by RF power not delivered; pass/helper/DC input stay at the same electrical point',
                     'No reflected-power detector exists in the native netlist. Valid application progress can keep WDI alive after an antenna fault',
                     'A stopped AF waveform can retain a crest command until the independent watchdog withdraws permission',
                     '800Hz ripple included separately, known via/copper storage retained; package/FR4 capacitances are bounded assumptions'],
        cases=rows,operating_efficiency_sweep=operating_sweep,physical='NOT_RUN'))
    import os;os.environ.setdefault('MPLCONFIGDIR','/tmp/m5b-e6-matplotlib')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    if traces:
        a=np.array([[x[0],*x[2:]] for x in traces]);fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
        for key in ['PA_junction','PA_source_case','pass_case','shared_plate','NTC']:ax.plot(a[:,0],a[:,NAMES.index(key)+1],label=key)
        ax.axhline(125,color='red',ls='--',label='PA125°C ceiling');ax.axhline(110,color='orange',ls=':',label='PA110°C target')
        ax.set(xlabel='Classic cycle / s',ylabel='temperature / °C',title='RF absorption sensitivity, same DC point; not a measured antenna fault');ax.legend();ax.grid()
        fig.savefig(OUT/'fault-response.pdf');fig.savefig(OUT/'fault-response.png',dpi=150);plt.close(fig)
    for z in rows:
        if z['capacity_scale']==1:print('Rsource',round(z['source_to_bar_R_K_W'],3),'absorbedRFpeak',[(a['absorbed_fraction'],round(a['PA_peak_with_periodic_audio_C'],1)) for a in z['RF_absorption']],flush=True)


if __name__=='__main__':main()
