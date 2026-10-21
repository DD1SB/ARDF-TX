"""Exact copper escapes for remaining fine-pitch controls and GND stitching."""
import math,sys
from m5b_e6r2_common import *
HELD=[]
def blocked(b,objects,net,extra_exclude=()):
 exclude={id(x) for x in objects}|{id(x) for x in extra_exclude}
 for obj in objects:
  for other in list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads()]:
   if id(other) in exclude or other.GetNetname()==net:continue
   for l in [p.F_Cu,p.B_Cu]:
    if obj.IsOnLayer(l) and other.IsOnLayer(l) and p.SHAPE.Collide(obj.GetEffectiveShape(l),other.GetEffectiveShape(l),MM(.165)):return True
 return False
def escape(ground=False,all_pins=False):
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));report=json.loads((OUT/'DRC.json').read_text());wanted={i['uuid'] for v in report['unconnected_items'] for i in v['items']};log=[]
 pads=[a for f in b.GetFootprints() for a in f.Pads()]
 for a in pads:
  net=a.GetNetname();ref=a.GetParentFootprint().GetReference()
  if (a.m_Uuid.AsString() not in wanted and not all_pins) or a.GetAttribute()!=p.PAD_ATTRIB_SMD:continue
  if all_pins and ref not in ['U970','U971','U972','U973']:continue
  if net.startswith('unconnected-'):continue
  if (net=='GND')!=ground:continue
  if not ground and ref not in ['U970','U971','U972','U973','U305','U601','U204','R973','R974']:continue
  origin=xy(a.GetPosition());b.BuildConnectivity();conn=list(b.GetConnectivity().GetConnectedItems(a))
  if not ground and any(t.GetClass()=='PCB_VIA' and math.dist(origin,xy(t.GetPosition()))<3. for t in conn):continue
  fp=a.GetParentFootprint();side=-1 if origin[0]<xy(fp.GetPosition())[0] else 1
  candidates=[]
  for dist in ([.8,.9,1.,1.1,1.2] if ref in ['U601','U305'] else [])+[1.3,1.6,2.,2.4,2.8,3.2,4.]:
   for dy in [0,.05,-.05,.1,-.1,.2,-.2,.4,-.4,.8,-.8,1.2,-1.2]:
    candidates.append((origin[0]+side*dist,origin[1]+dy))
    if ref in ['U601','U305','U970','U971','U972','U973']:candidates.append((origin[0]-side*dist,origin[1]+dy))
   if ground:candidates.extend([(origin[0],origin[1]+dist),(origin[0],origin[1]-dist),(origin[0]-side*dist,origin[1])])
  found=None
  for target in candidates:
   if not(21<target[0]<169 and 21<target[1]<129):continue
   if 84<target[0]<100 and 27<target[1]<73:continue
   via=p.PCB_VIA(b);via.SetPosition(pt(*target));via.SetWidth(MM(.6));via.SetDrill(MM(.3));via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(b.FindNet(net));via.SetFrontTentingMode(1);via.SetBackTentingMode(1)
   # No via-in-pad, even on this net. Distinct drilled holes must stay apart.
   if any(p.SHAPE.Collide(p.SHAPE_CIRCLE(pt(*target),MM(.35)),q.GetEffectiveShape(p.F_Cu),0) for q in pads if q.IsOnLayer(p.F_Cu) and not(ref in ['U601','U305'] and q.m_Uuid.AsString()==a.m_Uuid.AsString())):continue
   if any(isinstance(v,p.PCB_VIA) and math.dist(target,xy(v.GetPosition()))<.61 for v in b.GetTracks()):continue
   paths=[[origin,target],[origin,(target[0],origin[1]),target],[origin,(origin[0]+side*.8,origin[1]),(target[0],origin[1]),target]]
   for path in paths:
    tracks=[]
    for u,v in zip(path,path[1:]):
     if math.dist(u,v)<1e-6:continue
     t=p.PCB_TRACK(b);t.SetStart(pt(*u));t.SetEnd(pt(*v));t.SetLayer(p.F_Cu);t.SetWidth(MM(.25 if ground else .18));t.SetNet(b.FindNet(net));tracks.append(t)
    if not blocked(b,[via,*tracks],net):found=(via,tracks,path);break
   if found:break
  if found:
   v,ts,path=found;b.Add(v)
   for t in ts:b.Add(t)
   log.append(dict(ref=ref,pin=a.GetNumber(),net=net,via=target,path=path));print(ref,a.GetNumber(),net,target,flush=True)
  else:print('NO EXACT ESCAPE',ref,a.GetNumber(),net,origin,flush=True)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('ground-escapes.json' if ground else 'control-escapes.json',log)
