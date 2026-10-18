#!/usr/bin/python3
"""Locally widen 3.3V copper where actual native foreign-copper permits.
No circuit or placement change. Mandatory zone refill and full DRC afterwards.
"""
import json,math
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));foreign={p.F_Cu:[],p.B_Cu:[]}
 for f in b.GetFootprints():
  for a in f.Pads():
   for l in foreign:
    if a.IsOnLayer(l) and a.GetNetname()!='V3V3':foreign[l].append(a.GetEffectiveShape(l))
 for t in b.GetTracks():
  for l in foreign:
   if t.IsOnLayer(l) and t.GetNetname()!='V3V3':foreign[l].append(t.GetEffectiveShape(l))
 changes=[]
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA) or t.GetNetname()!='V3V3' or p.ToMM(t.GetWidth())<.35:continue
  old=t.GetWidth()
  for width in [1.0,.8,.65]:
   if p.FromMM(width)<=old:continue
   t.SetWidth(p.FromMM(width));s=t.GetEffectiveShape(t.GetLayer());bb=s.BBox()
   if min(p.ToMM(bb.GetLeft())-20,p.ToMM(bb.GetTop())-20,120-p.ToMM(bb.GetRight()),120-p.ToMM(bb.GetBottom()))<.5:continue
   if not any(p.SHAPE.Collide(s,v,p.FromMM(.165)) for v in foreign[t.GetLayer()]):break
  else:t.SetWidth(old)
  if t.GetWidth()!=old:changes.append({'uuid':t.m_Uuid.AsString(),'old_width_mm':p.ToMM(old),'new_width_mm':p.ToMM(t.GetWidth()),'length_mm':p.ToMM(t.GetLength())})
 p.SaveBoard(str(P/'CTRL.kicad_pcb'),b)
 (D/'power-copper-reinforcement.json').write_text(json.dumps({'method':'Actual native shape clearance>=0.165mm before refill; no placement/net change; final KiCad and independent DFM remain mandatory','segments':changes},indent=2)+'\n');print('Locally widened',len(changes),'V3V3 segments')
if __name__=='__main__':main()
