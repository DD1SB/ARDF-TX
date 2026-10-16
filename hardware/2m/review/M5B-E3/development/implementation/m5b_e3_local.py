#!/usr/bin/python3
"""Localized native repair aids for changed substrate/annulus geometry.
These aids do not authorize waiver of final DRC or independent DFM checks.
"""
import argparse,collections,json,math,sys,time
import pcbnew as p
from m5b_e3_common import *
MM=p.FromMM
def pt(x,y):return p.VECTOR2I(MM(x),MM(y))
def xy(q):return(p.ToMM(q.x),p.ToMM(q.y))
def uid(q):return q.m_Uuid.AsString()
def aliases():
 parts=json.loads((HW/'RF2M.electrical.json').read_text())['parts'];par={}
 def find(a):
  par.setdefault(a,a)
  if par[a]!=a:par[a]=find(par[a])
  return par[a]
 for f in parts:
  if f['ref'].startswith('TL'):
   a,z=f['pins'].values();par[find(z)]=find(a)
 return{a:find(a)for a in par}
def move_vias():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));alias=aliases();tracks=list(b.GetTracks());pads=[a for f in b.GetFootprints()for a in f.Pads()];items=tracks+pads;extras=[]
 for f in b.GetFootprints():
  if f.GetReference().startswith('TL'):
   for g in f.GraphicalItems():
    if g.GetLayer()==p.F_Cu:extras.append((g,next(iter(f.Pads())).GetNetname()))
 def net(a):return alias.get(a.GetNetname(),a.GetNetname())
 idx=collections.defaultdict(list);step=4
 def keys(bb):
  return[(i,j)for i in range(math.floor(p.ToMM(bb.GetLeft())/step),math.floor(p.ToMM(bb.GetRight())/step)+1)for j in range(math.floor(p.ToMM(bb.GetTop())/step),math.floor(p.ToMM(bb.GetBottom())/step)+1)]
 for a in items:
  for k in keys(a.GetBoundingBox()):idx[k].append(a)
 logs=[];blocked=[];vias=[t for t in tracks if isinstance(t,p.PCB_VIA)];keep=[]
 for count,v in enumerate(vias):
  x,y=xy(v.GetPosition())
  if abs(x-112)<=1 and abs(y-55)<=2.2:continue
  near={uid(a):a for i in range(math.floor((x-3)/step),math.floor((x+3)/step)+1)for j in range(math.floor((y-3)/step),math.floor((y+3)/step)+1)for a in idx[(i,j)]}
  foreign=[a for a in near.values()if net(a)!=net(v)];friends=[t for t in near.values()if isinstance(t,p.PCB_TRACK)and not isinstance(t,p.PCB_VIA)and t.GetNetname()==v.GetNetname()]
  attached=[]
  for t in friends:
   for end in ['Start','End']:
    if math.dist(xy(getattr(t,'Get'+end)()),(x,y))<.001:attached.append((t,end))
  def valid(xx,yy,d):
   viashape=p.SHAPE_CIRCLE(pt(xx,yy),MM(d/2))
   for a in foreign:
    for layer in[p.F_Cu,p.B_Cu]:
     if a.IsOnLayer(layer)and a.GetEffectiveShape(layer).Collide(viashape,MM(.155)):return False
   # Via holes from same net also retain0.2mm edge spacing.
   for a in near.values():
    if isinstance(a,p.PCB_VIA)and uid(a)!=uid(v):
     if math.dist((xx,yy),xy(a.GetPosition()))<.505:return False
   for t,end in attached:
    other=getattr(t,'GetEnd'if end=='Start'else'GetStart')();shape=p.SHAPE_SEGMENT(pt(xx,yy),other,t.GetWidth())
    bb=shape.BBox();bboxkeys=keys(bb);ob={uid(a):a for k in bboxkeys for a in idx[k]if net(a)!=net(v)}
    for a in ob.values():
     if a.IsOnLayer(t.GetLayer())and a.GetEffectiveShape(t.GetLayer()).Collide(shape,MM(.155)):return False
    for g,n in extras:
     if alias.get(n,n)!=net(v):
      poly=p.SHAPE_POLY_SET();g.TransformShapeToPolygon(poly,p.F_Cu,0,MM(.002),p.ERROR_OUTSIDE)
      if t.GetLayer()==p.F_Cu and poly.Collide(shape,MM(.155)):return False
   return True
  candidates=[(0,x,y)]
  for r in [.10,.15,.20,.30,.40,.50,.65,.80,1.0]:
   for dx,dy in[(r,0),(-r,0),(0,r),(0,-r),(r,r),(-r,r),(r,-r),(-r,-r)]:candidates.append((dx*dx+dy*dy,x+dx,y+dy))
  chosen=None
  for d in[.8,.7]:
   for dist,xx,yy in candidates:
    if valid(xx,yy,d):chosen=(xx,yy,d);break
   if chosen:break
  if not chosen:blocked.append(dict(uuid=uid(v),net=v.GetNetname(),at_mm=[x,y]));continue
  xx,yy,d=chosen
  if math.dist((x,y),(xx,yy))>.001 or abs(p.ToMM(v.GetWidth(p.F_Cu))-d)>.001:
   v.SetPosition(pt(xx,yy));v.SetWidth(MM(d))
   for t,end in attached:getattr(t,'Set'+end)(pt(xx,yy))
   for a in[v]+[t for t,e in attached]:
    for k in keys(a.GetBoundingBox()):idx[k].append(a)
   logs.append(dict(uuid=uid(v),net=v.GetNetname(),from_mm=[x,y],to_mm=[xx,yy],diameter_mm=d,reason='Local annulus/clearance adaptation;0.7mm exceptions retain0.20mm ring,normal via fabrication.'))
  if count%100==0:print('via',count,'moved',len(logs),'pending',len(blocked),flush=True)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('development/via-adaptation.json',dict(changes=logs,pending=blocked));print('vias moved',len(logs),'pending',len(blocked))

