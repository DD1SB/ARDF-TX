#!/usr/bin/python3
"""Targeted reroutes forced by wider matching artwork;no RF circuit change."""
import pcbnew as p,json
from m5b_e3_common import *
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));remove=[]
 for t in b.GetTracks():
  if not isinstance(t,p.PCB_VIA)and t.GetNetname()in['MOD_OFF_BASE','MOD_DRIVE','VDRV_MMIC']:
   ys=[p.ToMM(t.GetStart().y),p.ToMM(t.GetEnd().y)]
   if t.GetLayer()==p.F_Cu and min(ys)<66 and max(ys)>40:remove.append(t)
 for t in remove:b.Remove(t)
 tracks={t.m_Uuid.AsString():t for t in b.GetTracks()}
 # A widened power bus next to mechanicalH5 retains a short0.6mmneck,
 # which is included explicitly in the power-loss calculation.
 tracks['318ce3b5-dbe4-4c24-9b1f-29f918e4f68e'].SetWidth(p.FromMM(.6))
 # Tangential via overlaps exposed by strict neck-check:restore smallerland
 # instead of letting an almost-touching land be a current connection.
 for uid in['8697788b-46e1-43ce-a255-1b2da5b8ceff','8c74cbbb-4c88-48c4-815c-5c98d269013d']:tracks[uid].SetWidth(p.FromMM(.6))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('development/control-reroute-removals.json',dict(removed_track_ids=[t.m_Uuid.AsString()for t in remove],nets=['MOD_OFF_BASE','MOD_DRIVE','VDRV_MMIC']))
if __name__=='__main__':main()
