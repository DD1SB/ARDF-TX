#!/usr/bin/python3
"""Native main-current copper paths; inherited contact-graph numerical method.
Every traversed segment is charged its full80C resistance, ignoring parallel
planes; this overbounds partial traversals. No thermal measurement claim.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'tools/m5b_e3_power_paths.py').read_text()
code=code.replace('from m5b_e3_common import *',"ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/controller';OUT=HW/'review/M6-C1'\ndef save(n,x):(OUT/n).write_text(json.dumps(x,indent=2)+'\\n')")
code=code.replace('import pcbnew as p,math,heapq,json,collections','import pcbnew as p,math,heapq,json,collections\nfrom pathlib import Path')
code=code.replace("HW/'RF2M.kicad_pcb'","HW/'CTRL.kicad_pcb'")
a=code.index('pairs=[');e=code.index('\n for r,n,s,k',a)
code=code[:a]+"pairs=[('J1','1','F1','1'),('F1','2','D1','2'),('D1','1','D4','2'),('D4','1','U1','3'),('U1','5','L1','1'),('L1','2','U10','2'),('L1','2','U40','1'),('L1','2','U50','1'),('U40','6','J4','1'),('U50','6','J5','1')]"+code[e:]
code=code.replace('w<.5 and l>2','w<.3 and l>2')
code=code.replace('Thinlongsensebranchesexcluded.','Controller main routes>=0.30mm or individual<=2mm necks; thin long sense branches excluded.10um via plating is a sensitivity assumption, not a factory minimum.')
code=code.replace('18e-6','10e-6').replace("i=3 if net in POWER_INPUT else 1.8 if net=='VPA'else 2.","i=1.2 if net=='BUCK_SW' else .4 if net in ['V3V3','PACK_RAW','PACK_FUSED','PACK_PROT','VIN_SYS'] else .15")
code=code.replace("'power-native-main-paths.json'","'power-native-main-paths.json'")
exec(compile(code,__file__,'exec'))