def fanout():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b);j=manifest();parts={z['ref']:z for z in j['parts']}
 # Same ORfunction/manufacturer pin map, ordinary0.65mm DCT pitch gives
 # practical2layer fanout without smaller-than-standard drills/annuli.
 old=fs['U972'];f=p.FootprintLoad('/usr/share/kicad/footprints/Package_SO.pretty','SSOP-8_2.95x2.8mm_P0.65mm');f.SetReference('U972');f.SetValue('SN74LVC2G32DCTR');f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid);f.SetPosition(old.GetPosition());f.SetFPID(p.LIB_ID('ARDF_2M','LVC2G32_DCT_E6R2'))
 for a in f.Pads():a.SetNet(b.FindNet(parts['U972']['pins'][a.GetNumber()]))
 for fld in f.GetFields():fld.SetLayer(p.F_Fab)
 for sh in f.GraphicalItems():
  if sh.GetLayer()==p.F_SilkS:sh.SetLayer(p.F_Fab)
 local=p.Cast_to_FOOTPRINT(f.Duplicate(False));local.SetPosition(pt(0,0));p.FootprintSave(str(HW/'ARDF_2M.pretty'),local)
 b.Remove(old);HELD.append(old);b.Add(f);fs['U972']=f
 parts['U972']['mpn']=parts['U972']['value']='SN74LVC2G32DCTR';parts['U972']['footprint']='ARDF_2M:LVC2G32_DCT_E6R2'
 import m5a_r1_design as c
 fn=HW/'13_carrier_keying.kicad_sch';sx=c.parse(fn.read_text())
 for sy in c.children(sx,'symbol'):
  props={q[1]:q for q in c.children(sy,'property')}
  if props['Reference'][2]=='U972':
   for n,key in [('MPN','mpn'),('Value','value'),('Footprint','footprint')]:props[n][2]=parts['U972'][key]
 fn.write_text(c.dump(sx)+'\n');j['parts']=list(parts.values());(HW/'RF2M.electrical.json').write_text(json.dumps(j,indent=2)+'\n')
 allowed={n for r in ['U970','U971','U972','U973'] for n in parts[r]['pins'].values() if n};removed=[]
 for t in list(b.GetTracks()):
  if t.GetNetname() not in allowed:continue
  bb=t.GetBoundingBox()
  if any(bb.Intersects(p.BOX2I(fp.GetPosition()-pt(4.6,3.2),pt(9.2,6.4))) for r,fp in fs.items() if r in ['U970','U971','U972','U973']):
   removed.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname()));b.Remove(t);HELD.append(t)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('fine-pitch-fanout-reset.json',removed)
 escape(False,True);escape(True,True)
def nudge():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));j=json.loads((OUT/'DRC.json').read_text());log=[]
 wanted={i['uuid'] for v in j['violations'] if v['type'] in ['clearance','hole_clearance'] for i in v['items']}
 for via in list(b.GetTracks()):
  if not isinstance(via,p.PCB_VIA) or via.m_Uuid.AsString() not in wanted:continue
  assert not via.IsLocked();old=via.GetPosition();net=via.GetNetname();attached=[]
  for t in b.GetTracks():
   if isinstance(t,p.PCB_VIA):continue
   for end,get in [('start',t.GetStart),('end',t.GetEnd)]:
    if get()==old:attached.append((t,end))
  candidates=sorted([(dx*.025,dy*.025) for dx in range(-10,11) for dy in range(-10,11)],key=lambda q:q[0]**2+q[1]**2)
  others=[t for t in b.GetTracks() if t.m_Uuid.AsString()!=via.m_Uuid.AsString() and all(t.m_Uuid.AsString()!=x.m_Uuid.AsString() for x,e in attached)]+[a for f in b.GetFootprints() for a in f.Pads()]
  good=False
  for dx,dy in candidates:
   pos=old+pt(dx,dy);via.SetPosition(pos)
   for t,end in attached:(t.SetStart if end=='start' else t.SetEnd)(pos)
   legal=True
   for obj in [via,*[t for t,e in attached]]:
    for other in others:
     if other.GetNetname()==net:continue
     for layer in [p.F_Cu,p.B_Cu]:
      if obj.IsOnLayer(layer) and other.IsOnLayer(layer) and p.SHAPE.Collide(obj.GetEffectiveShape(layer),other.GetEffectiveShape(layer),MM(.165)):legal=False;break
     if not legal:break
    if not legal:break
   if legal:good=True;break
  if not good:
   via.SetPosition(old)
   for t,end in attached:(t.SetStart if end=='start' else t.SetEnd)(old)
  log.append(dict(net=net,old=xy(old),new=xy(via.GetPosition()),succeeded=good))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('grid-clearance-adjustments.json',log)
if __name__=='__main__':
 if sys.argv[1]=='fanout':fanout()
 elif sys.argv[1]=='nudge':nudge()
 else:escape(sys.argv[1]=='ground')
