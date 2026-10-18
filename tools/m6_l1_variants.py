#!/usr/bin/python3
"""Orthogonal base-controller/radio populations; explicit alternate module BOMs."""
import json,csv,copy
from pathlib import Path
from m6_c1_analysis import fitted_part,VARIANTS
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-L1'
RADIO={'U70','J7','C70','C71','R70','R71'}
def main():
 parts=json.loads((P/'CTRL.electrical.json').read_text())['parts'];parts=[p for p in parts if not p['ref'].startswith(('#','TP'))];out={};cost={}
 fields=['ref','value','mpn','footprint','population','fitted','quantity_per_unit','supplier','supplier_part_number','availability','moq','evidence','price_1_eur','price_10_eur','price_20_eur']
 for base in ['FOX_MIN','RF80_FULL','RF2M_FULL','UNIVERSAL']:
  for opt in ['NO_LORA','LORA_433','LORA_868']:
   name=base+'_'+opt;rows=[];total={str(q):0 for q in [1,10,20]};unquoted=copy.copy(total)
   for pp in parts:
    a=copy.deepcopy(pp);fit=fitted_part(a,base) or (opt!='NO_LORA' and a['ref'] in RADIO)
    if a['ref']=='U70' and opt=='LORA_433':a.update(value='Silicontra SX1262TR4-GC',mpn='SX1262TR4-GC',supplier_part_number='C42381681',availability='189 indexed; not reserved',price_breaks_eur={'1':5.5656*.9,'10':4.7161*.9,'20':4.7161*.9})
    prices={q:float(max((int(k),v) for k,v in a['price_breaks_eur'].items() if int(k)<=q)[1]) for q in [1,10,20]}
    row={k:a.get(k,'OPEN') for k in fields if not k.startswith('price_')};row.update(fitted='FIT' if fit else 'DNP',quantity_per_unit=1 if fit else 0,**{f'price_{q}_eur':v for q,v in prices.items()});rows.append(row)
    if fit:
     for q,v in prices.items():total[str(q)]+=v;unquoted[str(q)]+=0 if a['evidence'].startswith('OBSERVED') else v
   out[name]={'base':base,'radio':opt,'fitted':[x['ref'] for x in rows if x['fitted']=='FIT'],'DNP':[x['ref'] for x in rows if x['fitted']=='DNP'],'selected_U70':next(x['mpn'] for x in rows if x['ref']=='U70') if opt!='NO_LORA' else None};cost[name]={'netEUR_per_unit':{q:round(v,3) for q,v in total.items()},'unquoted_netEUR':{q:round(v,3) for q,v in unquoted.items()}}
   with (D/('BOM-'+name+'.csv')).open('w') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 for name,x in out.items():
  assert set(x['fitted'])&RADIO==(set() if x['radio']=='NO_LORA' else RADIO)
 (D/'LoRa-populations.json').write_text(json.dumps(out,indent=2)+'\n');(D/'LoRa-costs.json').write_text(json.dumps(dict(classification='NetEUR planning estimates incl indexed prices; no supplier quote',USD_to_EUR_planning_factor=.90,FX_status='Engineering allowance, not an exchange-rate observation; assess +/-10%',shipping_import_VAT='Excluded/unquoted',variants=cost),indent=2)+'\n')
 print({k:v['netEUR_per_unit']['10'] for k,v in cost.items()})
if __name__=='__main__':main()
