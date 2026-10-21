#!/usr/bin/env python3
"""Cost exact electrical populations; separate observed prices from allowances."""
import csv,json,math,copy
from collections import defaultdict
from pathlib import Path
P=Path(__file__).resolve().parents[1];A=P/'assembly';A.mkdir(exist_ok=True)
# USD catalog observations accessed 2026-10-21; not reserved inventory or checkout.
Q={
'ATTINY1616-MNR':('Mouser','https://www.mouser.com/en/ProductDetail/Microchip-Technology/ATTINY1616-MNR?qs=HXFqYaX1Q2yKNpuKQU9qww%3D%3D',{1:.90,25:.872},1,1,'16509 shown; refresh'),
'SI5351A-B-GT':('DigiKey','https://www.digikey.com/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847',{1:2.33,10:1.718},1,1,'4766 shown; cached prices vary'),
'74HCT240PW,118':('Mouser','https://www.mouser.com/ProductDetail/Nexperia/74HCT240PW118?qs=P62ublwmbi%252BM8OUN39MiMw%3D%3D',{1:.38,10:.262,25:.234},1,1,'4580 shown; refresh'),
'TPS61099DRVR':('LCSC C2842395','https://www.lcsc.com/product-image/C2842395.html',{1:.9925,10:.8432,30:.7694},1,1,'1293 shown; alternate page has MOQ10; refresh'),
'MCP1700T-3002E/TT':('LCSC C62244','https://www.lcsc.com/product-image/C62244.html',{1:.5207,10:.4123,30:.3663},1,1,'2186 shown; refresh'),
'DMP2035U-7':('LCSC C110499','https://lcsc.com/product-detail/MOSFETs_Diodes-Incorporated-DMP2035U-7_C110499.html',{10:.0569,100:.0454},10,10,'372830 cached; stale observation, refresh mandatory'),
'ABS07-32.768KHZ-T':('Mouser','https://www.mouser.com/en/ProductDetail/ABRACON/ABS07-32.768KHZ-T?qs=3SpAxaLJ01g8GJWeO3sA3Q%3D%3D',{1:.61,10:.528,25:.479},1,1,'cut tape; alternate Symmetry .61/.53'),
'CX3225FB25000F0FZZH1':('Mouser','https://www.mouser.com/ProductDetail/KYOCERA-AVX/CX3225FB25000F0FZZH1?qs=Tc%252BHE9vUsnv4CjUnsmTvrA%3D%3D',{1:.36,10:.31,25:.294},1,1,'50 detail / 17991 list; refresh'),
'CL05B104KO5NNNC':('LCSC C1525','https://www.lcsc.com/de/product-detail/C1525.html',{100:.0045,1000:.0034},100,100,'millions shown; locale price varies'),
'MF-FSMF020X-2':('DigiKey','https://www.digikey.com/en/products/detail/bourns-inc/MF-FSMF020X-2/2039254',{1:.54,5:.448,10:.414,50:.3432},1,1,'85792 shown; refresh'),
'1812LS-333XJRC':('Mouser','https://www.mouser.com/ProductDetail/Coilcraft/1812LS-333XJRC?qs=lc2O%252BfHJPVbUeCCXE6deKw%3D%3D',{1:1.18,10:.99,25:.908},1,1,'397 shown; refresh'),
'1008LS-102XJRC':('Mouser','https://www.mouser.com/ProductDetail/Coilcraft/1008LS-102XJRC',{1:1.48},1,1,'1134 shown; no unobserved quantity discount assumed'),
}
for value in ['332','222','103']:
 Q['1008LS-'+value+'XJRC']=('Coilcraft direct','https://www.coilcraft.com/en-us/products/rf/ferrite-core-chip-inductors/1008-%282520%29/1008ls/1008ls-'+value+'/',{1:1.00,200:.78},1,1,'catalog price; selected stock requires confirmation; cut tape no leader service')
def quote(p):
 mpn=p['mpn']
 if mpn in Q:
  supplier,url,prices,moq,multiple,stock=Q[mpn];basis='CATALOG OBSERVATION'
 else:
  basis='BUDGET ALLOWANCE, NOT A QUOTE';supplier='OPEN';url=p.get('source_url','');stock='Exact basket/availability OPEN';moq=10;multiple=10
  if p['ref'].startswith('R'):price=.005;moq=multiple=100
  elif p['ref'].startswith('C'):price=.12 if '0805' in p['footprint']else .08
  elif mpn=='2N7002,215':price=.08
  elif p['ref']=='J1':price=.95;moq=multiple=1
  elif p['ref']=='L1':price=.10
  elif p['ref'].startswith('L'):price=1.50;moq=multiple=1
  else:raise ValueError(p)
  prices={moq:price}
 return dict(supplier=supplier,url=url,breaks_USD=prices,moq=moq,multiple=multiple,availability=stock,basis=basis)
def pop(name):
 parts=copy.deepcopy(json.loads((P/'Mini80.electrical.json').read_text())['parts'])
 if name.startswith('FOX10'):
  for p in parts:
   if p['ref']in ['R'+str(i)for i in range(31,39)]:p.update(value='560',mpn='RC0402FR-07560RL')
 if name=='MINI50-wire-initial':
  for p in parts:
   if p['ref']in ['L30','C30','L31','L33']:p['population']='ALL'
   if p['ref']in ['R50','R51','R53']:p['population']='DNP'
 return [p for p in parts if not p['ref'].startswith(('#','TP'))and p['ref']not in ['J2','J3']]
def main():
 summary={'date_accessed':'2026-10-21','currency':'USD','status':'Parts estimate with quoted core and explicit unquoted allowances; no purchase or JLC checkout','excludes':['shipping','tax','tariffs','PCB','stencil','assembly','battery','housing','wire','fixture','test/calibration labor'],'variants':{}}
 for variant in ['MINI50-bench','FOX10-bench','MINI50-wire-initial']:
  parts=pop(variant);rows=[];groups=defaultdict(list)
  for p in parts:
   q=quote(p);rows.append({k:p.get(k,'')for k in ['ref','value','mpn','footprint','population','note']}|{'price_basis':q['basis'],'supplier':q['supplier'],'source_url':q['url']})
   if p['population']!='DNP':groups[p['mpn']].append(p)
  with (A/(variant+'-BOM.csv')).open('w')as f:
   w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
  costs=[]
  for boards in [5,12]:
   basket=[]
   for mpn,ps in sorted(groups.items()):
    q=quote(ps[0]);needed=boards*len(ps);buy=math.ceil(max(needed,q['moq'])/q['multiple'])*q['multiple'];price=q['breaks_USD'][max(n for n in q['breaks_USD']if n<=buy)]
    basket.append(dict(mpn=mpn,refs=' '.join(p['ref']for p in ps),per_board=len(ps),needed=needed,buy=buy,excess=buy-needed,unit_USD=price,extended_USD=round(price*buy,4),**q))
   total=sum(r['extended_USD']for r in basket);allow=sum(r['extended_USD']for r in basket if r['basis'].startswith('BUDGET'))
   costs.append(dict(boards=boards,total_USD=round(total,2),per_board_USD=round(total/boards,2),unquoted_allowance_USD=round(allow,2),basket=basket))
  summary['variants'][variant]={'placed_parts_per_board':sum(len(v)for v in groups.values()),'costs':costs}
 (A/'cost-review.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:[{s:t for s,t in c.items()if s!='basket'}for c in v['costs']]for k,v in summary['variants'].items()},indent=2))
if __name__=='__main__':main()
