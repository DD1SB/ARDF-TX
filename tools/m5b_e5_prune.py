#!/usr/bin/python3
"""Walk native-reported unused DC tails; no severity change or exclusions.
Intermediate DRC omits zone refill only to speed tail discovery. The final full
refill/ERC/DRC and power/connectivity gates remain mandatory.
"""
import subprocess
from m5b_e5_common import *
REMOVED=[]
def main():
 guard();records=[];tmp=OUT/'development/prune';tmp.mkdir(parents=True,exist_ok=True)
 for i in range(80):
  path=tmp/(str(i)+'.json');r=subprocess.run(['kicad-cli','pcb','drc','--format','json','--severity-all','-o',str(path),str(HW/'RF2M.kicad_pcb')],capture_output=True,text=True);assert r.returncode==0,r.stderr
  d=json.loads(path.read_text());bad=[v for v in d['violations']if v['type']in['track_dangling','via_dangling']and any('[VMOD]'in a['description']or'[VPA]'in a['description']for a in v['items'])]
  if not bad:break
  ids={a['uuid']for v in bad for a in v['items']};b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));gone=[]
  for t in list(b.GetTracks()):
   if t.m_Uuid.AsString()not in ids:continue
   assert t.GetNetname()in['VMOD','VPA']
   gone.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),start_mm=xy(t.GetStart()),end_mm=xy(t.GetEnd())));b.Remove(t);REMOVED.append(t)
  assert gone;records.extend(gone);p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);print('NativeDCtailprune',i,len(gone),flush=True)
 else:raise AssertionError('Native tail pruning failed to converge')
 save('unused-DC-tail-removal.json',dict(iterations=i,removed=records,native_DRC_identified_each_step=True,manufacturing_suppression=False,final_full_refill_required=True));print('Removed',len(records),'unusedDCsegments',flush=True)
if __name__=='__main__':main()
