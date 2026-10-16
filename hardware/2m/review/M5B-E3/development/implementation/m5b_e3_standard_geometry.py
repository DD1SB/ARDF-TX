#!/usr/bin/python3
"""Select larger ordinary vias/power copper where native clearance permits.
No tracks or via centres are moved by this pass. Congested positions retain
ordinary0.6/0.3vias,which exceedJLC's published via land requirements.
"""
import collections,math,json
import pcbnew as p
from m5b_e3_common import *
from m5b_e3_local import aliases,xy,uid

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));aa=aliases();objects=list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()];extras=[]
 for f in b.GetFootprints():
  if f.GetReference().startswith('TL'):
   for g in f.GraphicalItems():
    if g.GetLayer()==p.F_Cu:extras.append((g,next(iter(f.Pads())).GetNetname()))
 for g in b.GetDrawings():
  if g.GetLayer()in[p.F_Cu,p.B_Cu]and hasattr(g,'GetNetname'):extras.append((g,g.GetNetname()))
 def net(n):return aa.get(n,n)
 idx=collections.defaultdict(list)
 def keys(bb,gap=.2):
  return[(i,j)for i in range(math.floor((p.ToMM(bb.GetLeft())-gap)/4),math.floor((p.ToMM(bb.GetRight())+gap)/4)+1)for j in range(math.floor((p.ToMM(bb.GetTop())-gap)/4),math.floor((p.ToMM(bb.GetBottom())+gap)/4)+1)]
 for ob in objects:
  for k in keys(ob.GetBoundingBox()):idx[k].append(ob)
 def valid(t):
  near={uid(o):o for k in keys(t.GetBoundingBox())for o in idx[k]if uid(o)!=uid(t)and net(o.GetNetname())!=net(t.GetNetname())}
  for layer in[p.F_Cu,p.B_Cu]:
   if not t.IsOnLayer(layer):continue
   shape=t.GetEffectiveShape(layer)
   for o in near.values():
    if o.IsOnLayer(layer)and shape.Collide(o.GetEffectiveShape(layer),p.FromMM(.152)):return False
   for g,n in extras:
    if g.GetLayer()==layer and net(n)!=net(t.GetNetname()):
     poly=p.SHAPE_POLY_SET();g.TransformShapeToPolygon(poly,layer,0,p.FromMM(.002),p.ERROR_OUTSIDE)
     if poly.Collide(shape,p.FromMM(.152)):return False
  return True
 logs=[];vias=[]
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):
   x,y=xy(t.GetPosition());thermal=abs(x-112)<1 and abs(y-55)<2.2;old=p.ToMM(t.GetWidth(p.F_Cu));chosen=old
   if not thermal:
    for d in[.8,.7,.6]:
     t.SetWidth(p.FromMM(d))
     if valid(t):chosen=d;break
    t.SetWidth(p.FromMM(chosen))
   vias.append(dict(uuid=uid(t),net=t.GetNetname(),at_mm=[x,y],diameter_mm=chosen,drill_mm=p.ToMM(t.GetDrillValue()),ring_mm=round((chosen-p.ToMM(t.GetDrillValue()))/2,3),thermal_source=thermal,reason='Preferred0.25ring'if chosen>=.8 else'Existing congested control/decoupling connection;largerland conflicts withactualadjacentcopper. Standard0.3drill/land>=0.6(no premium process).'))
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA)or t.GetNetname()not in POWER_INPUT|POWER_RAIL:continue
  old=p.ToMM(t.GetWidth());length=p.ToMM(t.GetLength())
  if old<.49:continue
  best=old
  for w in([1.5,1.2,1,.8,.7,.6]if t.GetNetname()in POWER_INPUT else[1.2,1,.8,.7,.6]):
   if w<old:continue
   t.SetWidth(p.FromMM(w))
   if valid(t):best=w;break
  t.SetWidth(p.FromMM(best))
  logs.append(dict(uuid=uid(t),net=t.GetNetname(),layer=t.GetLayerName(),start_mm=xy(t.GetStart()),end_mm=xy(t.GetEnd()),length_mm=length,old_width_mm=old,width_mm=best))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('via-policy-exceptions.json',dict(vias=vias,counts=dict(collections.Counter(str(v['diameter_mm'])for v in vias)),note='Preference0.8/0.3;localexceptionsretainstandardviafabrication. NativeclearanceandindependentDFMremainmandatory.'));save('power-copper-changes.json',dict(paths=logs))
 print('Via diameter counts',collections.Counter(v['diameter_mm']for v in vias),'powersegments',len(logs))
if __name__=='__main__':main()
