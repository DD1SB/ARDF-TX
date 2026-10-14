#!/usr/bin/python3
"""Focused E1->E2 PCB patch. Run once on E1; never replaces placement/whole routing."""
from m3b_pcb import *
import copy,heapq
D=HW/'review/M3B-E2'
class LocalRouter(Layout):
 def __init__(self,b):self.b=b;self.manual=[];self.nets={n:b.FindNet(n)for n in ('VPA_LOAD','SHAPE_BASE','VREF_2V5','GND')}
 def route_path(self,n,a,b,width,layer):
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
    if layer==pcb.B_Cu and p.GetAttribute()==pcb.PAD_ATTRIB_SMD:continue
    if p.GetNetname()==n:continue
    pg=max(gap,.65+width/2)if p.GetNetname()=='DRAIN_PA'else gap
    box=p.GetBoundingBox();mark_rect(pcb.ToMM(box.GetLeft())-pg,pcb.ToMM(box.GetTop())-pg,pcb.ToMM(box.GetRight())+pg,pcb.ToMM(box.GetBottom())+pg)
  for t in self.b.GetTracks():
   if t.GetNetname()==n:continue
   if isinstance(t,pcb.PCB_VIA):
    x,y=xy(t.GetPosition());rad=pcb.ToMM(t.GetWidth(pcb.F_Cu))/2+gap;mark_rect(x-rad,y-rad,x+rad,y+rad);continue
   if t.GetLayer()!=layer:continue
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
 def path(self,n,a,c,w,layer):
  path=self.route_path(n,a,c,w,layer)
  if path is None:raise RuntimeError(('No local path',n,a,c,w,layer))
  for aa,bb in zip(path,path[1:]):
   if math.dist(aa,bb)<.00001:continue
   t=pcb.PCB_TRACK(self.b);t.SetStart(pt(*aa));t.SetEnd(pt(*bb));t.SetWidth(MM(w));t.SetLayer(layer);t.SetNet(self.b.FindNet(n));self.b.Add(t)
  self.manual.append(dict(net=n,from_mm=a,to_mm=c,width_mm=w,layer=self.b.GetLayerName(layer),points_mm=path))

def main():
 b=pcb.LoadBoard(str(HW/'RF80.kicad_pcb'));assert b.GetTitleBlock().GetRevision()=='M3B-E1','Patch applies only to E1; use Git tag to reproduce'
 f={x.GetReference():x for x in b.GetFootprints()};m={p['ref']:p for p in json.loads((HW/'RF80.electrical.json').read_text())['parts']};removed=[];changes=[]
 def rm(n,a,c,layer=pcb.F_Cu):
  ts=[t for t in b.GetTracks()if not isinstance(t,pcb.PCB_VIA)and t.GetNetname()==n and t.GetLayer()==layer and(math.dist(xy(t.GetStart()),a)<.002 and math.dist(xy(t.GetEnd()),c)<.002 or math.dist(xy(t.GetStart()),c)<.002 and math.dist(xy(t.GetEnd()),a)<.002)]
  assert len(ts)==1,(n,a,c,len(ts))
  t=ts[0];removed.append(t);changes.append(dict(action='remove',net=n,from_mm=xy(t.GetStart()),to_mm=xy(t.GetEnd()),layer=b.GetLayerName(layer)));b.Remove(t)
 # Rotate the actual numbered ST footprint about its fixed collector.
 # Physical pad1 moves onto existing base copper, pad3 onto existing emitter copper.
 # No hidden pad renumbering, no PA/filter/source routing change.
 q=f['Q403'];q.SetOrientationDegrees(180);q.SetPosition(pt(160.56,69))
 for r in ('Q403','U311'):
  for p in f[r].Pads():p.SetNet(b.FindNet(m[r]['pins'][p.GetNumber()]))
 q.SetFPID(pcb.LIB_ID('ARDF_TX','ST_BD140_SOT32_1p3Drill'))
 for p in q.Pads():p.SetDrillSize(pt(1.3,1.3));p.SetSize(pt(1.9,1.9))
 model=pcb.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/3dmodels/ST_BD140_envelope.wrl';q.Models().clear();q.Models().push_back(model)
 # Only the reference's short terminal branches require electrical rerouting.
 for a,c in [((107.9375,72),(107.0125,72)),((107.0125,72),(106.0625,71.05)),((107.9375,73.7056),(107.9375,72))]:rm('VREF_2V5',a,c)
 rm('GND',(106.0625,72.95),(106.0625,73.95))
 rt=LocalRouter(b)
 for n,a,c,w,layer in [('VREF_2V5',(106.0625,72.95),(106.0625,71.05),.2,pcb.F_Cu),('VREF_2V5',(107.9375,73.7056),(106.0625,72.95),.2,pcb.F_Cu),('GND',(107.9375,72),(108.9,72),.28,pcb.F_Cu)]:rt.path(n,a,c,w,layer)
 v=pcb.PCB_VIA(b);v.SetPosition(pt(108.9,72));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v)
 # Synchronize actual schematic metadata, keeping position/orientation/other routes.
 comps={x.attrib['ref']:x for x in ET.parse(D/'RF80.xml').findall('./components/comp')}
 for r,q in f.items():
  if r not in comps:continue
  for key in ('MPN','Population','Function','Engineering_Note'):
   value=next((x.attrib.get('value','')for x in comps[r].findall('property')if x.attrib['name']==key),'');q.GetField(key).SetText(value)
  for key,kind in [('Datasheet',pcb.FIELD_T_DATASHEET),('Description',pcb.FIELD_T_DESCRIPTION)]:
   value=next((x.text or''for x in comps[r].findall('./fields/field')if x.attrib['name']==key),'');q.GetField(kind).SetText(value)
 for t in b.GetDrawings():
  if isinstance(t,pcb.PCB_TEXT)and'M3B-E1'in t.GetText():t.SetText(t.GetText().replace('M3B-E1','M3B-E2'))
 tb=b.GetTitleBlock();tb.SetRevision('M3B-E2');tb.SetDate('2026-10-15');b.SetTitleBlock(tb)
 ds=b.GetDesignSettings();ds.m_SolderMaskExpansion=MM(.025);ds.m_SolderMaskMinWidth=MM(.075)
 b.BuildConnectivity();pcb.ZONE_FILLER(b).Fill(b.Zones());pcb.SaveBoard(str(HW/'RF80.kicad_pcb'),b)
 (D/'local-copper-changes.json').write_text(json.dumps(dict(revision='M3B-E2',removed=changes,added=rt.manual,extra_ground_via_mm=[108.9,72]),indent=2)+'\n')
 print('Patched Q403/U311 physical nets; local branches only;',len(changes),'segments removed')
if __name__=='__main__':main()
