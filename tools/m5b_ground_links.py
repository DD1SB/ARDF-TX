#!/usr/bin/python3
"""Translate disconnected filled-ground regions into explicit pad/via routes.
No waiver: chosen GND pads/actual main-region vias become a routing request;
native DRC still decides whether the islands are connected.
"""
import json,math
import pcbnew as p
from m5b_pcb import P,D,xy
b=p.LoadBoard(str(P/'RF2M.kicad_pcb'));groups=json.loads((D/'ground-region-stitching.json').read_text())['remaining_regions'];main=max(groups,key=lambda k:len(groups[k]));small={k:bb for k,bb in groups.items()if k!=main}
def inside(pt,bb):return bb[0]-.001<=pt[0]<=bb[2]+.001 and bb[1]-.001<=pt[1]<=bb[3]+.001
allboxes=[bb for bbs in small.values()for bb in bbs];gnd=[pa for f in b.GetFootprints()for pa in f.Pads()if pa.GetNetname()=='GND'];vias=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)and t.GetNetname()=='GND'and not any(inside(xy(t.GetPosition()),bb)for bb in allboxes)];out=[]
for key,boxes in small.items():
 pads=[pa for pa in gnd if any(inside(xy(pa.GetPosition()),bb)for bb in boxes)]
 if not pads:continue
 _,a,v=min(((math.dist(xy(a.GetPosition()),xy(v.GetPosition())),a,v)for a in pads for v in vias),key=lambda x:x[0])
 out.append(dict(region=key,items=[dict(uuid=x.m_Uuid.AsString(),pos=dict(x=xy(x.GetPosition())[0],y=xy(x.GetPosition())[1]))for x in [a,v]]))
 print(key,a.GetParentFootprint().GetReference(),a.GetNumber(),xy(a.GetPosition()),'to',xy(v.GetPosition()))
(D/'ground-link-gaps.json').write_text(json.dumps(dict(unconnected_items=out),indent=2)+'\n')
