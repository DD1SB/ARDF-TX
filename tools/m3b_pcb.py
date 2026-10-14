#!/usr/bin/python3
"""Deterministic evaluation placement and constrained RF/power routing in KiCad.

Local pcbnew/FreeRouting; never uploads or orders. Rerunning --place replaces PCB.
"""
import argparse,json,math,os,statistics,sys
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as pcb
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/80m';REV=HW/'review/M3B-E1'
MM=pcb.FromMM

def pt(x,y):return pcb.VECTOR2I(MM(x),MM(y))
def xy(v):return (pcb.ToMM(v.x),pcb.ToMM(v.y))
def bbox(f,margin=0):
 b=f.GetBoundingBox(False,False);return [pcb.ToMM(b.GetLeft())-margin,pcb.ToMM(b.GetTop())-margin,pcb.ToMM(b.GetRight())+margin,pcb.ToMM(b.GetBottom())+margin]
def intersects(a,b):return a[0]<b[2]and a[2]>b[0]and a[1]<b[3]and a[3]>b[1]
def netname(p):return p.GetNetname()

class Layout:
 def __init__(self):
  self.b=pcb.BOARD();self.b.SetCopperLayerCount(2);self.b.GetDesignSettings().SetBoardThickness(MM(1.6))
  self.b.SetFileName(str(HW/'RF80.kicad_pcb'))
  tb=self.b.GetTitleBlock();tb.SetTitle('RF80 80 m evaluation PCB - ENGINEERING REVIEW');tb.SetRevision('M3B-E1');tb.SetDate('2026-10-14');tb.SetCompany('ARDF-TX');tb.SetComment(0,'UNBUILT - NOT A MANUFACTURING RELEASE');self.b.SetTitleBlock(tb)
  self.m=json.loads((HW/'RF80.electrical.json').read_text());self.parts={p['ref']:p for p in self.m['parts']if not p['ref'].startswith('#')}
  xml=ET.parse(REV/'RF80.xml');self.comps={c.attrib['ref']:c for c in xml.findall('./components/comp')}
  self.netpins={}
  for net in xml.findall('./nets/net'):
   for node in net.findall('node'):self.netpins[(node.attrib['ref'],node.attrib['pin'])]=net.attrib['name'].removeprefix('/')
  names=sorted(set(self.netpins.values()))
  self.nets={}
  for i,n in enumerate(names,1):
   self.nets[n]=pcb.NETINFO_ITEM(self.b,n,i);self.b.Add(self.nets[n])
  self.f={};self.occupied=[];self.manual=[];self.vias=[]
  for r,p in self.parts.items():
   lib,name=p['footprint'].split(':');folder=HW/'ARDF_TX.pretty'if lib=='ARDF_TX'else Path('/usr/share/kicad/footprints')/(lib+'.pretty')
   f=pcb.FootprintLoad(str(folder),name);assert f,(r,p['footprint'])
   f.SetReference(r);f.SetValue(p['value']);f.SetFPID(pcb.LIB_ID(lib,name))
   comp=self.comps[r];path=comp.find('sheetpath').attrib['tstamps']+comp.findtext('tstamps')
   f.SetPath(pcb.KIID_PATH(path))
   for name in ('MPN','Population','Function','Engineering_Note'):
    value=next((x.attrib.get('value','')for x in comp.findall('property')if x.attrib['name']==name),'')
    field=pcb.PCB_FIELD(f,pcb.FIELD_T_USER,name);field.SetText(value);field.SetVisible(False);f.Add(field)
   for name,kind in [('Datasheet',pcb.FIELD_T_DATASHEET),('Description',pcb.FIELD_T_DESCRIPTION)]:
    val=next((x.text or ''for x in comp.findall('./fields/field')if x.attrib['name']==name),'')
    f.GetField(kind).SetText(val)
   f.SetDNP(p['population']in ('FOX','DNP'))
   f.Reference().SetLayer(pcb.F_Fab);f.Reference().SetTextSize(pt(.8,.8));f.Reference().SetTextThickness(MM(.12))
   f.Value().SetVisible(False)
   for pad in f.Pads():
    n=self.netpins.get((r,pad.GetNumber()))
    if n:pad.SetNet(self.nets[n])
   custom={'T401':('FT50A43_envelope',(0,0,0)),'L410':('T60_2_flat_envelope',(0,0,0)),'L411':('T60_2_upright_envelope',(0,0,0)),'L301':('SRP7050TA_envelope',(0,0,0)),'F301':('Fuse467_envelope',(0,0,0)),'L510':('78F_envelope',(5.08,0,0)),'L511':('78F_envelope',(5.08,0,0))}
   if r in custom:
    name,off=custom[r];model=pcb.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/3dmodels/'+name+'.wrl';model.m_Offset=pcb.VECTOR3D(*off);f.Models().clear();f.Models().push_back(model)
   self.b.Add(f);self.f[r]=f
  # Ordinary 210x160mm two-layer evaluation outline, no cutouts or special vias.
  for a,b in [((20,20),(230,20)),((230,20),(230,180)),((230,180),(20,180)),((20,180),(20,20))]:
   s=pcb.PCB_SHAPE();s.SetShape(pcb.SHAPE_T_SEGMENT);s.SetStart(pt(*a));s.SetEnd(pt(*b));s.SetLayer(pcb.Edge_Cuts);s.SetWidth(MM(.05));self.b.Add(s)
  for i,(x,y)in enumerate([(25,25),(225,25),(225,175),(25,175)],1):
   f=pcb.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');f.SetReference('H'+str(i));f.SetPosition(pt(x,y));f.SetAttributes(pcb.FP_BOARD_ONLY|pcb.FP_EXCLUDE_FROM_BOM|pcb.FP_EXCLUDE_FROM_POS_FILES);self.b.Add(f);self.occupied.append(bbox(f,.3))
 def place(self,r,x,y,angle=0,fixed=False):
  f=self.f[r];f.SetOrientationDegrees(angle);f.SetPosition(pt(x,y));bb=bbox(f,.25)
  if not fixed:
   candidates=[]
   for d in range(0,23):
    for dx,dy in([(0,0)]if d==0 else [(i,d)for i in range(-d,d+1)]+[(i,-d)for i in range(-d,d+1)]+[(d,i)for i in range(-d+1,d)]+[(-d,i)for i in range(-d+1,d)]):
     f.SetPosition(pt(x+dx,y+dy));a=bbox(f,.25)
     if a[0]<28 or a[1]<28 or a[2]>222 or a[3]>170:continue
     if any(intersects(a,b)for b in self.occupied):continue
     candidates.append((dx*dx+dy*dy,x+dx,y+dy,a))
    if candidates:break
   if not candidates:raise ValueError(('No placement',r,x,y))
   _,x,y,bb=min(candidates)
   f.SetPosition(pt(x,y))
  self.occupied.append(bb)
  return f
 def place_all(self):
  # Fixed signal-flow anchors. Small parts are then placed around the real pads.
  anchors={
   'J101':(30,80,0),'J301':(120,30,0),'J401':(219,98,0),'J502':(208,158,0),
   'U101':(125,97,0),'Y101':(125,90,0),
   'U201':(43,42,0),'U202':(58,52,0),'U203':(83,52,0),'U211':(48,82,0),'U212':(74,82,0),'U221':(50,110,0),'U222':(77,110,0),'U223':(50,136,0),'U224':(80,136,0),
   'U311':(107,72,0),'U312':(114,64,0),'U314':(113,82,0),'U313':(159,61,0),
   'U301':(137,40,0),'U302':(151,57,0),'U401':(170,40,180),'Q402':(173,34,0),'Q403':(156,69,0),
   'T401':(179,45,0),'L410':(184,82,0),'L411':(212,82,0),
   'U501':(163,137,0),'L510':(181,139,0),'L511':(198,139,0),
  }
  for r,(x,y,a)in anchors.items():self.place(r,x,y,a,True)
  hints={
   'L301':(145,45,0),'F301':(125,31,0),'D301':(127,29,90),'D302':(120,42,90),'R350':(127,40,90),'C350':(125,49,0),
   'C301':(132,34,0),'C302':(132,39,0),'C303':(138,43,0),'C304':(151,40,0),'C305':(151,45,0),
   'R301':(135,36,0),'R302':(136,47,90),'R303':(132,48,0),'R304':(131,55,0),'Q301':(134,53,0),'R305':(138,55,0),'Q302':(142,54,0),
   'C306':(150,61,90),'R306':(153,62,90),'R307':(149,53,0),
   'R330':(159,56,0),'R331':(157,59,90),'R332':(162,59,90),'C320':(160,63,0),
   'R410':(161,46,0),'C404':(162,40,0),'C401':(173,41,0),'C402':(167,44,0),
   'R403':(173,37,90),'R404':(169,34,0),'R401':(166,38,90),'Q401':(166,49,0),'Q405':(169,53,0),'R409':(171,51,0),'R402':(163,50,0),'R408':(172,55,0),
   'C405':(170,48,90),'Q404':(153,76,0),'R406':(151,71,90),'R405':(164,65,90),'C403':(165,69,0),'R407':(165,73,0),
   'TH301':(180,29,0),
   'C410':(174,64,90),'C411':(171,73,0),'C412':(171,77,0),'C413':(198,87,90),'C414':(211,66,0),'C415':(220,91,0),'C416':(225,91,90),
   'R451':(95,105,0),'D451':(100,109,0),'R452':(109,105,0),'C451':(104,105,0),'R453':(104,112,0),'Q406':(99,117,0),
   'Q225':(92,131,0),'Q226':(98,131,0),'Q227':(92,140,0),'Q228':(98,140,0),'Q229':(103,137,0),
   'R501':(142,130,90),'Q501':(146,137,0),'R502':(143,135,0),'R503':(142,140,0),'Q502':(141,144,0),'C501':(148,140,0),'C502':(151,141,90),'R504':(153,142,0),
   'R505':(150,129,0),'R506':(153,131,90),'Q503':(154,134,0),'R507':(157,131,0),'D501':(155,137,0),'R508':(160,147,0),'Q504':(165,149,0),'R509':(168,149,0),
   'R510':(157,136,0),'R511':(157,139,0),'R512':(157,142,0),'C510':(172,141,90),'C511':(175,144,90),'C512':(175,147,90),'C513':(188,145,90),'C514':(198,132,0),'C515':(206,145,90),'C516':(206,148,90),'R513':(208,152,90),'R514':(204,151,90),'R515':(213,152,90),'R516':(212,161,0),'C517':(215,159,90),
  }
  bypass={'C101':'U101','C102':'U101','C103':'J101','C210':'U201','C211':'U202','C212':'U203','C220':'U211','C222':'U212','C230':'U221','C231':'U222','C232':'U223','C233':'U224','C313':'U312','C323':'U314','C322':'U313'}
  for r,parent in bypass.items():
   f=self.f[parent];vdd=next((p for p in f.Pads()if p.GetNetname()=='V3V3'),None)
   if vdd:
    x,y=xy(vdd.GetPosition());hints.setdefault(r,(x+3,y,0))
  for r,(x,y,a)in hints.items():
   if r not in anchors:self.place(r,x,y,a)
  # Remaining dividers/pull-downs go near their owning IC and connected signals.
  defaults={'01_source_interface':(40,101),'02_interlocks':(62,42),'03_safety_logic':(94,86),'04_arm_key':(92,120),'05_power':(140,60),'06_analog_protection':(112,72),'06b_thresholds':(117,75),'07_current_thermal':(147,80)}
  placed=set(anchors)|set(hints)
  nonglobal={'V3V3','GND','VIN_PA','VIN_PACK','VPA','VPA_LOAD','VREF_2V5'}
  for r,p in self.parts.items():
   if r in placed or r.startswith('TP'):continue
   ns={n for n in p['pins'].values()if n and n not in nonglobal};locations=[]
   for rr in placed:
    if rr not in self.f:continue
    if self.parts[rr]['sheet']!=p['sheet']and not rr.startswith('U'):continue
    for pad in self.f[rr].Pads():
     if pad.GetNetname()in ns:locations.append(xy(pad.GetPosition()))
   x,y=defaults.get(p['sheet'],(110,110))
   if locations:x=statistics.median(a[0]for a in locations);y=statistics.median(a[1]for a in locations)
   self.place(r,round(x),round(y));placed.add(r)
  # Test pads are placed close to their actual node; no remote probe bus stubs.
  for r,p in self.parts.items():
   if not r.startswith('TP'):continue
   n=p['pins']['1'];points=[]
   for rr,f in self.f.items():
    if rr.startswith('TP'):continue
    for pad in f.Pads():
     if pad.GetNetname()==n:points.append((rr,xy(pad.GetPosition())))
   if n=='GND':
    i=int(r[2:]);x,y=[(166,40),(48,130),(153,58),(163,145),(127,96),(111,82)][i%6]
   elif points:
    priority={'DRAIN_PA':'Q402','GATE_PA':'Q402','GATE_DRV':'U401','ARM_ACCEPT':'U224','ARMED':'U223','LEASE_OK':'U202','BUS_QUIET':'U221','RESET_N':'U223','HEALTH_N':'U224','PA_INB':'U401','CLK_PA':'U401','CLK_FOX':'U101','VDRV':'U401','VPA':'U301','VPA_LOAD':'R330','VIN_PA':'U301','VIN_PACK':'D301','RF_NORMAL':'J401','RF_FOX':'J502'}
    rr,(x,y)=next(((rr,p)for rr,p in points if rr==priority.get(n)),points[0]);x+=1.8;y+=1.8
   else:raise AssertionError((r,n))
   self.place(r,round(x,1),round(y,1));placed.add(r)
  self.b.BuildConnectivity()
 def pad(self,r,p):return next(x for x in self.f[r].Pads()if x.GetNumber()==str(p))
 def track(self,n,points,width=.3,layer=pcb.F_Cu,locked=True):
  for a,b in zip(points,points[1:]):
   if math.dist(a,b)<.005:continue
   t=pcb.PCB_TRACK(self.b);t.SetStart(pt(*a));t.SetEnd(pt(*b));t.SetWidth(MM(width));t.SetLayer(layer);t.SetNet(self.nets[n]);t.SetLocked(locked);self.b.Add(t)
  self.manual.append(dict(net=n,points=points,width_mm=width,layer='F.Cu'if layer==pcb.F_Cu else'B.Cu'))
 def link(self,r1,p1,r2,p2,width=.3,via=None):
  a=self.pad(r1,p1);b=self.pad(r2,p2);assert a.GetNetname()==b.GetNetname(),(r1,p1,r2,p2)
  aa=xy(a.GetPosition());bb=xy(b.GetPosition());self.track(a.GetNetname(),[aa,* (via or []),bb],width)
 def ground_vias(self):
  # Local escape to return plane. Check geometry before accepting each via.
  allpads=[p for f in self.b.GetFootprints()for p in f.Pads()]
  for r,f in self.f.items():
   for p in f.Pads():
    if p.GetNetname()!='GND'or p.GetAttribute()!=pcb.PAD_ATTRIB_SMD:continue
    x,y=xy(p.GetPosition());best=None
    for dist in (.9,1.2,1.6,2.0,2.5):
     for dx,dy in [(0,dist),(0,-dist),(dist,0),(-dist,0),(dist,dist),(-dist,-dist),(dist,-dist),(-dist,dist)]:
      pos=pt(x+dx,y+dy);safe=True
      for q in allpads:
       if q.GetNetname()=='GND':continue
       qb=q.GetBoundingBox();qb.Inflate(MM(.95 if q.GetNetname()=='DRAIN_PA' else .51))
       if qb.Contains(pos):safe=False;break
      if safe:best=(x+dx,y+dy);break
     if best:break
    assert best,('No ground via',r,p.GetNumber())
    existing=next((v for v in self.vias if math.dist(v,best)<.85),None)
    if existing:best=existing
    else:
     v=pcb.PCB_VIA(self.b);v.SetPosition(pt(*best));v.SetWidth(MM(.7));v.SetDrill(MM(.35));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(self.nets['GND']);v.SetLocked(True);self.b.Add(v)
    self.track('GND',[(x,y),best],.28);self.vias.append(best)
 def route_path(self,n,a,b,width):
  import heapq
  step=.2;nx=1051;ny=801;blocked=bytearray(nx*ny);offset=(20,20)
  def index(p):return (round((p[0]-20)/step),round((p[1]-20)/step))
  def mark_rect(x0,y0,x1,y1):
   ix0=max(0,math.floor((x0-20)/step));ix1=min(nx-1,math.ceil((x1-20)/step))
   iy0=max(0,math.floor((y0-20)/step));iy1=min(ny-1,math.ceil((y1-20)/step))
   if ix1<ix0 or iy1<iy0:return
   bar=b'\1'*(ix1-ix0+1)
   for y in range(iy0,iy1+1):blocked[y*nx+ix0:y*nx+ix1+1]=bar
  # Conservative rectangle envelopes around alien pads; actual copper checked by DRC.
  gap=(.65 if n=='DRAIN_PA' else .17)+width/2
  for f in self.b.GetFootprints():
   for p in f.Pads():
    if p.GetNetname()==n:continue
    pg=max(gap,.65+width/2)if p.GetNetname()=='DRAIN_PA'else gap
    box=p.GetBoundingBox();mark_rect(pcb.ToMM(box.GetLeft())-pg,pcb.ToMM(box.GetTop())-pg,pcb.ToMM(box.GetRight())+pg,pcb.ToMM(box.GetBottom())+pg)
  for t in self.b.GetTracks():
   if t.GetNetname()==n:continue
   if isinstance(t,pcb.PCB_VIA):
    x,y=xy(t.GetPosition());rad=pcb.ToMM(t.GetWidth(pcb.F_Cu))/2+gap;mark_rect(x-rad,y-rad,x+rad,y+rad);continue
   if t.GetLayer()!=pcb.F_Cu:continue
   p,q=xy(t.GetStart()),xy(t.GetEnd());tg=max(gap,.65+width/2)if t.GetNetname()=='DRAIN_PA'else gap;rad=pcb.ToMM(t.GetWidth())/2+tg
   count=max(1,math.ceil(math.dist(p,q)/.1))
   for j in range(count+1):
    x=p[0]+(q[0]-p[0])*j/count;y=p[1]+(q[1]-p[1])*j/count;mark_rect(x-rad,y-rad,x+rad,y+rad)
  s=index(a);g=index(b)
  for p in (s,g):
   if not(0<=p[0]<nx and 0<=p[1]<ny)or blocked[p[1]*nx+p[0]]:return None
  si=s[1]*nx+s[0];gi=g[1]*nx+g[0];queue=[(0,0,si)];dist={si:0};parent={};found=False
  dirs=[(1,0,10),(-1,0,10),(0,1,10),(0,-1,10),(1,1,14),(1,-1,14),(-1,1,14),(-1,-1,14)]
  while queue:
   _,cost,i=heapq.heappop(queue)
   if cost!=dist.get(i):continue
   if i==gi:found=True;break
   x,y=i%nx,i//nx
   for dx,dy,dc in dirs:
    xx,yy=x+dx,y+dy
    if xx<4 or yy<4 or xx>=nx-4 or yy>=ny-4:continue
    ii=yy*nx+xx
    if blocked[ii]or(dx and dy and(blocked[y*nx+xx]or blocked[yy*nx+x])):continue
    nc=cost+dc
    if nc>=dist.get(ii,10**12):continue
    dist[ii]=nc;parent[ii]=i;ddx=abs(xx-g[0]);ddy=abs(yy-g[1]);h=10*max(ddx,ddy)+4*min(ddx,ddy)
    heapq.heappush(queue,(nc+h,nc,ii))
  if not found:return None
  cells=[gi]
  while cells[-1]!=si:cells.append(parent[cells[-1]])
  cells.reverse();ps=[a];last=None
  for j in range(1,len(cells)):
   old,new=cells[j-1],cells[j];v=(new%nx-old%nx,new//nx-old//nx)
   if last is not None and v!=last:ps.append((20+(old%nx)*step,20+(old//nx)*step))
   last=v
  ps.append((20+g[0]*step,20+g[1]*step));ps.append(b)
  return ps
 def manual_routes(self):
  # Route the complete RF and high-current net trees on top copper before general routing.
  # Net membership comes from physical pads, never a hand-copied topology.
  priority=['DRAIN_PA','GATE_PA','GATE_DRV','SW_PA','BOOT_PA','VDRV','VPA_SHAPED','RF_RAW','LPF_N1','LPF_N2','RF_NORMAL','VPA_ISO','VPA_LOAD','SENSE_PLUS','SENSE_MINUS','VPA','VIN_PA','VIN_PACK','VBAT_FUSED','VBAT','FOX_GATE1','FOX_GATE2','FOX_GATE3','FOX_SUM','FOX_LPF1','FOX_LPF2','FOX_PAD_IN','RF_FOX','FOX_CLK','FOX_GATE_EN','CLK_PA','CLK_FOX','XA','XB']
  for n in priority:
   pads=[p for f in self.f.values()for p in f.Pads()if p.GetNetname()==n]
   if len(pads)<2:continue
   width=1.0 if n=='DRAIN_PA'else .75 if n in ('VPA_SHAPED','VPA_LOAD','VPA_ISO','VPA','VIN_PA','VIN_PACK','VBAT_FUSED','VBAT')else .55 if n in ('RF_RAW','LPF_N1','LPF_N2','RF_NORMAL','SW_PA')else .3
   seen={0};pairs=[]
   while len(seen)<len(pads):
    _,i,j=min((math.dist(xy(pads[i].GetPosition()),xy(pads[j].GetPosition())),i,j)for i in seen for j in range(len(pads))if j not in seen)
    seen.add(j);pairs.append((i,j))
   root={'VPA_LOAD':('R330','2'),'VPA_ISO':('R330','1')}.get(n)
   if root:
    root_pad=self.pad(*root);ri=next(i for i,p in enumerate(pads)if p.m_Uuid==root_pad.m_Uuid);pairs=[(ri,j)for j in range(len(pads))if j!=ri]
   for i,j in pairs:
    a,b=xy(pads[i].GetPosition()),xy(pads[j].GetPosition());path=None
    for w in sorted(set([width,.3,.25]),reverse=True):
     path=self.route_path(n,a,b,w)
     if path is not None:break
    if path is None:
     print('Deferred to DRC-aware general router:',n,flush=True);continue
    self.track(n,path,w)
   print('Top-copper RF/power tree:',n,flush=True)
   pcb.SaveBoard(str(HW/'RF80.kicad_pcb'),self.b)
 def save(self):
  pcb.SaveBoard(str(HW/'RF80.kicad_pcb'),self.b)
  (REV/'placement_plan.json').write_text(json.dumps({r:dict(position_mm=xy(f.GetPosition()),angle_deg=f.GetOrientationDegrees(),footprint=self.parts[r]['footprint'],population=self.parts[r]['population'])for r,f in self.f.items()},indent=2)+'\n')
  (REV/'critical_routes.json').write_text(json.dumps(self.manual,indent=2)+'\n')
  assert pcb.ExportSpecctraDSN(self.b,str(REV/'RF80.dsn'))
  # Route digital low-current nets locally; ground is poured after routing.
  # Preserve the explicit HV-drain clearance in the external routing rules.
  import re
  path=REV/'RF80.dsn';s=path.read_text().replace('(clearance 200)','(clearance 150)').replace('(clearance 50 (type smd_smd))','(clearance 150 (type smd_smd))')
  a=s.index('    (class kicad_default');b=s.index('  (wiring',a)
  section=s[a:b];section=re.sub(r'\bGND\b','',section);section=re.sub(r'\bDRAIN_PA\b','',section)
  extra='    (class GROUND GND (circuit (use_via "Via[0-1]_600:300_um")) (rule (width 300)(clearance 150)))\n    (class HV_RF DRAIN_PA (circuit(use_via "Via[0-1]_600:300_um"))(rule(width 750)(clearance 600)))\n'
  pos=section.rfind('  )');section=section[:pos]+extra+section[pos:];s=s[:a]+section+s[b:];path.write_text(s)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--place',action='store_true');ap.add_argument('--import-session');a=ap.parse_args()
 if a.place:
  l=Layout();l.place_all();l.ground_vias();l.save();l.manual_routes();l.save();print('Placed',len(l.f),'electrical footprints;',len(l.vias),'local GND vias;',len(l.manual),'critical route records')
 elif a.import_session:
  b=pcb.LoadBoard(str(HW/'RF80.kicad_pcb'));assert pcb.ImportSpecctraSES(b,a.import_session);pcb.SaveBoard(str(HW/'RF80.kicad_pcb'),b);print('Imported local routing session')
 else:ap.error('Use --place or --import-session')
