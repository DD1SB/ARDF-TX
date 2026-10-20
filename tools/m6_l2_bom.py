#!/usr/bin/python3
"""Native-manifest populations and explicit indexed/estimated cost deltas.
No quote, reservation, procurement or remote fabrication action.
"""
import json,csv,math,subprocess,collections
from m6_l2_design import P,D,BASE
from m6_c1_analysis import FOX_OMIT
QUANTITIES=[1,5,10,20]
RF=['FOX_MIN','RF80_FULL','RF2M_FULL','UNIVERSAL']
OPTIONS=['BASE','GPIO','FOXPRO','BOTH'];LORA=['NO_LORA','LORA_433','LORA_868']
S={}
def evidence(mpn,supplier,sku,moq,stock,currency,prices,url,kind='INDEXED_NOT_QUOTED'):
 S[mpn]=dict(supplier=supplier,sku=sku,minimum=moq,multiple=moq,indexed_stock=stock,currency=currency,price_breaks=prices,url=url,kind=kind,observed='2026-10-20',stock_reserved=False)
def init():
 evidence('ESP32-S3-WROOM-1U-N4','LCSC','C2980296',1,'1700..2128 regional indexed','USD',{1:4.4084,10:3.9152,30:3.6235},'https://www.lcsc.com/product-detail/C2980296.html')
 evidence('TCA9534APWR','LCSC','C206010',1,9998,'USD',{1:1.3727,10:1.1255,30:.9904},'https://www.lcsc.com/product-detail/C206010.html')
 evidence('TCA9517DR','LCSC','C182421',5,2045,'USD',{5:.3518,50:.2782},'https://lcsc.com/product-detail/Logic-ICs_TI_TCA9517DR_TCA9517DR_C182421.html')
 evidence('LM66100DCKR','LCSC','C2869734',5,34225,'USD',{5:.2374,50:.186},'https://www.lcsc.com/product-detail/C2869734.html')
 evidence('PESD1IVN24-AX','Mouser','771-PESD1IVN24-AX',1,5301,'USD',{1:.45,10:.311,100:.197},'https://www.mouser.com/en/ProductDetail/Nexperia/PESD1IVN24-AX?qs=0lQeLiL1qybgljIcQ3N7PA%3D%3D')
 evidence('CL10B103KB8NNNC','LCSC','C1589',50,1731900,'USD',{50:.0097,500:.0075},'https://www.lcsc.com/product-detail/C1589.html')
 evidence('BZX84-C12,215','LCSC','C108437',50,146050,'USD',{50:.0189,500:.0146},'https://www.lcsc.com/product-detail/C108437.html')
 evidence('BSS138BK,215','Mouser DE','771-BSS138BK-T/R',1,5781,'EUR',{1:.232,10:.099,100:.086},'https://www.mouser.de/de/ProductDetail/Nexperia/BSS138BK215?qs=A1cBxND5mHIu7uZeHkM5Xw%3D%3D')
 evidence('MMBT3904LT1G','LCSC','C81464',50,1688250,'USD',{50:.0167,500:.0133},'https://www.lcsc.com/product-detail/C81464.html')
 evidence('BAS316,115','LCSC','C109218',50,51900,'USD',{50:.0146,500:.011},'https://www.lcsc.com/product-detail/C109218.html')
 evidence('B3B-PH-K-S(LF)(SN)','LCSC','C131339',10,172230,'USD',{10:.0453,100:.037},'https://www.lcsc.com/zh-CN/product-detail/wire-to-board-connector_jst-b3b-ph-k-s-lf-sn_C131339.html')
 evidence('61301021121','Mouser DE','710-61301021121',1,9406,'EUR',{1:.946,10:.929,50:.86},'https://www.mouser.de/en/ProductDetail/Wurth-Elektronik/61301021121?qs=ZtY9WdtwX5612K9FdDCZCA%3D%3D')
 evidence('RC2512FK-07680RL','DigiKey','311-680AFCT-ND',1,4910,'USD',{1:.32,10:.17,25:.1384},'https://www.digikey.com/en/products/detail/yageo/RC2512FK-07680RL/5922351')
 evidence('RC2512FK-07470RL','Mouser EU','603-RC2512FK-07470RL',1,33460,'EUR',{1:.189,10:.105,50:.086},'https://eu.mouser.com/en/ProductDetail/YAGEO/RC2512FK-07470RL?qs=sGAEpiMZZMvdGkrng054t8AJgcdMkx7x8M1E0XPCVyA%3D')
 evidence('RC2512FK-0722RL','DigiKey','YAG3392CT-ND',1,31272,'USD',{1:.31,10:.166,25:.1348},'https://www.digikey.com/en/products/detail/yageo/RC2512FK-0722RL/5962214')
 for mpn,sku,stock,price in [('RC0603JR-070RL','C95177',3216500,.0031),('RC0603FR-07100KL','C14675',3111400,.0047),('RC0603FR-074K7L','C99782',6556400,.0043),('CL10B104KB8NNNC','C1591',2417100,.0086)]:
  evidence(mpn,'LCSC',sku,100,stock,'USD',{100:price},'https://www.lcsc.com/product-detail/'+sku+'.html')
 evidence('RC0603FR-071KL','South Electronics','RC0603FR071KL',1,3129,'EUR',{1:.10,10:.015,100:.008},'https://www.southelectronics.com/partdetail/yageo/rc0603fr071kl/23428','STOCK_INDEXED_PRICE_ESTIMATE')
 evidence('RC0603FR-0747KL','Mouser EU','603-RC0603FR-0747KL',1,476884,'EUR',{1:.086,10:.012,100:.007},'https://www.mouser.be/c/passive-components/resistors/smd-resistors-chip-resistors/thick-film-resistors/?case+code+-+in=0603&packaging=Reel&resistance=47+kOhms&tolerance=1+%25')
 evidence('RC0603FR-0710KL','Mouser','603-RC0603FR-0710KL',1,2782034,'USD',{1:.1,10:.014,100:.008},'https://www.mouser.com/en/ProductDetail/603-RC0603FR-0710KL')
 evidence('RC0603FR-07160RL','Mouser','603-RC0603FR-07160RL',1,47763,'USD',{1:.10,10:.014,100:.008},'https://www.mouser.com/en/ProductDetail/YAGEO/RC0603FR-07160RL')
 evidence('RC0603FR-07620RL','Mouser regional','603-RC0603FR-07620RL',1,71841,'USD',{1:.10,10:.014,100:.008},'https://www.mouser.in/en/ProductDetail/YAGEO/RC0603FR-07620RL','STOCK_INDEXED_PRICE_ESTIMATE')
