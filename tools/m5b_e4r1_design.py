#!/usr/bin/python3
"""Local E4 source-joint correction, explicitly open ordinary vias."""
import pcbnew as p,json,uuid
from m5b_e4r1_common import *
MM=p.FromMM
REMOVED=[]
def pt(x,y):return p.VECTOR2I(MM(x),MM(y))
def rect(parent,layer,r,label,net=None):
 g=p.PCB_SHAPE(parent);g.SetShape(p.SHAPE_T_RECT);g.SetStart(pt(*r[:2]));g.SetEnd(pt(*r[2:]));g.SetLayer(layer);g.SetFilled(True);g.SetWidth(0)
 g.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,REV+'/'+label))))
 if net is not None:g.SetNet(net)
 parent.Add(g);return g
def mask(f):
 for g in list(f.GraphicalItems()):
  if g.GetLayer()in[p.F_Mask,p.F_Paste]:f.Remove(g);REMOVED.append(g)
 x,y=p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)
 def relative(r):return tuple(r[i]-(112 if i%2==0 else 55)+(x if i%2==0 else y)for i in range(4))
 rect(f,p.F_Mask,relative(SOLDER),'source-mask-continuous-opening')
 for i,r in enumerate(PASTE):rect(f,p.F_Paste,relative(r),'source-paste-window/'+str(i))
 f.SetLibDescription('ST PD54008L-E Jan2007 Rev2 p13 G/D0.5x5 S2.7x5; E4R1 source mask2.1x5, five paste windows,16 open source vias; physical process NOT_RUN')
def main():
 guard();base=OUT/'development/E4-native.kicad_pcb';base.parent.mkdir(parents=True,exist_ok=True);base.write_bytes(gitfile('hardware/2m/RF2M.kicad_pcb'));base.with_suffix('.kicad_pro').write_bytes(gitfile('hardware/2m/RF2M.kicad_pro'))
 (HW/'RF2M.kicad_pro').write_bytes(gitfile('hardware/2m/RF2M.kicad_pro'))
 b=p.LoadBoard(str(base));assert b.GetTitleBlock().GetRevision()=='M5B-E4'
 old=[v for v in b.GetTracks()if isinstance(v,p.PCB_VIA)and 109<p.ToMM(v.GetPosition().x)<115 and 48<p.ToMM(v.GetPosition().y)<62];assert len(old)==104
 # Retain outer/near objects where possible. Remove only the old40 source vias.
 direct=[v for v in old if 52.2<p.ToMM(v.GetPosition().y)<57.8];assert len(direct)==50
 for v in direct:b.Remove(v);REMOVED.append(v)
 for x,y,d,w,kind in via_specs():
  if kind=='wing':continue
  v=p.PCB_VIA(b);v.SetPosition(pt(x,y));v.SetWidth(MM(w));v.SetDrill(MM(d));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));v.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,REV+'/via/'+str((x,y))))));b.Add(v)
  # Suppress automatic via-land mask circles. The single explicit source
  # opening exposes every joint hole; this is NOT a physical tent/closure.
  v.SetFrontTentingMode(1);v.SetBackTentingMode(2)
 # Broad source rails accommodate side vias. No RF signal copper changes.
 for g in list(b.GetDrawings()):
  if g.GetLayer()==p.F_Cu and g.GetShape()==p.SHAPE_T_RECT and abs(p.ToMM(g.GetStart().x)-110.4)<.001 and abs(p.ToMM(g.GetStart().y)-51.9)<.001:b.Remove(g);REMOVED.append(g)
 rect(b,p.F_Cu,TOP_RECTS[0],'source-rails',b.FindNet('GND'))
 fs={f.GetReference():f for f in b.GetFootprints()};mask(fs['Q501'])
 lib=p.FootprintLoad(str(HW/'ARDF_2M.pretty'),'PD54008L_ST_GDS_5x5');mask(lib);p.FootprintSave(str(HW/'ARDF_2M.pretty'),lib)
 b.GetTitleBlock().SetRevision(REV)
 for g in b.GetDrawings():
  if isinstance(g,p.PCB_TEXT)and'M5B-E4'in g.GetText():g.SetText(g.GetText().replace('M5B-E4',REV))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 for f in HW.glob('*.kicad_sch'):f.write_text(f.read_text().replace('M5B-E4',REV))
 f=HW/'RF2M.electrical.json';s=f.read_text().replace('"revision": "M5B-E4"','"revision": "'+REV+'"').replace('THERMAL CANDIDATE / SOURCE-JOINT HOLD','SOURCE-JOINT EVALUATION CANDIDATE / PHYSICAL QUALIFICATION NOT_RUN');f.write_text(s)
 profile=json.loads((HW/'review/M5B-E4/JLCPCB-standard-profile.json').read_text());profile['revision']=REV;profile['retrieved']='2026-10-17';profile['E4R1_thermal_process']='16 intentionally open source vias;20 side and8 end vias outside source opening. No closure/fill guarantee. Stencil and initial joint qualification required.';profile['sources']['ST_PowerFLAT_assembly']='https://www.st.com/resource/en/application_note/an5046-printed-circuit-board-assembly-recommendations-for-stmicroelectronics-powerflat-packages-stmicroelectronics.pdf';save('JLCPCB-standard-profile.json',profile)
 save('implemented-geometry.json',dict(revision=REV,source_pad_mm=SOURCE,source_mask_opening_mm=SOLDER,paste_windows_mm=PASTE,source_vias=len(INNER),side_vias=len(SIDE),near_vias=len(NEAR),wing_vias=len(OUTER),total_thermal_vias=len(VIAS),via_specs=via_specs(),top_ground_rectangles_mm=TOP_RECTS,bottom_mask_window_mm=WINDOW,bar_mm=[15,44,10],sink='Fischer SK 81 100 SA',source_via_mode='EXPLICIT_MASK_OPENING_EXPOSES_HOLES_AUTOMATIC_VIA_LAND_OPENINGS_SUPPRESSED',guaranteed_closure=False,signal_copper_changes=False,purchased_electrical_changes=False))
 print('Implemented E4R1 hybrid:16 open joint +20 side +8 near +54 wing vias;5 paste windows, continuous2.1x5 opening')
if __name__=='__main__':main()
