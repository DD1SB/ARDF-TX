#!/usr/bin/env python3
"""Reproduce the gated Mitsubishi review; this script creates no CAD or orders.

R2 layout is deliberately stopped at the user's mandatory sourcing gate. All
endurance/thermal values below are planning assumptions, never measurements.
"""
import argparse
import collections
import copy
import csv
import hashlib
import itertools
import json
import math
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'hardware/2m/review/M5A-R2'
DATE = '2026-10-15'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2) + '\n')

def write_csv(name, rows):
    with (OUT / name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def snapshot():
    paths = [ROOT / 'README.md']
    for directory in ['hardware/80m', 'hardware/2m', 'docs/decisions']:
        paths += list((ROOT / directory).rglob('*'))
    paths += list((ROOT / 'docs').glob('M5_2M*'))
    paths += list((ROOT / 'docs').glob('M5A_R1*'))
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(paths))
            if p.is_file() and not p.is_relative_to(OUT)
            and p.suffix not in ('.pyc', '.kicad_prl')}

def calculate():
    inputs = json.loads((OUT / 'inputs.json').read_text())
    antenna_factor = 10 ** (-inputs['antenna_net_gain_dbd'] / 10)
    rf = []
    for erp, depth, loss in itertools.product([1, .9, .3], [.75, .8], [.35, .75, 1.0]):
        carrier = erp * antenna_factor
        pep = carrier * (1 + depth) ** 2
        mean = carrier * (1 + depth * depth / 2)
        factor = 10 ** (loss / 10)
        cap = pep * 10 ** .1 * factor
        rf.append(dict(erp_w=erp, depth=depth, filter_loss_db=loss,
            connector_carrier_w=carrier, connector_average_rf_w=mean,
            connector_pep_w=pep, module_carrier_w=carrier * factor,
            module_pep_w=pep * factor, module_capability_with_1db_w=cap,
            ra07_fm_rating_minus_capability_db=10 * math.log10(6.5 / cap),
            ra08_fm_rating_minus_capability_db=10 * math.log10(8 / cap)))
    write_csv('rf-budget.csv', rf)
    # Passively available TOTAL AC power of a bounded clock, not an estimate of
    # Si5351 fundamental drive. Source high/low variance <= Vpp^2/4.
    source_bounds = []
    for shorts in [0, 1]:
        resistance = (2 - shorts) * 47 * .99
        bound = 3.465 ** 2 / (16 * resistance)
        source_bounds.append(dict(series_resistor_short_faults=shorts,
            minimum_series_ohm=resistance, maximum_available_total_ac_w=bound,
            comparison_module_input_absolute_w=.030,
            scope='Calculation only; passive network, bounded 3.3V source, no downstream RF gain'))
    write_csv('source-power-bound.csv', source_bounds)
    # This is a fixed-supply class-AB planning model. eta_dynamic excludes the
    # separately counted idle bias. It is NOT the manufacturer's FM efficiency.
    states, endurance, sensitivity = [], [], []
    packs = {'2S2P': 4, '2S3P': 6, '2S4P': 8, '4S1P': 4, '4S2P': 8}
    cells = {'25R_min_2p45Ah': 8.82, 'M35A_min': 11.9}
    def state(erp, depth, efficiency, iq, ctrl, lora, converter_eff, duty):
        prf = erp * antenna_factor * 10 ** .075 * (1 + depth * depth / 2)
        pa = 7.2 * iq + prf / efficiency
        active = (pa + .15) / converter_eff
        mean = ctrl + .04 + lora + duty * active
        return dict(erp_w=erp, modulation=depth, dynamic_eff_assumed=efficiency,
            iq_assumed_a=iq, controller_assumed_w=ctrl, lora_assumed_w=lora,
            converter_eff_assumed=converter_eff, duty=duty,
            module_average_rf_w=prf, pa_dc_assumed_w=pa,
            pa_waste_assumed_w=pa-prf, active_increment_battery_w=active,
            mean_battery_w=mean, need12_wh=mean*12, need24_wh=mean*24,
            envelope_crest_current_estimate_a=iq +
                erp * antenna_factor * 10 ** .075 * (1+depth)**2 / (7.2*efficiency))
    for arch, conv in [('2S_regulation_required', .87), ('4S_buck_candidate', .91)]:
        for erp, depth in itertools.product([1, .9, .3], [.75, .8]):
            efficiency = .40 if erp >= .9 else .28
            p = state(erp, depth, efficiency, .30, .14, 0, conv, .2)
            p['architecture'] = arch
            states.append(p)
            beacon = state(erp, depth, efficiency, .30, .14, 0, conv, 1)
            for pack, count in packs.items():
                if pack.startswith('2S') != arch.startswith('2S'):
                    continue
                for cell, wh in cells.items():
                    energy = count * wh * .8 * .9 * .9
                    hours = energy / p['mean_battery_w']
                    goal = 12 if erp >= .9 else 24
                    endurance.append(dict(architecture=arch, erp_w=erp, modulation=depth,
                        pack=pack, cell_basis=cell, usable_energy_assumed_wh=energy,
                        mean_battery_assumed_w=p['mean_battery_w'], hours_calculated=hours,
                        target_h=goal, arithmetic_target_met=hours>=goal,
                        margin20_percent=hours>=goal*1.2,
                        continuous_beacon_hours=energy/beacon['mean_battery_w'],
                        electrical_supply_compatibility='NOT_QUALIFIED',
                        hardware_endurance='NOT_RUN'))
    for erp, iq, eff, ctrl, lora, conv in itertools.product(
            [1, .3], [.15, .30, .75, 2.0], [.25, .40, .50],
            [.14, .28], [0, .006, .045587], [.87, .91]):
        sensitivity.append(state(erp, .8, eff, iq, ctrl, lora, conv, .2))
    write_csv('operating-states.csv', states)
    write_csv('endurance.csv', endurance)
    write_csv('sensitivity.csv', sensitivity)
    write_json('calculations.json', dict(status='CALCULATED_NOT_MEASURED',
        antenna_net_gain_dbd=-1, inputs=inputs, rf_budget=rf,
        envelope_span_db={str(m):20*math.log10((1+m)/(1-m)) for m in [.7,.75,.8]},
        max_available_source_ac=source_bounds, operating_states=states,
        thermal=dict(reference_fm_waste_w=6.5/.45-6.5,
            required_sink_c_per_w_for_10w_45ambient_60case=(60-45)/10,
            warning='Steady 10W heat is an assumed cooler-sizing case, not linear-AM measurement')))
    return rf, source_bounds, states, endurance

