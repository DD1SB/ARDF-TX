#!/usr/bin/python3
"""Candidate basket accounting and transparent unmeasured RF/energy models."""
import collections,csv,itertools,json,math
from m5a_r4_design import ROOT,DEST,OUT
from m5a_r1_costs import effective,price

def write(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def table(name,rows):
    with (OUT/name).open('w')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def purchased(p):return not p['ref'].startswith(('#','TP','TL'))
def costs():
    parts=json.loads((DEST/'RF2M.electrical.json').read_text())['parts'];rows=[];summ=[];delta=[]
    variants={'BOOST2S':{'ALL','NORMAL','BOOST2S'},'BUCK4S':{'ALL','NORMAL','BUCK4S'},'TRAIN_ONLY':{'ALL','TRAIN_ONLY'}}
    core={'source','source_filter','driver','pa','pa_match','bias','output_filter','am','modulator','driver_supply'}
    old=json.loads((DEST/'review/M5A-R3/costs.json').read_text())['summary'];r1=json.loads((DEST/'review/M5A-R1/costs.json').read_text())['summary']
    for var,pops in variants.items():
      ps=[p for p in parts if purchased(p)and p['population']in pops]
      for q in [6,10,20]:
        demand=collections.Counter(effective(p,var)[1]for p in ps);blocks=collections.defaultdict(float);classes=collections.defaultdict(float);cor=0;openamount=0
        for p in ps:
          value,mpn=effective(p,var);need=demand[mpn]*q;order=math.ceil(max(need,p['moq'])/p['multiple'])*p['multiple'];unit=max(price(x,order)for x in ps if effective(x,var)[1]==mpn);allocated=unit*order/need
          cls='CURRENT_INDEXED_OBSERVATION'if p['evidence'].startswith('OBSERVED_2026_10_16')else'HISTORICAL_INDEXED_OBSERVATION'if p['evidence'].startswith('OBSERVED')else'ESTIMATE'
          classes[cls]+=allocated;blocks[p['group']]+=allocated
          if p['group']in core:cor+=allocated
          if p['mpn'].startswith('OPEN')or not p['footprint']:openamount+=allocated
          rows.append(dict(variant=var,fleet=q,ref=p['ref'],value=value,MPN=mpn,footprint=p['footprint']or'OPEN',function=p['group'],quantity_per_board=1,pooled_demand=need,order_quantity=order,MOQ=p['moq'],multiple=p['multiple'],unit_net_EUR=unit,allocated_per_board_net_EUR=allocated,evidence=cls,supplier=p['supplier'],supplier_PN=p['supplier_part_number'],availability=p['availability'],source=p['source_url'],note=p['note']))
        x=dict(variant=var,fleet=q,physical_components=len(ps),IC_count=sum(p['ref'].startswith('U')for p in ps),component_net_EUR=sum(blocks.values()),RF_core_net_EUR=cor,blocks=dict(blocks),price_evidence=dict(classes),amount_with_OPEN_MPN_or_footprint_EUR=openamount,OPEN_MPN=[p['ref']for p in ps if p['mpn'].startswith('OPEN')],OPEN_footprint=[p['ref']for p in ps if not p['footprint']]);summ.append(x)
        o=next(z for z in old if z['variant']==var and z['fleet']==q);r=next(z for z in r1 if z['variant']==var and z['fleet']==q)
        delta.append(dict(variant=var,fleet=q,R3_EUR=o['net_eur_allowance'],R4_EUR=x['component_net_EUR'],saving_vs_R3_EUR=o['net_eur_allowance']-x['component_net_EUR'],R1_EUR=r['component_allowance_net_eur'],saving_vs_R1_EUR=r['component_allowance_net_eur']-x['component_net_EUR'],R3_parts=o['physical_components'],R4_parts=len(ps),R3_IC=o['IC_count'],R4_IC=x['IC_count']))
    table('RF2M_BOM.csv',rows);table('comparison.csv',delta)
    table('positions.csv',[{k:p[k]for k in ['ref','value','mpn','footprint','group','population','evidence','source_url','note']}for p in parts])
    # Component-by-component historical ledger, including genuine additions.
    import subprocess
    prev={p['ref']:p for p in json.loads(subprocess.check_output(['git','show','m5a-r3:hardware/2m/RF2M.electrical.json']))['parts']}
    current={p['ref']:p for p in parts};changes=[]
    for ref in sorted(prev.keys()|current.keys()):
        a=prev.get(ref);b=current.get(ref)
        if a and b and all(a.get(k)==b.get(k)for k in ['value','mpn','pins','footprint','population','price_breaks_eur']):continue
        changes.append(dict(ref=ref,change='ADDED'if not a else'REMOVED'if not b else'CHANGED',old=a,new=b))
    write('component-delta.json',changes)
    write('costs.json',dict(date='2026-10-16',currency='EUR',VAT='EXCLUDED; actual destination VAT separate.19% illustration only, not assumed for all purchases.',status='CONDITIONAL CANDIDATE BASKETS, NOT QUOTED OR ORDERABLE RELEASE',summary=summ,comparison=delta,RF_core_definition=sorted(core),not_purchased_positions=[p['ref']for p in parts if not purchased(p)],external_estimates=dict(bare_PCB_per_board_at6=6,bare_PCB_per_board_at10=4.5,bare_PCB_per_board_at20=3.5,RF_harness_extra=3,antenna_feeder=12,thermal_and_mounting=7,scope='Separate provisional estimates, board dimensions/stackup and quotations NOT established. No savings booked from hypothetical area or labor.'),labor='EXCLUDED, record assembly/alignment minutes on first complete build',uncertainty='Only indexed listings are observations; all other prices are estimates. Exact OPEN MPN/footprint amount is quantified rather than hidden in a contingency. MOQ1 on estimates is assumed, not supplier verified. No component omitted for an unquoted position.'))
    for x in summ:print(x['variant'],x['fleet'],round(x['component_net_EUR'],2),x['physical_components'],x['IC_count'])

def power():
    rf=[];drive=[]
    for erp,gain,m in itertools.product([1,.9,.3],[-1,0],[.75,.8]):
        pc=erp/10**(gain/10);pep=pc*(1+m)**2;final=pep*10**(.75/10)
        rf.append(dict(ERP_W=erp,net_antenna_gain_dBd=gain,depth=m,connector_carrier_W=pc,connector_mean_RF_W=pc*(1+m*m/2),connector_PEP_W=pep,final_PEP_0p75dB_matching_plus_LPF_loss_W=final,optional_1dB_capability_W=final*10**.1))
        if erp==1 and m==.8:
          for gp in [15,17,19,20,22]:
            pout=10*math.log10(final*1000)-gp+1
            drive.append(dict(net_antenna_gain_dBd=gain,final_gain_dB_ASSUMED=gp,input_matching_loss_dB_ASSUMED=1,driver_output_dBm=pout,required_driver_P1dB_dBm=pout+3,optional_1dB_adds_dB=1))
    table('RF_power.csv',rf);table('driver_budget.csv',drive)
    # An explicit ideal model; not a measured PA envelope or guaranteed thermal design.
    therm=[]
    for profile,crest,erp,eff in [('full',7.2,1,.50),('reduced',4.0,.3,.40)]:
      for m in [.75,.8]:
        vc=crest/(1+m);vin=9.021;ic=erp*10**(.175)/(vc*eff);avg=(vin-vc)*ic-vc*ic*m*m/2;no=(vin-vc)*ic
        therm.append(dict(profile=profile,depth=m,upstream_V=vin,PA_crest_V=crest,PA_center_V=vc,PA_trough_V=vc*(1-m),carrier_drain_current_A_ASSUMED=ic,crest_current_A_ASSUMED=ic*(1+m),pass_mean_AM_W=avg,pass_no_tone_W=no,pass_worst_instant_W=ic/vc*vin*vin/4,case_C_at40C_ambient_5KperW_sink_plus1KperW_interface=40+no*6,junction_C_same_RthJC2p5=40+no*(6+2.5),NTC_trip_model_C=66,qualification='IDEAL current proportional to voltage ONLY; PA transfer/knee/gain, SOA and thermal contact NOT_RUN'))
    table('thermal.csv',therm)
    # Input power is budgeted conservatively independently of the ideal RF thermal example.
    states=[];end=[]
    for profile,crest,erp,paeta,target in [('full',7.2,1,.50,12),('reduced',4.0,.30,.40,24)]:
      for arch,eta in [('BOOST2S',.87),('BUCK4S',.91)]:
        vin=(7.5096 if profile=='reduced' else 8.9996) if arch=='BUCK4S' else 9.02086
        vc=crest/1.8;ic=erp*10**.175/(vc*paeta);active9=vin*(ic+.146)+.1
        idle=.14+.04;avg=idle+.2*active9/eta;beacon=idle+active9/eta
        states.append(dict(profile=profile,variant=arch,controller_W_ASSUMED=.14,RF_idle_W_ASSUMED=.04,upstream_V=vin,PA_carrier_V_IDEAL=vc,PA_carrier_current_A_DERIVED=ic,PA_efficiency_ASSUMED=paeta,driver_current_A=.146,active_upstream_W_CALCULATED=active9,converter_efficiency_ASSUMED=eta,duty=.2,mean_battery_W=avg,need12_Wh=12*avg,need24_Wh=24*avg,beacon_battery_W=beacon,RF_and_current_measurements='NOT_RUN'))
        for pack,cells in [('2S2P',4),('2S3P',6),('2S4P',8),('4S1P',4),('4S2P',8)]:
          if pack.startswith('2S')!=(arch=='BOOST2S'):continue
          for cls,wh in [('2450mAh_min',8.82),('M35A_min_energy',11.90)]:
            usable=cells*wh*.8*.9*.9
            for lora,extra in [('absent',0),('intermittent',.006),('continuous_RX_plus_bursts',.045587)]:
              hours=usable/(avg+extra)
              end.append(dict(profile=profile,variant=arch,pack=pack,cell_class=cls,LoRa=lora,usable_Wh_ASSUMED=usable,mean_battery_W=avg+extra,hours_MODELED=hours,target_h=target,arithmetic_meets=hours>=target,margin20percent=hours>=target*1.2,continuous_beacon_h=usable/(beacon+extra),measured='NOT_RUN'))
    table('operating-states.csv',states);table('endurance.csv',end)
    sensitivity=[]
    for ctrl,rf,eta in itertools.product([.14,.28,.5],[6,8.2,10.5],[.78,.87,.91]):
        pw=ctrl+.04+.2*rf/eta;sensitivity.append(dict(controller_W=ctrl,active9V_W=rf,efficiency=eta,need12_Wh=pw*12,need24_Wh=pw*24,RF_power_not_established=True))
    table('sensitivity.csv',sensitivity)
    pa_sensitivity=[]
    for arch,vin in [('BOOST2S',9.02086),('BUCK4S',7.5096)]:
      for eta,ctrl,driver in itertools.product([.35,.40,.50,.55],[.14,.28],[.146,.18]):
        ic=.30*10**.175/((4/1.8)*eta);active=vin*(ic+driver)+.10;conv=.87 if arch=='BOOST2S' else .91
        mean=ctrl+.04+.2*active/conv
        pa_sensitivity.append(dict(variant=arch,profile='reduced',PA_efficiency_ASSUMED=eta,controller_W=ctrl,driver_current_A=driver,mean_battery_W=mean,need24_Wh=24*mean))
    table('reduced-efficiency-sensitivity.csv',pa_sensitivity)
    # LPF response from actual documented topology including finite inductor Q.
    import cmath
    response=[]
    def mul(a,b):return [[sum(a[i][k]*b[k][j]for k in range(2))for j in range(2)]for i in range(2)]
    for freq in [144.5e6,144.9e6,289.4e6,434.1e6]:
        for qual in [40,80,1000000]:
            w=2*math.pi*freq;M=[[1+0j,0j],[0j,1+0j]]
            caps=[22,27,22,15]
            for i in range(4):
                M=mul(M,[[1,0],[1j*w*caps[i]*1e-12,1]])
                if i<3:
                    L=[39,22,27][i]*1e-9;C=[3.3,18,12][i]*1e-12;zl=w*L/qual+1j*w*L;z=1/(1/zl+1j*w*C);M=mul(M,[[1,z],[0,1]])
            s21=2/(M[0][0]+M[0][1]/50+50*M[1][0]+M[1][1]);s11=(M[0][0]+M[0][1]/50-50*M[1][0]-M[1][1])/(2/s21)
            response.append(dict(frequency_Hz=freq,inductor_Q_ASSUMED=qual,S21_dB_CALCULATED=20*math.log10(abs(s21)),S11_dB_CALCULATED=20*math.log10(abs(s11)),model='Lumped50ohm ABCD only; no pads/ESL/tolerance/microstrip/PA interaction, NOT measured nor SPICE'))
    table('LPF_model.csv',response)
    # Read actual resistor values. Physical comparator latency and capacitor properties remain assumptions.
    ps={p['ref']:p for p in json.loads((DEST/'RF2M.electrical.json').read_text())['parts']}
    def ohms(ref):
        v=ps[ref]['value'];return float(v[:-1])*1000 if v.endswith('k')else float(v)
    a,b,c,d=[ohms(x)for x in ['R815','R816','R817','R818']];tol=.001
    trip=2.495*d/(c+d)*(1+a/b)
    hi=2.495*1.015*d*(1+tol)/(c*(1-tol)+d*(1+tol))*(1+a*(1+tol)/(b*(1-tol)))
    lo=2.495*.985*d*(1-tol)/(c*(1+tol)+d*(1-tol))*(1+a*(1-tol)/(b*(1+tol)))
    maximum=hi+(16.8-hi)*(1-math.exp(-20e-6/(8.118*120e-6)))+(16.8-hi)/8.118*.1
    write('calculations.json',dict(buck_reduced_nominal_V=.596*12.6,buck_full_nominal_V=.596*(12.6+116/46.4),boost_nominal_V=1.229*7.34,AM_reference_scale=2.8,full_80pct_ideal_reference_center_V=4/2.8,full_80pct_ideal_reference_trough_V=.8/2.8,full_80pct_ideal_reference_crest_V=7.2/2.8,helper_current_limit_A=.6/8.2,driver_OV_nominal_V=trip,driver_OV_min_V_under_assumed_1p5percent_reference=lo,driver_OV_max_V_under_same=hi,driver_20us_RC_plus_ESR_upper_calculation_V=maximum,driver_fault_model_assumptions='16.8V sustained source;Rmin8.118ohm;Cmin120uF;ESRmax0.1ohm;0.1percent dividers;reference +/-1.5percent;20us FROM threshold crossing to isolation. No inductive overshoot or hardware timing proof.',pass_SOA='ST D45H11 RthJC2.5K/W;hot DC/repetitive SOA NOT established by power rating',all_hardware_tests='NOT_RUN',source_and_training_overhead='RF_idle40mW and controller140mW assumptions from existing models. Measure3.3Vrail states, no invented measured currents.'))

if __name__=='__main__':costs();power()
