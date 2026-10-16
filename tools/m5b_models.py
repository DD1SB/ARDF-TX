#!/usr/bin/python3
"""Transparent M5B materials and analytic RF/power calculations. No measurements."""
import collections,csv,hashlib,itertools,json,math,subprocess,cmath
from pathlib import Path
from m5a_r1_costs import effective,price
from m5b_design import HW,OUT
from m5b_footprints import microstrip,width50

def write(n,x):(OUT/n).write_text(json.dumps(x,indent=2)+'\n')
def tab(n,rows):
    with(OUT/n).open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def purchased(p):return not p['ref'].startswith(('#','TP','TL'))

def costs():
    data=json.loads((HW/'RF2M.electrical.json').read_text());parts=data['parts']
    # Reproducible current source observations, separate from exact CAD fields.
    updates={
        'J701':dict(price_breaks_eur={'1':3.68,'25':3.34,'50':3.13},evidence='OBSERVED_2026_10_16_INDEXED',availability='Indexed3444/3192EUstock,MOQ1. Reconfirm;not a reserved quote.',supplier='Mouser Europe',supplier_part_number='710-66012102111404',price_source_url='https://www.mouser.fi/ProductDetail/Wurth-Elektronik/66012102111404?qs=uwxL4vQweFOxFryf63clWg%3D%3D'),
        'L301':dict(price_breaks_eur={'1':1.27,'10':1.05,'25':.912},evidence='OBSERVED_2026_10_16_INDEXED',availability='ZERO indexed stock;MOQ1 backorder;October/November incoming dates require confirmation.',supplier='Mouser Germany',supplier_part_number='652-SRP1265A-100M',price_source_url='https://www.mouser.de/de/ProductDetail/Bourns/SRP1265A-100M?qs=sGAEpiMZZMv126LJFLh8y36wtw7x1v3mwdR0qvJGqrs%3D'),
        'L302':dict(price_breaks_eur={'1':1.20,'10':.989,'25':.86},evidence='OBSERVED_2026_10_16_INDEXED',availability='Indexed7309/8319EUstock;cutMOQ1;reconfirm.',supplier='Mouser Europe',supplier_part_number='652-SRP1265A-4R7M',price_source_url='https://www.mouser.at/ProductDetail/Bourns/SRP1265A-4R7M?qs=7z%252BmIopC6%2FJSLqjYt7xEMQ%3D%3D'),
        'L604':dict(price_breaks_eur={'1':1.56,'10':1.32,'25':1.22},evidence='OBSERVED_2026_10_16_INDEXED',availability='Indexed690EUstock;MOQ1cut. Reconfirm before procurement.',supplier='Mouser Europe',supplier_part_number='994-1812SMS-R15JLC',price_source_url='https://www.mouser.at/de/ProductDetail/Coilcraft/1812SMS-R15JLC?qs=zCSbvcPd3pbBFWMl4xhz9Q%3D%3D'),
        'L634':dict(availability='NON_STOCKED;Mouser994-0603HC-47NXJRW cutMOQ1,estimated9weekfactoryleadtime;price0.75EUR remains estimate. Current W replaces obsolete U.',supplier='Mouser Europe',supplier_part_number='994-0603HC-47NXJRW'),
        'U950':dict(availability='DigiKeyregionalcaches conflict:FI17344vsIE0withDec2026incoming. MOQ1offering;0.664EURcandidateestimate,not stock assurance.'),
    }
    for p in parts:
        if p['ref']in updates:p.update(updates[p['ref']])
    # Procurement metadata only; no electrical/footprint/value mutations.
    (HW/'RF2M.electrical.json').write_text(json.dumps(data,indent=2)+'\n')
    old=json.loads((HW/'review/M5A-R4/costs.json').read_text())['summary'];rows=[];summary=[];delta=[]
    core={'source','source_filter','driver','pa','pa_match','bias','output_filter','am','modulator','driver_supply'}
    for v,pops in {'BOOST2S':{'ALL','NORMAL','BOOST2S'},'BUCK4S':{'ALL','NORMAL','BUCK4S'},'TRAIN_ONLY':{'ALL','TRAIN_ONLY'}}.items():
      ps=[p for p in parts if purchased(p)and p['population']in pops]
      for q in [6,10,20]:
        demand=collections.Counter(effective(p,v)[1]for p in ps);blocks=collections.defaultdict(float);classes=collections.defaultdict(float)
        for p in ps:
            val,mpn=effective(p,v);need=demand[mpn]*q;order=math.ceil(max(need,p['moq'])/p['multiple'])*p['multiple'];u=max(price(x,order)for x in ps if effective(x,v)[1]==mpn);allocated=u*order/need
            cls='CURRENT_INDEXED_OBSERVATION'if p['evidence'].startswith('OBSERVED_2026_10_16')else'HISTORICAL_INDEXED_OBSERVATION'if p['evidence'].startswith('OBSERVED')else'ESTIMATE_UNQUOTED';blocks[p['group']]+=allocated;classes[cls]+=allocated
            rows.append(dict(population=v,fleet=q,ref=p['ref'],value=val,MPN=mpn,footprint=p['footprint'],block=p['group'],per_board_quantity=1,pooled_order=order,MOQ=p['moq'],multiple=p['multiple'],component_unit_net_EUR=u,allocated_per_board_net_EUR=allocated,evidence=cls,supplier=p['supplier'],supplier_part=p['supplier_part_number'],availability=p['availability'],source=p.get('price_source_url',p['source_url']),manufacturer_document=p['source_url']))
        o=next(x for x in old if x['variant']==v and x['fleet']==q);cost=sum(blocks.values());s=dict(population=v,fleet=q,physical_components=len(ps),IC_count=sum(p['ref'].startswith('U')for p in ps),component_net_EUR=cost,RF_core_net_EUR=sum(z for b,z in blocks.items()if b in core),blocks=dict(blocks),price_evidence=dict(classes),unquoted_net_EUR=classes['ESTIMATE_UNQUOTED'],R4_net_EUR=o['component_net_EUR'],delta_net_EUR=cost-o['component_net_EUR'],fleet_components_net_EUR=cost*q);summary.append(s)
        delta.append({k:s[k]for k in ['population','fleet','R4_net_EUR','component_net_EUR','delta_net_EUR','physical_components','IC_count','unquoted_net_EUR']})
    tab('RF2M_BOM.csv',rows);tab('cost-delta.csv',delta);write('costs.json',dict(currency='EUR',VAT='EXCLUDED;Germany19percent illustration only;shipping/destination VAT separate',date='2026-10-16',summary=summary,not_quoted=True,external=dict(evaluation_PCB_5board_batch_net_EUR_range=[60,100],prototype_shipping_net_EUR_range=[10,25],production_bare_PCB_estimate_each_at6_10_20=[12,9,7],thermal_material_each_net_EUR_estimate=12,harness_each_net_EUR_estimate=3,antenna_feeder_each_net_EUR_estimate=12,optional_driver_load_R651_net_EUR_estimate=.025),observed_thermal_comparator=dict(MPN='SK 48 50 SA',supplier='Buerklin72B792',quantity1_gross_EUR=3.7128,quantity10_gross_EUR=3.4391,net1_EUR=3.7128/1.19,net10_EUR=3.4391/1.19,stock_indexed=17,source='https://www.buerklin.com/en/p/fischer-elektronik/heat-sinks/sk-48-50-sa/72B792/'),labor='EXCLUDED;measure first complete assembly/alignment time;no speculative labor saving booked'))
    tab('component-fields.csv',[{k:p[k]for k in ['ref','value','mpn','footprint','population','group','evidence','source_url','note']}for p in parts])
    for v in ['BOOST2S','BUCK4S','TRAIN_ONLY']:tab('BOM_'+v+'.csv',[r for r in rows if r['population']==v and r['fleet']==10])
    for x in summary:print(x['population'],x['fleet'],round(x['component_net_EUR'],2),'unquoted',round(x['unquoted_net_EUR'],2),x['physical_components'],x['IC_count'])

