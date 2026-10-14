#!/usr/bin/env python3
"""Independent requirements checks of exported KiCad nets and analogue arithmetic.

No assertion is a hardware measurement, RF simulation or production release.
Run after KiCad CLI ERC/netlist export; --write records the reproducible report.
"""
import argparse
import csv
import itertools
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

from m3_80m_design import parse, children

ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware/80m'

def report():
    manifest=json.loads((HW/'RF80.electrical.json').read_text())
    parts={p['ref']:p for p in manifest['parts']}
    xml=ET.parse(HW/'review/RF80.xml')
    actual={}
    for net in xml.findall('./nets/net'):
        name=net.attrib['name'].removeprefix('/')
        for node in net.findall('node'):actual[(node.attrib['ref'],node.attrib['pin'])]=name
    pins=0
    for ref,p in parts.items():
        if ref.startswith('#'):continue
        for pin,net in p['pins'].items():
            if net is not None:
                assert actual.get((ref,pin))==net,(ref,pin,net,actual.get((ref,pin)))
                pins+=1
    # Physical pin assertions independent of schematic/library drawings.
    needed={
      'U201':{'1':'POR_N','2':'V3V3','3':'GND'},
      'U313':{'1':'I_PA_RAW','2':'GND','3':'SENSE_PLUS','4':'SENSE_MINUS','5':'V3V3'},
      'U301':{'1':'GND','2':'SW_PA','3':'VIN_PA','4':'FB_PA','5':'PA_PERMIT','6':'BOOT_PA'},
      'U401':{'1':'VDRV','2':None,'3':'GATE_DRV','4':'GND','5':'PA_INB','6':'CLK_PA'},
      'Q402':{'1':'GATE_PA','2':'DRAIN_PA','3':'GND'},
      'Q403':{'1':'VPA_LOAD','2':'VPA_SHAPED','3':'SHAPE_BASE'},
      'T401':{'1':'VPA_SHAPED','2':'DRAIN_PA','3':'DRAIN_PA','4':'RF_RAW'},
      'D301':{'1':'VIN_PA','2':'VBAT_FUSED'},'D302':{'1':'VIN_PA','2':'GND'},
      'D501':{'1':'FOX_CLK','2':'FOX_CLK_B'},
      'J502':{'1':'RF_FOX','2':'GND','3':'FOX_ID'},'J401':{'1':'RF_NORMAL','2':'GND'}
    }
    for ref,pinsmap in needed.items():assert parts[ref]['pins']==pinsmap,(ref,parts[ref]['pins'])
    assert parts['Q403']['mpn']=='BD140'
    assert parts['Q401']['pins']=={'1':'PA_PERMIT','2':'PA_MUTE_MID','3':'PA_INB'}
    assert parts['Q405']['pins']=={'1':'KEY_TAIL','2':'GND','3':'PA_MUTE_MID'}
    assert parts['Q406']['pins']=={'1':'NOT_ARMED','2':'GND','3':'KEY_TAIL_RESET_D'}
    assert parts['U203']['pins']['13']=='KEY_TAIL_C' and parts['U203']['pins']['12']=='KEY_TAIL_N'
    assert parts['U212']['pins']['8']=='KEY_TAIL'
    assert parts['U212']['pins']['12']=='FOX_PERMIT' and parts['U212']['pins']['13']=='KEY_TAIL' and parts['U212']['pins']['11']=='FOX_MUTE'
    assert parts['R451']['pins']['1']=='CW_KEY'
    assert parts['U223']['pins']['1']=='RESET_N' and parts['U223']['pins']['2']=='ARM_ACCEPT' and parts['U223']['pins']['3']=='ARM_CLK' and parts['U223']['pins']['4']=='V3V3'
    assert parts['U202']['pins']['6']=='GND' and parts['U202']['pins']['14']=='GND'
    assert parts['D201']['pins']=={'1':'V3V3','2':'LEASE_RC'} and parts['D202']['pins']=={'1':'V3V3','2':'BUS_RC'}
    for ref in ('R451','D451','R452','C451','R453','Q406'):
        assert parts[ref]['population']=='BOTH'
    assert parts['D501']['mpn']=='BAT54WS-7-F'
    # No PA power or watt RF node on any low-output circuitry.
    forbidden={'RF_NORMAL','RF_RAW','DRAIN_PA','GATE_PA','VPA','VPA_ISO','VPA_LOAD','VPA_SHAPED','VIN_PA','VBAT'}
    for p in parts.values():
        if p['group']=='fox' or p['ref']=='J502':
            assert not forbidden.intersection(p['pins'].values()),p['ref']
    assert parts['U501']['pins']['14']=='VFOX'
    for pin in ('2','5','10'):assert parts['U501']['pins'][pin]=='FOX_GATE_EN'
    for ref in ('R510','R511','R512'):assert parts[ref]['pins']['2']=='FOX_SUM'
    # Pad and transmission-zero positions are different requirements from generic LPFs.
    assert set(parts['C414']['pins'].values())=={'LPF_N2','RF_NORMAL'}
    assert set(parts['C514']['pins'].values())=={'FOX_LPF2','FOX_PAD_IN'}
    assert parts['R501']['value']=='27'
    assert parts['R501']['footprint']=='Resistor_SMD:R_2512_6332Metric'
    assert parts['Q504']['pins']['3']=='FOX_GATE_EN'

    footprints=0
    for p in parts.values():
        if not p['footprint']:continue
        lib,name=p['footprint'].split(':')
        f=(HW/'ARDF_TX.pretty'/f'{name}.kicad_mod' if lib=='ARDF_TX' else Path('/usr/share/kicad/footprints')/(lib+'.pretty')/(name+'.kicad_mod'))
        assert f.exists(),(p['ref'],f)
        pads={x[1]for x in children(parse(f.read_text()),'pad')if x[1]}
        # Native passive/transistor drawings include every actual package pad;
        # explicit no-connect pins remain in the manifest.
        assert set(p['pins']).issubset(pads),(p['ref'],p['pins'],pads)
        package_nc={'U211':{'3','11'}}.get(p['ref'],set()) # 74HC21 physical NC pads; native library omits them.
        assert pads.issubset(set(p['pins'])|package_nc),(p['ref'],'unrepresented package pad',pads)
        footprints+=1
    erc=json.loads((HW/'review/ERC.json').read_text())
    violations=[v for s in erc['sheets']for v in s['violations']]
    assert not violations,violations
    assert not list(HW.rglob('*.kicad_pcb'))
    assert not list(HW.rglob('*.gbr'))

    # Audit purchase arithmetic independently of the cost generator.
    costs=json.loads((ROOT/'docs/M3_80M_COSTS.json').read_text())
    cost_baskets=0
    for scope,batches in costs['scopes'].items():
        for batch,basket in batches.items():
            by_mpn={}
            for line in basket['lines']:by_mpn.setdefault(line['mpn'],[]).append(line)
            cash=0
            for mpn,lines in by_mpn.items():
                item=lines[0];needed_count=len(lines)*int(batch)
                assert item['needed_mpn']==needed_count
                assert item['ordered_mpn']>=max(needed_count,item['moq'])
                assert item['ordered_mpn']%item['multiple']==0
                assert item['price_break']<=item['ordered_mpn']
                assert item['unit_price_eur']==item['price_breaks_eur'][str(item['price_break'])]
                cash+=item['ordered_mpn']*item['unit_price_eur']
            assert abs(cash-basket['batch_eur'])<.0001
            assert abs(cash/int(batch)-basket['per_unit_eur'])<.0001
            assert abs(sum(l['line_per_unit_eur']for l in basket['lines'])-basket['per_unit_eur'])<.0002
            cost_baskets+=1
    with (ROOT/'docs/M3_80M_BOM.csv').open()as f:csv_rows=list(csv.DictReader(f))
    assert len(csv_rows)==sum(len(b['lines'])for scope in costs['scopes'].values()for b in scope.values())
    for name in ('PA_SELECTION','SCHEMATIC_REVIEW','BOM','TEST_PLAN','REVIEW_DECISION'):
        assert (ROOT/'docs'/('M3_80M_'+name+'.md')).exists()

    # Functional tests now include real HC123/HC74/HC175 state and physical pins.
    from m3a_r1_logic import verify
    logical=verify();cases=logical['truth_cases'];fault_cases=len(logical['state_scenarios'])
    ref=2.495
    uv2=ref*10000/(127000+10000)*31.9
    uv4=ref*10000/(61900+10000)*31.9
    ov=ref*10000/(78700+10000)*31.9
    oc=ref*10000/(69800+10000)/(.05*20*.25)
    # Thermal hub load is ratio-metric. Each voltage/current reference is independent.
    temp={}
    for ntc in (10000,1655.629,1e99):
        conductance=1/(10000+ntc)+1/(60400+10000)+1/(1300+10000)
        vhub=(ref*1000/(1500+1000))/(1+600*conductance)
        source_current=(ref-vhub)/1500
        temp[str(ntc)]=dict(hub_v=vhub,ntc_signal_v=vhub*ntc/(10000+ntc),hot_ref_v=vhub*10000/70400,open_ref_v=vhub*10000/11300,hub_current_a=source_current)
    ref_div_load=sum(ref/(r+10000)for r in(127000,61900,78700,69800))
    worst_tl_cathode=(3.135-ref*1.02)/180-ref_div_load-max(t['hub_current_a']for t in temp.values())
    assert worst_tl_cathode>.001
    max_input=max(28/31.9,3.465*.25,max(t['hub_v']for t in temp.values()))
    assert max_input<3.135-2 # Conservative full-temperature VCM bound.
    temptrip=1/(1/298.15+math.log(1655.629/10000)/3434)-273.15
    rails={}
    for mode,resistors in [('Sprint',()),('Extended',(91000,)),('Full',(24900,)),('Invalid',(91000,24900))]:
        rb=1/(1/20000+sum(1/r for r in resistors));rails[mode]=.596*(1+137000/rb)
    assert 4<rails['Sprint']<rails['Extended']<rails['Full']<8.6<ov
    assert rails['Invalid']<ov # invalid combination stopped by logic, not OV.
    pad_r=750;series=6.8
    # ABCD pi-network S21 with matched50ohm ports.
    a=1+series/pad_r;b=series;c=2/pad_r+series/(pad_r*pad_r);dd=a
    gain=2/(a+b/50+c*50+dd);pad_db=-20*math.log10(abs(gain))
    assert pad_db>1
    fault_p=(3.6**2/(4*27*.99)+2*3.6**2/(10000*.99))*10**(-1/10)
    assert fault_p<.1

    # Energy model retains explicit new circuit losses and always-powered source.
    # Drain-stage eta differs from M2's effective whole-PA eta. No double-counted measured data.
    baseline=.127+.0916667+.035+.004
    profiles=[]
    for name,p,vd,vs,eta in [('Full3.15W',3.15,7.6,7.958,.60),('Extended1.2W',1.2,5.25,5.576,.55),('Sprint0.85W',.85,4.4,4.679,.50)]:
        current=p/(eta*vd)
        ib=max(0,(vs-.9)/100-.9/1000)
        gate=8.2e-9*vs*3.55e6 # typical10VQg used as allowance; not measured atthisV
        pass_loss=.5*current
        active_buck_output=p/eta+pass_loss+ib*vs+gate+.003*vs
        mean=baseline+.2*active_buck_output/.9+.2*.4*(active_buck_output/.9)/12
        wh=4*3.6*2.45*.648
        profiles.append(dict(profile=name,drain_eta_assumed=eta,base_a_assumed=ib,driver_gate_w_assumed=gate,mean_pack_w=mean,wh12=mean*12,wh24=mean*24,usable_4S1P25R_wh=wh,runtime_h=wh/mean))
    poor=[]
    for name,p,vd,vs in [('Full3.15W',3.15,7.6,7.958),('Extended1.2W',1.2,5.25,5.576)]:
        cc=p/(.4*vd);ib=max(0,(vs-.9)/100-.0009)
        bb=p/.4+.5*cc+ib*vs+8.2e-9*vs*3.55e6+.003*vs
        mean=baseline+.2*bb/.85+.2*.4*(bb/.85)/12
        poor.append(dict(profile=name,PA_eta=.4,buck_eta=.85,mean_pack_w=mean,runtime_4S1P25R_h=22.86144/mean))
    power=dict(baseline_pack_w_assumed=baseline,source_policy='Always powered25mA allowance; do not creditSiidlepoweruntilmeasured',profiles=profiles,Fox_W_retained=.350,poor_efficiency_cases=poor,idle_plus_018W_runtime_h=[p['usable_4S1P25R_wh']/(p['mean_pack_w']+.18)for p in profiles])
    return dict(date='2026-10-14',classification='NETLIST/FOOTPRINT/BOOLEAN CHECKS AND DESIGN CALCULATIONS; NO MEASUREMENTS OR RF SIMULATION',schematic_sheets=14,revision='M3A-R1',manifest_parts=len(parts),connected_pins_checked=pins,footprints_checked=footprints,ERC_violations=0,Boolean_cases=cases,individual_fault_cases=fault_cases,cost_baskets_checked=cost_baskets,cost_csv_rows_checked=len(csv_rows),physical_pinmaps_checked=list(needed),analogue=dict(reference_v=ref,protected_input_UV2_v=uv2,protected_input_UV4_v=uv4,PA_OV_v=ov,PA_OC_a=oc,thermal_approx_trip_c=temptrip,thermal_hub_cases=temp,worst_TL431_cathode_a=worst_tl_cathode,maximum_comparator_input_v=max_input,conservative_VCM_max_v=3.135-2,rails_v=rails,pad_insertion_db_ideal=pad_db,maximum_Fox_fault_available_w_calculated=fault_p,fault_resistor_tolerance_fraction=.01),power=power)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    r=report();f=ROOT/'docs/M3_80M_CALCULATIONS.json'
    text=json.dumps(r,indent=2)+'\n'
    if args.write:f.write_text(text)
    else:assert f.read_text()==text,'Calculation output stale; run --write after valid ERC/export'
    print(f"PASS: {r['connected_pins_checked']} exportedpinconnections, {r['footprints_checked']}footprintmaps, ERC0, {r['Boolean_cases']}Booleanstates; analogue/costresultsnotmeasured")
if __name__=='__main__':main()
