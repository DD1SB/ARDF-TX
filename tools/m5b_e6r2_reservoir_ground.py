"""Short bulk-driver capacitor GND return to the common bottom plane."""
import math
from m5b_e6r2_common import *
from m5b_e6r2_local_routes import blocked

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));a=next(a for a in fps(b)['C409'].Pads() if a.GetNumber()=='2');assert a.GetNetname()=='GND';bottom=next(z.GetFilledPolysList(p.B_Cu) for z in b.Zones() if not z.GetIsRuleArea() and z.GetLayer()==p.B_Cu);log=[]
 candidates=[(104.8+dx*.2,121+dy*.2) for dx in range(-20,21) for dy in range(-20,21)]
 candidates.sort(key=lambda q:math.dist(q,xy(a.GetPosition())))
 for target in candidates:
  if len(log)==2:break
  v=p.PCB_VIA(b);v.SetPosition(pt(*target));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1)
  t=p.PCB_TRACK(b);t.SetStart(a.GetPosition());t.SetEnd(v.GetPosition());t.SetWidth(MM(.6));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet('GND'))
  if not bottom.Contains(v.GetPosition()):continue
  if blocked(b,[v,t],'GND'):continue
  if any(isinstance(q,p.PCB_VIA) and math.dist(xy(q.GetPosition()),target)<.8 for q in b.GetTracks()):continue
  b.Add(v);b.Add(t);log.append(dict(via_mm=target,track_width_mm=.6,from_pin='C409.2',land_drill_mm=[.6,.3]))
 assert len(log)==2,'Two safe short reservoir returns required'
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('C409-ground-return.json',dict(correction='Actual contact graph found isolated C409GND pad andFpour; connect with short wide traces/two ordinary vias to nativeBgroundplane',routes=log))
if __name__=='__main__':main()
