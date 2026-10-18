#!/usr/bin/python3
"""Replay frozen M4A engines into V1R1 only; no historical output writes."""
import sys,types,json,copy
from m4a_v1r1_common import *
def load(name,replacements=()):
 code=(R/'tools'/(name+'.py')).read_text().replace('from m4a_design import','from m4a_v1r1_common import')
 for a,b in replacements:
  assert a in code,(name,'Missing adaptation anchor',a[:80]);code=code.replace(a,b)
 code=code.replace("date='2026-10-15'","date=DATE")
 code=code.replace("revision='M4A-V1'","revision='M4A-V1R1'").replace("candidate_revision='M4A-V1'","candidate_revision='M4A-V1R1'")
 m=types.ModuleType(name+'_v1r1');m.__file__=str(R/'tools'/(name+'.py'));m.DATE=DATE;sys.modules[m.__name__]=m;exec(compile(code,m.__file__,'exec'),m.__dict__)
 assert m.D==D,(name,'Historical output rejected');return m
def main():
 action=sys.argv[1];sys.argv=[sys.argv[0]]+sys.argv[2:]
 if action=='exports':load('m4a_exports').main();return
 if action=='verify':
  import m3be2_pinouts as maker
  base=json.loads(gitfile('hardware/80m/production/RF80_V1.electrical.json'));old={x['ref']:x for x in base['parts']}
  manifest=json.loads((P/(NAME+'.electrical.json')).read_text())
  for x in manifest['parts']:
   if x['ref']in ALIASES:maker.CAT[x['mpn']]['footprint']=ALIASES[x['ref']][0]
  reps=[("assert om==nm,'A non-test component identity/value/net/population was modified'", "\n    nm=copy.deepcopy(nm)\n    for ref in ALIASES:\n        assert nm[ref]['footprint']==ALIASES[ref][0]\n        nm[ref]['footprint']=om[ref]['footprint'];nm[ref]['note']=om[ref]['note']\n    assert om==nm,'A non-test electrical component field changed'"),
   ('assert identities(ot)==identities(nt)',"origids=identities(ot);newids=identities(nt)\n    for ref in ALIASES:newids[ref]=(newids[ref][0],origids[ref][1],newids[ref][2])\n    assert origids==newids"),
   ("assert geometry(f)==geometry(old_fs[r]),(r,'Footprint-local pad/lead/drill geometry changed from E2')", "ga=geometry(f);gb=geometry(old_fs[r])\n        if r in ALIASES:\n            for k in ga:ga[k]=(ga[k][0],gb[k][1],gb[k][2],*ga[k][3:])\n        assert ga==gb,(r,'Unapproved local geometry change')"),
   ("v['footprint']=='ARDF_TX:ST_BD140_SOT32_1p3Drill'", "v['footprint']=='ARDF_TX:ST_BD140_SOT32_StandardPTH'"),
   ("abs(z-1.3)<.001", "abs(z-1.4)<.001"),
   ('all_native_footprint_local_geometries_unchanged=True','all_unmodified_local_pad_geometries_unchanged=True,approved_PTH_changes=list(ALIASES)')]
  m=load('m4a_verify',reps);m.ALIASES=ALIASES;m.main()
  if (D/'logic-results.json').exists():
   report=json.loads((D/'logic-results.json').read_text());report.update(engine_revision=report['revision'],engine_original_report_date=report['date'],revision=REV,date=DATE);save('logic-results.json',report)
  return
 if action=='geometry':load('m4a_geometry_review').main();return
 if action=='artifacts':
  m=load('m4a_artifact_audit',[("critical_finished_holes={'J101':'1.20+/-0.05mm','J502':'0.95+/-0.05mm','Q402/Q403':'1.30+/-0.05mm; incoming lead/body fit required'}", "critical_finished_holes={'J101':'1.40mm','J301':'1.90mm','J401':'1.30mm','J502':'1.30mm','Q402/Q403':'1.40mm','tolerance':'Ordinary component PTH +0.13/-0.08mm; no press-fit service'}")]);m.audit();return
 if action=='documents':
  m=load('m4a_document_checks',[("D/'routing-history/README.md'","D/'CHANGE_REPORT.md'"),
   ("for result in json.loads((D/'historical-version-regressions.json').read_text()):assert result['exit_code']==0", "for result in json.loads((P/'review/M4A-V1/historical-version-regressions.json').read_text()):assert result['exit_code']==0")]);m.main();return
 if action=='manifest':
  frozen();files=[];sources=[]
  for f in sorted(D.rglob('*')):
   if f.is_file()and f.name not in ['SHA256SUMS','file-manifest.json']:files.append(dict(path=str(f.relative_to(D)),bytes=f.stat().st_size,sha256=sha(f)))
  candidates=[f for f in P.rglob('*')if f.is_file()and 'review'not in f.relative_to(P).parts]+list((R/'tools').glob('m4a*.py'))+list((R/'docs').glob('M4A_V1R1*'))
  for f in sorted(set(candidates)):
   if f.suffix not in ['.kicad_prl','.lck']:sources.append(dict(path=str(f.relative_to(R)),sha256=sha(f)))
  save('file-manifest.json',dict(revision=REV,baseline=BASE,review_files=files,native_and_reproduction_sources=sources));(D/'SHA256SUMS').write_text(''.join(f"{x['sha256']}  {x['path']}\n"for x in files));print('Manifest',len(files),'review files,',len(sources),'sources');return
 raise SystemExit('Unknown read-only action')
if __name__=='__main__':main()
