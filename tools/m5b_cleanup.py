#!/usr/bin/python3
"""Remove routing remnants which reach no actual component/test pad.
Uses native KiCad copper connectivity; never treats an unrouted required pad
as disposable. No DRC category or intentional electrical connection is hidden.
"""
import json
import pcbnew as p
from m5b_pcb import P,D,MM
b=p.LoadBoard(str(P/'RF2M.kicad_pcb'));b.BuildConnectivity();cc=b.GetConnectivity();dead=[];logs=[];seen=set()
for tr in b.GetTracks():
 if tr.m_Uuid.AsString()in seen:continue
 cluster=list(cc.GetConnectedItems(tr));seen.update(x.m_Uuid.AsString()for x in cluster)
 if any(x.GetClass()=='PAD'for x in cluster):continue
 if tr.GetNetname()=='GND':continue
 for x in cluster:
  if x.GetClass()not in ['PCB_TRACK','PCB_VIA','PCB_ARC']:continue
  dead.append(x);logs.append(dict(uuid=x.m_Uuid.AsString(),net=x.GetNetname(),reason='Copper component contains no actual footprint pad'))
for tr in dead:b.Remove(tr)
# Merge only exact duplicate same-net vias, retaining all touching endpoints.
seen_v={};duplicates=[]
for tr in list(b.GetTracks()):
 if not isinstance(tr,p.PCB_VIA):continue
 key=(tr.GetNetname(),tr.GetPosition().x,tr.GetPosition().y)
 if key in seen_v:b.Remove(tr);duplicates.append(tr)
 else:seen_v[key]=tr
p.SaveBoard(str(P/'RF2M.kicad_pcb'),b);old=json.loads((D/'copper-cleanup.json').read_text())if(D/'copper-cleanup.json').exists()else[];old.extend(logs);(D/'copper-cleanup.json').write_text(json.dumps(old,indent=2)+'\n');print('Removed',len(dead),'padless remnant copper objects and',len(duplicates),'exact duplicate vias')
