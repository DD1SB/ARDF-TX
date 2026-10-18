#!/usr/bin/python3
"""Dimensioned controller mechanics from native geometry; no enclosure claim."""
import json,html
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};mm=p.ToMM
 def xy(v):return[mm(v.x),mm(v.y)]
 refs=['J1','J2','J4','J5','J7','U10','U20','BT1','H1','H2','H3','H4']
 geom={'dimensions_mm':[100,100,1.6],'origin_native_mm':[20,20],'manufacturing':'standard2L1ozFR4/HASL','components':{r:{'at_native_mm':xy(fs[r].GetPosition()),'rotation_deg':fs[r].GetOrientationDegrees(),'MPN':next((f.GetText() for f in fs[r].GetFields() if f.GetName()=='MPN'),'mechanical'),'pads':{a.GetNumber():xy(a.GetPosition()) for a in fs[r].Pads() if a.GetNumber()}} for r in refs},'mounts':'four3.2mmNPTH/M3, no common bolt pattern with RF80 or RF2M','installation':'side-by-side on independently supported boards; no forced direct stacking','controller_below_clearance_mm':10,'controller_top_reserved_mm':15,'RF2M_below_cooling_projection_mm':25.2,'RF2M_support_initial_min_mm':30,'RF_cooling_airflow':'30mm support is mechanical clearance only; enclosure/convection qualification remains OPEN','RF_cables':'IDC150mm initial, no hot-plug while armed, straight-through continuity checked','antenna':'ESP all-layer copper keepout retained; no metal/cable in manufacturer clearance. Optional external LoRa antenna not under RF heatsinks.','enclosure_qualification':'NOT_RUN','primary_cell_holder':'Keystone3000 PCB negative contact, no paste; HASL cleanliness/contact-retention physical gate'}
 (D/'mechanical-interface.json').write_text(json.dumps(geom,indent=2)+'\n')
 s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 780"><style>text{font:14px sans-serif;fill:#17212b}.small{font-size:11px}</style><rect width="900" height="780" fill="white"/><text x="25" y="27">M6-C1 native mounting/interface drawing — dimensions mm — review only</text><g transform="translate(55,65) scale(5)"><rect x="0" y="0" width="100" height="100" fill="#e5f4e9" stroke="#17212b" stroke-width=".3"/>']
 for r in refs:
  f=fs[r];x,y=xy(f.GetPosition());x-=20;y-=20
  if r.startswith('H'):s.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="white" stroke="black" stroke-width=".2"/>')
  else:s.append(f'<circle cx="{x}" cy="{y}" r=".7" fill="#15445c"/>')
  s.append(f'<text x="{x+1}" y="{y-1}" style="font-size:2.4px">{r} ({x:.2f},{y:.2f})</text>')
 s.append('<path d="M0,-4 H100 M-4,0 V100" stroke="black" stroke-width=".2"/><text x="43" y="-5" style="font-size:3px">100.00</text><text x="-12" y="50" style="font-size:3px" transform="rotate(-90,-12,50)">100.00</text></g>')
 s+=['<text x="590" y="88">Top-view connector numbering</text><text x="590" y="112" class="small">J4/J5: pad1 at upper-left, pad2 right;</text><text x="590" y="130" class="small">odd/even columns increase downward.</text><text x="590" y="155" class="small">Both RF boards have same local pin order.</text><text x="590" y="180" class="small">16P female: Würth61201623021</text><text x="590" y="198" class="small">20P female: Würth61202023021</text><text x="590" y="222" class="small">Continuity-test every conductor,1↔1.</text><text x="590" y="246" class="small">Stripe/key appearance alone is insufficient.</text><text x="590" y="280">J1 internal coded harness only</text><text x="590" y="304" class="small">1PACK_RAW /2GND /3ID resistor</text><text x="590" y="324" class="small">XHP-3 + SXH-001T-P0.6 contacts</text><text x="590" y="344" class="small">NOT a Li-ion balance connector.</text><text x="590" y="380">USB exits left edge.</text><text x="590" y="405" class="small">Keep top antenna area free of metal.</text>']
 s+=['<text x="40" y="610">Mechanical section (envelopes; not a common enclosure)</text><rect x="70" y="650" width="350" height="8" fill="#429a61"/><rect x="115" y="610" width="80" height="40" fill="#8999a3"/><text x="215" y="638">Controller top reserve15mm</text><path d="M80,658 V708 H410 V658" fill="none" stroke="black"/><text x="90" y="730">10mm controller standoffs; trim solder-side leads</text><rect x="550" y="650" width="290" height="8" fill="#429a61"/><rect x="620" y="658" width="150" height="105" fill="#a5afb6"/><text x="555" y="626">RF2M: retain25.2mm cooling below PCB</text><text x="555" y="778" class="small">Separate≥30mm supports; airflow/enclosure still unqualified.</text></svg>']
 (D/'mechanical-drawing.svg').write_text(''.join(s))
 print('Native mechanical drawing and connector coordinate tables generated')
if __name__=='__main__':main()
