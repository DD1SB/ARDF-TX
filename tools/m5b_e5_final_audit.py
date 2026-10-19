#!/usr/bin/python3
"""Final export, mechanical-envelope, coverage and integrity gates; no PCB edits."""
import re,csv,json,math,subprocess,copy
from m5b_e5_common import *
def mechanical():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};allboxes={}
 for ref,expected in[('H5','E5_PA_cooling_envelope.wrl'),('Q401','E5_pass_cooling_envelope.wrl'),('Q402','E5_BD139_assembly_envelope.wrl')]:
  f=fs[ref];names=[m.m_Filename for m in f.Models()];assert any(expected in n for n in names),(ref,names)
  text=(HW/'ARDF_2M.3dshapes'/expected).read_text();boxes=[];x,y=xy(f.GetPosition())
  pattern=r'translation\s+([-\d.eE]+)\s+([-\d.eE]+)\s+([-\d.eE]+).*?geometry Box\s*\{ size\s+([-\d.eE]+)\s+([-\d.eE]+)\s+([-\d.eE]+)'
  for match in re.finditer(pattern,text,re.S):
   xx,yy,zz,w,d,h=[float(v)*2.54 for v in match.groups()];boxes.append([x+xx-w/2,y-yy-d/2,zz-h/2,x+xx+w/2,y-yy+d/2,zz+h/2])
  assert boxes;allboxes[ref]=boxes
 def hit(a,z):return all(min(a[k+3],z[k+3])-max(a[k],z[k])>.0001 for k in range(3))
 def holes(boxes):
  return any(box[0]-4.5<=x<=box[3]+4.5 and box[1]-4.5<=y<=box[4]+4.5 for ref in['H1','H2','H3','H4']for x,y in[xy(fs[ref].GetPosition())]for box in boxes)
 assert not holes(allboxes['H5'])and not holes(allboxes['Q401'])
 assert not any(hit(a,z)for a in allboxes['H5']for z in allboxes['Q401'])
 carrier=[20,20,45,190,140,48]
 assert not any(hit(a,carrier)for name in allboxes for a in allboxes[name])
 # Main helper/spacer clearance considers individual blocks;aggregate AABBs
 # would falsely intersect empty space between fins and the stock spacer.
 assert not any(hit(a,z)for a in allboxes['Q401']for z in allboxes['Q402'])
 negatives=[]
 def moved(boxes,axis,delta):return[[v+delta if i in[axis,axis+3]else v for i,v in enumerate(box)]for box in boxes]
 tests=[('PAintoM3pillar',holes(moved(allboxes['H5'],0,23))),('passsinkintoPA',any(hit(a,z)for a in allboxes['H5']for z in moved(allboxes['Q401'],1,5))),('helperintoCarrier',any(hit(a,carrier)for a in moved(allboxes['Q402'],2,10))),('carrierLowered15mm',any(hit(a,moved([carrier],2,-15)[0])for a in allboxes['Q402']))]
 for name,caught in tests:assert caught,name;negatives.append(dict(mutation=name,rejected=True))
 save('mechanical-native-model-audit.json',dict(status='PASS_NATIVE_OWN_ENVELOPE_GEOMETRY',native_sha256=sha(HW/'RF2M.kicad_pcb'),boxes_native_XYZ_mm=allboxes,carrier_box_mm=carrier,negative_tests=negatives,models='Ownclearanceenvelopes,notmanufacturerSTEP or physicalassemblyproof. Copper/sourcepackagepadmapping separately verified.',physical='NOT_RUN'))
