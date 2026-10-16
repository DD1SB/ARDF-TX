#!/usr/bin/python3
"""Prune only KiCad-reported redundant vias and dead-end track branches.
Each iteration reruns native DRC; required pads are retained and any new
required airwire remains visible. This is routing cleanup, not a waiver.
"""
import json,subprocess
import m5a_r1_design as c
from m5b_pcb import P,D
bpath=P/'RF2M.kicad_pcb';logs=[]
for run in range(12):
 out=D/f'trim-{run}-DRC.json';r=subprocess.run(['kicad-cli','pcb','drc','--format','json','--severity-all','--refill-zones','--save-board','-o',str(out),str(bpath)],capture_output=True,text=True);assert r.returncode==0,r.stderr
 report=json.load(open(out));bad={i['uuid']for v in report['violations']if v['type']in ['via_dangling','track_dangling']for i in v['items']}
 if not bad:break
 b=c.parse(bpath.read_text());dead=[t for t in b[1:]if isinstance(t,list)and t[0]in ['segment','via','arc']and c.child(t,'uuid')[1]in bad]
 if not dead:break
 for t in dead:b.remove(t)
 bpath.write_text(c.dump(b)+'\n');logs.append(dict(iteration=run,removed=len(dead),objects=sorted(bad)));print('Trim',run,len(dead),flush=True)
(D/'routing-remnant-trim.json').write_text(json.dumps(logs,indent=2)+'\n')
