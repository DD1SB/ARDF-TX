#!/usr/bin/python3
"""Ordinary via fanout: no via in SMD pad, no hole overlap; actual copper retained."""
from m3b_pcb import *

def point_segment(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=0 if dx*dx+dy*dy==0 else max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)));return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
def seg_box(a,b,r):
 t0,t1=0,1;dx,dy=b[0]-a[0],b[1]-a[1]
 for pp,qq in[(-dx,a[0]-r[0]),(dx,r[2]-a[0]),(-dy,a[1]-r[1]),(dy,r[3]-a[1])]:
  if abs(pp)<1e-12:
   if qq<0:return False
  elif pp<0:t0=max(t0,qq/pp)
  else:t1=min(t1,qq/pp)
  if t0>t1:return False
 return True
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def segdist(a,b,c,d):
 if orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0:return 0
 return min(point_segment(a,c,d),point_segment(b,c,d),point_segment(c,a,b),point_segment(d,a,b))
def run():
 b=pcb.LoadBoard(str(HW/'RF80.kicad_pcb'))
 removed_items=list(b.GetTracks()) # keep SWIG wrappers alive until board save
 for t in removed_items:
  if t.GetNetname()=='GND':b.Remove(t)
 f={q.GetReference():q for q in b.GetFootprints()};m=json.loads((HW/'RF80.electrical.json').read_text());parts={p['ref']:p for p in m['parts']if not p['ref'].startswith('#')};net=b.FindNet('GND')
 # Synchronize fields after exact-package corrections, without moving geometry.
 comps={c.attrib['ref']:c for c in ET.parse(REV/'RF80.xml').findall('./components/comp')}
 for r,q in f.items():
  if r not in parts:continue
  if r=='J101':
   q.SetFPID(pcb.LIB_ID('ARDF_TX','Wurth_61201621621'))
   for pad in q.Pads():pad.SetDrillSize(pt(1.2,1.2));pad.SetSize(pt(1.9,1.9))
  for k in ('MPN','Population','Function','Engineering_Note'):
   text=next((x.attrib.get('value','')for x in comps[r].findall('property')if x.attrib['name']==k),'');q.GetField(k).SetText(text)
 pads=[p for q in f.values()for p in q.Pads()];obstacles=[]
 for p in pads:
  z=p.GetBoundingBox();obstacles.append((p.GetNetname(),[pcb.ToMM(z.GetLeft()),pcb.ToMM(z.GetTop()),pcb.ToMM(z.GetRight()),pcb.ToMM(z.GetBottom())]))
 tracks=[(t.GetNetname(),xy(t.GetStart()),xy(t.GetEnd()),pcb.ToMM(t.GetWidth()))for t in b.GetTracks()if not isinstance(t,pcb.PCB_VIA)and t.GetLayer()==pcb.F_Cu]
 vias=[];connections=[]
 for p in pads:
  if p.GetNetname()!='GND'or p.GetAttribute()!=pcb.PAD_ATTRIB_SMD:continue
  a=xy(p.GetPosition());choice=None
  center=xy(p.GetParentFootprint().GetPosition());candidates=[center]
  for dist in(1.0,1.4,1.8,2.2,2.6,3.,3.6,4.2):
   candidates.extend((a[0]+dx,a[1]+dy)for dx,dy in [(dist,0),(-dist,0),(0,dist),(0,-dist),(dist,dist),(-dist,-dist),(dist,-dist),(-dist,dist)])
  for v in candidates:
    if not(21<v[0]<229 and 21<v[1]<179):continue
    bad=False
    for n,r in obstacles:
     g=.91 if n=='DRAIN_PA'else .47
     if r[0]-g<v[0]<r[2]+g and r[1]-g<v[1]<r[3]+g:bad=True;break
     if n!='GND':
      g=.76 if n=='DRAIN_PA'else .30
      if seg_box(a,v,[r[0]-g,r[1]-g,r[2]+g,r[3]+g]):bad=True;break
    if bad:continue
    for n,c,d,w in tracks:
     g=.65 if n=='DRAIN_PA'else .17
     if point_segment(v,c,d)<w/2+.30+g or segdist(a,v,c,d)<w/2+.14+g:bad=True;break
    if bad:continue
    choice=v;break
  if not choice:raise AssertionError(('Ground fanout blocked',p.GetParentFootprint().GetReference(),p.GetNumber()))
  shared=next((v for v in vias if math.dist(v,choice)<.60),None)
  if shared:choice=shared
  else:
   v=pcb.PCB_VIA(b);v.SetPosition(pt(*choice));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(net);v.SetLocked(True);b.Add(v);vias.append(choice)
  t=pcb.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*choice));t.SetWidth(MM(.28));t.SetLayer(pcb.F_Cu);t.SetNet(net);t.SetLocked(True);b.Add(t);connections.append(dict(pad=str(p.m_Uuid),from_mm=a,to_mm=choice))
 pcb.SaveBoard(str(HW/'RF80.kicad_pcb'),b)
 (REV/'ground_fanout.json').write_text(json.dumps(dict(vias_mm=vias,connections=connections),indent=2)+'\n')
 l=Layout.__new__(Layout);l.b=b;l.m=m;l.parts=parts;l.f={r:q for r,q in f.items()if r in parts};l.manual=json.loads((REV/'critical_routes.json').read_text());l.save()
 print('Ground fanout:',len(vias),'ordinary non-VIP vias;',len(connections),'pad returns')
if __name__=='__main__':run()
