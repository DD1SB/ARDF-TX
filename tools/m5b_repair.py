#!/usr/bin/python3
"""Remove exact CAD-reported conflicting track segments, preserving traceability."""
import json,sys
from m5b_design import HW,OUT
import m5a_r1_design as c
p=HW/'RF2M.kicad_pcb';b=c.parse(p.read_text());report=json.load(open(sys.argv[1]));bad={}
for v in report['violations']:
 if v['type']not in ['shorting_items','clearance','track_dangling']:continue
 for i in v['items']:
  if i['description'].startswith('Track '):bad[i['uuid']]=v['description']
removed=[]
for item in list(c.children(b,'segment')):
 uid=c.child(item,'uuid')[1]
 if uid in bad:removed.append(dict(uuid=uid,reason=bad[uid],actual_segment=item));b.remove(item)
 elif float(c.child(item,'width')[1])<.15:c.child(item,'width')[1]=c.Atom('.15')
p.write_text(c.dump(b)+'\n');(OUT/'routing-repair.json').write_text(json.dumps(removed,indent=2)+'\n');print('Removed',len(removed),'reported conflicts;remaining gaps require routing/nativeDRC')