def costs():
    """Itemized R1-derived accounting bridge; NOT a completed R2 ordering BOM."""
    import m5a_r1_costs as old
    parts = json.loads((ROOT/'hardware/2m/RF2M.electrical.json').read_text())['parts']
    r1 = json.loads((ROOT/'hardware/2m/review/M5A-R1/costs.json').read_text())
    r0 = json.loads((ROOT/'hardware/2m/review/M5A-R0/costs.json').read_text())
    # Block removals count actual previous positions; retained material is a
    # conservative scope bridge, not a net-connected new transmitter.
    removed = {'pa', 'driver', 'driver_supply', 'pa_match', 'modulator', 'bias'}
    additions = [
        ('MODULE','RA07M1317M-501', {1:28.91/1.1208,10:27.46/1.1208},
         'OBSERVED_USD_FX_CONVERTED_NOT_LANDED','RF Parts RA07 product','Quantity stock/lead time OPEN'),
        ('RF_AM','MAAV-011017-TR0500',{1:6.79,10:5.24,25:4.85},
         'OBSERVED_EUR_DISPLAY_NET_TREATMENT_PROVISIONAL','Mouser 937-MAAV011017TR0500','0 stock; Dec2026/Jan2027 incoming; OPEN'),
        ('AM_SUPPORT','OPEN passive bias/control/decoupling allowance',{1:1.0},
         'ESTIMATE','UNQUOTED','No final circuit or component count'),
        ('VGG_PROTECTION','OPEN bounded bias and independent RF-off allowance',{1:1.5},
         'ESTIMATE','UNQUOTED','No final circuit or component count'),
        ('SUPPLY_REVISION','OPEN rail/current-limit retuning allowance',{1:.5},
         'ESTIMATE','UNQUOTED','Converter remains scope allowance; 2S topology OPEN')]
    rows, summaries = [], []
    for fleet in [6,10,20]:
        for var in ['BOOST2S','BUCK4S','TRAIN_ONLY']:
            base = next(x for x in r1['summary'] if x['fleet']==fleet and x['variant']==var)
            fitted = [p for p in parts if old.physical(p) and
                      p['population'] in {'ALL', 'NORMAL' if var!='TRAIN_ONLY' else 'TRAIN_ONLY', var}]
            demand = collections.Counter(old.effective(p,var)[1] for p in fitted)
            saved=0; retained=0; retained_count=0; removed_count=0
            for p in fitted:
                value,mpn=old.effective(p,var)
                amount=old.price(p, demand[mpn]*fleet)
                remove=var!='TRAIN_ONLY' and p['group'] in removed
                if remove:saved+=amount;removed_count+=1
                else:retained+=amount;retained_count+=1
                rows.append(dict(fleet=fleet,variant=var,ref=p['ref'],mpn=mpn,
                    value=value,quantity_per_board=1,quantity_fleet=fleet,
                    cost_eur_per_board=amount,function=p['group'],
                    disposition='REMOVE_IN_ACCOUNTING_ONLY'if remove else'RETAIN_R1_SCOPE_ALLOWANCE',
                    evidence=p['evidence'],supplier=p['supplier'],source=p['source_url'],
                    availability=p['availability']))
            added=0
            if var!='TRAIN_ONLY':
                for ref,mpn,prices,evidence,supplier,availability in additions:
                    amount=prices[max(k for k in prices if k<=fleet)]
                    added+=amount
                    rows.append(dict(fleet=fleet,variant=var,ref=ref,mpn=mpn,
                        value=mpn,quantity_per_board=1,quantity_fleet=fleet,
                        cost_eur_per_board=amount,function=ref,
                        disposition='ADD_COUNTERFACTUAL_NOT_DESIGN_BOM',evidence=evidence,
                        supplier=supplier,source='',availability=availability))
            total=retained+added
            assert abs(base['component_allowance_net_eur']-retained-saved)<1e-8
            old0=next(x for x in r0['summary']if x['fleet']==fleet and x['variant']==var)
            summaries.append(dict(fleet=fleet,variant=var,r0_eur=old0['component_allowance_net_eur'],
                r1_eur=base['component_allowance_net_eur'],removed_r1_eur=saved,
                retained_r1_eur=retained,new_allowance_eur=added,
                r2_accounting_bridge_eur=total,delta_vs_r1_eur=total-base['component_allowance_net_eur'],
                removed_r1_positions=removed_count,retained_r1_positions=retained_count,
                final_r2_component_count=None,final_r2_bom='NOT_CREATED_SOURCING_GATE',
                landed_shipping_duty_eur=None,vat='EXCLUDED; separate applicable VAT',
                heat_sink_external_estimate_eur=[6,12],
                pcb_external_estimate_eur=[3,8],rf_harness_estimate_eur=[2,4],
                antenna_feeder_estimate_eur=[8,15],assembly_test_labor_eur=None))
    write_csv('accounting-bridge.csv',rows)
    write_json('cost-comparison.json',dict(classification='INCOMPLETE_COUNTERFACTUAL_NOT_AN_ORDERING_BOM',
        currency='EUR',fx_usd_per_eur=1.1208,
        source_date=DATE,source_1='RF Parts live HTML USD28.91/27.46 at1/10',
        source_2='Mouser EU EUR6.79/5.24 at1/10; MAAV incoming, not stock',
        excluded='Shipping, duty, broker fees, VAT, PCB, cooling, battery, controller, enclosure, labor',
        summary=summaries))
    return summaries

