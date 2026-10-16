#!/usr/bin/python3
"""Expose a grounded bottom thermal contact while retaining source-via tents.
This is a mechanical/assembly provision, not a qualified thermal resistance.
No non-ground bottom copper is permitted in the 14x12mm contact envelope.
"""
import json,uuid
import pcbnew as p
import m5a_r1_design as c
from m5b_pcb import P,D
RECTS=[(105,49,110.95,61),(111.75,49,112.25,61),(113.05,49,119,61),(110.95,49,113.05,52.6),(110.95,57.4,113.05,61)]
def main():
 fn=P/'RF2M.kicad_pcb';b=p.LoadBoard(str(fn))
 for t in list(b.GetTracks())+[pa for f in b.GetFootprints()for pa in f.Pads()]:
  if not t.IsOnLayer(p.B_Cu)or t.GetNetname()=='GND':continue
  bb=t.GetBoundingBox();assert not(p.ToMM(bb.GetRight())>=105 and p.ToMM(bb.GetLeft())<=119 and p.ToMM(bb.GetBottom())>=49 and p.ToMM(bb.GetTop())<=61),('Foreign bottom copper in thermal contact',t.GetNetname())
 s=c.parse(fn.read_text());ids={str(uuid.uuid5(uuid.NAMESPACE_URL,'ARDF-TX/M5B/thermal-mask/'+str(i)))for i in range(len(RECTS))}
 for x in list(c.children(s,'gr_rect')):
  if c.child(x,'uuid')and c.child(x,'uuid')[1]in ids:s.remove(x)
 for i,(a,b1,cc,d)in enumerate(RECTS):
  u=str(uuid.uuid5(uuid.NAMESPACE_URL,'ARDF-TX/M5B/thermal-mask/'+str(i)))
  s.append(c.parse(f'(gr_rect(start {a} {b1})(end {cc} {d})(stroke(width 0)(type default))(fill solid)(layer "B.Mask")(uuid "{u}"))'))
 fn.write_text(c.dump(s)+'\n')
 (D/'thermal-contact.json').write_text(json.dumps(dict(mask_openings_mm=RECTS,overall_contact_mm=[105,49,119,61],source_via_tented_strips_mm=[[110.95,52.6,111.75,57.4],[112.25,52.6,113.05,57.4]],reason='Expose ground copper for thin TIM/spreader;do not press a bare spreader against live tracks or untented solder-filled barrels.',interface='Electrically insulating thermal sheet0.15-0.25mm,k>=3W/mK,dielectric>=100V across16x44x8mm spreader face;exact external material OPEN. Separate verified ground strap;do not rely on solder mask insulation.40mm bench supports,independent mechanical support/lead clearance.',physical='NOT_RUN;via conduction/solder voids/TIM/contact resistance require thermal measurement'),indent=2)+'\n')
 print('Bottom ground thermal window added;source-via mask tents retained')
if __name__=='__main__':main()
