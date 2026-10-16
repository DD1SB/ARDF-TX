#!/usr/bin/python3
"""Implement flat-ended RF copper and controlled local junctions on E3."""
import pcbnew as p,json,math
from m5b_e3_common import *
from m5b_e3_local import pt,xy

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};parts={a['ref']:a for a in json.loads((HW/'RF2M.electrical.json').read_text())['parts']}
 def pad(r,n):return next(a for a in fs[r].Pads()if a.GetNumber()==str(n))
 def at(r,n):return xy(pad(r,n).GetPosition())
 nets={'MMIC_COUPLED','MMIC_AC','ST_IS_A','ST_IS_B','ST_IS_C','ST_IS_D','PA_GATE','PA_DRAIN','ST_O_A','ST_O_B','ST_O_C','ST_O_D','ST_DC_BLOCK','ST_LPF_IN','ST_F1','ST_F2','NORMAL_RF'}
 removed=[]
 for t in list(b.GetTracks()):
  if t.GetNetname()in nets and not isinstance(t,p.PCB_VIA):b.Remove(t);removed.append(t)
 for g in list(b.GetDrawings()):
  if g.GetLayer()==p.F_Cu and hasattr(g,'GetNetname')and g.GetNetname()in nets:b.Remove(g);removed.append(g)
 rows=[]
 def track(n,points,w=.4):
  for a,z in zip(points,points[1:]):
   if math.dist(a,z)<.0001:continue
   t=p.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*z));t.SetWidth(p.FromMM(w));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(n));t.SetLocked(True);b.Add(t)
 def join(r,n,s,k,w=.4):
  a=pad(r,n);z=pad(s,k);assert a.GetNetname()==z.GetNetname();track(a.GetNetname(),[at(r,n),at(s,k)],w)
 def poly(n,points):
  g=p.PCB_SHAPE(b);g.SetShape(p.SHAPE_T_POLY);z=p.SHAPE_POLY_SET();z.NewOutline()
  for x,y in points:z.Append(p.FromMM(x),p.FromMM(y))
  g.SetPolyShape(z);g.SetFilled(True);g.SetWidth(0);g.SetLayer(p.F_Cu);g.SetNet(b.FindNet(n));g.SetLocked(True);b.Add(g)
 def butt(n,a,z,w=WIDTH):
  assert abs(a[1]-z[1])<1e-5
  x0,x1=sorted([a[0],z[0]]);y=a[1];poly(n,[(x0,y-w/2),(x1,y-w/2),(x1,y+w/2),(x0,y+w/2)]);track(n,[a,z],.15);rows.append(dict(net=n,start_mm=a,end_mm=z,width_mm=w,type='butt-ended50ohm_nominal'))
 join('C602','2','R650','1',.55);join('R650','2','TL603','1',.15);join('R651','1','C602','2',.3)
 join('U501','3','C602','1',.7)
 for r,n,s,k in [('TL603','2','C631','1'),('TL603','2','C632','1'),('C632','2','TL604','1'),('TL604','2','C633','1'),('TL604','2','L634','1'),('L634','2','TL605','1'),('TL605','2','Q501','G'),('TL606','1','Q501','D'),('TL606','2','C636','1'),('TL606','2','TL607','1'),('TL607','2','L638','1'),('TL607','2','C637','1'),('L638','2','C638','1'),('L638','2','TL608','1'),('TL608','2','C639','1'),('C639','2','TL609','1')]:join(r,n,s,k)
 track('PA_GATE',[at('L606','2'),(107,51),(109.75,52.5),at('Q501','G')],.35)
 track('PA_DRAIN',[at('L635','2'),(117,50),(114.25,52.5),at('Q501','D')],.5)
 butt('ST_LPF_IN',at('TL609','2'),at('L641','1'))
 butt('ST_F1',at('L641','2'),at('L642','1'))
 butt('ST_F2',at('L642','2'),at('L643','1'))
 for i in range(3):
  l='L'+str(641+i);c='C'+str(641+i);sh='C'+str(644+i);join(l,'1',c,'1');join(l,'2',c,'2');join(l,'1',sh,'1')
 # Flat-ended1.02->2.741mm first1mm;last8mm tapers to1mm atSMA.
 a=at('L643','2');z=at('J501','1');x,y=a;end=z[0]
 poly('NORMAL_RF',[(x,y-.51),(x+1,y-WIDTH/2),(end-8,y-WIDTH/2),(end,y-.5),(end,y+.5),(end-8,y+WIDTH/2),(x+1,y+WIDTH/2),(x,y+.51)])
 track('NORMAL_RF',[a,z],.15);join('L643','2','C643','2');join('C647','1','L643','2')
 # Mirror exact new electrical metadata into the nativefootprint fields.
 for r in LENGTHS:
  for fld in fs[r].GetFields():
   if fld.GetName()=='Engineering_Note':fld.SetText(parts[r]['note'])
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('RF-extra-copper.json',dict(rectangles=rows,normal_launch=dict(start_mm=a,end_mm=z,width_mm=WIDTH,first_taper_mm=1,last_taper_mm=8,end_width_mm=1),source_and_drain_bias_routes='Retained reference points and values;single coherent routes replace obsolete duplicate copper',physical='NOT_RUN'))
 print('Flat RF copper and exact connectivity regenerated')
if __name__=='__main__':main()
