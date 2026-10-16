#!/usr/bin/python3
"""Locate actualdisconnectedGNDcoppercomponents,includingzoneholes."""
import pcbnew as p,collections,json
from m5b_e3_common import *
from m5b_e3_dfm import bbox,nearby

def main():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));rows=[];par={}
 def find(u):
  par.setdefault(u,u)
  if par[u]!=u:par[u]=find(par[u])
  return par[u]
 def add(shape,layer,ident,kind):rows.append(dict(shape=shape,layer=layer,id=ident,bb=bbox(shape),kind=kind));find(ident)
 for ob in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
  if ob.GetNetname()!='GND':continue
  for layer in[p.F_Cu,p.B_Cu]:
   if ob.IsOnLayer(layer):add(ob.GetEffectiveShape(layer),layer,ob.m_Uuid.AsString(),ob.GetClass())
 for z in b.Zones():
  if z.GetIsRuleArea()or z.GetNetname()!='GND':continue
  layer=z.GetLayer();poly=z.GetFilledPolysList(layer)
  for i in range(poly.OutlineCount()):
   sh=p.SHAPE_POLY_SET();sh.AddOutline(poly.Outline(i))
   for k in range(poly.HoleCount(i)):sh.AddHole(poly.Hole(i,k),0)
   add(sh,layer,'zone-'+str(layer)+'-'+str(i),'zone')
 for a,z in nearby(rows,.005):
  if a['layer']!=z['layer']:continue
  if 'zone'in[a['kind'],z['kind']]:
   if a['kind']==z['kind']=='zone':continue
   zone,other=(a,z)if a['kind']=='zone'else(z,a);x0,y0,x1,y1=other['bb'];hit=False
   for ix in range(7):
    for iy in range(7):
     v=p.VECTOR2I(p.FromMM(x0+(x1-x0)*ix/6),p.FromMM(y0+(y1-y0)*iy/6))
     if p.SHAPE.Collide(other['shape'],v,0)and zone['shape'].Contains(v):hit=True;break
    if hit:break
  else:hit=p.SHAPE.Collide(a['shape'],z['shape'],p.FromMM(.001))
  if hit:par[find(z['id'])]=find(a['id'])
 groups=collections.defaultdict(list)
 for row in rows:groups[find(row['id'])].append({k:v for k,v in row.items()if k not in['shape']})
 out=sorted(groups.values(),key=lambda x:len(x),reverse=True);save('development/GND-components-fast.json',dict(groups=out));print('GNDcomponents',len(out))
 for g in out[1:]:print([(a['kind'],a['bb'],a['id'])for a in g])
if __name__=='__main__':main()
