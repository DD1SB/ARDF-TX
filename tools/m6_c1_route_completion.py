#!/usr/bin/python3
"""Controller-only adaptation of the proven local two-layer airwire router."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'tools/m5b_route_completion.py').read_text()
code=code.replace('from m5b_pcb import P,D,MM',"from m6_c1_pcb import P,D,MM").replace("NAME='RF2M'","NAME='CTRL'")
code=code.replace('NX=1801;NY=1401','NX=1001;NY=1001').replace('NX=7201;NY=5601','NX=4001;NY=4001')
code=code.replace('g+.30','g+.40').replace('g+.30','g+.40').replace('MM(.6)','MM(.8)')
code=code.replace("if not(net=='GND'and p.GetNetname()=='GND'):","if True:")
code=code.replace('g=-.33','g=.2')
code=code.replace('STEP=.1;X0','STEP=.05;X0').replace('NX=1001;NY=1001','NX=2001;NY=2001').replace('expanded>1000000','expanded>4000000')
code=code.replace('.20 if p.GetNetname()==net else g+.40+extra','.45 if p.GetNetname()==net else g+.40+extra')
code=code.replace('bb=zone.GetBoundingBox();layer=0 if zone.GetLayer()==pcb.F_Cu else 1\n            rect(ds[layer],[pcb.ToMM(bb.GetLeft()),pcb.ToMM(bb.GetTop()),pcb.ToMM(bb.GetRight()),pcb.ToMM(bb.GetBottom())],width/2)', 'bb=zone.GetBoundingBox()\n            for layer in [l for l,copper in enumerate([pcb.F_Cu,pcb.B_Cu]) if zone.IsOnLayer(copper)]:\n                rect(ds[layer],[pcb.ToMM(bb.GetLeft()),pcb.ToMM(bb.GetTop()),pcb.ToMM(bb.GetRight()),pcb.ToMM(bb.GetBottom())],width/2);rect(vs[layer],[pcb.ToMM(bb.GetLeft()),pcb.ToMM(bb.GetTop()),pcb.ToMM(bb.GetRight()),pcb.ToMM(bb.GetBottom())],.4)')
exec(compile(code,__file__,'exec'))
