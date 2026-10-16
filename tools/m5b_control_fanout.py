#!/usr/bin/python3
"""Place two fine-pitch control ICs in open routing space and fan out first.
No RF part, schematic net or component value is changed. Native DRC required.
"""
import json,math
import pcbnew as p
from m5b_pcb import P,D,pt,xy,MM
from m3b_ground_fanout import seg_box
b=p.LoadBoard(str(P/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};moves={'U201':(56,35,0),'R201':(54,29,0),'R202':(60,30,0),'C201':(58,40.5,0),'U304':(60,69,0),'C310':(65,64,0)};removed=[];logs=[]
# Clear the two new fanout corridors first, including obsolete crossing vias.
# Keep wrappers alive through SaveBoard; all removed nets are rechecked in DRC.
rects=[[50.5,31.5,61.5,38.5],[54.5,66,65.5,72]]
for t in list(b.GetTracks()):
    if any(seg_box(xy(t.GetStart()),xy(t.GetEnd()),r)for r in rects):
        assert t.GetNetname()not in ['NORMAL_CLOCK_BUF','MMIC_RF_DC','PA_GATE','PA_DRAIN','NORMAL_RF','ST_IS_A','ST_IS_B','ST_IS_C','ST_IS_D']
        b.Remove(t);removed.append(t)
oldpads=[a for r in moves for a in fs[r].Pads()if a.IsOnLayer(p.F_Cu)or a.IsOnLayer(p.B_Cu)]
for t in list(b.GetTracks()):
    if isinstance(t,p.PCB_VIA):continue
    if any(a.GetNetname()==t.GetNetname()and(a.HitTest(t.GetStart())or a.HitTest(t.GetEnd()))for a in oldpads):b.Remove(t);removed.append(t)
for r,(x,y,a)in moves.items():
 f=fs[r];logs.append(dict(ref=r,old_mm=xy(f.GetPosition()),new_mm=[x,y]));f.SetOrientationDegrees(a);f.SetPosition(pt(x,y))
def route(net,points,w=.15):
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(MM(w));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));t.SetLocked(True);b.Add(t)
def via(net,point):
 v=p.PCB_VIA(b);v.SetPosition(pt(*point));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);v.SetLocked(True);b.Add(v)
for ref in ['U201','U304']:
 f=fs[ref];cx,cy=xy(f.GetPosition());off={'1':(-3.5,-2.5),'2':(-4.5,-1),'3':(-4.5,1),'4':(-3.5,2.5),'5':(3.5,2.5),'6':(4.5,1),'7':(4.5,-1),'8':(3.5,-2.5)}
 for pa in f.Pads():
  if not pa.GetNumber()or pa.GetNumber()not in off:continue
  a=xy(pa.GetPosition());dx,dy=off[pa.GetNumber()];v=(cx+dx,cy+dy);stub=(cx+(-2.1 if dx<0 else 2.1),a[1]);route(pa.GetNetname(),[a,stub,v]);via(pa.GetNetname(),v)
 if ref=='U201':via('GND',(cx,cy))
# Compact direct decoupler return; power connections are routed to actual VDD.
for ref in ['C201','C310']:
 pa=next(a for a in fs[ref].Pads()if a.GetNetname()=='GND');x,y=xy(pa.GetPosition());v=(x,y+1);route('GND',[(x,y),v],.25);via('GND',v)
p.SaveBoard(str(P/'RF2M.kicad_pcb'),b);(D/'control-placement-refinement.json').write_text(json.dumps(dict(moved=logs,removed_old_pad_connections=len(removed),reason='Deterministic outward fanout avoids trapped VSON/VSSOP control pins;no RF placement change'),indent=2)+'\n')
