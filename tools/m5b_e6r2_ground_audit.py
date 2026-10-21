"""Actual GND copper contact graph, individual filled-zone islands included."""
from collections import defaultdict
from m5b_e6r2_common import *
from m5b_e3_dfm import nearby,bbox

def main():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));items=[];desc={};parent={}
 def root(q):
  parent.setdefault(q,q)
  if parent[q]!=q:parent[q]=root(parent[q])
  return parent[q]
 def add(shape,ident,l,detail):
  items.append(dict(shape=shape,id=ident,layer=l,bb=bbox(shape)));desc[ident]=detail;root(ident)
 for t in list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads()]:
  if t.GetNetname()!='GND':continue
  ident=t.m_Uuid.AsString();detail=dict(kind=t.GetClass(),at=xy(t.GetPosition()))
  if isinstance(t,p.PAD):detail.update(ref=t.GetParentFootprint().GetReference(),pin=t.GetNumber())
  for l in [p.F_Cu,p.B_Cu]:
   if t.IsOnLayer(l):add(t.GetEffectiveShape(l),ident,l,detail)
 for z in b.Zones():
  if z.GetIsRuleArea() or z.GetNetname()!='GND':continue
  l=z.GetLayer();ps=z.GetFilledPolysList(l)
  for i in range(ps.OutlineCount()):
   shape=p.SHAPE_POLY_SET();shape.AddOutline(ps.COutline(i))
   for j in range(ps.HoleCount(i)):shape.AddHole(ps.CHole(i,j),0)
   add(shape,f'{b.GetLayerName(l)}-zone-{i}',l,dict(kind='zone-island',layer=b.GetLayerName(l),bbox=bbox(shape)))
 for g in b.GetDrawings():
  if g.GetLayer() in [p.F_Cu,p.B_Cu] and hasattr(g,'GetNetname') and g.GetNetname()=='GND':
   sh=p.SHAPE_POLY_SET();g.TransformShapeToPolygon(sh,g.GetLayer(),0,MM(.002),p.ERROR_OUTSIDE);add(sh,g.m_Uuid.AsString(),g.GetLayer(),dict(kind='GNDgraphic',bbox=bbox(sh)))
 for a,c in nearby(items,.01):
  if a['layer']!=c['layer'] or a['id']==c['id']:continue
  if p.SHAPE.Collide(a['shape'],c['shape'],MM(.002)):parent[root(a['id'])]=root(c['id'])
 groups=defaultdict(list)
 for k,d in desc.items():groups[root(k)].append(d)
 report=sorted(groups.values(),key=len);save('ground-contact-audit.json',dict(components=len(report),groups=report,method='Actual pad/track/via effective copper +individual native filled-zone polygons;2um contact tolerance;paired via/PTH layers share terminal',native_SHA256=sha(HW/'RF2M.kicad_pcb')))
 print('GND contact component sizes',[len(g)for g in report]);print('Small groups',report[:-1],flush=True)
 assert len(report)==1,'Every GNDterminal andfilledisland must share the physicalground'
if __name__=='__main__':main()
