#!/usr/bin/python3
"""Three dense local ground fanouts; manufacturer pad geometry unchanged."""
import math
from m5b_e5_common import *
REMOVED=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};records=[]
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString()=='61325f71-7c97-42d1-9463-e3aa683fe2e8':b.Remove(t);REMOVED.append(t)
 f=fs['R810'];old=f.GetPosition();pads=list(f.Pads());nets={a.GetNetname()for a in pads};found=None
 # Move only a two-terminal reference-divider resistor, not a sensitive RF part.
 candidates=sorted([(x/4,y/4)for x in range(456,521)for y in range(380,433)if 2.5<math.dist((x/4,y/4),xy(old))<9],key=lambda q:math.dist(q,xy(old)))
 for x,y in candidates:
  f.SetPosition(pt(x,y));okay=True;box=f.GetCourtyard(p.F_CrtYd).BBox()
  for other in fs.values():
   if other==f:continue
   ob=other.GetCourtyard(p.F_CrtYd).BBox()
   if box.Intersects(ob):okay=False;break
  if not okay:continue
  for a in f.Pads():
   sh=a.GetEffectiveShape(p.F_Cu)
   for o in list(b.GetTracks())+[z for ff in fs.values()if ff!=f for z in ff.Pads()]:
    if o.GetNetname()==a.GetNetname()or not o.IsOnLayer(p.F_Cu):continue
    if p.SHAPE.Collide(sh,o.GetEffectiveShape(p.F_Cu),MM(.16)):okay=False;break
   if not okay:break
  if okay:found=(x,y);break
 assert found,'No ordinary R810 placement found'
 oldpoints=[xy(a.GetPosition()-(f.GetPosition()-old))for a in f.Pads()]
 for t in list(b.GetTracks()):
  if t.GetNetname()in nets and not isinstance(t,p.PCB_VIA)and any(math.dist(xy(q),z)<.5 for q in[t.GetStart(),t.GetEnd()]for z in oldpoints):b.Remove(t);REMOVED.append(t)
 records.append(dict(ref='R810',old_mm=xy(old),new_mm=found,reason='Escape ground reference without via-in-SMD-land or reference/supply crossing'))
 def place(r,n,preferred):
  anchor=next(a for a in fs[r].Pads()if a.GetNumber()==n);origin=xy(anchor.GetPosition());obs=list(b.GetTracks())+[a for f in fs.values()for a in f.Pads()];found=None
  candidates=list(preferred)+[(origin[0]+d*math.cos(t*math.pi/8),origin[1]+d*math.sin(t*math.pi/8))for d in[1,1.2,1.5,1.8,2.2,2.7,3.3]for t in range(16)]
  for x,y in candidates:
   circ=p.SHAPE_CIRCLE(pt(x,y),MM(.3));env=p.SHAPE_CIRCLE(pt(x,y),MM(.29))
   if any(o.GetNetname()!='GND'and any(o.IsOnLayer(ly)and p.SHAPE.Collide(circ,o.GetEffectiveShape(ly),MM(.16))for ly in[p.F_Cu,p.B_Cu])for o in obs):continue
   if any(isinstance(o,p.PAD)and o.GetAttribute()==p.PAD_ATTRIB_SMD and p.SHAPE.Collide(env,o.GetEffectiveShape(p.F_Cu),0)for o in obs):continue
   for path in[[origin,(x,y)],[origin,(x,origin[1]),(x,y)],[origin,(origin[0],y),(x,y)]]:
    ts=[];okay=True
    for aa,zz in zip(path,path[1:]):
     if math.dist(aa,zz)<.000001:continue
     t=p.PCB_TRACK(b);t.SetStart(pt(*aa));t.SetEnd(pt(*zz));t.SetWidth(MM(.2));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet('GND'))
     if any(o.GetNetname()!='GND'and o.IsOnLayer(p.F_Cu)and p.SHAPE.Collide(t.GetEffectiveShape(p.F_Cu),o.GetEffectiveShape(p.F_Cu),MM(.16))for o in obs):okay=False;break
     ts.append(t)
    if okay:found=(x,y,ts,path);break
   if found:break
  assert found,('No source-ground fanout',r,n)
  x,y,ts,path=found
  for t in ts:b.Add(t)
  v=p.PCB_VIA(b);v.SetPosition(pt(x,y));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetNet(b.FindNet('GND'));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v)
  records.append(dict(ref=r,pin=n,via_mm=[x,y],path_mm=path,ordinary_land_drill_mm=[.6,.3],no_solder_land_hole=True))
 c=fs['C307'];oldpad=next(a for a in c.Pads()if a.GetNumber()=='1').GetPosition();oldxy=xy(oldpad)
 for t in list(b.GetTracks()):
  if t.GetNetname()=='VMOD'and not isinstance(t,p.PCB_VIA)and t.GetLayer()==p.F_Cu and any(math.dist(xy(q),oldxy)<.3 for q in[t.GetStart(),t.GetEnd()]):b.Remove(t);REMOVED.append(t)
 c.SetOrientationDegrees(c.GetOrientationDegrees()+180);records.append(dict(ref='C307',rotation_added_deg=180,reason='Groundlandfacesclearcopper,VMODbypassvaluenetunchanged'))
 place('C307','2',[(126.2,110.8),(126.3,110.4)])
 place('U701','3',[(130,111.8),(130.7,111.6),(130.5,111.5)])
 place('R810','2',[])
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('dense-ground-fanouts.json',dict(actions=records,values_pads_nets_changed=False,source98unchanged=True));print(records,flush=True)
if __name__=='__main__':main()
