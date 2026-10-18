#!/usr/bin/python3
"""V1 variant materials and explicit, unquoted installed-module allowances."""
import csv,json
from pathlib import Path
from m4a_design import R,E,P,D
def main():
    old=json.loads((R/'docs/M3B_E2_COSTS.json').read_text());m=json.loads((P/'RF80_V1.electrical.json').read_text());parts=[p for p in m['parts']if not p['ref'].startswith(('#','TP'))]
    catalogs=json.loads((R/'docs/M1_COST_PARTS.json').read_text())['parts'];accessories={}
    rows=list(csv.DictReader((R/'docs/M1_COST_BOM.csv').open()))
    for name in ('long80','compact80'):
        selected=[r for r in rows if r['board']==name and r['part_id']not in('RFPORT','PADRES')];ls=[]
        for row in selected:
            c=catalogs[row['part_id']];qty=float(row['quantity_per_board']);price=float(c['price_breaks_eur']['1']);ls.append(dict(part=row['part_id'],quantity=qty,unit_eur=price,line_eur=round(qty*price,4),source='Preserved M1 allowance',evidence=c['evidence']))
        accessories[name]=dict(total_eur=round(sum(x['line_eur']for x in ls),4),lines=ls,scope='Independent antenna/matching/wire/support; RFPORT omitted because actual PCB RF connector is already in component basket; compact PADRES omitted because actual R513/R514/R515 calibration pad is already in PCB BOM')
    result=dict(date='2026-10-15',revision='M4A-V1',currency='EUR NET; VAT excluded',classification='Component baskets retain dated observations/estimates; all fabrication/harness/thermal costs UNQUOTED ALLOWANCES',PCB_model=dict(board_mm=[150,110],two_up_panel_mm=[160,232],panel_routing_gap_mm=2,panel_border_mm=5,setup_eur=[12,25],area_rate_eur_m2=[180,350],minimum_panel_count='3/5/10 at6/10/20, all are even; no unusable purchased surplus',critical_hole_process_surcharge='OPEN; not absorbed into an invented quote',excludes='Freight, VAT, labor, coupons/fiducial process changes and yield losses'),accessories=accessories,batches={})
    for n in(6,10,20):
        bare=[round(s/n+.160*.232/2*r,4)for s,r in[(12,180),(25,350)]];node={}
        for pop,pops in [('Full',('BOTH','NORMAL')),('Fox',('BOTH','FOX'))]:
            refs={p['ref']for p in parts if p['population']in pops};ledger=old['scopes'][pop]['batches'][str(n)];priced_refs={r.strip()for line in ledger['lines']for r in line['refs'].split(',')};assert refs==priced_refs
            comp=ledger['per_board_eur'];harness=[4,8]if pop=='Full'else[3,6];thermal=[2,6]if pop=='Full'else[0,0];mount=[.8,2];antenna=accessories['compact80']['total_eur']+(accessories['long80']['total_eur']if pop=='Full'else 0)
            lo=comp+bare[0]+harness[0]+thermal[0]+mount[0]+antenna;hi=comp+bare[1]+harness[1]+thermal[1]+mount[1]+antenna
            node[pop]=dict(purchased_parts=len(refs),ICs=sum(r.startswith('U')for r in refs),component_eur=comp,component_observed_eur=ledger['historical_observation_eur'],component_estimated_eur=ledger['estimate_eur'],component_groups=ledger['groups'],PCB_eur=bare,PCB_mandatory_hole_process_surcharge='OPEN',board_connectors_included_eur=ledger['groups']['connectors'],additional_mating_harness_eur=harness,harness_scope='Controller/power mates, wire and strain relief; excludes board-side connectors and the Fox accessory plug/identity already in ACCESSKEY',antenna_matching_and_wire_eur=round(antenna,4),thermal_material_eur=thermal,mounting_insulation_eur=mount,installed_module_material_eur=[round(lo,4),round(hi,4)],optional_labor='Unpriced; winding/assembly/test labor explicit and separate',component_lines=ledger['lines'])
        result['batches'][str(n)]=node
    (R/'docs/M4A_COSTS.json').write_text(json.dumps(result,indent=2)+'\n')
    with(R/'docs/M4A_VARIANT_BOM.csv').open('w')as out:
        fields=['population','batch']+list(old['scopes']['Full']['batches']['6']['lines'][0]);w=csv.DictWriter(out,fieldnames=fields,lineterminator='\n');w.writeheader()
        for n,bb in result['batches'].items():
            for pop,v in bb.items():
                for l in v['component_lines']:w.writerow(dict(population=pop,batch=n,**l))
    with(D/'population.csv').open('w')as out:
        w=csv.writer(out,lineterminator='\n');w.writerow(['reference','MPN','value','footprint','population','full_fit','Fox_fit'])
        for p in parts:w.writerow([p['ref'],p['mpn'],p['value'],p['footprint'],p['population'],p['population']in('BOTH','NORMAL'),p['population']in('BOTH','FOX')])
    print('PASS: actual V1 full/Fox BOM equals E2 material scopes at6/10/20; installed estimates exclude all shared controller/battery/charger costs')
if __name__=='__main__':main()
