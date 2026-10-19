#!/usr/bin/python3
"""Remove DRC-identified nonfunctional stubs and repair one local DC crossing.
All electrical pad/net membership and source/matching geometry stay protected.
"""
import math
from m5b_e5_common import *
REMOVED=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));d=json.loads((OUT/'DRC.json').read_text());objects={t.m_Uuid.AsString():t for t in b.GetTracks()};log=[]
 targets={i['uuid']for v in d['violations']if v['type']in['track_dangling','via_dangling']for i in v['items']}
 targets.add('ccaeda0e-5ad7-40b4-a30b-ae1f78d0b1d8')
 for t in list(b.GetTracks()):
  uid=t.m_Uuid.AsString();sliver=t.GetNetname()=='CLK_TRAIN'and not isinstance(t,p.PCB_VIA)and set([xy(t.GetStart()),xy(t.GetEnd())])=={(23.5,70.9),(23.5,73.)}
  if uid not in targets and not sliver:continue
  if t.IsLocked()and t.GetNetname()not in['GND','VMOD','VPA','OV_REF','NORMAL_OFF','MOD_SINK']:continue
  if isinstance(t,p.PCB_VIA)and 89<p.ToMM(t.GetPosition().x)<95 and 48<p.ToMM(t.GetPosition().y)<62:raise AssertionError('Do not remove thermal via')
  assert t.GetNetname()not in['GATE_PA','DRAIN_PA','PA_DRAIN','RF_OUT','RF_NORMAL'],'RF protected track unexpectedly dangling'
  log.append(dict(uuid=uid,net=t.GetNetname(),start_mm=xy(t.GetStart()),end_mm=xy(t.GetEnd()),reason='LocatedCLKdoubleback'if sliver else'DRCdangling/localSAFE_Ncrossing'));b.Remove(t);REMOVED.append(t)
 for v in d['violations']:
  if v['type']!='track_not_centered_on_via':continue
  os=[objects.get(i['uuid'])for i in v['items']];via=next((t for t in os if isinstance(t,p.PCB_VIA)),None);tr=next((t for t in os if t and not isinstance(t,p.PCB_VIA)),None)
  if not via or not tr or tr in REMOVED:continue
  edge=min(['Start','End'],key=lambda s:math.dist(xy(getattr(tr,'Get'+s)()),xy(via.GetPosition())));assert math.dist(xy(getattr(tr,'Get'+edge)()),xy(via.GetPosition()))<.4;getattr(tr,'Set'+edge)(via.GetPosition())
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('stub-clearance-cleanup.json',dict(actions=log,warning_suppression=False));print('Removed',len(log),'nonfunctionalstubs/localDCconflict',flush=True)
if __name__=='__main__':main()
