#!/usr/bin/python3
"""Open local routing exits for seven already-connected packages.
No new electrical net; all removed trace pieces require native DRC closure.
"""
import json,math
import pcbnew as p
from m5b_pcb import P,D,pt,xy,MM
from m3b_ground_fanout import point_segment,segdist
b=p.LoadBoard(str(P/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};pads=[pa for f in b.GetFootprints()for pa in f.Pads()if pa.IsOnLayer(p.F_Cu)or pa.IsOnLayer(p.B_Cu)];removed=[];logs=[]
for ref,pn,direction in [('U201','2',-1),('U201','6',1),('U304','8',1),('U304','2',-1),('U304','6',1),('U401','14',1),('U301','4',1)]:
    pa=next(a for a in fs[ref].Pads()if a.GetNumber()==pn);net=pa.GetNetname();a=xy(pa.GetPosition());end=None
    candidates=[]
    for dist in [2.,2.5,3.,3.5,4.]:candidates.append([a,(a[0]+direction*dist,a[1])])
    for stub in [1.1,1.4,1.7]:
      for dy in [-1.2,1.2,-1.8,1.8,-2.4,2.4]:candidates.append([a,(a[0]+direction*stub,a[1]),(a[0]+direction*stub,a[1]+dy)])
    chosen=None
    for path in candidates:
        e=path[-1];bad=False
        for q in pads:
            if q.GetNetname()==net:continue
            bb=q.GetBoundingBox();l,r,t,bt=[p.ToMM(x)for x in [bb.GetLeft(),bb.GetRight(),bb.GetTop(),bb.GetBottom()]]
            if l-.47<e[0]<r+.47 and t-.47<e[1]<bt+.47:bad=True;break
            for c0,c1 in [((l,t),(r,t)),((r,t),(r,bt)),((r,bt),(l,bt)),((l,bt),(l,t))]:
                if any(segdist(p0,p1,c0,c1)<.23 for p0,p1 in zip(path,path[1:])):bad=True;break
            if bad:break
        if not bad:end=e;chosen=path;break
    assert end,('No justified outward escape',ref,pn)
    gone=[]
    for tr in list(b.GetTracks()):
        if tr.GetNetname()==net:continue
        via=isinstance(tr,p.PCB_VIA);rad=p.ToMM(tr.GetWidth(p.F_Cu)if via else tr.GetWidth())/2
        clearance=point_segment(end,xy(tr.GetStart()),xy(tr.GetEnd()))<rad+.46
        if via or tr.GetLayer()==p.F_Cu:clearance|=any(segdist(a0,b0,xy(tr.GetStart()),xy(tr.GetEnd()))<rad+.23 for a0,b0 in zip(chosen,chosen[1:]))
        if not clearance:continue
        assert tr.GetNetname()not in ['PA_GATE','PA_DRAIN','ST_LPF_IN','ST_F1','ST_F2','NORMAL_RF'],('RF must not be touched',ref,pn)
        gone.append(dict(uuid=tr.m_Uuid.AsString(),net=tr.GetNetname(),start=xy(tr.GetStart()),end=xy(tr.GetEnd())));b.Remove(tr);removed.append(tr)
    for a0,b0 in zip(chosen,chosen[1:]):
        tr=p.PCB_TRACK(b);tr.SetStart(pt(*a0));tr.SetEnd(pt(*b0));tr.SetWidth(MM(.15));tr.SetLayer(p.F_Cu);tr.SetNet(pa.GetNet());tr.SetLocked(True);b.Add(tr)
    via=p.PCB_VIA(b);via.SetPosition(pt(*end));via.SetWidth(MM(.6));via.SetDrill(MM(.3));via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(pa.GetNet());via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via)
    logs.append(dict(ref=ref,pin=pn,net=net,pin_mm=a,escape_via_mm=end,removed_conflicting_segments=gone))
p.SaveBoard(str(P/'RF2M.kicad_pcb'),b);(D/'local-pin-escapes.json').write_text(json.dumps(logs,indent=2)+'\n');print('Prepared',len(logs),'physical pin escapes;removed',len(removed),'conflicting trace pieces for rerouting')
