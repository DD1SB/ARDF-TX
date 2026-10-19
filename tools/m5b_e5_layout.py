#!/usr/bin/python3
"""Native E4R1→compact floorplan, retaining the RF/source assembly rigid group."""
import argparse,math,collections,csv,copy
from m5b_e5_common import *
REMOVED=[]
def bbox(f):
 b=f.GetBoundingBox(False,False);return[round(p.ToMM(v),6)for v in[b.GetX(),b.GetY(),b.GetRight(),b.GetBottom()]]
def displacement(ref,part,x,y):
 special={'H1':(25,25),'H2':(165,25),'H3':(165,125),'H4':(25,125),'J101':(27,80),'J301':(35,120),'J302':(61,103),'C305':(59,126)}
 if ref in special:return(special[ref][0]-x,special[ref][1]-y,'corner_or_connector')
 g=part.get('group','');sheet=part.get('sheet','')
 if ref in['H5','H6','J501','R651','R952','TP951','TP401','C635']or g in['pa','pa_match','output_filter','source_filter','driver','bias','transmission_line']or ref in['TP601','TP602','TP603','TP604','C941']:
  return(DX,DY,'rigid_RF_thermal')
 if (sheet=='01_interface_source'or g=='source'or ref in['U103','Y101','C101','C102','C103'])and y<74:return(-12,0,'synthesizer')
 if y<74:
  if x>=130 or g=='modulator':return(-15,0,'upper_AM_pass')
  if 102<=x<=122 and y>=64:return(DX,0,'RF_local_test')
  return(-8,-5,'top_rail_logic')
 if sheet.startswith('07_')or g=='training':
  if y>=110:return(-25,-24,'rigid_training_RF')
  return(-8,-7,'training_logic')if x<100 else(-9,-10,'training_control')
 if sheet.startswith('05_')or g in['am','modulator']:return(-9,-10,'lower_AM_control')
 if sheet.startswith('08_')and x>=110:return(-16,-20,'protection')
 if sheet.startswith('04_')and g=='converter'or ref=='C960':return(-1,-20,'boost_supply')
 if g=='driver_supply'or sheet.startswith('04_'):return(-8,-20,'driver_and_boost_supply')
 if ref=='C961':return(-2,-17,'input_buck_supply')
 if sheet.startswith('03_'):
  return(-2,-17,'input_buck_supply')
 if y>=110:
  if x<95:return(-3,-20,'lower_input_controls')
  return(-8,-20,'lower_driver_controls')
 if g in['interlock','interface','decoupling','passive','test','power','supply_isolation']or 74<=y<110:
  return(0 if x<50 else -8,-7,'interlocks')
 return(-8,-5,'other_control')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');a=parser.parse_args();guard();work=OUT/'development';work.mkdir(exist_ok=True)
 old=work/'E4R1-baseline.kicad_pcb';old.write_bytes(gitfile('hardware/2m/RF2M.kicad_pcb'));old.with_suffix('.kicad_pro').write_bytes(gitfile('hardware/2m/RF2M.kicad_pro'))
 b=p.LoadBoard(str(old));manifest=json.loads(gitfile('hardware/2m/RF2M.electrical.json'));parts={a['ref']:a for a in manifest['parts']};fs={f.GetReference():f for f in b.GetFootprints()};moves={};initial=[]
 for r,f in fs.items():
  x,y=xy(f.GetPosition());dx,dy,group=displacement(r,parts.get(r,{}),x,y);moves[r]=(dx,dy,group);initial.append(dict(ref=r,before_mm=[x,y],before_bbox_mm=bbox(f),rotation_deg=f.GetOrientationDegrees(),group=group,shift_mm=[dx,dy],after_mm=[x+dx,y+dy],MPN=parts.get(r,{}).get('mpn'),footprint=f.GetFPIDAsString()))
 save('initial-placement-and-impact.json',dict(baseline=BASE,parts=initial,tracks=len(list(b.GetTracks())),zones=[dict(uuid=z.m_Uuid.AsString(),net=z.GetNetname(),layers=z.GetLayerSet().FmtBin(),rule_area=z.GetIsRuleArea())for z in b.Zones()],rigid_group='RF matching/filter/PA/source joint and H5/H6 translate(-20,0)mm; no rotation. All others initial placement targets subject to clearance repair.'))
 if not a.apply:print('Extracted E4R1 source and proposed block impact',len(initial));return
 # Tracks wholly inside the RF strip stay a rigid assembly; other routing is
 # removed for deliberate compact routing. Original routes stay in baseline.
 keep=[]
 rfrefs={r for r,d in moves.items()if d[2]=='rigid_RF_thermal'}
 rfnets={n for r in rfrefs for n in parts.get(r,{}).get('pins',{}).values()}
 for t in list(b.GetTracks()):
  xx,yy=xy(t.GetPosition())if isinstance(t,p.PCB_VIA)else xy(t.GetStart());xe,ye=(xx,yy)if isinstance(t,p.PCB_VIA)else xy(t.GetEnd())
  isRF=48<=xx<=193 and 28<=yy<=73 and 48<=xe<=193 and 28<=ye<=73
  # Preserve the RF strip including thermal via/return features, excluding
  # unrelated top power devices; later native DRC identifies any local clash.
  if isRF and t.GetNetname()in rfnets and not(t.GetNetname()=='V3V3'and yy<44)and not(t.GetNetname()in['VMOD','MOD_SINK','MOD_BASE','VPA','AF_REF','LEVEL_REF']and (xx>126 or xe>126)):
   t.Move(pt(DX,DY));t.SetLocked(True);keep.append(t)
  else:b.Remove(t);REMOVED.append(t)
 for r,f in fs.items():
  f.Move(pt(*moves[r][:2]))
  if r=='J302':f.SetOrientationDegrees(90)
  f.SetLocked(moves[r][2]=='rigid_RF_thermal')
 # Deliberate ground-copper/mask/mechanical features belonging to the PA.
 for g in list(b.GetDrawings()):
  layer=g.GetLayer()
  if layer==p.Edge_Cuts:b.Remove(g);REMOVED.append(g);continue
  if isinstance(g,p.PCB_TEXT):
   text=g.GetText().replace('M5B-E4R1',REV);g.SetText(text)
   x,y=xy(g.GetPosition());dx,dy,_=displacement('',{},x,y);g.Move(pt(dx,dy))
   if 'ARDF-TX RF2M' in text:g.SetPosition(pt(95,22))
   if 'REVIEW ONLY'in text:g.SetPosition(pt(95,128))
   if '2S BOOST OR' in text:g.SetPosition(pt(70,127))
   if 'NORMAL 50R'in text:g.SetPosition(pt(154,65))
   if 'TRAIN' in text and 'MMCX'in text:g.SetPosition(pt(153,126))
   continue
  if layer in[p.F_Cu,p.B_Cu,p.F_Mask,p.B_Mask,p.F_Fab,p.B_Fab]:g.Move(pt(DX,DY))
 # Native mechanical keepouts follow thermal group; fills are recreated to the
 # target outline. Preserve original thermal relief settings/minimum thickness.
 for z in list(b.Zones()):
  if z.GetIsRuleArea():z.Move(pt(DX,DY));continue
  poly=z.Outline();poly.RemoveAllContours();poly.NewOutline()
  for xx,yy in[(20.5,20.5),(169.5,20.5),(169.5,129.5),(20.5,129.5)]:poly.Append(MM(xx),MM(yy))
 for aa,zz in[((20,20),(170,20)),((170,20),(170,130)),((170,130),(20,130)),((20,130),(20,20))]:
  g=p.PCB_SHAPE(b);g.SetShape(p.SHAPE_T_SEGMENT);g.SetStart(pt(*aa));g.SetEnd(pt(*zz));g.SetLayer(p.Edge_Cuts);g.SetWidth(MM(.05));b.Add(g)
 tb=b.GetTitleBlock();tb.SetRevision(REV);tb.SetDate(DATE);tb.SetComment(0,'COMPACT EVALUATION / PHYSICAL QUALIFICATION NOT_RUN');b.SetTitleBlock(tb);b.SetFileName(str(HW/'RF2M.kicad_pcb'));p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 for f in HW.glob('*.kicad_sch'):f.write_text(f.read_text().replace('M5B-E4R1',REV).replace('2026-10-17',DATE))
 manifest.update(revision=REV,date=DATE,status='COMPACT EVALUATION CANDIDATE / NOT RELEASED / PHYSICAL NOT_RUN');(HW/'RF2M.electrical.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (work/'rigid-track-UUIDs.json').write_text(json.dumps([t.m_Uuid.AsString()for t in keep],indent=2)+'\n')
 save('floorplan.json',dict(status='INITIAL_PLACEMENT_NOT_ROUTED',moved_components=initial,preserved_RF_tracks_vias=len(keep),new_outline_mm=[150,110],common_holes_mm=[[5,5],[145,5],[145,105],[5,105]],heatsink_native_envelope_mm=[42,20,142,120],bar_native_envelope_mm=[84.5,28,99.5,72],PA_native_mm=[92,55]))
 print('Native compact floorplan applied;',len(keep),'RF/ground tracks-vias retained; all parts retained')
if __name__=='__main__':main()
