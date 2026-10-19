#!/usr/bin/python3
"""Prune padless DC routing leaves; widen actual main VMOD copper where legal.
Exact native shapes and net contact graph, no DRC suppression or net reassignment.
"""
import collections,math,sys
from m5b_e5_common import *
REMOVED=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));pruned=[];widths=[]
 for net in([]if '--width-only'in sys.argv else['VMOD','VPA','OV_REF']):
  obs=[t for t in b.GetTracks()if t.GetNetname()==net]+[a for f in b.GetFootprints()for a in f.Pads()if a.GetNetname()==net];edges=collections.defaultdict(set);objs={o.m_Uuid.AsString():o for o in obs};pads={o.m_Uuid.AsString()for o in obs if isinstance(o,p.PAD)}
  for i,o in enumerate(obs):
   for z in obs[:i]:
    if any(o.IsOnLayer(ly)and z.IsOnLayer(ly)and p.SHAPE.Collide(o.GetEffectiveShape(ly),z.GetEffectiveShape(ly),MM(.001))for ly in[p.F_Cu,p.B_Cu]):edges[o.m_Uuid.AsString()].add(z.m_Uuid.AsString());edges[z.m_Uuid.AsString()].add(o.m_Uuid.AsString())
  queue=[u for u in objs if u not in pads and len(edges[u])<=1];gone=set()
  while queue:
   u=queue.pop()
   if u in gone or u in pads or len(edges[u]-gone)>1:continue
   gone.add(u);queue.extend(v for v in edges[u]if v not in pads)
  for u in gone:
   o=objs[u];pruned.append(dict(uuid=u,net=net,kind=o.GetClass(),reason='leaf of exact copper contact graph,not a component/test-pad terminal'));b.Remove(o);REMOVED.append(o)
 # Partition only long main-current VMOD conductors before local widening.
 # Same centreline/width first;this permits a local neck at a real obstacle
 # without constraining the entire80..100mmtrunk to that neck's width.
 subdivisions=[]
 for t in list(b.GetTracks()):
  if isinstance(t,p.PCB_VIA)or t.GetNetname()!='VMOD'or t.GetWidth()<MM(.5)or t.GetLength()<=MM(4):continue
  aa,zz=xy(t.GetStart()),xy(t.GetEnd());n=math.ceil(p.ToMM(t.GetLength())/2);prev=t.GetStart()
  for i in range(1,n+1):
   end=pt(aa[0]+(zz[0]-aa[0])*i/n,aa[1]+(zz[1]-aa[1])*i/n);q=p.PCB_TRACK(b);q.SetStart(prev);q.SetEnd(end);q.SetWidth(t.GetWidth());q.SetLayer(t.GetLayer());q.SetNet(t.GetNet());b.Add(q);prev=end
  subdivisions.append(dict(old_uuid=t.m_Uuid.AsString(),pieces=n,centreline_start_mm=aa,centreline_end_mm=zz));b.Remove(t);REMOVED.append(t)
 wanted={t.m_Uuid.AsString()for t in b.GetTracks()if not isinstance(t,p.PCB_VIA)and t.GetNetname()=='VMOD'and t.GetWidth()>=MM(.5)}

 copper=[];holes=[]
 for o in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
  for ly in[p.F_Cu,p.B_Cu]:
   if o.IsOnLayer(ly):copper.append((o.GetNetname(),ly,o.GetEffectiveShape(ly),o))
  if isinstance(o,p.PAD)and o.GetAttribute()==p.PAD_ATTRIB_NPTH:
   poly=p.SHAPE_POLY_SET();o.TransformHoleToPolygon(poly,0,MM(.002),p.ERROR_OUTSIDE);holes.append(poly)
 for g in list(b.GetDrawings())+[g for f in b.GetFootprints()for g in f.GraphicalItems()]:
  if g.GetLayer()not in[p.F_Cu,p.B_Cu]:continue
  poly=p.SHAPE_POLY_SET();g.TransformShapeToPolygon(poly,g.GetLayer(),0,MM(.002),p.ERROR_OUTSIDE);copper.append((g.GetNetname()if hasattr(g,'GetNetname')else'RF',g.GetLayer(),poly,g))
 for t in b.GetTracks():
  if t.m_Uuid.AsString()not in wanted or isinstance(t,p.PCB_VIA):continue
  old=p.ToMM(t.GetWidth());selected=old
  for w in[2.,1.8,1.5,1.2]:
   if w<=old:continue
   t.SetWidth(MM(w));sh=t.GetEffectiveShape(t.GetLayer());bb=sh.BBox()
   if min(p.ToMM(bb.GetLeft())-20,p.ToMM(bb.GetTop())-20,170-p.ToMM(bb.GetRight()),130-p.ToMM(bb.GetBottom()))<.5:continue
   if any(n!='VMOD'and ly==t.GetLayer()and p.SHAPE.Collide(sh,s,MM(.16))for n,ly,s,o in copper):continue
   if any(p.SHAPE.Collide(sh,s,MM(.5))for s in holes):continue
   selected=w;break
  t.SetWidth(MM(selected))
  if selected!=old:widths.append(dict(uuid=t.m_Uuid.AsString(),layer=t.GetLayerName(),old_mm=old,new_mm=selected,length_mm=p.ToMM(t.GetLength())))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('power-copper-correction.json',dict(pruned_DC_leaves=pruned,centreline_partitions=subdivisions,width_changes=widths,reason='Full-segment80CmainVMODdrop initially0.357V;broadenfreecopperwithoutmovingRFgeometry orusingthincontrolbranches',component_or_net_changes=False,physical='NOT_RUN'));print('Pruned',len(pruned),'DCleaves;widened',len(widths),'VMODsegments',flush=True)
if __name__=='__main__':main()
