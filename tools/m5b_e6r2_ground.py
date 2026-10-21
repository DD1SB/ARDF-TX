"""Stitch remaining bottom filled islands from current native zone polygons."""
import math
from m5b_e6r2_common import *
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));zs={z.GetLayer():z for z in b.Zones() if not z.GetIsRuleArea()};bot=p.SHAPE_POLY_SET(zs[p.B_Cu].GetFilledPolysList(p.B_Cu));top=p.SHAPE_POLY_SET(zs[p.F_Cu].GetFilledPolysList(p.F_Cu));via=[t for t in b.GetTracks() if isinstance(t,p.PCB_VIA)];holes=[a for f in b.GetFootprints() for a in f.Pads() if a.GetDrillSize().x];landmarks=[t.GetPosition() for t in via if t.GetNetname()=='GND']+[a.GetPosition() for a in holes if a.GetNetname()=='GND'];bot.Inflate(-MM(.32),p.CORNER_STRATEGY_ROUND_ALL_CORNERS,MM(.005));top.Inflate(-MM(.32),p.CORNER_STRATEGY_ROUND_ALL_CORNERS,MM(.005));log=[]
 for i in range(bot.OutlineCount()):
  if any(bot.Contains(q,i) for q in landmarks):continue
  poly=bot.COutline(i);points=[xy(poly.CPoint(k)) for k in range(poly.PointCount())];xx=[q[0]for q in points];yy=[q[1]for q in points];cx=(min(xx)+max(xx))/2;cy=(min(yy)+max(yy))/2
  candidates=[(x/10,y/10)for x in range(math.floor(min(xx)*10),math.ceil(max(xx)*10)+1)for y in range(math.floor(min(yy)*10),math.ceil(max(yy)*10)+1)];candidates.sort(key=lambda q:(q[0]-cx)**2+(q[1]-cy)**2)
  for x,y in candidates:
   pos=pt(x,y)
   if 84<x<100 and 27<y<73:continue
   if not bot.Contains(pos,i) or not top.Contains(pos):continue
   if any(math.dist((x,y),xy(t.GetPosition()))<.65 for t in via):continue
   if any(math.dist((x,y),xy(a.GetPosition()))<p.ToMM(a.GetDrillSize().x)/2+.62 for a in holes):continue
   v=p.PCB_VIA(b);v.SetPosition(pos);v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v);via.append(v);landmarks.append(pos);log.append([x,y]);break
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('bottom-island-stitches.json',log);print('Bottom island new stitches',len(log))
if __name__=='__main__':main()
