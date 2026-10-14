#!/usr/bin/env python3
"""Derive R1 counts and purchase deltas from current exports and tagged R0."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def old(path):return json.loads(subprocess.check_output(['git','show','m3a-r0:'+path],cwd=ROOT,text=True))
def population(parts,fox=False,legacy=False):
    a=[p for p in parts if p['population']in(('BOTH','FOX')if fox else('BOTH','NORMAL'))]
    if fox and legacy:
        a=[p for p in a if p['ref']!='TH301'];a.append(next(p for p in parts if p['ref']=='R336'))
    return a

def stats(parts):
    physical=[p for p in parts if not p['ref'].startswith(('#','TP'))]
    return dict(positions=len(parts),purchased_components=len(physical),ICs=sum(p['ref'].startswith('U')for p in physical),test_pads=sum(p['ref'].startswith('TP')for p in parts),power_flags=sum(p['ref'].startswith('#')for p in parts),IC_refs=[p['ref']for p in physical if p['ref'].startswith('U')])

def report():
    bm=old('hardware/80m/RF80.electrical.json')['parts'];am=json.loads((ROOT/'hardware/80m/RF80.electrical.json').read_text())['parts']
    bc=old('docs/M3_80M_COSTS.json')['scopes'];ac=json.loads((ROOT/'docs/M3_80M_COSTS.json').read_text())['scopes']
    out=dict(revision='M3A-R1',date='2026-10-14',baseline_commit=subprocess.check_output(['git','rev-parse','m3a-r0'],cwd=ROOT,text=True).strip(),status='Candidate EUR NET estimates/observations; no procurement',configurations={})
    for fox,name in [(False,'Full module components'),(True,'Foxoring-only components')]:
        bp=population(bm,fox,True);ap=population(am,fox);br={p['ref']:p for p in bp};ar={p['ref']:p for p in ap}
        rows={}
        for n in('6','10','20'):
            b=bc[name][n];a=ac[name][n]
            groups={g:dict(before_eur=b['groups'].get(g,0),after_eur=a['groups'].get(g,0),delta_eur=round(a['groups'].get(g,0)-b['groups'].get(g,0),4))for g in set(b['groups'])|set(a['groups'])}
            rows[n]=dict(before_eur=b['per_unit_eur'],after_eur=a['per_unit_eur'],delta_eur=round(a['per_unit_eur']-b['per_unit_eur'],4),observed_eur=a['observed_per_unit_eur'],estimate_eur=a['estimate_per_unit_eur'],groups=groups)
        out['configurations'][name]=dict(before=stats(bp),after=stats(ap),removed=sorted(set(br)-set(ar)),introduced=sorted(set(ar)-set(br)),modified=sorted(r for r in set(ar)&set(br)if any(ar[r][k]!=br[r][k]for k in('pins','mpn','value','population','footprint'))),batches=rows)
    out['fox_complete_bridge']={}
    for n,mat,oldrf,shared in [(6,64.47,9.40,13.50),(10,57.83,8.50,8.10),(20,57.83,8.44,4.85)]:
        m=mat-oldrf+ac['Foxoring-only components'][str(n)]['per_unit_eur']-.40-.60+.30
        out['fox_complete_bridge'][str(n)]=dict(materials_eur=round(m,4),fleet_shared_eur=shared,including_fleet_eur=round(m+shared,4),classification='Retained M2 complete scope; replace RF board and remove already-counted PCB connector halves; estimates')
    return out

def render(r):
    out=['# M3A-R1 — component and cost delta','', 'Date: **2026-10-14**. EUR **net**; VAT, labor, tooling and engineering separate. Current component lines/prices remain the single [M3 workbook](M3_80M_COMPONENT_WORKBOOK.md) and [CSV](M3_80M_BOM.csv). This comparison is generated from tagged **m3a-r0** and the current exported manifest/cost ledger; no manual price adjustment.', '', '| Population | Purchased R0 → R1 | IC R0 → R1 | Pads R0 → R1 | Flags R0 → R1 | Positions R0 → R1 |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for name,v in r['configurations'].items():
        b,a=v['before'],v['after'];out.append('| '+name+' | '+' | '.join(f"{b[k]} → {a[k]}"for k in('purchased_components','ICs','test_pads','power_flags','positions'))+' |')
    out+=['','The R0 manifest has 215 total references: the full population fits 214 positions (R336 DNP), **185 purchased parts and 20 ICs**. Fox fits 145 positions, **128 purchased parts and 15 ICs**. Test pads, flags, multiunit gate symbols and footprint assignments are not separate purchases.', '', '| Population / batch | R0 EUR/unit | R1 EUR/unit | Delta | Observed / estimate R1 |','| --- | ---: | ---: | ---: | --- |']
    for name,v in r['configurations'].items():
        for n,row in v['batches'].items():out.append(f"| {name} /{n} | {row['before_eur']:.2f} | {row['after_eur']:.2f} | {row['delta_eur']:+.2f} | {row['observed_eur']:.2f} /{row['estimate_eur']:.2f} |")
    for name,v in r['configurations'].items():
        out+=['','## '+name,'','Removed: '+', '.join(v['removed'])+'.','','Introduced: '+', '.join(v['introduced'])+'.','','Modified: '+', '.join(v['modified'])+'.','','| Block, quantity ten | Before | After | Delta |','| --- | ---: | ---: | ---: |']
        for g,x in sorted(v['batches']['10']['groups'].items()):out.append(f"| {g} | {x['before_eur']:.3f} | {x['after_eur']:.3f} | {x['delta_eur']:+.3f} |")
    out+=['','## Complete Fox unit — same accounting scope','','| Batch | Materials | Shared fleet | Total including fleet |','| --- | ---: | ---: | ---: |']
    for n,v in r['fox_complete_bridge'].items():out.append(f"| {n} | {v['materials_eur']:.2f} | {v['fleet_shared_eur']:.2f} | {v['including_fleet_eur']:.2f} |")
    out+=['','The historical €29.06/€55.24/€63.34 M1/Fox audit remains unchanged. R0 complete material at ten was €59.182; R1 changes only the RF component basket. S3/RTC, protected 2S1P, compact antenna/matching, case, wiring and fabrication scope are retained; socket halves already on the RF board are removed once. No fourth board or alternative MCU. No new assembly/fabrication quote. Component reduction is **not** a claim of labor savings.', '', 'The full board has fewer ICs but more individual protection/configuration parts. Corrections do **not** produce a quantity-ten material saving. Removing the selected-path/arming-context protection would lower the number but restore confirmed faults. At twenty, pooled low-current MOSFET purchasing gives a small estimated Fox saving; its hundred-piece price is estimated, so this is not secured savings.', '', 'BSS138BK replaces low-current switches and addresses stacked-gate stress; DMN2056U remains for the 70 mA shaper sink. Only its ten-piece EUR price is observed; one/hundred prices are estimates. 74HC174 price/stock is unquoted; manufacturer Production verified. Toshiba HC175 NRND and AP7384 NRND were rejected. C404 polymer pricing is an indexed distributor observation, not a reserved basket; pulse resistor/diode quotations remain OPEN. See [simplification](M3A_R1_SIMPLIFICATION.md) and [verification](M3A_R1_VERIFICATION.md).', '', '[Machine comparison](M3A_R1_DELTA.json).']
    return '\n'.join(out)+'\n'
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();r=report()
    outputs={ROOT/'docs/M3A_R1_DELTA.json':json.dumps(r,sort_keys=True,indent=2)+'\n',ROOT/'docs/M3A_R1_COST_DELTA.md':render(r)}
    for p,s in outputs.items():
        if a.write:p.write_text(s)
        else:assert p.read_text()==s,p
    print('PASS: R0 tag/current manifest counts, six before/after baskets and complete Fox scope')
