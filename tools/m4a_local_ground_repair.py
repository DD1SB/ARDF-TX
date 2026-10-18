#!/usr/bin/python3
"""Make four local routing openings for real IC-ground stitching.
Only V1 changes. No symbol/value/functional net change or DRC suppression.
Signal gaps are deliberately reported for the routing aid; all must close
and native DRC pass before fabrication exports are generated.
"""
import json,math
import pcbnew as p
from m4a_design import P,D,NAME,MM
from m3b_pcb import pt,xy
from m3b_ground_fanout import point_segment
FIXES=[('U501 return',(112.5,113.6),'d8dea6fa-1654-45c3-aff1-bcacaa7c76ca'),('R112 return',(55.9,68.9),'27d02a67-3c5c-4da1-ac69-5484246a78e7'),('U312 return',(96.7,59.3),'8687dbdd-a785-4425-af92-4dc363da491c'),('U401 return',(121.5,36.3),'dcacc6a0-bb25-4509-95d9-f9b539382fc8')]
def main():
    b=p.LoadBoard(str(P/(NAME+'.kicad_pcb')));items={t.m_Uuid.AsString():t for t in b.GetTracks()};removed=[];cases=[];logs=[]
    for label,pos,uid in FIXES:
        t=items[uid];net=t.GetNetname();ends=[xy(t.GetStart()),xy(t.GetEnd())];layer=t.GetLayer();b.Remove(t);removed.append(t);eitems=[]
        for ep in ends:
            candidates=[q for q in b.GetTracks()if q.GetNetname()==net and(isinstance(q,p.PCB_VIA)or q.GetLayer()==layer)and point_segment(ep,xy(q.GetStart()),xy(q.GetEnd()))<.001]
            candidates.extend(q for f in b.GetFootprints()for q in f.Pads()if q.GetNetname()==net and q.IsOnLayer(layer)and q.HitTest(pt(*ep)))
            assert candidates,(label,net,'No physical copper at removed-track endpoint',ep)
            q=candidates[0];eitems.append(dict(uuid=q.m_Uuid.AsString(),pos=dict(zip(('x','y'),ep)),description=net))
        via=p.PCB_VIA(b);via.SetPosition(pt(*pos));via.SetWidth(MM(.6));via.SetDrill(MM(.3));via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(b.FindNet('GND'));via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via)
        cases.append(dict(items=eitems));logs.append(dict(reason=label,new_ground_via_mm=pos,removed_signal_segment=dict(uuid=uid,net=net,start=ends[0],end=ends[1],layer=b.GetLayerName(layer))))
    b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(P/(NAME+'.kicad_pcb')),b);(D/'local-ground-openings.json').write_text(json.dumps(logs,indent=2)+'\n');(D/'local-ground-signal-gaps.json').write_text(json.dumps(dict(unconnected_items=cases),indent=2)+'\n');print('Four local ground openings made; four signal routes require closure before DRC PASS')
if __name__=='__main__':main()
