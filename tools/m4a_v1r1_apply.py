"""Apply reviewed local land/marking edits once, from preserved M4A-V1 sources.
Not a verifier; never run to restore/reset a later manually edited revision.
"""
import json,math
import pcbnew as p
from m3_80m_design import parse,dump,child,children
from m4a_v1r1_common import *
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def main():
 frozen();board=P/(NAME+'.kicad_pcb');b=p.LoadBoard(str(board));assert b.GetTitleBlock().GetRevision()=='M4A-V1','Refuse to overwrite a later native revision'
 m=json.loads((P/(NAME+'.electrical.json')).read_text());parts={x['ref']:x for x in m['parts']};fs={f.GetReference():f for f in b.GetFootprints()}
 changes=[]
 notes={
 'J101':'V1R1:1.40mm ordinary finished PTH,1.90mm lands. Maker square0.64+/-0.15mm; max diagonal1.117mm, min finished1.32mm. No press-fit tolerance; inspect all16 contacts/key/cable pin1.',
 'J301':'V1R1:1.90mm ordinary finished PTH. Maker1.14mm square, tolerance not published; incoming assembly envelope<=1.19mm square is an engineering screening limit. Separate fused pack input1VBAT/2GND.',
 'J401':'V1R1:1.30mm ordinary finished PTH. Maker0.5x0.9mm pins; no published tolerance, incoming engineering envelope<=0.55x0.95mm.1RF_NORMAL/2GND; hand solder, strain relieve coax.',
 'J502':'V1R1:1.30mm ordinary finished PTH,1.90x1.95mm lands. Maker0.64mm square without lead tolerance; engineering incoming ceiling0.79mm square.1RF_FOX/2GND/3FOX_ID. Same package/key; no press-fit.',
 'Q402':'V1R1:Vishay IRF610PbF-BE3, exact Siliconix92506 drawing.1G/2D/3S,tabD;1.40mm ordinary finished holes,1.905x2.0mm lands. External b/c maxima0.91x0.61mm; larger generic diode TO220 drawing not used as identity. Insulate sink/thermocouple; physical hot SOA NOT_RUN.',
 'Q403':'V1R1:ST BD140 SOT32 drawing0016114E,1B/2C/3E;180deg/illustrated face+PCB Y retained.1.40mm ordinary finished holes/1.90mm lands. Max lead0.88x0.63mm.2mm body stand-off; conductive case is collector. No generic-vendor substitution.'}
 for r,(fid,drill,size) in ALIASES.items():
  f=fs[r];oldfid=parts[r]['footprint'];old=next(a for a in f.Pads() if a.GetNumber());changes.append(dict(ref=r,old_footprint=oldfid,new_footprint=fid,old_hole_mm=p.ToMM(old.GetDrillSize().x),new_hole_mm=drill,pad_centres='UNCHANGED',nets='UNCHANGED'))
  lib,name=oldfid.split(':');folder=P/(lib+'.pretty') if lib=='ARDF_TX' else Path('/usr/share/kicad/footprints')/(lib+'.pretty');fp=p.FootprintLoad(str(folder),name);assert fp
  fp.SetFPID(p.LIB_ID('ARDF_TX',fid.split(':')[1]));fp.SetLibDescription(notes[r])
  for a in list(f.Pads())+list(fp.Pads()):
   if a.GetDrillSize().x:a.SetDrillSize(pt(drill,drill))
   if size:a.SetSize(pt(*size))
  for g in list(fp.GraphicalItems()):
   if g.GetLayer()==p.F_SilkS:g.SetLayer(p.F_Fab)
  p.FootprintSave(str(P/'ARDF_TX.pretty'),fp)
  f.SetFPID(p.LIB_ID('ARDF_TX',fid.split(':')[1]));parts[r]['footprint']=fid;parts[r]['note']=notes[r]
  for field in f.GetFields():
   if field.GetName() in ['Note','Engineering_Note','Design_Note']:field.SetText(notes[r])
 for path in P.glob('*.kicad_sch'):
  s=parse(path.read_text());tb=child(s,'title_block');child(tb,'rev')[1]=REV;child(tb,'date')[1]=DATE
  for sym in children(s,'symbol'):
   props={z[1]:z for z in children(sym,'property')};r=props.get('Reference',[None,None,''])[2]
   if r in ALIASES:
    props['Footprint'][2]=ALIASES[r][0]
    for k in ['Note','Engineering_Note','Design_Note']:
     if k in props:props[k][2]=notes[r]
  path.write_text(dump(s)+'\n')
 m.update(revision=REV,date=DATE,scope='M4A-V1 local standard-PTH and legend closure; no circuit/value/population changes');(P/(NAME+'.electrical.json')).write_text(json.dumps(m,indent=2)+'\n')
 # Small component outlines/references remain authoritative on assembly artwork.
 moved=0
 for f in b.GetFootprints():
  for g in list(f.GraphicalItems())+list(f.GetFields()):
   if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:g.SetLayer(p.F_Fab if g.GetLayer()==p.F_SilkS else p.B_Fab);moved+=1
 for g in b.GetDrawings():
  if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:g.SetLayer(p.F_Fab if g.GetLayer()==p.F_SilkS else p.B_Fab);moved+=1
 # Position essential marks outside actual component/pad envelopes. No routing moves.
 boxes=[f.GetBoundingBox(False,False) for f in b.GetFootprints() if not f.GetReference().startswith('TP')]
 masks=[]
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.IsOnLayer(p.F_Mask):masks.append(a.GetBoundingBox())
 occupied=[];labels=[]
 def place(text,x,y,limit=12,height=1.0):
  t=p.PCB_TEXT(b);t.SetText(text);t.SetLayer(p.F_SilkS);t.SetTextSize(pt(height,height));t.SetTextThickness(p.FromMM(.15));t.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
  candidates=[]
  for dx in range(-int(limit*2),int(limit*2)+1):
   for dy in range(-int(limit*2),int(limit*2)+1):candidates.append((dx*dx+dy*dy,x+dx*.5,y+dy*.5))
  for _,xx,yy in sorted(candidates):
   t.SetPosition(pt(xx,yy));q=t.GetBoundingBox();q.Inflate(p.FromMM(.2))
   if q.GetLeft()<p.FromMM(20.5)or q.GetRight()>p.FromMM(169.5)or q.GetTop()<p.FromMM(20.5)or q.GetBottom()>p.FromMM(129.5):continue
   if any(q.Intersects(z)for z in boxes+masks+occupied):continue
   b.Add(t);occupied.append(q);labels.append(dict(text=text,xy_mm=[xx,yy],height_mm=height,stroke_mm=.15));return
  raise RuntimeError(('No safe essential label location',text))
 place('RF80 V1R1 / EVAL - NOT RELEASED',99,21.6,3,1.2)
 place('FULL:4S  FOX:2S',52,22.5,4)
 for text,r,dx,dy in [('J101 CTRL 3V3','J101',10,9),('J301 1=BAT+ 2=GND','J301',2,-5),('J401 NORMAL RF','J401',0,7),('J502 FOX 10mW','J502',0,6),('FOX: R228 R348 R349','R348',-10,53),('INSULATE DRAIN TAB','Q402',5,-5)]:
  f=fs[r];place(text,p.ToMM(f.GetPosition().x)+dx,p.ToMM(f.GetPosition().y)+dy,12)
 for r in ['J101','J301','J401','J502']:
  a=next(a for a in fs[r].Pads()if a.GetNumber()=='1');place(r+'-1',p.ToMM(a.GetPosition().x)-4,p.ToMM(a.GetPosition().y)-3,7)
 for r in sorted(KEEP):
  f=fs[r];place(r,p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)+2.5,7)
 tb=b.GetTitleBlock();tb.SetRevision(REV);tb.SetDate(DATE);tb.SetTitle('RF80 V1R1 - STANDARD JLCPCB EVALUATION CANDIDATE');tb.SetComment(0,'Independent review only; physical tests NOT_RUN');b.SetTitleBlock(tb)
 p.SaveBoard(str(board),b)
 # Explicit nominal metadata, not a custom dielectric procurement constraint.
 s=parse(board.read_text());setup=child(s,'setup')
 if not child(setup,'stackup'):
  from m3_80m_design import Atom
  setup.append(parse('(stackup (layer "F.Silkscreen" (type "Top Silk Screen") (color "White")) (layer "F.Mask" (type "Top Solder Mask") (color "Green") (thickness 0.01) (epsilon_r 3.8) (loss_tangent 0)) (layer "F.Cu" (type "copper") (thickness 0.035)) (layer "dielectric 1" (type "core") (thickness 1.53) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02)) (layer "B.Cu" (type "copper") (thickness 0.035)) (layer "B.Mask" (type "Bottom Solder Mask") (color "Green") (thickness 0.01) (epsilon_r 3.8) (loss_tangent 0)) (layer "B.Silkscreen" (type "Bottom Silk Screen") (color "White")) (copper_finish "Lead-free HASL") (dielectric_constraints no))'))
  board.write_text(dump(s)+'\n')
 pro=P/(NAME+'.kicad_pro');a=json.loads(pro.read_text());ds=a['board']['design_settings'];ds['defaults'].update(silk_line_width=.15,silk_text_size_h=1.0,silk_text_size_v=1.0,silk_text_thickness=.15);ds['rules']['min_silk_clearance']=.15;pro.write_text(json.dumps(a,indent=2)+'\n')
 save('applied-local-changes.json',dict(baseline=BASE,land_changes=changes,nonessential_silk_items_moved_to_fab=moved,essential_labels=labels,trace_via_placement_changes='NONE',component_MPN_changes='NONE'))
 print('Applied local PTH/legend changes',len(changes),'landings,',len(labels),'marks')
if __name__=='__main__':main()
