#!/usr/bin/python3
"""Targeted source-ground/thermal artwork, no RF signal or package-pad changes."""
import pcbnew as p,json,uuid
from m5b_e4_common import *
MM=p.FromMM
REMOVED=[]
def point(x,y):return p.VECTOR2I(MM(x),MM(y))
def uid(label):return p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'ARDF-TX/M5B-E4/'+label)))
def rect(parent,layer,coords,label,net=None,filled=True):
 g=p.PCB_SHAPE(parent)
 g.SetShape(p.SHAPE_T_RECT);g.SetStart(point(*coords[:2]));g.SetEnd(point(*coords[2:]));g.SetLayer(layer);g.SetFilled(filled);g.SetWidth(0 if filled else MM(.1));g.SetUuid(uid(label))
 if net is not None:g.SetNet(net)
 parent.Add(g);return g
def gaps(centers,lo,hi):
 ends=[lo]+[v+d for v in centers for d in[-.225,.225]]+[hi]
 return[(max(lo,a),min(hi,b))for a,b in zip(ends[::2],ends[1::2])if min(hi,b)>max(lo,a)]
def mask(f):
 for g in list(f.GraphicalItems()):
  if g.GetLayer()in[p.F_Mask,p.F_Paste]:f.Remove(g);REMOVED.append(g)
 ox,oy=p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)
 rects=[(a,-2.5,b,2.5)for a,b in gaps([-1.2,-.6,0,.6,1.2],-1.35,1.35)]
 rects +=[(-1.35,a,1.35,b)for a,b in gaps([-2.1+.6*r for r in range(8)],-2.5,2.5)]
 for layer in[p.F_Mask,p.F_Paste]:
  for i,r in enumerate(rects):rect(f,layer,(r[0]+ox,r[1]+oy,r[2]+ox,r[3]+oy),'source-grid/'+str(layer)+'/'+str(i))
 f.SetLibDescription('ST PD54008L-E Rev2 p13 G/D0.5x5/S2.7x5; E4 5x8 ordinary source vias, 0.45mm mask islands; assembly qualification OPEN')
 return rects
def main():
 guard();fn=HW/'RF2M.kicad_pcb';base=OUT/'development/E3-native.kicad_pcb';base.parent.mkdir(exist_ok=True);base.write_bytes(gitfile('hardware/2m/RF2M.kicad_pcb'))
 base.with_suffix('.kicad_pro').write_bytes(gitfile('hardware/2m/RF2M.kicad_pro'))
 (HW/'RF2M.kicad_pro').write_bytes(gitfile('hardware/2m/RF2M.kicad_pro'))
 b=p.LoadBoard(str(base));fs={f.GetReference():f for f in b.GetFootprints()}
 # Work only from the immutable E3 source geometry. Fail rather than accumulating edits.
 assert b.GetTitleBlock().GetRevision()=='M5B-E3','Design action expects pristine E3 native board'
 existing=sorted([v for v in b.GetTracks()if isinstance(v,p.PCB_VIA)and 110.5<p.ToMM(v.GetPosition().x)<113.5 and 52.7<p.ToMM(v.GetPosition().y)<57.3],key=lambda v:(v.GetPosition().x,v.GetPosition().y))
 assert len(existing)==32
 for i,(x,y)in enumerate(VIAS):
  v=existing[i]if i<len(existing)else p.PCB_VIA(b);v.SetPosition(point(x,y));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu)
  outer=i>=len(INNER)+len(NEAR);v.SetWidth(MM(1.1 if outer else .8));v.SetDrill(MM(.5 if outer else .3));v.SetNet(b.FindNet('GND'))
  if i>=len(existing):v.SetUuid(uid('thermal-via/'+str(i)));b.Add(v)
  v.SetFrontTentingMode(1);v.SetBackTentingMode(2)
 for i,r in enumerate(TOP_RECTS):rect(b,p.F_Cu,r,'top-source-wing/'+str(i),b.FindNet('GND'))
 # Expand only the underside mask opening, retaining the original grounded RF return.
 for g in list(b.GetDrawings()):
  if g.GetLayer()==p.B_Mask and g.GetShape()==p.SHAPE_T_RECT:
   bb=g.GetBoundingBox()
   if 104<p.ToMM(bb.GetLeft())<120 and 48<p.ToMM(bb.GetTop())<62:b.Remove(g);REMOVED.append(g)
 rect(b,p.B_Mask,WINDOW,'bottom-contact-window')
 rect(b,p.B_Fab,BAR,'bar-envelope',filled=False)
 rect(b,p.B_Fab,(62,20,162,120),'sink-envelope',filled=False)
 rect(b,p.B_Fab,WINDOW,'contact-envelope',filled=False)
 # Expose an existing ground-plane annulus for a metal M3 washer. No copper
 # is added and no signal is rerouted. Continuity is separately checked.
 rect(b,p.F_Mask,(111.,71.8,113.,72.3),'H6-ground-washer-mask')
 for ref in ['H5','H6']:fs[ref].Reference().SetPosition(point(119,p.ToMM(fs[ref].GetPosition().y)))
 for g in b.GetDrawings():
  if isinstance(g,p.PCB_TEXT)and'M5B-E3'in g.GetText():g.SetText(g.GetText().replace('M5B-E3','M5B-E4'))
 b.GetTitleBlock().SetRevision(REV)
 rectangles=mask(fs['Q501'])
 lib=p.FootprintLoad(str(HW/'ARDF_2M.pretty'),'PD54008L_ST_GDS_5x5');mask(lib);p.FootprintSave(str(HW/'ARDF_2M.pretty'),lib)
 # Envelope only: actual sink fin cross-section remains the manufacturer drawing.
 model=p.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/E4_PA_cooling_envelope.wrl';fs['H5'].Models().push_back(model)
 p.SaveBoard(str(fn),b)
 for fn in HW.glob('*.kicad_sch'):fn.write_text(fn.read_text().replace('M5B-E3','M5B-E4'))
 manifest=HW/'RF2M.electrical.json';text=manifest.read_text();text=text.replace('"revision": "M5B-E3"','"revision": "M5B-E4"').replace('INTEGRATED EVALUATION / ALL HARDWARE TESTS NOT_RUN','THERMAL CANDIDATE / SOURCE-JOINT HOLD / ALL HARDWARE TESTS NOT_RUN');manifest.write_text(text)
 save('implemented-geometry.json',dict(revision=REV,source_vias=len(INNER),near_vias=len(NEAR),wing_vias=len(OUTER),total_thermal_vias=len(VIAS),top_ground_rectangles_mm=TOP_RECTS,bottom_mask_window_mm=WINDOW,stock_bar_mm=[15,44,10],stock_bar_bounds_mm=BAR,sink_bounds_mm=[62,20,162,120],sink_height_mm=15,mounting_holes_mm=[[112,32],[112,68]],source_mask_island_mm=.45,source_mask_open_rectangles_local_mm=rectangles,source_paste='Same grid; 0.15mm minimum aperture, 0.10mm manual stencil starting thickness. No via plugging/fill credit.',source_assembly='OPEN: ordinary LPI tents and HASL do not guarantee closed holes or void-free source joint.',signal_copper_changes=False,purchased_electrical_changes=False))
 print('Implemented E4:40 source +10 near +54 external vias, local GND wings/mask, unchanged signal copper')
if __name__=='__main__':main()
