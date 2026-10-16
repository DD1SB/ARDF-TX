#!/usr/bin/python3
"""Generate the focused E2 audit from current native data; no procurement."""
import csv,json,math,collections,itertools,subprocess
from pathlib import Path
import pcbnew as p
from m5b_e2 import ROOT,HW,OUT,E1,BASE,sha,save,preserved
from m5b_footprints import microstrip

def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---'for _ in headers)+' |',*['| '+' | '.join(map(str,r))+' |'for r in rows]])+'\n'
def tab(name,rows):
 with(OUT/name).open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def doc(name,text):(ROOT/'docs'/('M5B_E2_'+name+'.md')).write_text(text)
def main():
 assert preserved()==json.loads((OUT/'preserved-baseline.json').read_text())
 drc=json.loads((OUT/'DRC.json').read_text());erc=json.loads((OUT/'ERC.json').read_text());v=json.loads((OUT/'verification.json').read_text());cost=json.loads((OUT/'costs.json').read_text());parts=json.loads((HW/'RF2M.electrical.json').read_text())['parts'];pr={x['ref']:x for x in parts}
 assert not drc['unconnected_items']and not drc['schematic_parity']
 assert len(drc['violations'])==11 and all(x['type']=='missing_courtyard'and x['severity']=='warning'for x in drc['violations'])
 assert not[v for s in erc['sheets']for v in s['violations']]
 pro=json.loads((HW/'RF2M.kicad_pro').read_text());ds=pro['board']['design_settings'];assert not ds['drc_exclusions']and ds['rules']['min_connection']==.15
 coverage=dict(tool=subprocess.check_output(['kicad-cli','version'],text=True).strip(),rules=ds['rules'],rule_severities=ds['rule_severities'],exclusions=ds['drc_exclusions'],disabled={k:val for k,val in ds['rule_severities'].items()if val=='ignore'},disabled_rationale='Only tuning_profile_track_geometries: no tuning-profile geometry exists. No manufacturing/copper/footprint/courtyard category suppressed.',warning_dispositions=[],limitations='Rule-based CAD checks are not supplier CAM acceptance or a proof of analog/RF performance. Explicit .15mm connection-width threshold now active.')
 assert coverage['disabled']=={'tuning_profile_track_geometries':'ignore'}
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};allowed={'TL'+str(i)for i in range(603,610)}|{'TP'+str(i)for i in range(601,605)};rows=[]
 for warning in drc['violations']:
  ref=warning['items'][0]['description'].split()[-1];assert ref in allowed;f=fs[ref]
  assert not any(g.GetLayer()==p.F_CrtYd for g in f.GraphicalItems())and not list(f.Models())
  assert f.IsExcludedFromBOM()and f.IsExcludedFromPosFiles()
  pads=list(f.Pads());assert all(not a.IsOnLayer(p.F_Paste)for a in pads)
  if ref.startswith('TL'):
   assert all(not a.IsOnLayer(p.F_Mask)for a in pads);lines=[g for g in f.GraphicalItems()if g.GetLayer()==p.F_Cu];assert len(lines)==1 and abs(p.ToMM(lines[0].GetWidth())-1.102)<1e-6
   geometry='1.102mm-wide real F.Cu line;endpoints are an intentional net tie;mask-covered,no paste,no body'
  else:
   assert len(pads)==1 and abs(p.ToMM(pads[0].GetSize().x)-.6)<1e-6 and pads[0].IsOnLayer(p.F_Mask)
   geometry='0.60mm inline bare probe pad,mask opening intentional,no paste;contained within1.102mm line,not a coax stub'
  item=dict(ref=ref,classification='B_INTENTIONAL_NON_COMPONENT',position_mm=[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)],geometry=geometry,reason='No purchased body or assembly volume;component courtyard inapplicable. Copper/mask/edge checks remain active. Adjacent assembly clearances evaluated using actual component courtyards.',net_or_tie=[a.GetNetname()for a in pads]);coverage['warning_dispositions'].append(item);rows.append([ref,','.join(f'{x:.3f}'for x in item['position_mm']),geometry,'B:retain warning'])
 assert {x['ref']for x in coverage['warning_dispositions']}==allowed
 save('DRC-coverage.json',coverage);save('DRC-warning-dispositions.json',coverage['warning_dispositions'])
 # Fresh native pad list and exact hole inventory.
 pads=[];holes=collections.Counter();vias=[]
 for f in fs.values():
  for a in f.Pads():
   if not a.GetNumber():continue
   d=a.GetDrillSize();pads.append(dict(ref=f.GetReference(),pad=a.GetNumber(),net=a.GetNetname(),x_mm=p.ToMM(a.GetPosition().x),y_mm=p.ToMM(a.GetPosition().y),drill_x_mm=p.ToMM(d.x),drill_y_mm=p.ToMM(d.y),footprint=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())))
   if d.x:holes[(round(p.ToMM(d.x),3),'NPTH'if a.GetAttribute()==p.PAD_ATTRIB_NPTH else'PTH')]+=1
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):vias.append(t)
 tab('pad-connectivity.csv',pads)
 sv=[t for t in vias if p.ToMM(t.GetPosition().x)in[111.35,112.65]and 52.9<p.ToMM(t.GetPosition().y)<57.1];assert len(sv)==12 and all(t.GetNetname()=='GND'for t in sv)
 for t in list(b.GetTracks())+[a for f in fs.values()for a in f.Pads()]:
  if not t.IsOnLayer(p.B_Cu)or t.GetNetname()=='GND':continue
  bb=t.GetBoundingBox();assert not(p.ToMM(bb.GetRight())>=105 and p.ToMM(bb.GetLeft())<=119 and p.ToMM(bb.GetBottom())>=49 and p.ToMM(bb.GetTop())<=61),('Foreign thermal contact copper',t.GetNetname())
 lengths=[6.23,6.62,5.8,2.2,11,12.4,2];tl=[];zn,ee=microstrip(1.102);zs,es=microstrip(.92,.508,.07,4.3)
 for ref,l in zip(['TL'+str(i)for i in range(603,610)],lengths):
  f=fs[ref];ports={a.GetNumber():a for a in f.Pads()};actual=math.hypot(ports['1'].GetPosition().x-ports['2'].GetPosition().x,ports['1'].GetPosition().y-ports['2'].GetPosition().y)/1e6;assert abs(actual-l)<1e-6
  phase=360*144.7e6*actual/1000*math.sqrt(ee)/299792458;stphase=360*144.7e6*l/1000*math.sqrt(es)/299792458
  tl.append(dict(ref=ref,length_mm=actual,width_mm=1.102,Z0_ASSUMED_ohm=zn,effective_Dk_ASSUMED=ee,phase_at144p7MHz_deg=phase,ST_length_mm=l,ST_width_mm=.92,ST_model_phase_deg=stphase,E1_E2_geometry='IDENTICAL',status='CALCULATED_NOT_MEASURED'))
 tab('transmission-lines.csv',tl)
 sens=[]
 for h,t,er,w in itertools.product([.59,.64,.69],[.06,.07,.08],[4.1,4.3,4.5],[1.052,1.102,1.152]):
  z,e=microstrip(w,h,t,er);sens.append(dict(h_mm=h,t_mm=t,Dk=er,w_mm=w,Z0_ohm=z,effective_Dk=e,phase_ratio=math.sqrt(e/ee)))
 tab('stackup-sensitivity.csv',sens)
 proposals=[]
 for h in [.54,.59,.64,.69,.70,.74,1.44]:
  lo,hi=.1,5
  for _ in range(70):
   mid=(lo+hi)/2
   if microstrip(mid,h,.07,4.3)[0]>50:lo=mid
   else:hi=mid
  w=(lo+hi)/2;z,e=microstrip(w,h,.07,4.3);proposals.append(dict(dielectric_mm=h,width_for50ohm_mm=w,length_scale_for_E1_phase=math.sqrt(ee/e),action='PROPOSAL_ONLY_DO_NOT_APPLY_WITHOUT_ENGINEERING_REVIEW'))
 tab('alternative-stackup-proposals.csv',proposals)
 stack=dict(revision='M5B-E2',outline_mm=[180,140],layers=2,finished_thickness_nominal_mm=.8,dielectric_nominal_mm=.64,finished_copper_each_um=70,mask_nominal_each_um=10,Dk_ASSUMED=4.3,Df_ASSUMED=.02,finish='ENIG proposed',fabricator_acceptance='PENDING_WRITTEN_CONFIRMATION;no files sent',request_core_thickness_mm=[.59,.69],request_finished_copper_um=[60,80],Dk_analysis_window=[4.1,4.5],track_clearance_min_mm=.15,connection_width_min_mm=.15,via_land_drill_mm=[.6,.3],annular_nominal_mm=.15,Cu_edge_min_mm=.5,hole_clearance_min_mm=.25,mask_web_min_mm=p.ToMM(b.GetDesignSettings().m_SolderMaskMinWidth),mask_expansion_mm=p.ToMM(b.GetDesignSettings().m_SolderMaskExpansion),finished_component_holes=[dict(diameter_mm=d,plating=k,count=n)for(d,k),n in sorted(holes.items())],via_count=len(vias),source_vias=12,mounts=[dict(ref='H'+str(i),x_mm=x,y_mm=y,NPTH_mm=3.2)for i,(x,y)in enumerate([(25,25),(195,25),(195,155),(25,155),(112,32),(112,68)],1)],supplier_confirmations=['Actual dielectric and laminate Dk;finished not starting copper','0.15mm features at70um Cu;0.15mm nominal annulus with hole registration','0.1mm mask webs andRNW isolated6/7/8 lands','Connector finished hole tolerance and lead diagonal','Source-via tents and segmented paste;no unsolicited RF CAM changes'])
 save('stackup-mechanical.json',stack)
 # Exact copper-plane comparison in the functional RF strip. The four
 # localized control repairs are outside this window; no RF ground edit.
 old=p.LoadBoard(str(OUT/'copper-investigation/before.kicad_pcb'));plane=[]
 for layer,ymax in [(p.F_Cu,63),(p.B_Cu,65)]:
  window=p.SHAPE_POLY_SET();window.NewOutline()
  for x,y in [(49,43),(190,43),(190,ymax),(49,ymax)]:window.Append(p.FromMM(x),p.FromMM(y))
  a=next(z.GetFilledPolysList(layer)for z in old.Zones()if not z.GetIsRuleArea()and z.IsOnLayer(layer));z=next(z.GetFilledPolysList(layer)for z in b.Zones()if not z.GetIsRuleArea()and z.IsOnLayer(layer));diff=a.CloneDropTriangulation();diff.BooleanXor(z);diff.BooleanIntersection(window);area=diff.Area()/1e12;assert area==0,('RF ground contour changed',layer,area)
  plane.append(dict(layer=p.LayerName(layer),window_mm=[49,43,190,ymax],symmetric_difference_area_mm2=area))
 save('RF-ground-geometry.json',dict(status='PASS_NATIVE_FILLED_COPPER_COMPARISON',regions=plane,all_RF_footprints_and_tracks_unchanged=True,limitation='CAD geometry invariance is not physical RF qualification. Control-side plane refill and the documented notch are outside these regions.'))
 # Minimum local gap of the corrected finite-width control track to other
 # nets, using native polygons. Curve approximation is disclosed.
 target=next(t for t in b.GetTracks()if t.m_Uuid.AsString()=='62c24e8d-cdd2-46ed-a062-f5dba1cb82c0');other=p.SHAPE_POLY_SET()
 for item in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]+[z for z in b.Zones()if not z.GetIsRuleArea()]:
  if item.GetNetname()!=target.GetNetname()and item.IsOnLayer(p.F_Cu):item.TransformShapeToPolygon(other,p.F_Cu,0,p.FromMM(p.ARC_HIGH_DEF_MM),p.ERROR_OUTSIDE)
 other.Simplify();near=p.VECTOR2I();sq=other.SquaredDistanceToSeg(p.SEG(target.GetStart(),target.GetEnd()),near);gap=math.sqrt(sq)/1e6-p.ToMM(target.GetWidth())/2;assert gap>=.15
 save('copper-clearance.json',dict(track_UUID=target.m_Uuid.AsString(),layer='F.Cu',net=target.GetNetname(),nominal_track_width_mm=.15,minimum_other_net_gap_mm=gap,nearest_point_mm=[p.ToMM(near.x),p.ToMM(near.y)],method='Native polygon distance to finite-width segment;high-definition outer curve approximation. CAD measurement,not an etched-board inspection.'))
 # Actual visible legend dimensions, in addition to configured rule minima.
 texts=[g for g in b.GetDrawings()if isinstance(g,p.PCB_TEXT)and g.GetLayer()in[p.F_SilkS,p.B_SilkS]]
 for f in fs.values():texts.extend(g for g in f.GetFields()if g.IsVisible()and g.GetLayer()in[p.F_SilkS,p.B_SilkS])
 graphics=[g for f in fs.values()for g in f.GraphicalItems()if g.GetLayer()in[p.F_SilkS,p.B_SilkS]and hasattr(g,'GetWidth')]
 save('legend-dimensions.json',dict(visible_text_count=len(texts),min_text_height_mm=min(p.ToMM(g.GetTextSize().y)for g in texts),min_text_stroke_mm=min(p.ToMM(g.GetTextThickness())for g in texts),min_graphic_stroke_mm=min(p.ToMM(g.GetWidth())for g in graphics),supplier_confirmation='Confirm fine legend capability;do not erase orientation/polarity marks in CAM.'))
 # Current package map audit; evidence remains linked to preserved E1 datasheet log.
 audit=json.loads((OUT/'pinout-audit.json').read_text());save('critical-package-audit.json',dict(revision='M5B-E2',evidence='../M5B-E1/source-log.json',evidence_SHA256=sha(E1/'source-log.json'),manufacturer_devices=audit['PCB_physical_devices'],native_package_count=v['native_PCB_package_checks'],all_local_libraries_unchanged_from_E1=True,source_thermal_vias=12,thermal_window_foreign_copper=False,physical_assembly='NOT_RUN',exceptions='No critical pin/package mapping OPEN. Incoming dimensions and external insulating TIM selection remain assembly checks. Three connector3D models absent;custom3D envelopes are not qualifiedSTEP.'))
 # Structural comparison ignores netlist export timestamps only.
 import xml.etree.ElementTree as ET
 def signature(fn):
  t=ET.parse(fn);components={c.get('ref'):(c.findtext('value'),c.findtext('footprint'))for c in t.findall('./components/comp')};nets={n.get('name'):sorted((i.get('ref'),i.get('pin'))for i in n.findall('node'))for n in t.findall('./nets/net')};return components,nets
 a=signature(E1/'RF2M.net.xml');z=signature(OUT/'RF2M.net.xml');assert a==z
 save('E1-E2-netlist-comparison.json',dict(status='PASS_IDENTICAL_COMPONENT_VALUE_FOOTPRINT_AND_NET_MEMBERSHIP',components=len(z[0]),nets=len(z[1]),timestamp_metadata_ignored=True))
 # Fresh E-test aliases; logical TL boundaries are physically tied.
 parent={}
 def find(x):
  parent.setdefault(x,x)
  if parent[x]!=x:parent[x]=find(parent[x])
  return parent[x]
 for part in parts:
  if part['ref'].startswith('TL'):
   a,c=list(part['pins'].values());parent[find(c)]=find(a)
 aliases={x:find(x)for x in parent};save('fabrication-net-aliases.json',dict(reason='IntentionalTLcopper net ties;use physicalIPCfor bare-boardE-test.',aliases=aliases))
 lines=(OUT/'RF2M-logical.ipc').read_text().splitlines();physical=[]
 for line in lines:
  if line[:3]in['317','327','367']:line=line[:3]+aliases.get(line[3:17].strip(),line[3:17].strip()).ljust(14)+line[17:]
  physical.append(line)
 (OUT/'RF2M-physical-netties.ipc').write_text('\n'.join(physical)+'\n')
 tab('E1-E2-cost-delta.csv',[dict(population=x['population'],fleet=x['fleet'],E1_component_net_EUR=x['component_net_EUR'],E2_component_net_EUR=x['component_net_EUR'],delta_net_EUR=0,unquoted_net_EUR=x['unquoted_net_EUR'])for x in cost['summary']])
 # Regenerate acceptance ledger: no inherited hardware PASS values.
 gates=[r['gate']for r in csv.DictReader((E1/'acceptance-register.csv').open())];tab('acceptance-register.csv',[dict(gate=g,status='NOT_RUN',board_serial='',instrument_and_calibration='',conditions='',result='',uncertainty='',operator_date='')for g in gates])
 model=json.loads((E1/'3D-model-status.json').read_text());model['E2_reaudit']='All embedded model placement and footprint geometry byte-equivalent to E1;fresh KiCad renders,not newvendor qualification.';save('3D-model-status.json',model)
 # Reference-only mechanical information regenerated from unchanged design.
 thermal=json.loads((E1/'thermal-contact.json').read_text());thermal['E2_native_window_recheck']='PASS_no_foreign_B.Cu_in_14x12_window';save('thermal-contact.json',thermal)
 summary=dict(revision='M5B-E2',baseline_commit=BASE,baseline_tag='m5b-e1',KiCad=coverage['tool'],ERC_errors=0,ERC_warnings=0,DRC_errors=0,DRC_warnings=11,unrouted=0,schematic_parity_issues=0,exclusions=0,disabled=list(coverage['disabled']),connection_width_min_mm=.15,logic_combinations=v['logic']['combinations'],state_scenarios=len(v['logic']['scenarios']),mutations=len(v['mutation_tests'])+len(v['M5B_additional_mutations']),critical_pin_maps=len(audit['devices']),native_pad_packages=v['native_PCB_package_checks'],ST_network_positions=26,physical_acceptance='NOT_RUN',decision='GO for independent small bare-evaluation-board manufacturing review and quotation preparation;no order authorization',preserved_files=len(preserved()))
 assert summary['mutations']==37 and summary['logic_combinations']==4096 and summary['state_scenarios']==39;save('final-checks.json',summary)
 native=[HW/'RF2M.kicad_pro',HW/'RF2M.kicad_pcb',HW/'RF2M.electrical.json',HW/'ARDF_2M.kicad_sym',HW/'sym-lib-table',HW/'fp-lib-table',*HW.glob('*.kicad_sch'),*(HW/'ARDF_2M.pretty').glob('*'),*(HW/'ARDF_2M.3dshapes').glob('*')];save('native-inputs.json',{str(x.relative_to(ROOT)):sha(x)for x in sorted(set(native))if x.is_file()})
 save('source-log.json',dict(date='2026-10-16',retained_component_evidence='../M5B-E1/source-log.json',retained_SHA256=sha(E1/'source-log.json'),new_sources=[dict(url='https://raw.githubusercontent.com/KiCad/kicad-source-mirror/10.0.6/pcbnew/drc/drc_test_provider_sliver_checker.cpp',scope='GPL2+algorithm;defaults20deg,.08mm,.0008mm',local_source_SHA256='d9df8f5c7867a1305969223c30332ae40df5ae75e468e42dc627eaee07568672'),dict(url='https://jlcpcb.com/help/article/jlcpcb-copper-weight',scope='2026-09-09 guide;2oz minimum.16mm;therefore NOT automaticacceptance ofthis.15mmboard'),dict(url='https://jlcpcb.com/capabilities/pcb-capabilities/',scope='0.8mmboardoverallthicknesstolerance±.1mm,notcorethicknessguarantee'),dict(url='https://www.pcbway.com/capabilities.html',scope='Published0.8mm/70um options,.15mmannulus,PTH±.08/NPTH±.05;combinedprocessrequiresquoteconfirmation')],no_supplier_contact_or_upload=True))
 warnings=table(['Feature','Position x,y mm','Native geometry / mask','Disposition'],rows)
 budget=table(['Population','6 each','10 each','20 each','Fitted parts / ICs','Unquoted at10','E1→E2'],[[pop,*[f"€{next(x for x in cost['summary']if x['population']==pop and x['fleet']==q)['component_net_EUR']:.2f}"for q in[6,10,20]],f"{next(x for x in cost['summary']if x['population']==pop)['physical_components']} / {next(x for x in cost['summary']if x['population']==pop)['IC_count']}",f"€{next(x for x in cost['summary']if x['population']==pop and x['fleet']==10)['unquoted_net_EUR']:.2f}",'€0.00']for pop in ['BOOST2S','BUCK4S','TRAIN_ONLY']])
 (OUT/'DRC-warning-dispositions.md').write_text('# Individual E2 warning dispositions\n\n'+warnings)
 (OUT/'COST_SUMMARY.md').write_text('# E2 material totals, EUR net\n\n'+budget)
 print('PASS E2review metadata;11dispositioned warnings;native/sources/BOM preserved')

if __name__=='__main__':main()
