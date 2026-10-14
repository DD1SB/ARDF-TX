#!/usr/bin/env python3
"""Document-only reference costing and energy arithmetic; no RF simulation or CAD design."""
import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
import io
import json
from pathlib import Path
import m1_costs

ROOT = Path(__file__).resolve().parents[1]
D = Decimal
BATCHES = (6, 10, 20)


def money(x):
    return str(D(str(x)).quantize(D('.01'), rounding=ROUND_HALF_UP))


def inputs():
    return json.loads((ROOT / 'docs/M2_80M_INPUTS.json').read_text())


def basket(rows, batch, parts):
    quantities = {}
    for r in rows:
        quantities[r['part_id']] = quantities.get(r['part_id'], 0) + r['qty'] * batch
    purchases = {}
    for pid, needed in quantities.items():
        p = parts[pid]
        ordered = max(needed, p['moq'])
        ordered = ((ordered + p['multiple'] - 1) // p['multiple']) * p['multiple']
        brk = max(int(k) for k in p['price_breaks_eur'] if int(k) <= ordered)
        price = D(str(p['price_breaks_eur'][str(brk)]))
        purchases[pid] = dict(needed=needed, ordered=ordered, leftover=ordered-needed,
                              price_break=brk, unit_eur=str(price), batch_eur=money(price*ordered))
    total = sum((D(p['batch_eur']) for p in purchases.values()), D(0))
    estimated = sum((D(p['batch_eur']) for pid,p in purchases.items()
                     if parts[pid]['evidence'] == 'ESTIMATE'), D(0))
    groups = {}
    lines = []
    for r in rows:
        p = purchases[r['part_id']]
        # Allocate purchases by identical MPN, including MOQ leftovers exactly once.
        cost = D(p['batch_eur']) * D(r['qty']*batch) / D(p['needed'])
        groups[r['group']] = groups.get(r['group'], D(0)) + cost / batch
        lines.append({**r, **p, 'line_per_unit_eur': str(cost/batch),
                      'evidence': parts[r['part_id']]['evidence']})
    return dict(per_unit_eur=money(total/batch), batch_eur=money(total),
                observed_eur=money((total-estimated)/batch), estimated_eur=money(estimated/batch),
                estimate_plus_50_percent_eur=money((total+estimated/2)/batch),
                purchases=purchases, groups={g:money(v) for g,v in groups.items()}, lines=lines)


def row(pid, qty, group, note=''):
    return dict(part_id=pid, qty=qty, group=group, note=note)


def proposed(fox=False, high=False):
    rows = [row(r['part_id'],r['qty'],r['cost_group'],r['note'])
            for r in m1_costs.population(['80m'],fox_only=True)
            if r['part_id'] not in ('OPAMP','TRIM')]
    rows += [row('NAND',1,'fox','TinyFox buffer mechanism; no local crystal/MCU/AA boost'),
             row('RES',2,'fox','Fixed calibration selections replace trimmer; values OPEN'),
             row('LOWGUARD',1,'safety','Preserved unquoted guard/limit completion provision')]
    if not fox:
        rows += [row('HFPA',1,'RF_semiconductors'),row('LM5134B',1,'drivers'),
                 row('ISOFET',2,'safety','Actual PA rail disconnect, not converter EN alone'),
                 row('CMP',1,'safety','Additional watt OC/temperature channels'),
                 row('BIFILAR',1,'filter_matching','SignalSlinger L101 9T #24 FT-50A-43'),
                 row('T60CORE',2,'filter_matching','SignalSlinger L301/L302 20T #24 T60-2'),
                 row('C0G',4,'filter_matching','1100p x2,1800p,91p; voltage/MPNs OPEN'),
                 row('RFBLOCK',1,'filter_matching','470nF RF DC block'),
                 row('MPS751',1,'shape','QCX integrator pass transistor; exact-vendor SOA gate'),
                 row('SMALLFET',1,'shape','QCX Q4 function; substitute 2N7002 needs qualification'),
                 row('RES',4,'shape','RC integrator + gate bleed/stop; values OPEN'),
                 row('CBULK',1,'shape','2.2uF RC capacitor starting value, not PA reservoir'),
                 row('C100N',4,'passive'),row('CBULK',2,'passive'),
                 row('CELECT',2,'passive','Local rail reservoirs upstream of shaped drain'),
                 row('INDUCTOR',1,'power_conversion'),row('SINK',1,'thermal')]
        if high:
            rows += [row('LTC3600',1,'power_conversion'),row('OPA171',1,'power_conversion'),
                     row('BOOST',1,'power_conversion'),row('INDUCTOR',1,'power_conversion'),
                     row('CBULK',2,'power_conversion'),row('CELECT',1,'power_conversion'),
                     row('RES',8,'power_conversion'),row('RFCOIL',1,'power_conversion'),
                     row('THERMALADD',1,'thermal','Continuous 5W thermal provision')]
        else:
            rows += [row('BUCK',1,'power_conversion','TPS62160: output <=6V; not a higher-power supply'),
                     row('RES',4,'power_conversion','Bounded two-level feedback and bleeders')]
    return rows


def report():
    data = inputs()
    parts = {**m1_costs.PARTS, **data['parts']}
    variants = {k:v for k,v in data['reference_baskets'].items()}
    variants.update({'Proposed Fox-only RF':proposed(fox=True),
                     'Proposed 1.2W Classic/Sprint + Fox RF':proposed(),
                     'Proposed 2-3W/5W supply alternative + Fox RF':proposed(high=True)})
    # Explicit modern-interface/50ohm/protection allowances prevent treating the bare
    # antenna-tuned DF1FO core as a complete substitute at its native price.
    df = [r for r in proposed() if r['part_id'] not in ('HFPA','LM5134B','BIFILAR','BUCK')]
    df += [row('SN75452',1,'RF_semiconductors','Native DF1FO output mechanism'),
           row('BOOST',1,'power_conversion','Regulated9V output, no direct depleted2S claim'),
           row('LEGLP2950',1,'power_conversion','Required5V logic rail'),
           row('RFCOIL',2,'filter_matching','Drain feed/native matching adjustment'),
           row('C0G',3,'filter_matching','Native matching retained before50ohm LPF'),
           row('DIODE',1,'safety','Native drain spike clamp'),
           row('SMALLFET',1,'shape','Bounded mode adjustment'),
           row('OPAMP',1,'shape','DC mode adjustment allowance; implementation OPEN')]
    variants['DF1FO mechanism adapted to protected programmable module allowance'] = df
    cost = {k:{str(n):basket(v,n,parts) for n in BATCHES} for k,v in variants.items()}
    # Keep preserved Fox fleet scope and change only explicitly identified RF population.
    fox_old = json.loads((ROOT/'docs/FOXORING_COST_TOTALS.json').read_text())
    fox = []
    for n in (10,20):
        ctrl = [row(r['part_id'],r['qty'],r['board']) for r in m1_costs.population(['controller'])]
        ant = [row(r['part_id'],r['qty'],r['board']) for r in m1_costs.population(['compact80'])]
        new = basket(ctrl+proposed(fox=True)+ant,n,parts)
        old = next(x for x in fox_old['batches'] if x['batch']==n)
        # LOWGUARD already in audited unit additions: subtract it from new core before bridge.
        delta = D(new['batch_eur'])/n - D(old['m1_baseline_batch_eur'])/n - D('.75')
        fox.append(dict(batch=n, RF_population_delta_eur=money(delta),
                        core_without_guard_eur=money(D(new['batch_eur'])/n-D('.75')),
                        unit_material_budget_eur=money(D(old['unit_budget_batch_eur'])/n+delta),
                        fleet_budget_per_unit_eur=money((D(old['unit_budget_batch_eur'])+
                          D(old['shared_equipment_batch_eur'])+D(old['freight_budget_batch_eur']))/n+delta)))
    # All currents/efficiencies here are engineering allowances. No measured DUT values.
    common = .120 + .020
    synth = 3.3*.025/.90
    profiles = []
    for name,power,eta,conversion,driver,duty in [
        ('Classic 1W boundary comparison',1,.55,.90,.220,.20),
        ('Classic preferred 1.2W',1.2,.55,.90,.220,.20),
        ('Classic 2W higher supply',2,.60,.85*.90,.400,.20),
        ('Classic 3W higher supply',3,.60,.85*.90,.400,.20),
        ('Classic 5W higher supply',5,.60,.85*.90,.400,.20),
        ('Sprint 0.85W',.85,.50,.90,.220,.20),
        ('Sprint 1W upper comparison',1,.50,.90,.220,.20),
        ('Foxoring 10mW continuous',.010,.25,.90,.015,1),
        ('Beacon continuous 1.2W',1.2,.55,.90,.220,1),
        ('Beacon continuous 5W',5,.60,.85*.90,.400,1)]:
        # Driver powered from buck in economy case, upstream boost in higher-power case.
        drv_conversion = .85 if 'higher' in name or '5W' in name else .90
        active_extra = power/eta/conversion + driver/drv_conversion + synth
        mean = common + duty*active_extra
        cases={}
        for ah in (2.45,3.4):
            wh = 7.2*ah*.8*.9*.9
            hours=[wh*p/mean for p in (1,2,3,4)]
            cases[str(ah)] = dict(usable_wh_per_parallel=wh,hours=hours,
                                  smallest_pack=next((f'2S{p}P'for p,h in enumerate(hours,1)if h>=24),'NONE'),
                                  smallest_always_RX=next((f'2S{p}P'for p in (1,2,3,4)
                                                           if wh*p/(mean+.045)>=24),'NONE'))
        profiles.append(dict(name=name,rf_w=power,PA_efficiency_assumed=eta,
                             power_conversion_efficiency_assumed=conversion,driver_w_assumed=driver,
                             duty=duty,mean_input_w=mean,wh_24h=mean*24,
                             active_current_at_6V_a=(common+active_extra)/6,
                             estimated_peak_current_allowance_a=(common+active_extra)/6*1.5+.12,
                             cells=cases))
    # Shaper stress is a separate illustrative drain-efficiency case, not a
    # measurement or the whole-PA-feed efficiency used in the energy scenarios.
    shaper=[]
    for rf,vd,eta,vs in ((1.2,5.3,.55,5.5),(5,10.2,.60,12)):
        current=rf/(vd*eta)
        shaper.append(dict(rf_w=rf,drain_v=vd,drain_efficiency_assumed=eta,
                           collector_a=current,steady_pass_w_at_02V_drop=.2*current,
                           resistive_surrogate_peak_w=vs*current/4))
    return dict(date='2026-10-13',classification='CANDIDATE; calculations and explicit estimates, no hardware validation',
                tax='EUR ex VAT planning; retail tax basis separately stated',costs=cost,fox_bridge=fox,
                power=dict(common_baseline_w=common,synth_active_w=synth,
                           lora_RX_10_percent_w=.006,lora_RX_always_w=.045,profiles=profiles),
                shaper_stress_calculations=shaper,
                kit_retail_eur_equivalent=money(D(90)/D('1.1181')))


def render_bom(data):
    parts={**m1_costs.PARTS,**inputs()['parts']}
    out=['# M2 80 m candidate cost workbook','',
         'Date: 2026-10-13. **Generated analysis, not an ordering BOM.** Current/indexed observations and '
         'explicit estimates; EUR ex VAT. Reference counts are inspected facts; unquoted prices, population '
         'choices and all derived RF performance remain unverified. See [comparison](M2_80M_COST_COMPARISON.md).','',
         '| Scope | 6 EUR/unit | 10 | 20 | Observed / estimated at ten |','| --- | ---: | ---: | ---: | --- |']
    for name,b in data['costs'].items():
        out.append(f"| {name} | {b['6']['per_unit_eur']} | {b['10']['per_unit_eur']} | {b['20']['per_unit_eur']} | {b['10']['observed_eur']} / {b['10']['estimated_eur']} |")
    out += ['', 'Identical MPNs pool only within each basket; different values do not share hypothetical breaks. '
            'Estimates assume MOQ1/multiple1 unless stated; stock and minimum bulk purchases remain open. '
            'A reference scope is described in the comparison; it is not an alternative complying ARDF-TX BOM.']
    for name,b in data['costs'].items():
        out+=['',f'## {name}','',
              '| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |',
              '| --- | --- | --- | --- | --- | --- |']
        for i,r in enumerate(b['6']['lines']):
            p=parts[r['part_id']];u=' / '.join(b[str(n)]['lines'][i]['unit_eur']for n in BATCHES)
            ex=' / '.join(money(b[str(n)]['lines'][i]['line_per_unit_eur'])for n in BATCHES)
            needed=' / '.join(str(r['qty']*n)for n in BATCHES)
            supplier=f"[{p['supplier']}]({p['source_url']})"if p['source_url']else p['supplier']
            out.append(f"| {r['group']} / {r['note'] or r['part_id']} | {r['qty']}; {needed} | {p['mpn']}; {supplier}: {p['supplier_part_number']} | {p['evidence']}; {p['moq']}/{p['multiple']} | {u} | {ex} |")
    return '\n'.join(out)+'\n'


def render_power(data):
    out=['# M2 80 m power arithmetic','',
         '**Engineering calculations only: no measured ARDF-TX current, efficiency or battery pass.** '
         'Generated by `tools/m2_80m_analysis.py`. See [assumptions and conclusions](M2_80M_POWER_COMPARISON.md).','',
         '| Profile | Mean W | 24 h Wh | Active A at 6V | Peak allowance A | 2.45Ah 1P / 2P / 3P / 4P hours | Smallest 2.45Ah / 3.4Ah |',
         '| --- | ---: | ---: | ---: | ---: | --- | --- |']
    for r in data['power']['profiles']:
        hrs=' / '.join(f'{h:.1f}'for h in r['cells']['2.45']['hours'])
        out.append(f"| {r['name']} | {r['mean_input_w']:.3f} | {r['wh_24h']:.2f} | {r['active_current_at_6V_a']:.2f} | {r['estimated_peak_current_allowance_a']:.2f} | {hrs} | {r['cells']['2.45']['smallest_pack']} / {r['cells']['3.4']['smallest_pack']} |")
    out+=['','## Preserved 3.4 Ah reference-cell runtime sensitivity','',
          '| Profile | 2S1P hours | 2S2P | 2S3P | 2S4P |',
          '| --- | ---: | ---: | ---: | ---: |']
    for r in data['power']['profiles']:
        out.append('| '+r['name']+' | '+' | '.join(f'{h:.1f}' for h in r['cells']['3.4']['hours'])+' |')
    out+=['','## Optional LoRa always-receiving sensitivity','',
          '| Profile | Smallest 2.45Ah | Smallest 3.4Ah |','| --- | --- | --- |']
    for r in data['power']['profiles']:
        out.append(f"| {r['name']} | {r['cells']['2.45']['smallest_always_RX']} | {r['cells']['3.4']['smallest_always_RX']} |")
    return '\n'.join(out)+'\n'


def csv_report(data):
    s=io.StringIO();fields=['variant','batch','group','part_id','qty','needed','ordered','leftover',
                           'price_break','unit_eur','line_per_unit_eur','evidence','note']
    w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n');w.writeheader()
    for variant,baskets in data['costs'].items():
        for n,b in baskets.items():
            for r in b['lines']:
                w.writerow({k:({'variant':variant,'batch':n,**r}).get(k,'')for k in fields})
    return s.getvalue()


def check(data):
    for variants in data['costs'].values():
        for n,b in variants.items():
            assert sum((D(p['batch_eur'])for p in b['purchases'].values()),D(0))==D(b['batch_eur'])
            assert all(p['ordered']>=p['needed'] for p in b['purchases'].values())
    assert not ({r['part_id']for r in proposed(fox=True)} & {'HFPA','LM5134B','BOOST','BUCK','ISOFET','LTC3600'})
    assert 'MONO'in {r['part_id']for r in proposed(fox=True)}
    assert 'BUSISO'in {r['part_id']for r in proposed(fox=True)}
    assert 'LM5134B' in {r['part_id']for r in proposed()}
    assert 'LM5134A' not in {r['part_id']for r in proposed()}
    inv=json.loads((ROOT/'docs/M2_80M_REFERENCE_INVENTORY.json').read_text())['components']
    assert sum(r['design']=='FlexFox80'for r in inv)==170
    assert sum(r['design']=='SignalSlinger'for r in inv)==131
    old=json.loads((ROOT/'docs/FOXORING_COST_TOTALS.json').read_text())
    assert old['batches'][0]['m1_baseline_per_unit_eur']=='29.06'
    assert old['batches'][0]['unit_budget_incl_bms_reserve_eur']=='55.24'
    for p in data['power']['profiles']:
        assert abs(p['wh_24h']-24*p['mean_input_w'])<1e-9
        for c in p['cells'].values():
            for i,h in enumerate(c['hours'],1):assert abs(h*p['mean_input_w']-c['usable_wh_per_parallel']*i)<1e-8
    assert .56 < data['shaper_stress_calculations'][0]['resistive_surrogate_peak_w'] < .58
    assert 2.44 < data['shaper_stress_calculations'][1]['resistive_surrogate_peak_w'] < 2.46
    for name in ('REFERENCE_COMPARISON','RF_TOPOLOGY','COST_COMPARISON','POWER_COMPARISON','VALIDATION_GATES','DECISION'):
        assert (ROOT/f'docs/M2_80M_{name}.md').is_file(),name
    print(f"PASS: {len(data['costs'])} baskets at 6/10/20; {len(data['power']['profiles'])} profiles; preserved Fox bridge; six deliverables")


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    data=report();outputs={'docs/M2_80M_TOTALS.json':json.dumps(data,indent=2)+'\n',
                         'docs/M2_80M_BOM.md':render_bom(data),'docs/M2_80M_BOM.csv':csv_report(data),
                         'docs/M2_80M_POWER_TABLES.md':render_power(data)}
    if args.write:
        for path,value in outputs.items():(ROOT/path).write_text(value)
    if args.check:
        for path,value in outputs.items():assert (ROOT/path).read_text()==value,f'stale {path}'
        check(data)
    if not(args.write or args.check):print(json.dumps(data,indent=2))


if __name__=='__main__':main()