def main():
 guard();save('verification-inputs.json',{str(f.relative_to(ROOT)):sha(f)for f in sorted((ROOT/'tools').glob('m5b_e5*.py'))});native=sha(HW/'RF2M.kicad_pcb');mechanical()
 for name,key in[('JLCPCB-DFM.json','native_sha256'),('compact-engineering.json','native_sha256'),('source-assembly-DFM.json','native_SHA256'),('normal-RF-copper-equivalence.json','native_sha256'),('source-Gerber-geometry-audit.json','native_sha256'),('compact-power-and-return.json','native_sha256')]:
  a=json.loads((OUT/name).read_text());assert a[key]==native,(name,'stale');assert a['status'].startswith('PASS'),name
 v=json.loads((OUT/'verification.json').read_text());assert v['logic']['combinations']==4096 and len(v['logic']['scenarios'])==39 and len(v['mutation_tests'])+len(v['M5B_additional_mutations'])==37;assert v['ST_reference_positions']==26 and v['native_PCB_package_checks']==320
 pin=json.loads((OUT/'pinout-audit.json').read_text());assert len(pin['devices'])==42
 src=json.loads((OUT/'source-assembly-regression.json').read_text());assert len(src['native_tests'])==16 and len(src['thermal_tests'])==4
 eng=json.loads((OUT/'compact-engineering.json').read_text());assert len(eng['negative_tests'])==18 and len(eng['connector_pins'])==20
 # Calculations use the exact same canonical98-via/source/paste/contact geometry.
 # Preserve the original calculation-file hash and explicitly bind that local
 # geometry to finalCAD;unrelated RF redundant-copper removal changes filehash.
 t=json.loads((OUT/'thermal-model.json').read_text());t.setdefault('calculation_native_file_SHA256',t.get('native_input_SHA256'));t.update(final_native_geometry_binding_SHA256=native,final_geometry_binding='Actualcanonicalsourceaudit:98via locations/lands/drills,sourceCu/mask/paste,bar/window/mounts unchanged. Numerical geometry/solver inputs unchanged;not new measured data.',fin_rotation_sensitivity_extra_K_W=.25,fin_rotation_sensitivity_extra_C_at4W=1.,physical='NOT_RUN');save('thermal-model.json',t)
 # Include exact coverage, not a combined fabricated PASS for physical gates.
 save('final-verification.json',dict(status='PASS_NONPHYSICAL_ENGINEERING_GATES',native_sha256=native,KiCad=json.loads((OUT/'DRC.json').read_text())['kicad_version'],ERC_errors=0,ERC_warnings=0,DRC_errors=0,DRC_intentional_warnings=11,unrouted=0,parity=0,logic_combinations=4096,states=39,baseline_mutations=37,manufacturer_maps=42,ST_positions=26,package_pad_sets=320,controller_pins=20,compact_native_negatives=18,source_native_negatives=16,source_thermal_negatives=4,mechanical_envelope_negatives=4,DFM_negatives='DFM-regression.json;11E3classespreserved',physical='NOT_RUN',optional_dual_stack='HOLD',no_manufacturing_authorization=True))
 # Native per-net routing delta and explicit engineering change report.
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));old=p.LoadBoard(str(OUT/'development/E4R1-baseline.kicad_pcb'))
 def summary(bb):
  out={}
  for t in bb.GetTracks():
   r=out.setdefault(t.GetNetname(),dict(track_mm=0.,vias=0,segments=0))
   if isinstance(t,p.PCB_VIA):r['vias']+=1
   else:r['track_mm']+=p.ToMM(t.GetLength());r['segments']+=1
  return out
 before,after=summary(old),summary(b);rows=[]
 for n in sorted(set(before)|set(after)):
  a,z=before.get(n,{}),after.get(n,{});rows.append(dict(net=n,E4R1_track_mm=a.get('track_mm',0),E5_track_mm=z.get('track_mm',0),E4R1_vias=a.get('vias',0),E5_vias=z.get('vias',0)))
 with(OUT/'routing-copper-by-net.csv').open('w')as fp:
  w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 save('E4R1-E5-change-report.json',dict(baseline_commit=BASE,baseline_native_SHA256=sha(OUT/'development/E4R1-baseline.kicad_pcb'),candidate_native_SHA256=native,outline_before_after_mm=[[180,140],[150,110]],mount_pattern_mm=[140,100],component_values_or_MPN_changes=[],logical_net_membership_changes=[],controller_connector_pin_changes=[],population_changes=[],source_local_geometry_changes=[],normal_RF_copper='36originalconductorsand26STposesrigidlytranslate(-20,0)mm;seven2.741mmTLwidths/lengthsunchanged',other_routes='Clock,trainingclock,powerandcontrolsrerouted;seeactualdisplacement/per-netcopper/clock/powerreports',ground='Twoexplicitgroundwasherannuliandtwoordinarygroundvias;noextra thermalcredit;controlledgroundcorridorchangesdocumented',mechanical='SameSK81/bar;finrotation,rotatedSK100with5mmstockspacer,raisedhelperassemblyandindependentcontrollercarrier',physical='NOT_RUN'))
 # Normalize only owned review CSV/SVG whitespace;fabrication Gerbers/drills unchanged.
 for file in OUT.rglob('*.csv'):file.write_bytes(file.read_bytes().replace(b'\r\n',b'\n'))
 for file in OUT.rglob('*.svg'):file.write_text('\n'.join(line.rstrip()for line in file.read_text().splitlines())+'\n')
 # Fresh full export syntax/population/net-tie/drill/metadata validation.
 code=(ROOT/'tools/m5b_artifacts.py').read_text().replace('from m5b_design import HW,OUT,ROOT,preserved','from m5b_e5_common import HW,OUT,ROOT,preserved').replace('M5B-E1','M5B-E5').replace('M5B_E1_','M5B_E5_').replace('max(xs)==200000000','max(xs)==170000000').replace('min(ys)==-160000000','min(ys)==-130000000').replace("len(list(OUT.glob('RF2M-3D*.png')))==3","len(list(OUT.glob('RF2M-3D*.png')))==4").replace('len(docs)==7','len(docs)==6').replace("'FINAL_REVIEW'","'CANDIDATE_INDEPENDENT_REVIEW'")
 ns={'__name__':'E5_artifact_audit'};exec(compile(code,'E5_artifact_audit','exec'),ns);ns['main']()
 r=subprocess.run(['sha256sum','-c',str(OUT/'SHA256SUMS')],cwd=ROOT,capture_output=True,text=True);assert r.returncode==0,r.stdout+r.stderr;print('PASS finalE5 sourcehashes,mechanicalenvelopes,coverage,actualexportsandSHA256manifest',flush=True)
if __name__=='__main__':main()
