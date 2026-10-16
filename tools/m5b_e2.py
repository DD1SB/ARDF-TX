#!/usr/bin/python3
"""Focused E1 -> E2 correction and reproducible verification/export entry point.
Never exports to E1, orders a board, or uploads manufacturing data.
"""
import argparse,hashlib,json,subprocess,sys,shutil,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E2';E1=HW/'review/M5B-E1';BASE='6931260';TRACK='62c24e8d-cdd2-46ed-a062-f5dba1cb82c0';REMOVE='deabdd94-a712-440c-b152-694a92481f7e'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2)+'\n')
def preserved():
 from m5b_design import preserved as old
 d=old()
 for p in list(E1.rglob('*'))+list((ROOT/'docs').glob('M5B_E1_*.md'))+[p for p in (ROOT/'tools').glob('m5b*.py')if not p.name.startswith('m5b_e2')]:
  if p.is_file()and p.suffix!='.pyc':d[str(p.relative_to(ROOT))]=sha(p)
 return dict(sorted(d.items()))
def baseline():
 OUT.mkdir(exist_ok=True)
 fn=OUT/'preserved-baseline.json'
 if not fn.exists():save(fn.name,preserved())
 assert preserved()==json.loads(fn.read_text()),'E1/RF80/history changed'
def gitfile(n):return subprocess.check_output(['git','show',BASE+':hardware/2m/'+n],cwd=ROOT)
def correct():
 import pcbnew as p
 baseline();remap={};fn=HW/'RF2M.kicad_pcb';b=p.LoadBoard(str(fn));ts={t.m_Uuid.AsString():t for t in b.GetTracks()}
 if REMOVE in ts:
  t=ts[TRACK];assert t.GetNetname()=='PACK_OK_N'and p.ToMM(t.GetEnd().x)==55.5
  t.SetEnd(p.VECTOR2I(p.FromMM(57),p.FromMM(68)));b.Remove(ts[REMOVE])
 # Additional manufacturing findings exposed by an active .15mm neck rule.
 remove=['3c662c47-3943-4820-a3ba-13068219c422','7625047e-c9e5-414d-823b-1fe499eb1bee','7ad57a14-8a9b-477f-b794-ce066b0429a2','a6349226-e655-461c-b43a-2c4d167812d2','8f0ab51e-61d1-4b2a-aac6-0aa2233f5854','328099ce-dc09-49aa-a643-68ffce92864d']
 for uid in remove:
  if uid in ts:b.Remove(ts[uid])
 ts['70b009b9-a023-416e-b4f0-a03dd7208999'].SetEnd(p.VECTOR2I(p.FromMM(57.45),p.FromMM(35.975)))
 ts['d9a54bae-b91b-4870-893c-d0f4fa8c3639'].SetEnd(p.VECTOR2I(p.FromMM(128.1),p.FromMM(82.4)));ts['d9a54bae-b91b-4870-893c-d0f4fa8c3639'].SetWidth(p.FromMM(.2))
 ts['ad10ef61-9d87-4da5-b25f-ed14c7b1ad29'].SetWidth(p.FromMM(.2))
 import uuid
 uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'ARDF-TX/M5B-E2/V3V3-junction'))
 if uid not in ts:
  t=p.PCB_TRACK(b);remap[t.m_Uuid.AsString()]=uid;t.SetStart(p.VECTOR2I(p.FromMM(174.9),p.FromMM(140.8)));t.SetEnd(p.VECTOR2I(p.FromMM(175.5),p.FromMM(141.1)));t.SetWidth(p.FromMM(.3));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet('V3V3'));b.Add(t)
 uid=str(uuid.uuid5(uuid.NAMESPACE_URL,'ARDF-TX/M5B-E2/ground-neck-keepout'))
 if not any(z.m_Uuid.AsString()==uid for z in b.Zones()):
  z=p.ZONE(b);remap[z.m_Uuid.AsString()]=uid;z.SetIsRuleArea(True);z.SetLayer(p.F_Cu);z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowTracks(False);z.SetDoNotAllowVias(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False);o=z.Outline();o.NewOutline()
  for x,y in [(128,126.9),(128.4,126.9),(128.4,127.3),(128,127.3)]:o.Append(p.FromMM(x),p.FromMM(y))
  b.Add(z)
 pro=HW/'RF2M.kicad_pro';data=json.loads(pro.read_text());data['board']['design_settings']['rules']['min_connection']=.15;pro.write_text(json.dumps(data,indent=2)+'\n')
 tb=b.GetTitleBlock();tb.SetRevision('M5B-E2');b.SetTitleBlock(tb)
 for text in b.GetDrawings():
  if isinstance(text,p.PCB_TEXT)and'M5B-E1 EVALUATION'in text.GetText():text.SetText(text.GetText().replace('M5B-E1','M5B-E2'))
 p.SaveBoard(str(fn),b)
 text=fn.read_text()
 for old,new in remap.items():text=text.replace(old,new)
 fn.write_text(text)
 assert preserved()==json.loads((OUT/'preserved-baseline.json').read_text())
 print('Applied localized copper corrections and .15mm neck rule;schematic/BOM unchanged')
