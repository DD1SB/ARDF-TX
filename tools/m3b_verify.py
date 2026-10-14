#!/usr/bin/python3
"""Current PCB/netlist/R1 logic regression, package and artifact consistency."""
import csv,hashlib,json,os,sys
from pathlib import Path
from collections import Counter
import xml.etree.ElementTree as ET
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/80m';REVISION=json.loads((HW/'RF80.electrical.json').read_text())['revision'];D=HW/'review'/REVISION;PREFIX='M3B_E2'if REVISION=='M3B-E2'else'M3B'
def main():
 m=json.loads((HW/'RF80.electrical.json').read_text());parts={x['ref']:x for x in m['parts']if not x['ref'].startswith('#')};b=p.LoadBoard(str(HW/'RF80.kicad_pcb'));fp={f.GetReference():f for f in b.GetFootprints()};xml=ET.parse(D/'RF80.xml')
 expected={}
 for n in xml.findall('./nets/net'):
  for nd in n.findall('node'):expected[(nd.attrib['ref'],nd.attrib['pin'])]=n.attrib['name'].removeprefix('/')
 assert set(parts)==set(fp)-{'H1','H2','H3','H4'}
 checked=0
 for r,f in fp.items():
  if r not in parts:continue
  assert str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())==parts[r]['footprint'],(r,'FPID')
  for d in f.Pads():
   target=expected.get((r,d.GetNumber()),'');assert d.GetNetname()==target,(r,d.GetNumber(),d.GetNetname(),target);checked+=1
 for name in ('DRC','ERC'):
  j=json.loads((D/(name+'.json')).read_text());violations=j.get('violations',[v for s in j.get('sheets',[])for v in s.get('violations',[])]);assert not violations,(name,violations)
  if name=='DRC':assert not j['unconnected_items']and not j['schematic_parity']
 os.environ['RF80_NETLIST']=str(D/'RF80.xml')
 from m3a_r1_logic import verify
 lr=verify();assert lr['truth_cases']==256 and len(lr['state_scenarios'])==31 and len(lr['timing_corners'])==16
 (ROOT/('docs/'+PREFIX+'_LOGIC_RESULTS.json')).write_text(json.dumps(dict(evaluation_revision=REVISION,netlist=str((D/'RF80.xml').relative_to(ROOT)),retained_R1_contract=lr),indent=2)+'\n')
 tracks=[t for t in b.GetTracks()if not isinstance(t,p.PCB_VIA)];vias=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)]
 assert all(t.GetWidth()>=p.FromMM(.15)for t in tracks)
 assert all(v.GetDrill()>=p.FromMM(.3)and v.GetWidth(p.F_Cu)>=p.FromMM(.6)for v in vias)
 for v in vias:
  for f in fp.values():
   for d in f.Pads():
    if d.GetAttribute()==p.PAD_ATTRIB_SMD:assert not d.HitTest(v.GetPosition()),('Via in SMD pad',f.GetReference(),d.GetNumber())
 # Independent manufacturer physical-pin maps, not symbol graphic order.
 maker={'U101':{'1':'V3V3','2':'XA','3':'XB','4':'SCL','5':'SDA','6':'CLK_FOX','7':'V3V3','8':'GND','10':'CLK_PA'},'U401':{'1':'VDRV','3':'GATE_DRV','4':'GND','5':'PA_INB','6':'CLK_PA'},'U301':{'1':'GND','2':'SW_PA','3':'VIN_PA','4':'FB_PA','5':'PA_PERMIT','6':'BOOT_PA'},'U302':{'1':'VPA','2':'GND','3':'PA_PERMIT','4':'CT_PA','5':'QOD_PA','6':'VPA_ISO'},'U313':{'1':'I_PA_RAW','2':'GND','3':'SENSE_PLUS','4':'SENSE_MINUS','5':'V3V3'},'Q402':{'1':'GATE_PA','2':'DRAIN_PA','3':'GND'},'Q403':{'1':'SHAPE_BASE','2':'VPA_SHAPED','3':'VPA_LOAD'},'U311':{'1':'VREF_2V5','2':'VREF_2V5','3':'GND'},'U202':{'13':'LEASE_OK','12':'BUS_HOLDOFF_N'},'U224':{'1':'HEALTH_N','9':'ARM'},'U501':{'7':'GND','14':'VFOX','3':'FOX_GATE1','6':'FOX_GATE2','8':'FOX_GATE3'},'J502':{'1':'RF_FOX','2':'GND','3':'FOX_ID'}}
 for ref,pinmap in maker.items():
  for pin,net in pinmap.items():assert expected[(ref,pin)]==net,(ref,pin,net)
 for q in parts.values():
  if q['group']=='fox':assert not set(q['pins'].values())&{'DRAIN_PA','GATE_PA','VPA_SHAPED','RF_NORMAL'}
 assert b.GetCopperLayerCount()==2
 assert all(abs(p.ToMM(q.GetDrillSize().x)-1.3)<.001 for q in fp['Q402'].Pads())
 assert all(abs(p.ToMM(q.GetDrillSize().x)-1.2)<.001 for q in fp['J101'].Pads())
 assert fp['F301'].GetFPID().GetLibItemName()=='Fuse_467_0603'
 assert len(list(b.Zones()))==2
 pads=[(r,f,parts[r])for r,f in fp.items()if r.startswith('TP')]
 with(D/'probe-map.csv').open('w')as out:
  w=csv.writer(out,lineterminator='\n');w.writerow(['reference','net','x_mm_absolute','y_mm_absolute','population','probe_caution'])
  for r,f,q in sorted(pads):w.writerow([r,q['pins']['1'],p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y),q['population'],'DRAIN: rated <=1pF active/differential'if q['pins']['1']=='DRAIN_PA'else 'Reset/clock: <=1pF active; local ground spring'])
 with(D/'population-map.csv').open('w')as out:
  w=csv.writer(out,lineterminator='\n');w.writerow(['reference','value','MPN','footprint','population','full_fit','fox_fit','x_mm_absolute','y_mm_absolute','rotation_deg'])
  for r,f in sorted(fp.items()):
   q=parts.get(r)
   if q:w.writerow([r,q['value'],q['mpn'],q['footprint'],q['population'],q['population']in('BOTH','NORMAL'),q['population']in('BOTH','FOX'),p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y),f.GetOrientationDegrees()])
 nets={}
 for n in ('GATE_DRV','GATE_PA','DRAIN_PA','VDRV','RF_NORMAL','RF_FOX','CLK_PA','CLK_FOX','SW_PA','VPA_ISO','VPA_LOAD'):
  ts=[t for t in tracks if t.GetNetname()==n];nets[n]=dict(track_length_mm=round(sum(p.ToMM(t.GetLength())for t in ts),3),widths_mm=sorted(set(round(p.ToMM(t.GetWidth()),3)for t in ts)),layers=sorted(set(b.GetLayerName(t.GetLayer())for t in ts)))
 models={}
 for f in fp.values():
  for model in f.Models():
   fn=model.m_Filename.replace('${KIPRJMOD}',str(HW)).replace('${KICAD10_3DMODEL_DIR}','/usr/share/kicad/3dmodels');assert Path(fn).exists(),fn;models[f.GetReference()]=model.m_Filename
 report=dict(date=m['date'],revision=REVISION,baseline_commit='55a5b3f',status='CAD AND IDEAL LOGIC CHECKS PASS; ALL PHYSICAL GATES NOT_RUN',manifest_refs=len(m['parts']),electrical_footprints=len(parts),mounting_holes=4,footprints=len(fp),physical_pad_memberships_checked=checked,manufacturer_pinmaps_checked=sorted(maker),test_pads=len(pads),track_segments=len(tracks),through_vias=len(vias),zones=2,board_mm=[210,160,1.6],copper_layers=2,track_width_histogram=dict(sorted(Counter(round(p.ToMM(t.GetWidth()),3)for t in tracks).items())),critical_net_geometry=nets,models_resolve=len(models),ERC_violations=0,DRC_violations=0,unrouted=0,schematic_parity=0,logic_truth_cases=256,state_scenarios=31,timing_corners=16,not_proved=['Physical propagation/reset recovery/metastability','Driver OV withdrawal timing and capacitor hot ESR','Cable/source transient envelope','RF power/efficiency/emissions/CW/thermal/antenna/isolation','Incoming exact component mechanical fit and stock'])
 (ROOT/('docs/'+PREFIX+'_CHECK_RESULTS.json')).write_text(json.dumps(report,indent=2)+'\n')
 print('PASS M3B:',checked,'pad net memberships;',len(fp),'footprints;',len(vias),'vias; ERC/DRC/parity/unrouted0; R1 256/31/16 retained')
if __name__=='__main__':main()
