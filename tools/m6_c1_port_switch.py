#!/usr/bin/python3
"""TPS22918DBVR native landing correction; preserve nets, local route endpoints.
Same1VIN/2GND/3ON/4CT(open)/5QOD/6OUT functional map, larger DBV package.
"""
import json,math
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};changes=[]
 for ref in ['U40','U50']:
  old=fs[ref];fid=str(old.GetFPIDAsString())
  if old.GetValue()=='TPS22918DBVR':continue
  new=p.FootprintLoad(str(P/'ARDF_CTL.pretty'),'SOT-23-6_CTL');new.SetReference(ref);new.SetValue('TPS22918DBVR');new.SetFPID(p.LIB_ID('ARDF_CTL','SOT-23-6_CTL'));new.SetPosition(old.GetPosition());new.SetOrientation(old.GetOrientation());new.SetPath(old.GetPath())
  for field in old.GetFields():
   if field.GetName() in ['Reference','Value','Footprint']:continue
   nf=next((x for x in new.GetFields() if x.GetName()==field.GetName()),None)
   if nf:nf.SetText(field.GetText())
   else:nf=p.PCB_FIELD(new,p.FIELD_T_USER,field.GetName());nf.SetText(field.GetText());new.Add(nf)
   nf.SetVisible(False)
  new.Reference().SetLayer(p.F_Fab);new.Value().SetVisible(False)
  pads={q.GetNumber():q for q in new.Pads()};moved=[]
  for q in old.Pads():
   a=pads[q.GetNumber()];a.SetNet(q.GetNet());sh=q.GetEffectiveShape(p.F_Cu)
   for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA) or t.GetNetname()!=q.GetNetname() or t.GetLayer()!=p.F_Cu:continue
    for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
     v=getter()
     if sh.Collide(p.SHAPE_CIRCLE(v,1)):
      moved.append({'uuid':t.m_Uuid.AsString(),'old_mm':[p.ToMM(v.x),p.ToMM(v.y)],'new_mm':[p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)]});setter(a.GetPosition())
  b.Remove(old);b.Add(new);changes.append({'ref':ref,'previous':fid,'selected':'ARDF_CTL:SOT-23-6_CTL','endpoints_moved':moved})
 # Save/reload before further KiCad APIs: SWIG removal lifetime is not stable.
 p.SaveBoard(str(P/'CTRL.kicad_pcb'),b)
 (D/'port-switch-correction.json').write_text(json.dumps({'selected':'TPS22918DBVR','manufacturer':'https://www.ti.com/lit/gpn/tps22918','reason':'TPS22919 hot RON was not represented by the earlier0.115ohm allowance','RON_bound_ohm':.088,'RON_evidence':'88mohm max at1.8V,-40..105C;80mohm max at2.5/3.3V. Use88mohm conservative envelope, not typical53mohm.','CT':'left open, explicitly permitted by datasheet; slow power-up wait250ms still required','QOD':'tied toOUT, manufacturer permitted','short_circuit':'No switch current limiter. Buck cycle current limit, controller fuse and independent supervisor reset/POWER pull-down shut down branch. Current-limited short/load-step bench test NOT_RUN.','changes':changes},indent=2)+'\n')
 print('Port switches corrected',len(changes))
if __name__=='__main__':main()