def checks():
 import m5b_pcb;m5b_pcb.D=OUT
 sys.argv=[sys.argv[0],'--checks'];import m5b_exports as e
 e.D=OUT;e.LOG=OUT/'check-commands.json';e.logs=[];e.main()
def verify():
 baseline();import m5b_verify as v
 v.OUT=OUT;v.preserved=preserved;v.main()
 a=json.loads((OUT/'pinout-audit.json').read_text());a['revision']='M5B-E2';save('pinout-audit.json',a)
 # Recompute material inputs without changing any selected electrical part.
 from m5b_models import costs,calculations
 import m5b_models as m;m.OUT=OUT;before=sha(HW/'RF2M.electrical.json');costs();calculations();assert sha(HW/'RF2M.electrical.json')==before
 (OUT/'cost-delta.csv').rename(OUT/'R4-context-cost-delta.csv')
 a=json.loads((OUT/'costs.json').read_text());o=json.loads((E1/'costs.json').read_text());assert a==o,'Cost or sourcing inputs unexpectedly changed'
 save('E1-E2-cost-delta.json',dict(revision='M5B-E2',component_changes=[],component_delta_EUR=0,notes='Same exact E1 procurement inputs;no new supplier quotation or stock assurance.',summary=a['summary']))
 # Run existing main-power connectivity check with the output redirected only.
 src=(ROOT/'tools/m5b_power_widths.py').read_text().replace("open('hardware/2m/review/M5B-E1/", "open('hardware/2m/review/M5B-E2/")
 subprocess.run(['/usr/bin/python3','-c',src],cwd=ROOT,check=True)
 print('E2 verification and unchanged itemized costs regenerated')
def exports(render):
 import m5b_pcb;m5b_pcb.D=OUT
 sys.argv=[sys.argv[0]]+(['--render']if render else[]);import m5b_exports as e
 e.D=OUT;e.LOG=OUT/'export-commands.json';e.logs=[];e.main()
