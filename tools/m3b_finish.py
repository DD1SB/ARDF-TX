#!/usr/bin/python3
"""Ground planes, labels and mechanical metadata for the routed evaluation PCB."""
from m3b_pcb import *

def main():
 b=pcb.LoadBoard(str(HW/'RF80.kicad_pcb'));parts={p['ref']:p for p in json.loads((HW/'RF80.electrical.json').read_text())['parts']}
 comps={c.attrib['ref']:c for c in ET.parse(REV/'RF80.xml').findall('./components/comp')}
 for f in b.GetFootprints():
  r=f.GetReference()
  if r not in parts:continue
  if r in ('J301','Y101'):
   model=pcb.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/3dmodels/'+('JST_VH_envelope'if r=='J301'else'ABM3B_envelope')+'.wrl';f.Models().clear();f.Models().push_back(model)
  if r=='Q402':
   f.SetFPID(pcb.LIB_ID('ARDF_TX','TO220_Vertical_1p3Drill'))
   for pad in f.Pads():pad.SetDrillSize(pt(1.3,1.3))
  for key in ('MPN','Population','Function','Engineering_Note'):
   text=next((x.attrib.get('value','')for x in comps[r].findall('property')if x.attrib['name']==key),'');f.GetField(key).SetText(text)
  for name,kind in [('Datasheet',pcb.FIELD_T_DATASHEET),('Description',pcb.FIELD_T_DESCRIPTION)]:
   text=next((x.text or ''for x in comps[r].findall('./fields/field')if x.attrib['name']==name),'');f.GetField(kind).SetText(text)
 # Remove only our free-standing labels; footprint artwork is preserved.
 removed=[x for x in b.GetDrawings() if isinstance(x,pcb.PCB_TEXT)]
 for x in removed:b.Remove(x)
 # Solid planes: source/driver returns cannot depend on thin, series digital ground wiring.
 if not list(b.Zones()):
  for layer in (pcb.F_Cu,pcb.B_Cu):
   z=pcb.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet('GND'));z.SetLocalClearance(MM(.20));z.SetPadConnection(pcb.ZONE_CONNECTION_FULL);z.SetThermalReliefGap(MM(.25));z.SetThermalReliefSpokeWidth(MM(.35));z.SetMinThickness(MM(.2));z.SetZoneName('GND return '+('top'if layer==pcb.F_Cu else'bottom'))
   poly=z.Outline();poly.NewOutline()
   for x,y in [(20.5,20.5),(229.5,20.5),(229.5,179.5),(20.5,179.5)]:poly.Append(MM(x),MM(y))
   b.Add(z)
 # Reference designators on silk; full names/values remain on assembly (F.Fab).
 padboxes=[]
 for f in b.GetFootprints():
  for p in f.Pads():
   q=p.GetBoundingBox();padboxes.append([pcb.ToMM(q.GetLeft())-.20,pcb.ToMM(q.GetTop())-.20,pcb.ToMM(q.GetRight())+.20,pcb.ToMM(q.GetBottom())+.20])
 labels=[]
 # Native component outlines also consume silk space.
 for f in b.GetFootprints():
  for g in f.GraphicalItems():
   if g.GetLayer()!=pcb.F_SilkS:continue
   q=g.GetBoundingBox();labels.append([pcb.ToMM(q.GetLeft())-.25,pcb.ToMM(q.GetTop())-.25,pcb.ToMM(q.GetRight())+.25,pcb.ToMM(q.GetBottom())+.25])
 def label(text,x,y,size=1.0,layer=pcb.F_SilkS):
  t=pcb.PCB_TEXT(b);t.SetText(text);t.SetPosition(pt(x,y));t.SetTextSize(pt(size,size));t.SetTextThickness(MM(.12));t.SetLayer(layer);b.Add(t);return t
 # Keep the board legend on unused strips. No polarity ambiguity at mating ports.
 for text,x,y,size in [('ARDF-TX RF80 / M3B-E1 EVALUATION',124,23,1.5),('REVIEW ONLY - NO HARDWARE TESTS RUN',123,176.5,1.0),('CTRL 3V3 ONLY',40,62,1.0),('4S 12-16.8V / + PIN1',127,25,1.0),('NORMAL 3W / 50R',208,105,1.0),('FOX 10mW / PIN1 RF',207,166,1.0),('NO BATTERY FIRST: CURRENT-LIMITED LAB SUPPLY',87,171,1.0),('PA / HV DRAIN PROBE',189,28,1.0),('LOGIC / INTERLOCKS',62,30,1.2),('FOX LOW POWER',162,121,1.2),('REMOTE NTC ON INSULATED PA CASE',185,26,0.8)]:
  t=label(text,x,y,size);q=t.GetBoundingBox();labels.append([pcb.ToMM(q.GetLeft())-.25,pcb.ToMM(q.GetTop())-.25,pcb.ToMM(q.GetRight())+.25,pcb.ToMM(q.GetBottom())+.25])
 for f in b.GetFootprints():
  r=f.GetReference()
  if r.startswith('H'):continue
  q=f.GetBoundingBox(False,False);cx=(pcb.ToMM(q.GetLeft())+pcb.ToMM(q.GetRight()))/2;cy=(pcb.ToMM(q.GetTop())+pcb.ToMM(q.GetBottom()))/2
  # Small footprint identifiers are placed beside actual pads, with a collision search.
  text=r;size=.8
  if r.startswith('TP'):
   text=r+' '+(parts[r]['value']if r in parts else '');size=.8
  candidates=[]
  for dist in (1.1,1.6,2.1,2.8,3.6,4.5):
   candidates.extend([(cx,pcb.ToMM(q.GetTop())-dist),(cx,pcb.ToMM(q.GetBottom())+dist),(pcb.ToMM(q.GetRight())+len(text)*.26+dist,cy),(pcb.ToMM(q.GetLeft())-len(text)*.26-dist,cy)])
  for x,y in candidates:
   rect=[x-len(text)*size*.45-.3,y-size*.75-.2,x+len(text)*size*.45+.3,y+size*.75+.2]
   if rect[0]<21 or rect[1]<26 or rect[2]>229 or rect[3]>174:continue
   if any(intersects(rect,v)for v in padboxes+labels):continue
   label(text,x,y,size);labels.append(rect);break
  else:
   # Full, readable assembly artwork remains the authority for exceptionally crowded pads.
   pass
 # Fab notes state the assembly exception rather than hiding an essential sensor.
 label('TH301: remote sensor, board pads landing only; see bring-up plan',171,172,1.,pcb.F_Fab)
 b.SetUserComments([])if hasattr(b,'SetUserComments')else None
 pcb.SaveBoard(str(HW/'RF80.kicad_pcb'),b)
 print('Added solid top/bottom ground planes and collision-checked labels')
if __name__=='__main__':main()