def cad_regression():
    """Run KiCad only on unchanged R1, with outputs clearly named as R1."""
    version=subprocess.check_output(['kicad-cli','version'],text=True).strip()
    base=['kicad-cli','sch']
    commands=[base+['erc','--format','json','--output',str(OUT/'r1-regression-erc.json'),
                    str(ROOT/'hardware/2m/RF2M.kicad_sch')],
              base+['export','netlist','--format','kicadxml','--output',
                    str(OUT/'r1-regression.net.xml'),str(ROOT/'hardware/2m/RF2M.kicad_sch')]]
    for cmd in commands:
        subprocess.run(cmd,check=True,timeout=60,capture_output=True,text=True)
    write_json('tool-versions.json',dict(python=sys.version.split()[0],kicad=version,
        scope='Fresh R1 regression only; no R2 schematic or PCB',
        commands=commands))

def check():
    expected=json.loads((OUT/'preserved-baseline.json').read_text())['files']
    assert snapshot()==expected, 'R1/HF/accepted decisions changed'
    import m5a_r1_verify as r1
    parts,nets=r1.load()
    r1.revised_checks(parts,nets)
    audit=r1.audit(nets,parts)
    logic=r1.tests(nets)
    assert r1.power_checks(parts,nets)
    detected=[]
    for ref,pin,wrong in [('U303','3','VDRV_FILTER'),('Q501','D','GND'),
            ('Q501','S','PA_DRAIN'),('Q401','1','VMOD'),('U101','6','GND'),
            ('U202','1','ARM'),('U501','4','MMIC_RF_DC'),
            ('Q701','2','TRAIN_COLLECTOR'),('U209','2','V3V3')]:
        changed=copy.deepcopy(nets);changed[ref][pin]=wrong
        try:r1.audit(changed,parts)
        except AssertionError:detected.append(ref+':'+pin)
        else:raise AssertionError('R1 pin mutation escaped')
    changed=copy.deepcopy(nets);changed['U205']['10']='PATH_Q'
    try:r1.tests(changed)
    except AssertionError:detected.append('normal_permit_wrong_path')
    else:raise AssertionError('R1 path mutation escaped')
    changed=copy.deepcopy(nets);changed['U304']['2']='HARD_OK_N'
    try:r1.power_checks(parts,changed)
    except AssertionError:detected.append('pack_switch_wrong_fault_bus')
    else:raise AssertionError('R1 fault bus mutation escaped')
    for ref,value in [('R506','100'),('C409','10u'),('F301','2A fast')]:
        changed=copy.deepcopy(parts);changed[ref]['value']=value
        try:r1.revised_checks(changed,nets)
        except AssertionError:detected.append(ref+':wrong_value')
        else:raise AssertionError('R1 value mutation escaped')
    assert len(detected)==14
    fresh=ET.parse(OUT/'r1-regression.net.xml')
    fresh_pins={}
    for net in fresh.findall('./nets/net'):
        for node in net.findall('node'):
            fresh_pins.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=(
                None if net.attrib['name'].startswith('unconnected-')else net.attrib['name'])
    assert fresh_pins==nets,'Fresh exported R1 netlist differs from preserved R1'
    erc=json.loads((OUT/'r1-regression-erc.json').read_text())
    violations=[v for s in erc['sheets']for v in s['violations']]
    assert len(violations)==3 and all(v['severity']=='warning'and
        v['type']=='footprint_filter'for v in violations)
    warnings={next(ref for ref in ['J301','J701','C409']if ref in v['items'][0]['description'])
              for v in violations}
    assert warnings=={'J301','J701','C409'}
    calc=json.loads((OUT/'calculations.json').read_text())
    exact=next(x for x in calc['rf_budget'] if x['erp_w']==1 and x['depth']==.8
               and x['filter_loss_db']==.75)
    assert abs(exact['connector_carrier_w']-1.2589254118)<1e-8
    assert abs(exact['connector_pep_w']-4.078918334)<1e-8
    assert abs(exact['module_capability_with_1db_w']-6.103023049947)<1e-9
    assert all(x['maximum_available_total_ac_w']<.03 for x in calc['max_available_source_ac'])
    src=json.loads((OUT/'sources.json').read_text())
    assert all(x['accessed']==DATE and x['url'].startswith('https://') for x in src['sources'])
    assert src['fleet_sourcing_gate']=='OPEN'
    assert not (ROOT/'hardware/2m/RF2M.kicad_pcb').exists()
    for p in (ROOT/'docs').glob('M5A_R2_*.md'):
        import re
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if not link.startswith(('http:', 'https:', '#')):
                assert (p.parent/link.split('#')[0]).exists(),(p,link)
    write_json('verification.json',dict(status='PASS_REVIEW_INTEGRITY_ONLY_MILESTONE_BLOCKED',
        frozen_files=len(expected),r1_manifest_net_parity=len(parts),r1_critical_assertions=len(audit),
        r1_logic=logic,r1_detected_mutations=detected,
        fresh_r1_export_parity=True,fresh_r1_erc_errors=0,fresh_r1_erc_open_warnings=3,
        new_scope='Arithmetic, evidence, preservation and stop-gate documentation; no new CAD',
        r1_original_freeze=r1.freeze(),
        r2_schematic='NOT_CREATED_SOURCING_GATE',r2_erc='NOT_RUN_NO_R2_SCHEMATIC',
        r2_pcb='NOT_CREATED_SOURCING_GATE',r2_drc='NOT_RUN_NO_PCB',
        r2_manufacturer_pad_net_assertions='NOT_RUN_NO_R2_CAD',
        hardware_tests='NOT_RUN',orders=0,fabrications=0,rf_transmissions=0))
    print('PASS review checks / R1 preserved:',len(expected),'files;',logic['combinations'],
          'R1 logic combinations;',len(logic['scenarios']),'states. R2 SOURCING GATE OPEN; NO PCB.')

def manifest():
    paths=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name not in {'SHA256SUMS','file-manifest.json'})
    hashes={str(p.relative_to(ROOT)):sha(p) for p in paths}
    write_json('file-manifest.json',hashes)
    (OUT/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(OUT))+'\n' for p in paths))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--initialize',action='store_true')
    parser.add_argument('--cad-regression',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    if args.initialize:
        assert not (OUT/'preserved-baseline.json').exists(), 'Never replace baseline snapshot'
        write_json('preserved-baseline.json',dict(date=DATE,tag='m5a-r1',commit='4785057',files=snapshot()))
    if args.cad_regression:cad_regression()
    calculate();costs();check();manifest()
