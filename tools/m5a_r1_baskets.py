#!/usr/bin/python3
"""Function-normalized counterfactual baskets; only R1 economical design is implemented."""
import csv,json,copy
from pathlib import Path
import m5a_r1_costs as c
R=Path(__file__).resolve().parents[1];O=R/'hardware/2m/review/M5A-R1'
def main():
 r0=json.loads((R/'hardware/2m/archive/M5A-R0/RF2M.electrical.json').read_text())['parts']
 r1=json.loads((R/'hardware/2m/RF2M.electrical.json').read_text())['parts'];p0={p['ref']:p for p in r0};p1={p['ref']:p for p in r1}
 strong=copy.deepcopy(p1)
 # Replace cheap driver AND its indispensable supply; an8Vdriver cannot run from5VLDO.
 for ref in list(strong):
  if strong[ref]['group']=='driver_supply':del strong[ref]
 for ref,p in p0.items():
  if p['group']=='driver_supply':strong[ref]=copy.deepcopy(p)
 strong['U501']=copy.deepcopy(p0['U501'])
 # Strong-driver basket uses10V upstream for BOTH profiles; its8Vrail cannot use7.5V.
 # Keep the switches as test/tuning population, set feedback for10V in both profile states.
 for ref in ['R301','R302','R401','R402']:
  strong[ref]=copy.deepcopy(p0[ref])
 # Fixed10V upstream: normal/reduced RF remain controller calibrated, not supply-selected.
 for ref in ['R303','Q301','R414','Q307']:strong.pop(ref,None)
 strong['R817']=copy.deepcopy(p0['R817']);strong['R815']=copy.deepcopy(p0['R815'])
 baskets=[('R0_2S',r0,'BOOST2S'),('R0_4S',r0,'BUCK4S'),('R1_2S_PHA1',r1,'BOOST2S'),('R1_4S_PHA1',r1,'BUCK4S'),('R1_2S_PHA13_strong',list(strong.values()),'BOOST2S'),('R1_4S_PHA13_strong',list(strong.values()),'BUCK4S'),('R1_training',r1,'TRAIN_ONLY')]
 rows=[];summary=[]
 for name,parts,var in baskets:
  fitted=[p for p in parts if c.physical(p)and p['population']in c.VARIANTS[var]]
  for q in [6,10,20]:
   demand={}
   for p in fitted:
    mpn=c.effective(p,var)[1];demand[mpn]=demand.get(mpn,0)+1
   total=0
   for p in fitted:
    value,mpn=c.effective(p,var);price=c.price(p,q*demand[mpn]);total+=price
    rows.append(dict(basket=name,fleet=q,ref=p['ref'],block=p['group'],value=value,mpn=mpn,footprint=p['footprint']or'OPEN',order_quantity=q*demand[mpn],unit_net_eur=price,evidence=p['evidence'],supplier=p['supplier'],supplier_code=p['supplier_part_number'],source=p['source_url']))
   summary.append(dict(basket=name,fleet=q,net_eur=total,parts=len(fitted),IC=sum(p['ref'].startswith('U')for p in fitted)))
 with(O/'comparison-baskets.csv').open('w')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (O/'comparison-baskets.json').write_text(json.dumps(dict(summary=summary,strong_driver_scope='Counterfactual complete basket, not an implemented second PA. Retains8Vbuck/associated RCand thresholds; upstream>=10V for BOTH profiles, so reduced-power heat/endurance differs. No7.5Vprofile claim.'),indent=2)+'\n')
 print('BASKETS',len(summary),'totals',len(rows),'itemized rows')
if __name__=='__main__':main()
