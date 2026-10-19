#!/usr/bin/python3
"""Local escape placement using actual two-layer copper, not guessed via sites.

Every candidate rejects foreign copper on both layers and a .29mm drill-envelope
radius over any SMD land. Straight/L-shaped surface connections are checked too.
Final native DRC/DFM remain independent, mandatory checks.
"""
import math,json
from m5b_e5_common import *
REMOVED=[]
def uid(a):return a.m_Uuid.AsString()
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};records=[]
 # Remove only the unsuccessful, explicitly identified added escapes.
 positions={(122.8,100.35),(65.8,113.5),(66.7,113.5),(23.5,73.),(128.6,110.),(27.8,61.)}
 for t in list(b.GetTracks()):
  rm=isinstance(t,p.PCB_VIA)and xy(t.GetPosition())in positions
  if not isinstance(t,p.PCB_VIA):
   rm=any(xy(t.GetStart())==q or xy(t.GetEnd())==q for q in positions)and t.GetNetname()=='GND'
   rm|=t.GetNetname()=='CLK_TRAIN'and((128.6,110.)in[xy(t.GetStart()),xy(t.GetEnd())])
   # Replace the diagonal chip-ground escape by an exact horizontal escape.
   rm|=t.GetNetname()=='GND'and set([xy(t.GetStart()),xy(t.GetEnd())])=={(32.1,48.),(30.9,47.8)}
  if rm:b.Remove(t);REMOVED.append(t)
 # Open the ordinary source-supply escape, retaining its width/current role.
 for t in b.GetTracks():
  if t.GetNetname()=='VCLK'and not isinstance(t,p.PCB_VIA):
   for end in['Start','End']:
    q=xy(getattr(t,'Get'+end)())
    if q in[(26.1951,60.174),(26.1951,62.2666)]:getattr(t,'Set'+end)(pt(25.2,q[1]))
 def addline(net,points,w):
  for aa,zz in zip(points,points[1:]):
   if math.dist(aa,zz)<.000001:continue
   t=p.PCB_TRACK(b);t.SetStart(pt(*aa));t.SetEnd(pt(*zz));t.SetWidth(MM(w));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));b.Add(t)
 addline('GND',[(32.1,48),(30.9,48),(30.9,47.8)],.2)
 def cache():
  rows=[]
  for o in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
   for layer in[p.F_Cu,p.B_Cu]:
    if not o.IsOnLayer(layer):continue
    sh=o.GetEffectiveShape(layer);bb=sh.BBox();rows.append((o.GetNetname(),layer,sh,bb,o))
  for g in b.GetDrawings():
   if g.GetLayer()in[p.F_Cu,p.B_Cu]and hasattr(g,'GetNetname'):
    sh=g.GetEffectiveShape();rows.append((g.GetNetname(),g.GetLayer(),sh,sh.BBox(),g))
  return rows
 def near(a,z,gap):return not(a.GetRight()+gap<z.GetLeft()or z.GetRight()+gap<a.GetLeft()or a.GetBottom()+gap<z.GetTop()or z.GetBottom()+gap<a.GetTop())
 def place(anchor,net,w,land=.6,preferred=(),count=1):
  origin=xy(anchor.GetPosition());results=[]
  for number in range(count):
   rows=cache();candidates=list(preferred)
   if isinstance(anchor,p.PAD):candidates.append(xy(anchor.GetParentFootprint().GetPosition()))
   for d in[1.,1.2,1.5,1.8,2.2,2.7,3.3,4.]:
    for i in range(16):candidates.append((round((origin[0]+d*math.cos(i*math.pi/8))*20)/20,round((origin[1]+d*math.sin(i*math.pi/8))*20)/20))
   found=None
   for x,y in candidates:
    if not(21<x<169 and 21<y<129)or 84<x<100 and 27<y<73:continue
    v=p.SHAPE_CIRCLE(pt(x,y),MM(land/2));env=p.SHAPE_CIRCLE(pt(x,y),MM(.29));bb=v.BBox()
    if any(n!=net and near(bb,ob,MM(.16))and p.SHAPE.Collide(v,sh,MM(.16))for n,ly,sh,ob,o in rows):continue
    # Plated hole envelope outside all SMD solder lands, even this net's land.
    if any(isinstance(o,p.PAD)and o.GetAttribute()==p.PAD_ATTRIB_SMD and near(env.BBox(),ob,0)and p.SHAPE.Collide(env,sh,0)for n,ly,sh,ob,o in rows):continue
    if any(isinstance(o,p.PCB_VIA)and math.dist((x,y),xy(o.GetPosition()))<max(.65,land/2+p.ToMM(o.GetWidth(p.F_Cu))/2+.1)for n,ly,sh,ob,o in rows):continue
    if any(z.GetIsRuleArea()and z.GetDoNotAllowVias()and z.GetBoundingBox().Contains(pt(x,y))for z in b.Zones()):continue
    paths=[[origin,(x,y)],[origin,(origin[0],y),(x,y)],[origin,(x,origin[1]),(x,y)]]
    for path in paths:
     legal=True
     for aa,zz in zip(path,path[1:]):
      if math.dist(aa,zz)<.000001:continue
      t=p.PCB_TRACK(b);t.SetStart(pt(*aa));t.SetEnd(pt(*zz));t.SetWidth(MM(w));t.SetLayer(p.F_Cu);sh=t.GetEffectiveShape(p.F_Cu);box=sh.BBox()
      if any(n!=net and ly==p.F_Cu and near(box,ob,MM(.16))and p.SHAPE.Collide(sh,s,MM(.16))for n,ly,s,ob,o in rows):legal=False;break
     if legal:found=(x,y,path);break
    if found:break
   assert found,('No justified directviafanout',net,origin,land)
   x,y,path=found;via=p.PCB_VIA(b);via.SetPosition(pt(x,y));via.SetWidth(MM(land));via.SetDrill(MM(.3));via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(b.FindNet(net));via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via);addline(net,path,w);results.append(via);records.append(dict(net=net,origin_mm=origin,via_mm=[x,y],path_mm=path,trace_mm=w,land_mm=land,drill_mm=.3,drill_sensitivity_radius_mm=.29,hidden_solder_pad_hole=False))
  return results
 def pad(r,n):return next(a for a in fs[r].Pads()if a.GetNumber()==n)
 place(pad('U101','2'),'GND',.2,preferred=[(26.1,60.5),(26.1,61)])
 # Dense reference divider is connected by the independent ground router.
 # A guessed direct via here would cross the reference and supply copper.
 place(pad('C960','2'),'GND',.35,land=.6,count=1,preferred=[(65.8,110.2),(64,111.5)])
 # The existing unpopulated clock stub is a legitimate non-component anchor.
 stub=next((t for t in b.GetTracks()if not isinstance(t,p.PCB_VIA)and t.GetNetname()=='CLK_TRAIN'and((23.5,73.)in[xy(t.GetStart()),xy(t.GetEnd())])),None)
 if stub is None:
  stub=p.PCB_TRACK(b);stub.SetStart(pt(23.5,73));stub.SetEnd(pt(23.5,74));stub.SetWidth(MM(.15));stub.SetLayer(p.F_Cu);stub.SetNet(b.FindNet('CLK_TRAIN'));b.Add(stub)
 start=place(stub,'CLK_TRAIN',.15,preferred=[(24,73),(24,74)])[0];end=pad('U701','2')
 scl=pad('U102','2')
 upper=next(t for t in b.GetTracks()if t.GetNetname()=='SCL_CLK'and t.GetLayer()==p.B_Cu and not isinstance(t,p.PCB_VIA)and math.dist(xy(t.GetStart()),(26.8702,49.6694))<.5)
 requests=[]
 for a,z in[(start,end),(upper,scl)]:requests.append(dict(items=[dict(uuid=uid(q),pos=dict(zip(['x','y'],xy(q.GetPosition()))))for q in[a,z]]))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('precision-fanout.json',dict(status='ACTUAL_COPPER_CHECKED_LOCAL_ESCAPES_PENDING_FULL_DRC',native_sha256=sha(HW/'RF2M.kicad_pcb'),connections=records,ordinary_vias=True,no_guaranteed_tenting=True,source98unchanged=True));save('precision-route-requests.json',dict(unconnected_items=requests));print('Placed',len(records),'exactcoppercheckedescapes',flush=True)
if __name__=='__main__':main()
