"""Exact-shape stitch for the small remaining ground island near interface.
No RF/source edits; ordinary unfilled0.6/0.3mm plated via.
"""
import math
from m5b_e6r2_common import *
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));zones=[z for z in b.Zones() if not z.GetIsRuleArea()];foreign=[]
 front=next(z.GetFilledPolysList(p.F_Cu) for z in zones if z.GetLayer()==p.F_Cu);island=None
 for i in range(front.OutlineCount()):
  q=front.COutline(i);pts=[xy(q.CPoint(k)) for k in range(q.PointCount())];xs=[x for x,y in pts];ys=[y for x,y in pts]
  if 34<min(xs) and max(xs)<38 and 90<min(ys) and max(ys)<95:island=i;break
 assert island is not None,'Reassess current native ground islands'
 for ob in list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads() if a.GetAttribute()!=p.PAD_ATTRIB_NPTH]:
  if ob.GetNetname()!='GND' and ob.GetBoundingBox().Intersects(p.BOX2I(pt(33,90),pt(6,5))):foreign.append(ob)
 holes=[a for f in b.GetFootprints() for a in f.Pads() if a.GetDrillSize().x];vias=[v for v in b.GetTracks() if isinstance(v,p.PCB_VIA)];v=p.PCB_VIA(b);v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1)
 pts=[(x/20,y/20)for x in range(692,742)for y in range(1827,1873)];pts.sort(key=lambda z:(z[0]-35.8)**2+(z[1]-92.5)**2)
 found=None
 for x,y in pts:
  pos=pt(x,y);v.SetPosition(pos)
  if not front.Contains(pos,island):continue
  if not all(any(z.GetLayer()==l and z.GetFilledPolysList(l).Contains(pos) for z in zones) for l in [p.F_Cu,p.B_Cu]):continue
  if any(math.dist((x,y),xy(q.GetPosition()))<.8 for q in vias):continue
  if any(math.dist((x,y),xy(q.GetPosition()))<p.ToMM(q.GetDrillSize().x)/2+.62 for q in holes):continue
  if any(any(o.IsOnLayer(l) and p.SHAPE.Collide(v.GetEffectiveShape(l),o.GetEffectiveShape(l),MM(.165)) for l in [p.F_Cu,p.B_Cu]) for o in foreign):continue
  found=(x,y);b.Add(v);break
 assert found,'No exact via overlap; route an explicit GND bridge'
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('last-ground-stitch.json',dict(position_mm=found,method='Actual effective foreign copper shapes, .165mm gap; actual F/Bfilledpoly overlap; no RF/source region',land_mm=.6,drill_mm=.3));print('Exact final ground stitch',found)
if __name__=='__main__':main()