def fitted(part,rf,lora,opt):
 pop=part['population'];r=part['ref'];groups={'ALL'}
 if rf in ['FOX_MIN','RF80_FULL','UNIVERSAL']:groups.add('RF80')
 if rf in ['RF2M_FULL','UNIVERSAL']:groups.add('RF2M')
 if lora!='NO_LORA':groups.add('LORA_OPTION')
 if opt in ['GPIO','BOTH']:groups.add('GPIO_OPTION')
 groups.add('FOXPRO' if opt in ['FOXPRO','BOTH'] else 'RECOVERY')
 return pop in groups and not(rf=='FOX_MIN' and r in FOX_OMIT) and not r.startswith(('#','TP','JP'))
def unit_price(s,n):
 q=max(n,s['minimum']);br={int(k):v for k,v in s['price_breaks'].items()};return br[max(k for k in br if k<=q)]
def baseline_price(part,n):
 br={int(k):v for k,v in part['price_breaks_eur'].items()};return br[max([k for k in br if k<=n] or [min(br)])]
def csvout(name,rows):
 if not rows:return
 with (D/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 init();m=json.loads((P/'CTRL.electrical.json').read_text());parts={x['ref']:x for x in m['parts']};old=json.loads(subprocess.check_output(['git','show',BASE+':hardware/controller/CTRL.electrical.json']));previous={x['ref']:x for x in old['parts']}
 new=[x for r,x in parts.items() if r not in previous and not r.startswith(('#','TP','JP'))];assert all(x['mpn'] in S for x in new)
 rows=[]
 for r,z in parts.items():
  if r.startswith(('#','TP','JP')):continue
  s=S.get(z['mpn']);rows.append(dict(ref=r,value=z['value'],mpn=z['mpn'],footprint=z['footprint'],population=z['population'],default='FITTED' if fitted(z,'UNIVERSAL','NO_LORA','BASE') else 'DNP',source_url=z['source_url'],supplier=s['supplier'] if s else z['supplier'],supplier_part=s['sku'] if s else z.get('supplier_part_number','OPEN'),moq=s['minimum'] if s else z['moq'],indexed_stock=s['indexed_stock'] if s else z['availability'],pricing='sourcing-index.json' if s else 'Inherited M6-L1 planning estimate; recheck before procurement'))
 csvout('BOM-all.csv',rows);delta=[z for z in rows if z['ref'] not in previous or z['ref']=='U10'];csvout('BOM-delta.csv',delta)
 variants={};costs={};buy=[]
 for rf in RF:
  for lora in LORA:
   for opt in OPTIONS:
    name=rf+'__'+lora+'__'+opt;fit={r for r,z in parts.items() if fitted(z,rf,lora,opt)}
    variants[name]=dict(fitted=sorted(fit),DNP=sorted(set(parts)-fit),UART='FOXPRO' if opt in ['FOXPRO','BOTH'] else 'RECOVERY',strap_links='OPEN')
    csvout('BOM-'+name+'.csv',[z for z in rows if z['ref'] in fit]);costs[name]={}
    # Compare the same RF/LoRa variant to L1, which has no interface links.
    oldfit={r for r,z in previous.items() if fitted(z,rf,lora,'BASE')}
    for q in QUANTITIES:
     added=collections.Counter(parts[r]['mpn'] for r in fit if r not in previous)
     delta_cost=sum(count*unit_price(S[mpn],q*count) for mpn,count in added.items())+unit_price(S[parts['U10']['mpn']],q)-baseline_price(previous['U10'],q)
     base=sum(baseline_price(previous[r],q) for r in oldfit)
     costs[name][str(q)]=dict(per_unit_added_component_planning_EUR=round(delta_cost,4),L1_same_population_reference_EUR=round(base,4),L2_component_planning_EUR=round(base+delta_cost,4),classification='ESTIMATE: indexed original currencies converted using planning factor1EUR/USD, not an exchange-rate quotation; excludes MOQ excess')
    if rf=='UNIVERSAL' and lora=='NO_LORA':
     grouped=collections.Counter(parts[r]['mpn'] for r in fit if r not in previous or r=='U10')
     for q in QUANTITIES:
      for mpn,count in sorted(grouped.items()):
       s=S[mpn];need=count*q;qty=max(s['minimum'],math.ceil(need/s['multiple'])*s['multiple']);buy.append(dict(option=opt,boards=q,mpn=mpn,required=need,purchase_quantity=qty,excess=qty-need,currency=s['currency'],indexed_or_estimated_unit_price=unit_price(s,qty),line_cost=round(qty*unit_price(s,qty),4),classification=s['kind']))
 (D/'population-variants.json').write_text(json.dumps(variants,indent=2)+'\n')
 (D/'sourcing-index.json').write_text(json.dumps(dict(date='2026-10-20',classification='Indexed observations; not quotations or reservations',parts=S,open_items=['All stock values are indexed and unreserved; recheck immediately before optional assembly procurement.','Panel TRS jack, mating PH housing/contacts, cable, strain relief and antenna are enclosure/harness selections and are unquoted.']),indent=2)+'\n')
 csvout('MOQ-purchase-model.csv',buy)
 (D/'costs.json').write_text(json.dumps(dict(classification='UNQUOTED planning estimates, not a fixed procurement total',currency_planning='1USD=1EUR deliberately conservative accounting factor, not current FX; evaluate±15% separately',quantities=QUANTITIES,variants=costs,excluded=['VAT, shipping, duty, assembly, spare parts, RF modules, antenna/cable, panel jack/harness, PCB and stencil','MOQ excess is separate in MOQ-purchase-model.csv'],bare_five_boards='100x100mm2L standard process; obtain a fresh quotation only after independent review. No order or upload performed.'),indent=2)+'\n')
 print(len(variants),'native population combinations;',len(new),'new purchased references; exact new MPNs',len(S))
if __name__=='__main__':main()
