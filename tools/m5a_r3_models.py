#!/usr/bin/python3
"""R3 candidate materials and explicit ASSUMED operating-state calculations."""
import collections
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from m5a_r3_design import ROOT,DEST,OUT

def jwrite(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def csvwrite(name,rows):
    with (OUT/name).open('w')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def costs():
    from m5a_r1_costs import effective,price
    parts=json.loads((DEST/'RF2M.electrical.json').read_text())['parts']
    variants={'BOOST2S':{'ALL','NORMAL','BOOST2S'},'BUCK4S':{'ALL','NORMAL','BUCK4S'},'TRAIN_ONLY':{'ALL','TRAIN_ONLY'}}
    rows=[];summaries=[]
    for var,pops in variants.items():
      fitted=[p for p in parts if p['population']in pops and not p['ref'].startswith(('#','TP'))]
      for qty in [6,10,20]:
        demands=collections.Counter(effective(p,var)[1] for p in fitted)
        blocks=collections.defaultdict(float);classes=collections.defaultdict(float)
        for p in fitted:
            value,mpn=effective(p,var);need=demands[mpn]*qty
            order=math.ceil(max(need,p['moq'])/p['multiple'])*p['multiple'];unit=price(p,order);per_board=unit*order/need
            if p['ref']in ['Q902','Q903']:classification='CURRENT_PRICE_COMPARATOR_MANUFACTURER_UNRESOLVED'
            elif p['ref']=='Q901':classification='CURRENT_SUPPLIER_LISTING_NO_FLEET_STOCK_CONFIRMATION'
            elif p['evidence'].startswith('OBSERVED'):classification='HISTORICAL_R1_OBSERVATION_RECHECK_REQUIRED'
            else:classification='ESTIMATE_NOT_QUOTED'
            blocks[p['group']]+=per_board;classes[classification]+=per_board
            rows.append(dict(variant=var,fleet=qty,ref=p['ref'],value=value,mpn=mpn,footprint=p['footprint']or'OPEN',block=p['group'],per_board_qty=1,pooled_mpn_demand=need,allocated_purchase_quantity=order,moq=p['moq'],multiple=p['multiple'],unit_net_eur=unit,allocated_per_board_net_eur=per_board,classification=classification,supplier=p['supplier'],supplier_identifier=p['supplier_part_number'],availability=p['availability'],datasheet_or_circuit_url=p['source_url'],note=p['note']))
        summaries.append(dict(variant=var,fleet=qty,physical_components=len(fitted),IC_count=sum(p['ref'].startswith('U')for p in fitted),net_eur_allowance=sum(blocks.values()),blocks=dict(blocks),evidence_classes=dict(classes),open_footprints=[p['ref']for p in fitted if not p['footprint']],open_mpns=[p['ref']for p in fitted if p['mpn'].startswith('OPEN')]))
    csvwrite('RF2M_BOM.csv',rows)
    csvwrite('RF2M_positions.csv',[{k:p[k]for k in ['ref','sheet','value','mpn','footprint','group','population','evidence','supplier','supplier_part_number','source_url','note']}for p in parts])
    r1=json.loads((DEST/'review/M5A-R1/costs.json').read_text())['summary']
    comparison=[]
    for x in summaries:
        previous=next(v for v in r1 if v['variant']==x['variant']and v['fleet']==x['fleet'])
        comparison.append(dict(variant=x['variant'],fleet=x['fleet'],R1_net_eur=previous['component_allowance_net_eur'],R3_net_eur=x['net_eur_allowance'],delta_net_eur=x['net_eur_allowance']-previous['component_allowance_net_eur'],R1_parts=previous['fitted_physical'],R3_parts=x['physical_components'],R1_IC=previous['ic_count'],R3_IC=x['IC_count']))
    csvwrite('comparison.csv',comparison)
    old={p['ref']:p for p in json.loads((DEST/'archive/M5A-R1/RF2M.electrical.json').read_text())['parts']}
    new={p['ref']:p for p in parts}
    delta=dict(removed=sorted(old.keys()-new.keys()),introduced=sorted(new.keys()-old.keys()),modified=[r for r in sorted(old.keys()&new.keys())if any(old[r][f]!=new[r][f]for f in ['pins','value','mpn','footprint','population'])])
    jwrite('component-delta.json',delta)
    jwrite('costs.json',dict(date='2026-10-15',currency='EUR',VAT='EXCLUDED. Dönberg listing displays23%; applicability/checkout tax unresolved. No assumption of universal19% or tax deduction from gross price.',basis='Conditional candidate allowances only. Q902/Q903 supplier listings do not identify the selected manufacturer. No fleet-stock or quote confirmation. Coil3EUR positions are estimates. Not an ordering list.',summary=summaries,comparison=comparison,external_estimates_net_eur=dict(bare_board_at6=6,bare_board_at10=4.5,bare_board_at20=3.5,rf_harness_extra=3,antenna_and_feeder=12,heat_and_mechanical=7,controller=18,enclosure=5,battery_and_charger='Separate system cost, NOT included; see M2 battery cost records'),labor='Excluded; alignment minutes unknown, no fictitious savings booked'))

def power():
    rf=[]
    for erp,m in itertools.product([1,.9,.3],[.75,.8]):
        c=erp*10**.1;rf.append(dict(erp_w=erp,depth=m,carrier_conducted_w=c,average_rf_w=c*(1+m*m/2),connector_pep_w=c*(1+m)**2,connector_capability_1db_w=c*(1+m)**2*10**.1))
    jwrite('rf-power.json',rf)
    capabilities=[]
    for pep in [1.2,3.0]:
      for m in [.75,.8]:
        capabilities.append(dict(reference_connector_pep_w=pep,depth=m,carrier_w=pep/(1+m)**2,erp_minus1dbd_w=pep/(1+m)**2*10**-.1,erp_minus1dbd_with1db_reserve_w=pep/(1+m)**2*10**-.2,required_net_antenna_gain_dbd_for1erp=10*math.log10((1+m)**2/pep),qualification='1.2W publisher MaxiTX PEAK under rectangular modulation;3W is DL3BBX LOWER BOUND, not measured maximum'))
    csvwrite('reference-power-limits.csv',capabilities)
    states=[];endurance=[]
    packs={'2S2P':4,'2S3P':6,'2S4P':8,'4S1P':4,'4S2P':8}
    for mode,v,i,target in [('full',13.8,.55,12),('reduced',10.9,.30,24)]:
      for arch,eff in [('2S_boost',.87),('4S_buck',.91)]:
        # The high/low RF levels are NOT established by these assumed currents.
        active=(v*i+.10)/eff;idle=.14+.04;avg=idle+.20*active
        states.append(dict(profile=mode,architecture=arch,rail_v_assumed=v,current_a_assumed=i,current_basis='Full0.55A is middle of original0.5-0.6A no-tone adjustment range, conservatively budgeted throughout each slot; reduced0.30A is an unmeasured assumption. RF AM crests may trip the0.593A limit.',converter_efficiency_assumed=eff,RF_active_added_w_assumed=.10,controller_w_assumed=.14,RF_idle_w_assumed=.04,tx_duty=.20,mean_battery_w=avg,need12_wh=12*avg,need24_wh=24*avg,continuous_beacon_battery_w=idle+active,RF_profile_qualification='NOT_RUN: target1ERP/full and0.30ERP/reduced must be measured, not inferred from supply'))
        for pack,count in packs.items():
          if pack.startswith('2S')!=arch.startswith('2S'):continue
          for cell,wh in [('25R_2450mAh_min',8.82),('M35A_min_energy',11.90)]:
            # 4S full-voltage dropout window has no measured capacity fraction.
            fractions=[.5,.7,.9]if arch=='4S_buck'and mode=='full'else[1.0]
            for fraction in fractions:
              energy=count*wh*.8*.9*.9*fraction;hours=energy/avg
              endurance.append(dict(profile=mode,architecture=arch,pack=pack,cell_basis=cell,additional_accessible_window_assumed=fraction,usable_wh_assumed=energy,hours_calculated=hours,goal_h=target,arithmetic_meets_goal=hours>=target,margin20_percent=hours>=target*1.2,continuous_beacon_hours=energy/(idle+active),hardware_endurance='NOT_RUN'))
    csvwrite('operating-states.csv',states);csvwrite('endurance.csv',endurance)
    sensitivity=[]
    for ctrl,lora,eff,current in itertools.product([.14,.28],[0,.006,.045587],[.78,.87,.92],[.35,.50,.60]):
        avg=ctrl+.04+lora+.2*(13.8*current+.1)/eff
        sensitivity.append(dict(controller_w=ctrl,lora_w=lora,converter_eff=eff,rail_current_a=current,mean_w=avg,need12_wh=avg*12,need24_wh=avg*24,RF_output_unknown=True))
    csvwrite('sensitivity.csv',sensitivity)
    therm=[]
    for center_i in [.30,.60]:
      vin=13.8;crest=11.8;center=crest/1.8;m=.8
      p=(vin-center)*center_i-m*m*center*center_i/2
      therm.append(dict(scope='IDEAL resistive/current-proportional example, not MRF237 transfer model.0.60A center case is an overload illustration, NOT a permitted AM operating profile.',vin_v=vin,center_v=center,trough_v=center*.2,crest_v=crest,carrier_current_a_assumed=center_i,crest_current_a_assumed=center_i*1.8,pass_average_am_w=p,pass_no_tone_w=(vin-center)*center_i,maximum_instantaneous_pass_w=center_i/center*vin*vin/4,TIP127_RthJC_C_per_W=1.92,estimated_case_C_at40C_3CperW_sink_plus1CperW_interface=40+(vin-center)*center_i*4,estimated_junction_C_same=40+(vin-center)*center_i*5.92))
    jwrite('thermal-examples.json',therm)
    threshold={}
    # Loaded1V reference and comparator dividers, taken from actual R3 values.
    rlow=1/(1/470+1/20000+1/59900+1/11000)
    ref=2.495*rlow/(620+rlow)
    threshold.update(loaded_ref_v=ref,rail_current_trip_a=ref/(2*10000/(1500+10000)),reg_and_VPA_OV_nominal_v=2.495*10000/(18200+10000)*17,temperature_trip='Original approximately66C NTC model; physical case coupling/lag NOT_RUN',boost_reduced_v=1.229*(1+787000/100000),boost_full_v=1.229*(1+787000/100000+787000/332000),buck_reduced_v=.596*(1+171000/10000),buck_full_v=.596*(1+171000/10000+171000/34000))
    jwrite('electrical-calculations.json',threshold)

if __name__=='__main__':costs();power();print('R3 BOM, cost comparisons, RF arithmetic and ASSUMED energy/thermal models regenerated')