def calculations():
    w=width50();z,ee=microstrip(w);zo,eo=microstrip(.92,.508,.07,4.3);f=144.7e6;c=299792458
    tl=[]
    for ref,l in [('TL603',6.23),('TL604',6.62),('TL605',5.8),('TL606',2.2),('TL607',11),('TL608',12.4),('TL609',2)]:
        a=360*f*l/1000*math.sqrt(eo)/c;b=360*f*l/1000*math.sqrt(ee)/c;tl.append(dict(ref=ref,ST_length_mm=l,M5B_length_mm=l,ST_width_mm=.92,M5B_width_mm=w,ST_Z0_model_ohm=zo,M5B_Z0_model_ohm=z,ST_phase_deg=a,M5B_phase_deg=b,delta_phase_deg=b-a,electrical_length_preserving_scale=math.sqrt(eo/ee)))
    tab('transmission-lines.csv',tl)
    def mul(a,b):return [[sum(a[i][k]*b[k][j]for k in range(2))for j in range(2)]for i in range(2)]
    def line(l):
        t=2*math.pi*f*l/1000*math.sqrt(ee)/c;return [[math.cos(t),1j*z*math.sin(t)],[1j/z*math.sin(t),math.cos(t)]]
    omega=2*math.pi*f;M=[[1+0j,0j],[0j,1+0j]]
    for a in [line(6.23),[[1,0],[1j*omega*22e-12,1]],[[1,1/(1j*omega*330e-12)],[0,1]],line(6.62),[[1,0],[1j*omega*22e-12,1]],[[1,1j*omega*47e-9],[0,1]],line(5.8)]:M=mul(M,a)
    gate_intrinsic=3+1/(1j*omega*80e-12)
    bias_feed=1j*omega*33e-9
    gate_complete=gate_intrinsic*bias_feed/(gate_intrinsic+bias_feed)
    zi=(M[0][0]*gate_complete+M[0][1])/(M[1][0]*gate_complete+M[1][1])
    rl=-20*math.log10(abs((zi-50)/(zi+50)))
    sens_gate=[]
    for rr,cc in itertools.product([1,3,6,10],[40,60,80,100,120,160]):
        zz=rr+1/(1j*omega*cc*1e-12);zz=zz*bias_feed/(zz+bias_feed);zin=(M[0][0]*zz+M[0][1])/(M[1][0]*zz+M[1][1]);sens_gate.append(dict(intrinsic_R_ohm_ASSUMED=rr,intrinsic_C_pF_ASSUMED=cc,bias_feed_nH=33,Zin_real_ohm=zin.real,Zin_imag_ohm=zin.imag,return_loss_dB_MODEL=-20*math.log10(abs((zin-50)/(zin+50))),physical='NOT_RUN'))
    tab('input-match-sensitivity.csv',sens_gate)
    # The load impedance which would make THIS lossless initial network look50ohms.
    # This is not a measured PD54008 input impedance!
    zl=(M[0][1]-50*M[1][1])/(50*M[1][0]-M[0][0])
    pre=.8*(1+58.2/10);prelo=.8*.99*(1+58.2*.999/(10*1.001));prehi=.8*1.01*(1+58.2*1.001/(10*.999))
    trip=2.495*10/(29.4+10)*(1+73.2/10)
    current_ref=2.495*470/(620+470);current_ratio=4.02/(5.11+4.02);old_needed=current_ref/(4.02/(10+4.02));current_needed=current_ref/current_ratio;current_trip=current_needed/(20*.068)
    # Independent reference and precision-divider tolerance bounds.
    lo=2.495*.985*10*.999/(29.4*1.001+10*.999)*(1+73.2*.999/(10*1.001));hi=2.495*1.015*10*1.001/(29.4*.999+10*1.001)*(1+73.2*1.001/(10*.999))
    write('calculations.json',dict(current_protection=dict(old_required_INA_output_V=old_needed,INA_supply_V=3.3,new_required_INA_output_V=current_needed,new_trip_A=current_trip,new_shunt_ohm=.068,new_divider_top_ohm=5110,new_divider_lower_ohm=4020,qualification='Static scale correction only;dynamic response NOT_RUN'),MMIC_bias=dict(old_choke_max_DCR_ohm=1.65,new_choke_max_DCR_ohm=.033,new_choke_nH=150,at180mA_old_drop_V=.18*1.65,at180mA_new_drop_V=.18*.033,bias_min_before_switch_trace_loss_V=5*(1-.0175)-.18*.033*1.3,qualification='DC tolerance model only;measure MMIC bias and RF output under load'),status='ANALYTIC_ESTIMATES_ONLY',microstrip=dict(finished_mm=.8,h_mm=.64,t_mm=.07,FR4_Dk_assumed=4.3,width_mm=w,Z0_ohm=z,effective_Dk=ee,approximation='Hammerstad/Jensen quasi-static, soldermask/pads/fringing not included'),initial_ST_input_network_50ohm_target_load=dict(real_ohm=zl.real,imag_ohm=zl.imag,interpretation='Inverse network calculation INCLUDING the retained33nH gate-feed shunt in the assumed load;NOT manufacturer144MHzimpedance or a measured50ohm interstage',assumed_intrinsic_R_ohm=3,assumed_intrinsic_C_pF=80,assumed_gate_with_feed_real_ohm=gate_complete.real,assumed_gate_with_feed_imag_ohm=gate_complete.imag,assumed_source_Zin_real_ohm=zi.real,assumed_source_Zin_imag_ohm=zi.imag,assumed_model_return_loss_dB=rl,limitations='Lossless lumped model;CISS is1MHz/zero-bias value,not144MHzlarge-signal;pad/bias-decoupler ESL/device feedback omitted. Physical tuning mandatory.'),driver=dict(target_dBm=19,target_mW=10**1.9,P1dB_typical_nearby_MHz=[50,200],P1dB_typical_dBm=[22.70,22.64],initial_pi_series_ohm=71.5,initial_pi_shunts_ohm=96.5,initial_pad_dB=10,calibration_pad_options_dB=[6,8,10],required_PA_gain_dB_at_minus1dBd=10*math.log10(4.079*10**(.75/10)*1000)-19+1,source_budget_assumed=dict(buffer_fundamental_dBm=10.4,filter_loss_dB=1.,pad6dB_driver_input_dBm=3.4,MMIC_gain_dB=16,MMIC_output_dBm=19.4),all_RF_measurements='NOT_RUN'),driver_protection=dict(prereg_nominal_V=pre,prereg_min_V=prelo,prereg_max_V=prehi,driver_OV_nominal_V=trip,driver_OV_min_V=lo,driver_OV_max_V=hi,nominal_output_min_max_V=[4.8,5.2],MMIC_absmax_V=6,TPS22810_recommended_max_V=18,TPS22810_absmax_V=20,TLV767_recommended_input_max_V=16,TLV767_absmax_input_V=18,TLV761_recommended_input_max_V=18,TLV761_absmax_input_V=20,fault_source_max_AT_PIN_V=16.8,fault_test_acceptance_MMIC_node_max_V=5.7,current_test_A=.18,old_20us_assumption='NOT relied upon as sole voltage barrier;fault detector/isolation times still measured',fault_limits='16.8Vfault exceeds TLV76716Vrecommended VIN;within18Vabs ONLY. Power-only bounded test and single-failure backupLDO;not normal operation or proof of unrestricted surge immunity.'),thermal=dict(NTC_B_K=3977,NTC_low_trip_ohm=10000*10/49.9,NTC_nominal_trip_C=1/(1/298.15+math.log(10/49.9)/3977)-273.15,pass_RthJC_K_per_W=2.5,pass_sink_max_K_per_W=3.5,pass_interface_assumed_K_per_W=1,case_acceptance_C=60,junction_engineering_limit_C=125,ambient_C=40,PA_RthJC_K_per_W=3,thermal_via_model_K_per_W_each=.0008/(385*math.pi*.0003*.000025),thermal_vias=12,qualification='NOT_RUN;plating/solder voids/spreading/contact are not proven by cylindrical-via model. Sensor lag/hot SOA remain open.'),physical_tests='NOT_RUN'))
    erp=[];therm=[];states=[];end=[]
    for gain,carrier,m in itertools.product([-1,0],[1,.9,.3],[.75,.8]):
        pc=carrier/10**(gain/10);pep=pc*(1+m)**2
        erp.append(dict(ERP_W=carrier,net_gain_dBd=gain,m=m,conducted_carrier_W=pc,average_RF_W=pc*(1+m*m/2),connector_PEP_W=pep,final_PEP_plus0p75dB_loss_W=pep*10**.075,optional_plus1dB_capability_W=pep*10**.175))
    for mode,crest,carrier,etaPA,target in [('full',7.2,1,.5,12),('reduced',4.,.3,.4,24)]:
      for v,eff in [('BOOST2S',.87),('BUCK4S',.91)]:
        bus=7.5096 if mode=='reduced'and v=='BUCK4S'else 9.021;vc=crest/1.8;ic=carrier*10**.175/(vc*etaPA);idrv=.1463;active=bus*(ic+idrv)+.10;mean=.18+.2*active/eff;continuous=.18+active/eff
        loss=(bus-vc)*ic-vc*ic*.8*.8/2;notone=(bus-vc)*ic
        therm.append(dict(mode=mode,population=v,carrier_center_V=vc,crest_V=crest,trough_V=vc*.2,carrier_Id_A_ASSUMED=ic,crest_Id_A_ASSUMED=ic*1.8,pass_AM_average_W=loss,pass_no_tone_W=notone,pass_case_no_tone_C=40+notone*4.5,pass_junction_no_tone_C=40+notone*7,measured='NOT_RUN'))
        states.append(dict(mode=mode,population=v,duty=.2,controller_W=.14,RF_idle_W=.04,driver_A=idrv,PA_efficiency_ASSUMED=etaPA,converter_efficiency_ASSUMED=eff,active_upstream_W=active,mean_battery_W=mean,required12_Wh=12*mean,required24_Wh=24*mean,continuous_beacon_W=continuous,measured='NOT_RUN'))
        for pack,cells in [('2S2P',4),('2S3P',6),('2S4P',8),('4S1P',4),('4S2P',8)]:
          if pack.startswith('2S')!=(v=='BOOST2S'):continue
          for cell,wh in [('2450mAh',8.82),('M35A_min_energy',11.9)]:
           for lora,extra in [('absent',0),('intermittent',.006),('continuous_receive_bursts',.045587)]:
            usable=cells*wh*.8*.9*.9;hours=usable/(mean+extra)
            end.append(dict(mode=mode,population=v,pack=pack,cell=cell,LoRa=lora,usable_Wh_ASSUMED=usable,mean_W=mean+extra,hours_MODELED=hours,target_h=target,arithmetic_pass=hours>=target,margin20percent=hours>=1.2*target,continuous_beacon_h=usable/(continuous+extra),physical='NOT_RUN'))
    tab('RF_power.csv',erp);tab('thermal.csv',therm);tab('power-states.csv',states);tab('endurance.csv',end)
    sens=[]
    for ep,ctrl,drv,conv in itertools.product([.35,.4,.5],[.14,.28],[.1463,.18],[.78,.87,.91]):
        ic=.3*10**.175/((4/1.8)*ep);p=ctrl+.04+.2*(9.021*(ic+drv)+.1)/conv;sens.append(dict(PA_efficiency=ep,controller_W=ctrl,driver_A=drv,converter_eta=conv,BOOST_reduced_W=p,required24_Wh=24*p,status='ASSUMED_NOT_MEASURED'))
    tab('sensitivity.csv',sens)

if __name__=='__main__':costs();calculations()
