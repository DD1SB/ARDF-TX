#!/usr/bin/python3
"""Remove only native-reported obsolete local switch routes for completion.
Run full DRC and reroute resulting local airwires; never a passing check itself.
"""
import json,sys
from pathlib import Path
from m5_2m_design import parse,dump,child,children,Atom
P=Path(__file__).resolve().parents[1]/'hardware/controller';D=P/'review/M6-C1'
s=parse((P/'CTRL.kicad_pcb').read_text());report=json.loads((D/'DRC.json').read_text());ids=set()
for v in report['violations']:
 if v['severity']!='error':continue
 for i in v['items']:
  if i['description'].startswith(('Track ','Via ')):ids.add(i['uuid'])
removed=[]
for kind in ['segment','via']:
 for item in children(s,kind)[:]:
  if str(child(item,'uuid')[1]) in ids:s.remove(item);removed.append(item)
for item in children(s,'gr_text'):
 if item[1]=='C10':child(item,'at')[1:3]=[Atom('35.8'),Atom('41.7')]
(P/'CTRL.kicad_pcb').write_text(dump(s)+'\n')
(D/'switch-local-reroute.json').write_text(json.dumps({'removed_route_UUIDs':sorted(ids),'removed_count':len(removed),'reason':'Larger manufacturer DBV landings replace smaller DCK; native DRC local clearances corrected before completing routes'},indent=2)+'\n')
print('Removed',len(removed),'reported local items; completing routes is mandatory')
