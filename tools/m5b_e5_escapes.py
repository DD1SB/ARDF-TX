#!/usr/bin/python3
"""Localized fine-pitch escapes, exact native copper tested before insertion."""
import math,sys
from m5b_e5_common import *
REMOVED=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};log=[];requests=[]
 # Release two ordinary low-frequency fanouts for a reproducible pin10 escape.
 for t in ([]if '--only-scl'in sys.argv else list(b.GetTracks())):
  if t.GetNetname()=='AF_PWM'and not isinstance(t,p.PCB_VIA)and t.GetLayer()==p.B_Cu and any(math.dist(xy(q),(78.0957,109.5176))<.0001 for q in[t.GetStart(),t.GetEnd()]):b.Remove(t);REMOVED.append(t)
  if t.GetNetname()=='CONV_EN'and any(math.dist(xy(q),(77.7483,108.9269))<.0001 for q in[t.GetStart(),t.GetEnd()]):b.Remove(t);REMOVED.append(t)
 for t in list(b.GetTracks()):
  if t.GetNetname()=='SAFE_N'and not isinstance(t,p.PCB_VIA)and t.GetLayer()==p.B_Cu and any(26.8<p.ToMM(q.x)<28 and 49<p.ToMM(q.y)<51 for q in[t.GetStart(),t.GetEnd()]):b.Remove(t);REMOVED.append(t)
 # Rebuild the trapped Si5351 SCL fanout, not any clock or matching line.
 for t in list(b.GetTracks()):
  if t.GetNetname()=='SCL_CLK'and max(p.ToMM(t.GetStart().y),p.ToMM(t.GetEnd().y))<55:b.Remove(t);REMOVED.append(t)
 def pad(r,n):return next(a for a in fs[r].Pads()if a.GetNumber()==n)
 def escape(anchor,net,preferred,width=.15):
  origin=xy(anchor.GetPosition());rows=[]
  for o in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
   for ly in[p.F_Cu,p.B_Cu]:
    if o.IsOnLayer(ly):
     sh=o.GetEffectiveShape(ly);bb=sh.BBox();rows.append((o.GetNetname(),ly,sh,bb,o))
  def overlaps(a,z,d):return not(a.GetRight()+d<z.GetLeft()or z.GetRight()+d<a.GetLeft()or a.GetBottom()+d<z.GetTop()or z.GetBottom()+d<a.GetTop())
  found=None
  candidates=list(preferred)
  for dx in range(-25,26,2):
   for dy in range(-25,26,2):candidates.append((origin[0]+dx/10,origin[1]+dy/10))
  for target in candidates:
   if net=='SCL_CLK'and not(27.25<target[0]<28.2 and 49.45<target[1]<51.):continue
   circ=p.SHAPE_CIRCLE(pt(*target),MM(.3));env=p.SHAPE_CIRCLE(pt(*target),MM(.29));bb=circ.BBox()
   if any(n!=net and overlaps(bb,ob,MM(.16))and p.SHAPE.Collide(circ,sh,MM(.16))for n,ly,sh,ob,o in rows):continue
   if any(isinstance(o,p.PAD)and o.GetAttribute()==p.PAD_ATTRIB_SMD and overlaps(env.BBox(),ob,0)and p.SHAPE.Collide(env,sh,0)for n,ly,sh,ob,o in rows):continue
   paths=[[origin,target],[origin,(target[0],origin[1]),target],[origin,(origin[0],target[1]),target]]
   for off in[-2,-1.5,-1,1,1.5,2]:paths.append([origin,(origin[0]+off,origin[1]),(origin[0]+off,target[1]),target])
   for path in paths:
    ts=[];legal=True
    for aa,zz in zip(path,path[1:]):
     if math.dist(aa,zz)<.000001:continue
     t=p.PCB_TRACK(b);t.SetStart(pt(*aa));t.SetEnd(pt(*zz));t.SetWidth(MM(width));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));sh=t.GetEffectiveShape(p.F_Cu);box=sh.BBox()
     if any(n!=net and ly==p.F_Cu and overlaps(box,ob,MM(.16))and p.SHAPE.Collide(sh,s,MM(.16))for n,ly,s,ob,o in rows):legal=False;break
     ts.append(t)
    if legal:found=(target,path,ts);break
   if found:break
  assert found,('No exact copper escape',net,origin)
  target,path,ts=found
  for t in ts:b.Add(t)
  v=p.PCB_VIA(b);v.SetPosition(pt(*target));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetNet(b.FindNet(net));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v)
  log.append(dict(net=net,origin_mm=origin,via_mm=target,path_mm=path,width_mm=width,ordinary_drill_mm=.3,hidden_solder_land_hole=False));print(net,target,flush=True);return v
 other=next(a for f in fs.values()for a in f.Pads()if a.GetNetname()=='CONV_EN'and f.GetReference()!='U302')
 for anchor,target in[(pad('U302','11'),other),(pad('U302','10'),pad('C402','1')),(pad('U103','4'),pad('U102','2'))]:
  n=anchor.GetNetname()
  if '--only-scl'in sys.argv and n!='SCL_CLK':continue
  v=escape(anchor,n,[(78.4,109)]if n=='CONV_EN'else[(77.3,109.65)]if n=='BOOST_VCC'else[(27.4,49.6),(27.5,49.8),(27.4,50)])
  requests.append(dict(items=[dict(uuid=o.m_Uuid.AsString(),pos=dict(zip(['x','y'],xy(o.GetPosition()))))for o in[v,target]]))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('fine-pitch-escape-audit.json',dict(native_sha256=sha(HW/'RF2M.kicad_pcb'),connections=log,net_changes=False));save('fine-pitch-route-requests.json',dict(unconnected_items=requests))
if __name__=='__main__':main()
