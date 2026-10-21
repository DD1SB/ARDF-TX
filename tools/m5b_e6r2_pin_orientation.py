"""Correct new frontup BD139 flat-footprint left3E/right1B lead ordering.
ST numeric1B2C3E is unchanged. Shared mounting/body geometry is unchanged.
"""
import shutil,zipfile
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry
from m5b_e6r2_pcb import power_footprints
HELD=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b);old=fs['Q402'];assert xy(old.GetPosition())==(130.72,41.25),'Already corrected'
 dest=OUT/'development/pre-flat-pin-correction';dest.mkdir(exist_ok=True)
 for fn in [HW/'RF2M.kicad_pcb',HW/'ARDF_2M.pretty/TO126_Flat_CommonPlane_E6R2.kicad_mod',HW/'ARDF_2M.3dshapes/Q402_CommonPlane_E6R2.step',OUT/'mechanical-source.json']:
  shutil.copy2(fn,dest/fn.name)
 with zipfile.ZipFile(dest/'draft-CAM.zip','w',zipfile.ZIP_DEFLATED)as z:
  for f in (OUT/'gerbers').iterdir():z.write(f,f.name)
 power_footprints();d=geometry()['devices']['Q402'];f=p.FootprintLoad(str(HW/'ARDF_2M.pretty'),d['footprint']);f.SetFPID(p.LIB_ID('ARDF_2M',d['footprint']));f.SetReference('Q402');f.SetValue(old.GetValue());f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid);f.SetPosition(pt(*d['pin1']))
 part=next(q for q in manifest()['parts'] if q['ref']=='Q402')
 for a in f.Pads():a.SetNet(b.FindNet(part['pins'][a.GetNumber()]))
 b.Remove(old);HELD.append(old);b.Add(f);removed=[]
 for t in list(b.GetTracks()):
  if t.GetNetname()in ['MOD_BASE','MOD_E']:
   assert not t.IsLocked();removed.append(dict(net=t.GetNetname(),uuid=t.m_Uuid.AsString()));b.Remove(t);HELD.append(t)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 save('flat-BD139-orientation-correction.json',dict(source='ST BD139/BD135 Rev5 front3-2-1 package illustration; ST2001drawing0016114/B frontleft3E,centre2C,right1B; drawingsviewed asmanufacturer-authoredreferences,not redistributedsources',numeric_pins='1B2C3Eunchanged',physical_left_to_right=['3=MOD_E','2=MOD_SINK','1=MOD_BASE'],new_pin1_mm=d['pin1'],mounting_body_cutouts_unchanged=True,local_routes_reopened=removed,physical='NOT_RUN'))
if __name__=='__main__':main()
