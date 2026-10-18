#!/usr/bin/python3
"""Remove only native-reported unused USB power tail; never suppress DRC."""
import json,subprocess,tempfile
from m6_c1_pcb import *
def main():
 log=[]
 with tempfile.TemporaryDirectory(prefix='m6-prune-') as temp:
  for i in range(20):
   report=Path(temp)/(str(i)+'.json');subprocess.run(['kicad-cli','pcb','drc','--format','json','--severity-all','--refill-zones','--save-board','-o',str(report),str(P/'CTRL.kicad_pcb')],capture_output=True,check=True);r=json.loads(report.read_text());bad=[v for v in r['violations'] if v['type']=='track_dangling']
   if not bad:break
   ids={x['uuid'] for v in bad for x in v['items']};b=Board(True)
   assert all(t.GetNetname()=='USB_VBUS' for t in b.b.GetTracks() if t.m_Uuid.AsString() in ids),'Unexpected non-USB dangling feature'
   sx=parse((P/'CTRL.kicad_pcb').read_text());sx[:]=[x for x in sx if not(isinstance(x,list) and x and x[0]=='segment' and child(x,'uuid') and str(child(x,'uuid')[1]) in ids)];(P/'CTRL.kicad_pcb').write_text(dump(sx)+'\n');log+=bad
  else:raise AssertionError('USB tail pruning did not converge')
 (D/'unused-USB-tail-removal.json').write_text(json.dumps(log,indent=2)+'\n');print('Removed',len(log),'native-reported unused USB branch segments')
if __name__=='__main__':main()
