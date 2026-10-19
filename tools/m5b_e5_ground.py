#!/usr/bin/python3
"""Exact native filled-copper contact graph; explicit ground bridge requests.

Distinct zone polygons are distinct nodes. Pad/via annuli contact the actual
filled polygon, not a test at its drilled-out centre. No new PCB is created.
"""
import collections,math
from m5b_e5_common import *
from m5b_e3_dfm import nearby,bbox
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));rows=[];objects={};parent={}
 def find(u):
  parent.setdefault(u,u)
  if parent[u]!=u:parent[u]=find(parent[u])
  return parent[u]
 def join(a,z):parent[find(a)]=find(z)
 def add(shape,node,layer,ob=None):
  rows.append(dict(shape=shape,id=node,layer=layer,bb=bbox(shape),object=ob));find(node)
  if ob:objects[node]=ob
 for ob in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
  if ob.GetNetname()!='GND':continue
  for layer in[p.F_Cu,p.B_Cu]:
   if ob.IsOnLayer(layer):add(ob.GetEffectiveShape(layer),ob.m_Uuid.AsString(),layer,ob)
 for zi,z in enumerate(b.Zones()):
  if z.GetIsRuleArea()or z.GetNetname()!='GND':continue
  pp=z.GetFilledPolysList(z.GetLayer())
  for i in range(pp.OutlineCount()):
   poly=p.SHAPE_POLY_SET();poly.AddOutline(pp.COutline(i))
   for h in range(pp.HoleCount(i)):poly.AddHole(pp.CHole(i,h),0)
   add(poly,f'zone{zi}.{i}',z.GetLayer())
 for g in b.GetDrawings():
  if g.GetLayer()not in[p.F_Cu,p.B_Cu]or not hasattr(g,'GetNetname')or g.GetNetname()!='GND':continue
  sh=p.SHAPE_POLY_SET();g.TransformShapeToPolygon(sh,g.GetLayer(),0,MM(.002),p.ERROR_OUTSIDE);add(sh,g.m_Uuid.AsString(),g.GetLayer())
 def contact(a,z):
  if a['id'].startswith('zone')and z['id'].startswith('zone'):return False # distinct polygons of one same-layer fill
  for zone,other in[(a,z),(z,a)]:
   if not zone['id'].startswith('zone'):continue
   ob=other.get('object');points=[]
   if ob is not None:
    if isinstance(ob,p.PCB_VIA)or isinstance(ob,p.PAD)and ob.GetDrillSize().x:
     radius=p.ToMM(ob.GetDrillValue()if isinstance(ob,p.PCB_VIA)else ob.GetDrillSize().x)/2+.05
     x,y=xy(ob.GetPosition());points=[pt(x+radius*math.cos(i*math.pi/4),y+radius*math.sin(i*math.pi/4))for i in range(8)]
    elif isinstance(ob,p.PAD):points=[ob.GetPosition()]
    else:
     points=[ob.GetStart(),ob.GetEnd(),pt(*[(x+y)/2 for x,y in zip(xy(ob.GetStart()),xy(ob.GetEnd()))])]
    # A point inside BOTH exact shapes is a positive copper-contact witness.
    if any(zone['shape'].Contains(q)and other['shape'].Collide(q)for q in points):return True
   return p.SHAPE.Collide(a['shape'],z['shape'],MM(.001))
  return p.SHAPE.Collide(a['shape'],z['shape'],MM(.001))
 for a,z in nearby(rows,.003):
  if a['layer']!=z['layer']or a['id']==z['id']or find(a['id'])==find(z['id']):continue
  if a['bb'][2]+.001<z['bb'][0]or z['bb'][2]+.001<a['bb'][0]or a['bb'][3]+.001<z['bb'][1]or z['bb'][3]+.001<a['bb'][1]:continue
  if contact(a,z):join(a['id'],z['id'])

 groups=collections.defaultdict(set)
 for node in parent:groups[find(node)].add(node)
 def score(nodes):return sum(max(0,r['bb'][2]-r['bb'][0])*max(0,r['bb'][3]-r['bb'][1])for r in rows if r['id']in nodes)
 main=max(groups.values(),key=score);mainobs=[objects[u]for u in main if u in objects];requests=[];noanchors=[]
 # Nodes in actual filled copper need an explicit routable native anchor.
 # Normally a pad/via/track already supplies it. Floating copper without any
 # circuit contact is reported rather than silently designated connected.
 for nodes in groups.values():
  if nodes is main:continue
  candidates=[objects[u]for u in nodes if u in objects]
  if not candidates:noanchors.append(sorted(nodes));continue
  def locs(o):return[xy(o.GetPosition())]if isinstance(o,(p.PAD,p.PCB_VIA))else[xy(o.GetStart()),xy(o.GetEnd())]
  pairs=[(math.dist(a,z),o,t,a,z)for o in candidates for a in locs(o)for t in mainobs for z in locs(t)]
  _,o,t,a,z=min(pairs,key=lambda q:q[0]);requests.append(dict(items=[dict(uuid=q.m_Uuid.AsString(),pos=dict(zip(['x','y'],v)))for q,v in[(o,a),(t,z)]],separation_mm=math.dist(a,z)))
 save('ground-contact-graph.json',dict(native_sha256=sha(HW/'RF2M.kicad_pcb'),nodes=len(parent),contact_shapes=len(rows),components=len(groups),groups=[dict(nodes=len(nodes),native_anchors=sum(u in objects for u in nodes))for nodes in groups.values()],no_anchor_regions=noanchors,method='Native filled polygons including holes,actual pad/track/via effective copper and GNDgraphics;independent geometry contacts.'))
 save('ground-bridge-requests.json',dict(unconnected_items=sorted(requests,key=lambda q:q['separation_mm']),no_anchor_regions=noanchors));print('Ground copper groups',len(groups),'bridge requests',len(requests),'unanchored',len(noanchors),flush=True)
if __name__=='__main__':main()