def evidence():
 """Native baseline/delta and reversible causal test in a disposable analysis copy."""
 import pcbnew as p
 from m5b_e2_sliver import polygons,locate,image
 baseline();work=OUT/'copper-investigation';work.mkdir(exist_ok=True)
 # Exact baseline and final used by CLI and polygon reproduction, not alternative designs.
 for name,content in [('before',gitfile('RF2M.kicad_pcb')),('after',(HW/'RF2M.kicad_pcb').read_bytes())]:
  fn=work/(name+'.kicad_pcb');fn.write_bytes(content);fn.with_suffix('.kicad_pro').write_bytes(gitfile('RF2M.kicad_pro')if name=='before'else(HW/'RF2M.kicad_pro').read_bytes())
 # KIPRJMOD libraries are relative to temporary board directories.
 for n in ['fp-lib-table','sym-lib-table']:(work/n).write_bytes((HW/n).read_bytes())
 lib=work/'ARDF_2M.pretty'
 if not lib.exists():lib.symlink_to(HW/'ARDF_2M.pretty',target_is_directory=True)
 # Controlled ablation: sliver correction alone, then the additional active rule.
 b=p.LoadBoard(str(work/'before.kicad_pcb'));ts={t.m_Uuid.AsString():t for t in b.GetTracks()};ts[TRACK].SetEnd(p.VECTOR2I(p.FromMM(57),p.FromMM(68)));b.Remove(ts[REMOVE])
 for name in ['sliver-only','strict-before']:
  p.SaveBoard(str(work/(name+'.kicad_pcb')),b);pro=json.loads(gitfile('RF2M.kicad_pro'))
  if name=='strict-before':pro['board']['design_settings']['rules']['min_connection']=.15
  (work/(name+'.kicad_pro')).write_text(json.dumps(pro,indent=2)+'\n')
 logs=[];bs={}
 for name in ['before','sliver-only','strict-before','after']:
  fn=work/(name+'.kicad_pcb');cmd=['kicad-cli','pcb','drc','--format','json','--severity-all','--refill-zones','--save-board','-o',str(work/(name+'-DRC.json')),str(fn)]
  r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0;logs.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
  b=p.LoadBoard(str(fn));bs[name]=b;poly=polygons(b);res=locate(poly);save('copper-'+name+'-locations.json',dict(findings=res))
  if name in ['before','after']:image(poly,OUT/('copper-'+name+'.png'),'E1 before correction'if name=='before'else'E2 after correction')
  g=work/(name+'-gerbers');g.mkdir(exist_ok=True);cmd=['kicad-cli','pcb','export','gerbers','--layers','F.Cu','-o',str(g)+'/',str(fn)];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0;logs.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
 old=json.loads((work/'before-DRC.json').read_text());new=json.loads((work/'after-DRC.json').read_text())
 assert len([v for v in old['violations']if v['type']=='copper_sliver'])==1
 assert not any(v['type']=='copper_sliver'or v['severity']=='error'for v in new['violations'])
 assert len(new['violations'])==11 and not new['unconnected_items']
 assert len(json.loads((work/'sliver-only-DRC.json').read_text())['violations'])==11
 strict=json.loads((work/'strict-before-DRC.json').read_text());assert len([v for v in strict['violations']if v['type']=='connection_width'])==5
 save('connection-width-before.json',strict)
 # Exact E1-to-E2 native item delta; no footprint, zone rule, via or RF edit.
 def tracks(b):
  return{t.m_Uuid.AsString():dict(net=t.GetNetname(),layer=t.GetLayerName(),start=[t.GetStart().x,t.GetStart().y],end=[t.GetEnd().x,t.GetEnd().y],width=t.GetWidth(p.F_Cu)if isinstance(t,p.PCB_VIA)else t.GetWidth())for t in b.GetTracks()}
 a,z=tracks(bs['before']),tracks(bs['after']);removed=set(a)-set(z);changed={k for k in a.keys()&z.keys()if a[k]!=z[k]};assert removed=={REMOVE,'3c662c47-3943-4820-a3ba-13068219c422','7625047e-c9e5-414d-823b-1fe499eb1bee','7ad57a14-8a9b-477f-b794-ce066b0429a2','a6349226-e655-461c-b43a-2c4d167812d2','8f0ab51e-61d1-4b2a-aac6-0aa2233f5854','328099ce-dc09-49aa-a643-68ffce92864d'}and changed=={TRACK,'70b009b9-a023-416e-b4f0-a03dd7208999','d9a54bae-b91b-4870-893c-d0f4fa8c3639','ad10ef61-9d87-4da5-b25f-ed14c7b1ad29'}and len(set(z)-set(a))==1
 def fprints(b):return{f.GetReference():(str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),f.GetOrientationDegrees(),f.GetPosition().x,f.GetPosition().y,[(pa.GetNumber(),pa.GetNetname(),pa.GetPosition().x,pa.GetPosition().y,pa.GetSize().x,pa.GetSize().y)for pa in f.Pads()])for f in b.GetFootprints()}
 assert fprints(bs['before'])==fprints(bs['after'])
 import m5a_r1_design as cad
 before_tree=cad.parse(gitfile('RF2M.kicad_pcb').decode());after_tree=cad.parse((HW/'RF2M.kicad_pcb').read_text())
 assert [cad.dump(f)for f in cad.children(before_tree,'footprint')]==[cad.dump(f)for f in cad.children(after_tree,'footprint')],'Embedded footprint geometry changed'
 oldpro=json.loads(gitfile('RF2M.kicad_pro'));oldpro['board']['design_settings']['rules']['min_connection']=.15;assert oldpro==json.loads((HW/'RF2M.kicad_pro').read_text())
 # Source files, symbols, libraries, variants and schematic values byte-identical.
 unchanged=[]
 for path in [*HW.glob('*.kicad_sch'),HW/'RF2M.electrical.json',HW/'ARDF_2M.kicad_sym',*HW.joinpath('ARDF_2M.pretty').glob('*'),*HW.joinpath('ARDF_2M.3dshapes').glob('*')]:
  if path.is_file():assert path.read_bytes()==gitfile(str(path.relative_to(HW)));unchanged.append(str(path.relative_to(ROOT)))
 save('layout-delta.json',dict(baseline_commit=BASE,baseline_tag='m5b-e1',modified_tracks={k:dict(before=a[k],after=z[k])for k in changed},removed_tracks={k:a[k]for k in removed},added_tracks={k:z[k]for k in set(z)-set(a)},all_other_tracks_vias_identical=True,rule_change='min_connection0.0->0.15mm;all severities unchanged',zone_change='0.4mm square fill-only keepout x128..128.4/y126.9..127.3mm',all_footprint_positions_and_pads_identical=True,schematic_manifest_libraries_unchanged=unchanged))
 # Verify actual Gerber track strokes (the tip is formed by overlapping draws,
 # not a single polygon vertex in the Gerber file).
 import re
 def strokes(fn):
  text=fn.read_text();aps={k:float(v)for k,v in re.findall(r'%ADD(\d+)C,([.\d]+)\*%',text)};selected=None;at=None;out=[];region=False
  for line in text.splitlines():
   if line=='G36*':region=True
   if line=='G37*':region=False
   m=re.fullmatch(r'D(\d+)\*',line)
   if m:selected=m[1]
   m=re.fullmatch(r'X(-?\d+)Y(-?\d+)D0([12])\*',line)
   if m:
    point=(int(m[1]),-int(m[2]));op=m[3]
    if op=='1'and at and not region and selected in aps:out.append((at,point,aps[selected]))
    at=point
  return out
 olddraw=strokes(work/'before-gerbers/before-F_Cu.gtl');newdraw=strokes(work/'after-gerbers/after-F_Cu.gtl')
 for track in [TRACK,REMOVE]:assert (tuple(a[track]['start']),tuple(a[track]['end']),.15)in olddraw
 assert (tuple(z[TRACK]['start']),tuple(z[TRACK]['end']),.15)in newdraw
 assert (tuple(a[REMOVE]['start']),tuple(a[REMOVE]['end']),.15)not in newdraw
 save('copper-investigation.json',dict(layer='F.Cu',net='PACK_OK_N',point_mm=[55.991446,68.075],angle_deg=17.354033132080808,track_width_mm=.15,minimum_clearance_requirement_mm=.15,original_tip_width_mm='Tapers toward zero at an acute polygon vertex;not a subminimum nominal track',root_cause='Overlapping doubled-back control tracks create an acute union tip. No isolated ground wedge.',original_warning_count=12,corrected_warning_count=11,copper_sliver_before=1,copper_sliver_after=0,native_Gerber_track_draws_confirmed=True,commands=logs,all_physical_measurements='NOT_RUN'))
 # Remove only disposable symlinks and incidental preference files from packet.
 lib.unlink()
 for fn in work.glob('*.kicad_prl'):fn.unlink()
 print('PASS causal DRC ablation, native/Gerber draw correspondence, and localized layout delta')
def main():
 a=argparse.ArgumentParser();a.add_argument('action',choices=['correct','checks','verify','exports','evidence','reports','artifacts']);a.add_argument('--render',action='store_true');x=a.parse_args();baseline()
 if x.action=='correct':correct()
 elif x.action=='checks':checks()
 elif x.action=='verify':verify()
 elif x.action=='exports':exports(x.render)
 elif x.action=='evidence':evidence()
 elif x.action=='reports':
  import m5b_e2_review;m5b_e2_review.main()
 elif x.action=='artifacts':
  import m5b_artifacts as a
  a.OUT=OUT;a.preserved=preserved
  # Reuse the original consistency checks with only revision and doc glob adapted.
  src=(ROOT/'tools/m5b_artifacts.py').read_text().replace("from m5b_design import HW,OUT,ROOT,preserved","from m5b_e2 import HW,OUT,ROOT,preserved").replace('M5B-E1','M5B-E2').replace('M5B_E1_','M5B_E2_')
  exec(compile(src,str(ROOT/'tools/m5b_artifacts.py'),'exec'),{'__name__':'__main__'})
if __name__=='__main__':main()
