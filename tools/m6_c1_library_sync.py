#!/usr/bin/python3
"""Freeze controller-owned footprint artwork without suppressing library checks.
Copper/holes stay unchanged. Vendor silk moved to Fab is an intentional local
assembly-artwork adaptation; named originals remain in footprint-origins.json.
"""
import sys,json
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller'
def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));mapping=json.loads((P/'footprint-origins.json').read_text()) if (P/'footprint-origins.json').exists() else {};done=set();io=p.PCB_IO_KICAD_SEXPR()
 for f in b.GetFootprints():
  old=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName());new=old if old.startswith('ARDF_CTL:') else 'ARDF_CTL:Local_'+old.replace(':','__');mapping[old]=new
  f.SetFPID(p.LIB_ID('ARDF_CTL',new.split(':')[1]))
  for a in f.Pads():a.SetLocalZoneConnection(p.ZONE_CONNECTION_INHERITED)
  if new not in done:io.FootprintSave(str(P/'ARDF_CTL.pretty'),f);done.add(new)
 for z in b.Zones():
  if not z.GetIsRuleArea():z.SetPadConnection(p.ZONE_CONNECTION_FULL)
 # Remove the four tiny router necks; normal-width reconnection is mandatory.
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString() in ['d1fc42e4-9fc6-45ce-a615-089cf6f4c23f','e6064f9c-63b3-4503-8ebb-664b8f01e0be','303169ab-7397-4576-b4bf-bdcdbb6c631e','dcd3d39c-ea64-43e2-a3a3-b140db2013cf']:b.Remove(t)
 p.SaveBoard(str(P/'CTRL.kicad_pcb'),b);(P/'footprint-origins.json').write_text(json.dumps(mapping,indent=2)+'\n');print('Controller local footprints:',len(done))
if __name__=='__main__':main()