def labels():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));removed=[]
 for g in list(b.GetDrawings()):
  if isinstance(g,p.PCB_TEXT)and g.GetLayer()in[p.F_SilkS,p.B_SilkS]:b.Remove(g);removed.append(g)
 # Retain actual component drawings on fabrication layers. Thin existing
 # library graphics are moved toFab,not erased or falsely waived forsilk.
 moved=[]
 for f in b.GetFootprints():
  for g in f.GraphicalItems():
   if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:
    g.SetLayer(p.F_Fab if g.GetLayer()==p.F_SilkS else p.B_Fab);moved.append(f.GetReference())
  for g in f.GetFields():
   if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:g.SetLayer(p.F_Fab)
 pads=[];occupied=[]
 def bb(obj,gap=0):
  z=obj.GetBoundingBox();return[p.ToMM(z.GetLeft())-gap,p.ToMM(z.GetTop())-gap,p.ToMM(z.GetRight())+gap,p.ToMM(z.GetBottom())+gap]
 def overlap(a,z):return a[0]<z[2]and a[2]>z[0]and a[1]<z[3]and a[3]>z[1]
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.IsOnLayer(p.F_Mask):pads.append(bb(a,.23))
 def put(t,x,y,size=1):
  g=p.PCB_TEXT(b);g.SetText(t);g.SetPosition(pt(x,y));g.SetTextSize(pt(size,size));g.SetTextThickness(MM(.15));g.SetLayer(p.F_SilkS);b.Add(g);occupied.append(bb(g,.16));return g
 for t,x,y,s in [('ARDF-TX RF2M / M5B-E3 / 1.6mm 1oz',108,23,1.2),('REVIEW ONLY / NOT RELEASED',112,157,1.1),('PACK +1 GND2',35,146,1),('3V3 LOGIC',38,73,1),('2S BOOST OR 4S BUCK / EXCLUSIVE',78,152,1),('NORMAL 50R SMA',184,63,1),('TRAIN uW MMCX',187,148,1),('INSULATED PASS SINK',180,23,1),('NTC TO PASS CASE',174,30,1)]:put(t,x,y,s)
 omitted=[]
 for f in b.GetFootprints():
  r=f.GetReference()
  if r.startswith('TL'):continue
  box=f.GetBoundingBox(False,False);x=(p.ToMM(box.GetLeft())+p.ToMM(box.GetRight()))/2;y=(p.ToMM(box.GetTop())+p.ToMM(box.GetBottom()))/2;found=False
  for d in[1.2,1.8,2.5,3.2,4.,5.,6.5,8.]:
   for xx,yy in[(x,p.ToMM(box.GetTop())-d),(x,p.ToMM(box.GetBottom())+d),(p.ToMM(box.GetRight())+d+len(r)*.3,y),(p.ToMM(box.GetLeft())-d-len(r)*.3,y)]:
    q=[xx-len(r)*.4-.3,yy-.8,xx+len(r)*.4+.3,yy+.8]
    if q[0]<21 or q[2]>199 or q[1]<26 or q[3]>154 or any(overlap(q,z)for z in pads+occupied):continue
    put(r,xx,yy);found=True;break
   if found:break
  if not found:omitted.append(r)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('silkscreen-disposition.json',dict(text_height_mm=1,stroke_mm=.15,omitted_ref_labels=omitted,refs_and_polarity_remain_on_FFab=True,thin_library_graphics_moved_to_FFab=sorted(set(moved)),assembly='Use complete Fab drawings for dense parts;power/RF/interface labels remain on board.'))
 print('E3 silk labels;omitted refs',len(omitted))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=['vias','labels']);x=a.parse_args();move_vias()if x.action=='vias'else labels()
