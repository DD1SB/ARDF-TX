#!/usr/bin/python3
"""Candidate allowances, not a released order list. Never fill unavailable quotes with fake observations."""
import csv,json,collections,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'hardware/2m';O=D/'review/M5A-R1'
VARIANTS={'BOOST2S':{'ALL','NORMAL','BOOST2S'},'BUCK4S':{'ALL','NORMAL','BUCK4S'},'TRAIN_ONLY':{'ALL','TRAIN_ONLY'}}
def physical(p):return not p['ref'].startswith(('TP','#'))
def price(p,qty):
 b={int(k):v for k,v in p['price_breaks_eur'].items()};return b[max(k for k in b if k<=qty)]
def effective(p,var):
 value=p.get('variant_values',{}).get(var,p['value']);mpn=p['mpn']
 if value!=p['value']:
  raw=value[:-1]
  code=raw.replace('.','K')if'.'in raw else raw+'K'
  mpn=p['mpn'].split('-07')[0]+'-07'+code+'L'
 return value,mpn
def main():
 m=json.loads((D/'RF2M.electrical.json').read_text());parts=m['parts'];rows=[];summary=[]
 for var,allowed in VARIANTS.items():
  fitted=[p for p in parts if physical(p)and p['population']in allowed]
  for q in [6,10,20]:
   demand=collections.Counter(effective(p,var)[1]for p in fitted);blocks=collections.defaultdict(float);total=0;observed=0
   for p in fitted:
    value,mpn=effective(p,var)
    needed=demand[mpn]*q;ordered=math.ceil(max(needed,p['moq'])/p['multiple'])*p['multiple'];unit=price(p,ordered);extended=unit*ordered/needed
    blocks[p['group']]+=extended;total+=extended
    if p['evidence'].startswith('OBSERVED'):observed+=extended
    rows.append(dict(variant=var,fleet=q,ref=p['ref'],group=p['group'],value=value,mpn=mpn,footprint=p['footprint']or'OPEN',quantity_per_board=1,fleet_component_demand=needed,order_qty_assumption=ordered,moq=p['moq'],multiple=p['multiple'],unit_net_eur_allowance=unit,per_board_net_eur=extended,evidence=p['evidence'],supplier=p['supplier'],supplier_part_number=p['supplier_part_number'],availability=p['availability'],source_url=p['source_url'],note=p['note']))
   summary.append(dict(variant=var,fleet=q,fitted_physical=len(fitted),ic_count=sum(p['ref'].startswith('U')for p in fitted),component_allowance_net_eur=total,observed_display_price_based_allowance=observed,remaining_estimates_net_eur=total-observed,blocks=dict(blocks),open_mpn_refs=[p['ref']for p in fitted if p['mpn'].startswith('OPEN')],open_footprint_refs=[p['ref']for p in fitted if not p['footprint']]))
 with(O/'RF2M_BOM.csv').open('w')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 # Master positions, including omitted and non-physical features, not confused with shopping quantities.
 with(O/'RF2M_positions.csv').open('w')as f:
  fields=['ref','value','mpn','footprint','group','population','evidence','supplier','supplier_part_number','availability','source_url','note'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(parts)
 result=dict(date='2026-10-15',currency='EUR',basis='EUR net allowances; PD54008L-E DigiKey IT displayed net price, PHA-1+ Mouser EU display provisionally held as net without tax deduction. Other estimates carried from frozen R0. No quotes or orders.',physical_position_count=sum(physical(p)for p in parts),all_positions=len(parts),summary=summary,external_allowances=dict(pcb_per_board=[2,6],rf_harness=[2,4],antenna_feeder=[8,15],thermal=[4,7],controller_shared=[15,20],enclosure=[3,6],bms_2s=[2,4],bms_4s=[3,6],pack_interconnect=[3,5],shared_charger_per_fleet=[15,25]),labor='EXCLUDED; explicit future measurements for minutes per assembly/calibration',pricing_warning='U501/Q501 use indexed displayed price observations, not live stock reservations; RF inductor familyUSD0.92/ECB conversion remains an allowance pending exact value checkout. Other lines are estimates. MOQ1 for estimated rows is an assumption, not sourcing verification.')
 (O/'costs.json').write_text(json.dumps(result,indent=2)+'\n')
 for x in summary:print(x['variant'],x['fleet'],'parts',x['fitted_physical'],'IC',x['ic_count'],'EUR',round(x['component_allowance_net_eur'],2),'unquotedMPNs',len(x['open_mpn_refs']))
if __name__=='__main__':main()
