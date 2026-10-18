#!/usr/bin/python3
"""Localized signal clearance corrections after routing; no DRC suppression."""
import json
from m6_c1_pcb import *
def main():
 b=Board(True);changes=[]
 moves=[('UART_TX',(59.7079,33.55),(59.7079,33.63)),('FOX_REQ',(50.6369,76.3994),(50.6369,76.44)),('BAND80',(63.3697,79.9322),(63.3697,79.86)),('RF2M_PA_RAIL_ADC',(81.7141,54.0144),(81.7141,54.08))]
 for t in b.b.GetTracks():
  if isinstance(t,pcb.PCB_VIA):continue
  for net,old,new in moves:
   if t.GetNetname()!=net:continue
   for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
    if math.dist(xy(getter()),old)<.00002:setter(pt(*new));changes.append({'net':net,'uuid':t.m_Uuid.AsString(),'old_mm':old,'new_mm':new})
 # Short bootstrap return retains compact converter loop; no main-current neck.
 if not any(t.GetNetname()=='BUCK_SW' and xy(t.GetStart())==(52.775,105.7) for t in b.b.GetTracks()):b.track('BUCK_SW',[(52.775,105.7),(52.775,107),(51,107)],.25)
 b.save();(D/'local-clearance-corrections.json').write_text(json.dumps(changes,indent=2)+'\n')
if __name__=='__main__':main()
