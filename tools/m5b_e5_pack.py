#!/usr/bin/python3
"""Native placement clearance repair; fixed RF/source geometry never packed."""
import math,collections
from m5b_e5_common import *

def bb(f):
 f.BuildCourtyardCaches();q=f.GetCourtyard(p.F_CrtYd)
 b=q.BBox()if q.OutlineCount()else f.GetBoundingBox(False,False)
 return[p.ToMM(v)for v in[b.GetX(),b.GetY(),b.GetRight(),b.GetBottom()]]
def overlap(a,b,gap=.15):return a[0]<b[2]+gap and a[2]>b[0]-gap and a[1]<b[3]+gap and a[3]>b[1]-gap

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};plan=json.loads((OUT/'floorplan.json').read_text());groups={x['ref']:x['group']for x in plan['moved_components']};m=json.loads((HW/'RF2M.electrical.json').read_text());parts={x['ref']:x for x in m['parts']};locked={r for r in fs if groups[r]=='rigid_RF_thermal'}|{'H1','H2','H3','H4','J101','J301','J302','Q401','Q402','Q403','Q404','U101','U102','U103','Y101','C101','C102','C103','U301','L301','U302','L302','C303','C304','C305','C401','C402','C403','C404','C405','C960','C961'}
 fixed=[];collisions=[]
 for r in sorted(locked):
  f=fs[r];a=bb(f)
  # TL/probe footprints intentionally represent distributed copper, not bodies.
  if r.startswith(('TL','TP')):continue
  for rr,z in fixed:
   if overlap(a,z,0):collisions.append((r,rr))
  fixed.append((r,a))
 print('Fixed body conflicts',collisions,flush=True)
 assert not collisions,collisions
 # Reference-coordinate snapshots bind all component moves to the initial plan.
 result=[]
 movable=[r for r in fs if r not in locked]
 def rank(r):
  a=bb(fs[r]);area=(a[2]-a[0])*(a[3]-a[1]);priority=0 if r.startswith('U')else 1 if area>10 else 2 if not r.startswith('TP')else 3
  return(priority,-area,r)
 for r in sorted(movable,key=rank):
  f=fs[r];x,y=xy(f.GetPosition());best=None
  # Prefer a small correction; a 0.5mm search grid retains ordinary assembly.
  for radius in range(0,35):
   opts=[(0,0)]if radius==0 else[(i,radius)for i in range(-radius,radius+1)]+[(i,-radius)for i in range(-radius,radius+1)]+[(radius,i)for i in range(-radius+1,radius)]+[(-radius,i)for i in range(-radius+1,radius)]
   candidates=[]
   for dx,dy in opts:
    xx,yy=x+.5*dx,y+.5*dy;f.SetPosition(pt(xx,yy));a=bb(f)
    if a[0]<21 or a[1]<23 or a[2]>169 or a[3]>128:continue
    if any(overlap(a,z)for rr,z in fixed):continue
    # Keep unrelated bodies outside RF strip, screw-washer envelopes and the
    # keyed IDC mating body. Holes are not a substitute for hardware envelopes.
    if overlap(a,[29,48,169,62],.4):continue
    if any(overlap(a,[cx-4.7,cy-4.7,cx+4.7,cy+4.7],0)for cx,cy in[(92,32),(92,68)]):continue
    if overlap(a,[21.8,74,34,109.5],0):continue
    candidates.append((dx*dx+dy*dy,xx,yy,a))
   if candidates:best=min(candidates);break
  if best is None:raise RuntimeError(('Placement exhausted',r,[x,y]))
  _,xx,yy,a=best;f.SetPosition(pt(xx,yy));fixed.append((r,a));result.append(dict(ref=r,before_pack_mm=[x,y],after_pack_mm=[xx,yy],additional_move_mm=[xx-x,yy-y]))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('placement-clearance-repair.json',dict(status='PASS_NATIVE_COURTYARD_PACKING',preserved_rigid_refs=sorted(locked),moves=result,limitations='AABB courtyard and explicit service envelopes; full native DRC follows, not inferred. RF/source joints never auto-moved.'))
 print('Placed',len(movable),'movable components; local corrections',sum(x['additional_move_mm']!=[0,0]for x in result))
if __name__=='__main__':main()
