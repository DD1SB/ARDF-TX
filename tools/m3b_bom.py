#!/usr/bin/env python3
"""M3B baskets from the actual manifest; never overwrites historical M3A prices."""
import csv,json,math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 m=json.loads((ROOT/'hardware/80m/RF80.electrical.json').read_text());parts=[p for p in m['parts']if not p['ref'].startswith(('#','TP'))];scopes={}
 for name,pops in [('Full',('BOTH','NORMAL')),('Fox',('BOTH','FOX'))]:
  ps=[p for p in parts if p['population']in pops];rr={}
  for n in (1,3,5,6,10,20):
   pools=defaultdict(list)
   for p in ps:pools[p['mpn']].append(p)
   total=observed=0.;lines=[];groups=defaultdict(float)
   for mpn,pp in sorted(pools.items()):
    p=pp[0];need=len(pp)*n;order=math.ceil(max(need,p['moq'])/p['multiple'])*p['multiple'];br=max(int(k)for k in p['price_breaks_eur']if int(k)<=order);price=p['price_breaks_eur'][str(br)];cash=price*order;total+=cash
    obs=p['evidence'].startswith('OBSERVED');observed+=cash if obs else 0
    for q in pp:groups[q['group']]+=cash/len(pp)/n
    lines.append(dict(refs=', '.join(q['ref']for q in pp),mpn=mpn,footprint=p['footprint'],needed=need,ordered=order,leftover=order-need,moq=p['moq'],multiple=p['multiple'],price_break=br,unit_eur=price,allocated_per_board_eur=round(cash/n,6),evidence=p['evidence'],supplier=p['supplier'],supplier_code=p['supplier_part_number'],stock=p['availability'],source=p['source_url'],note=p['note']))
   rr[str(n)]=dict(per_board_eur=round(total/n,4),batch_eur=round(total,4),historical_observation_eur=round(observed/n,4),estimate_eur=round((total-observed)/n,4),groups={k:round(v,4)for k,v in groups.items()},lines=lines)
  scopes[name]=dict(purchased_parts=len(ps),ICs=sum(p['ref'].startswith('U')for p in ps),batches=rr)
 r=dict(date='2026-10-14',revision='M3B-E1',currency='EUR NET; VAT excluded',status='Candidate baskets; dated observations not fresh quotes; no procurement',scopes=scopes)
 (ROOT/'docs/M3B_COSTS.json').write_text(json.dumps(r,indent=2)+'\n')
 with(ROOT/'docs/M3B_BOM.csv').open('w')as f:
  fields=['population','batch']+list(scopes['Full']['batches']['1']['lines'][0]);w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader()
  for scope,x in scopes.items():
   for n,b in x['batches'].items():
    for l in b['lines']:w.writerow(dict(population=scope,batch=n,**l))
 out=['# M3B — itemized component workbook','','Generated from the M3B-E1 manifest. EUR net. Same MPNs pooled across each population; **ordered quantities are per MPN pool**, not repeated per reference. Historical observations retain the exact source limitations; estimated values and OPEN supplier codes are unquoted. No order is authorized. PCB, batteries, antenna, harness mates, thermal fixture, labor and instruments are separate. All 74 test pads and four mounting holes are fabricated features, not purchased parts. TH301 is one purchased remote sensor, not two.','','| Population | Physical purchases | ICs | 1 board | 3 boards, each | 5 boards, each | 6 | 10 | 20 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
 for name,x in scopes.items():out.append('| '+name+' | '+str(x['purchased_parts'])+' | '+str(x['ICs'])+' | '+' | '.join(f"{x['batches'][str(n)]['per_board_eur']:.3f}"for n in (1,3,5,6,10,20))+' |')
 for name,x in scopes.items():
  out+=['','## '+name,'','| MPN / refs | Footprint | Supplier / code / MOQ / multiple | Price provenance / availability | Unit price at batch 1 / 6 / 10 / 20 | Allocated per board at 1 / 6 / 10 / 20 |','| --- | --- | --- | --- | ---: | ---: |']
  for l in x['batches']['1']['lines']:
   rows=[next(q for q in x['batches'][str(n)]['lines']if q['mpn']==l['mpn'])for n in (1,6,10,20)];src=f"[source]({l['source']})"if l['source']else'Unquoted'
   clean=lambda a:str(a).replace('|','/').replace('\n',' ')
   out.append('| '+ ' | '.join(map(clean,[l['mpn']+'; '+l['refs'],l['footprint'],f"{l['supplier']}; {l['supplier_code']}; MOQ{l['moq']}; multiple{l['multiple']}",f"{l['evidence']}; {l['stock']}; {src}",' / '.join(f"{q['unit_eur']:.4f}"for q in rows),' / '.join(f"{q['allocated_per_board_eur']:.4f}"for q in rows)]))+' |')
 out+=['','[CSV with required/ordered/leftover quantities](M3B_BOM.csv). [All basket and functional-block totals](M3B_COSTS.json). [Evaluation versus production scope](M3B_EVALUATION_BOM.md).']
 (ROOT/'docs/M3B_COMPONENT_WORKBOOK.md').write_text('\n'.join(out)+'\n')
 print({k:dict(count=v['purchased_parts'],ICs=v['ICs'],prices={n:q['per_board_eur']for n,q in v['batches'].items()})for k,v in scopes.items()})
if __name__=='__main__':main()
