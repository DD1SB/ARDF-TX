#!/usr/bin/python3
"""Bind finalfabrication/nativearchives toactualnativegeometryandexports."""
import json,re,zipfile,collections
from pathlib import Path
import pcbnew as p
from m5b_e3_common import *
def drill(fn):
 text=fn.read_text();tools={n:float(d)for n,d in re.findall(r'^T(\d+)C([\d.]+)',text,re.M)};tool=None;hits=[]
 for line in text.splitlines():
  q=re.fullmatch(r'T(\d+)',line)
  if q:tool=q[1]
  q=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
  if q:
   assert tool in tools;hits.append((round(float(q[1]),4),round(-float(q[2]),4),round(tools[tool],4)))
 assert len(hits)==len(set(hits)),'duplicateholedrills';return set(hits)
def archive(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for name,source in sorted(files):
   info=zipfile.ZipInfo(name,date_time=(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,source.read_bytes())
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));native=json.loads((OUT/'native-inputs.json').read_text());assert all(sha(ROOT/n)==h for n,h in native.items());dfm=json.loads((OUT/'JLCPCB-DFM.json').read_text());assert dfm['native_sha256']==sha(HW/'RF2M.kicad_pcb')
 expected={'PTH':set(),'NPTH':set()}
 for v in b.GetTracks():
  if isinstance(v,p.PCB_VIA):expected['PTH'].add((round(p.ToMM(v.GetPosition().x),4),round(p.ToMM(v.GetPosition().y),4),round(p.ToMM(v.GetDrillValue()),4)))
 for f in b.GetFootprints():
  for a in f.Pads():
   if not a.GetDrillSize().x:continue
   assert a.GetDrillSize().x==a.GetDrillSize().y,'unqualifiedslot';kind='NPTH'if a.GetAttribute()==p.PAD_ATTRIB_NPTH else'PTH';expected[kind].add((round(p.ToMM(a.GetPosition().x),4),round(p.ToMM(a.GetPosition().y),4),round(p.ToMM(a.GetDrillSize().x),4)))
 quantization=[]
 for k in expected:
  actual=drill(OUT/'gerbers'/('RF2M-'+k+'.drl'));assert len(actual)==len(expected[k]),('Drillcountmismatch',k)
  for x,y,d in expected[k]:
   candidate=min((q for q in actual if q[2]==d),key=lambda q:(q[0]-x)**2+(q[1]-y)**2);error=((candidate[0]-x)**2+(candidate[1]-y)**2)**.5;assert error<=.00072,('Native/drillcoordinate',k,(x,y,d),candidate);quantization.append(error)

 job=json.loads((OUT/'gerbers/RF2M-job.gbrjob').read_text());g=job['GeneralSpecs'];assert g['LayerNumber']==2 and g['BoardThickness']==1.6 and g['Finish']=='Lead-free HASL'and g['ProjectId']['Revision']==REV
 assert abs(g['Size']['X']-180)<.1 and abs(g['Size']['Y']-140)<.1 # jobincludesoutlinepenwidth
 files=[f for f in(OUT/'gerbers').iterdir()if f.suffix in['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1','.drl']];assert len(files)==11
 comparison=[]
 for f in files:
  old=HW/'review/M5B-E2/gerbers'/f.name;comparison.append(dict(file=f.name,E3_SHA256=sha(f),E2_SHA256=sha(old),identical_to_E2=sha(f)==sha(old)))
 assert all(not a['identical_to_E2']for a in comparison),'Exportswerenotregenerated'
 archive(OUT/'RF2M-M5B-E3-fabrication-review.zip',[(f.name,f)for f in files]);archive(OUT/'RF2M-M5B-E3-native.zip',[('RF2M-M5B-E3/'+str(Path(n).relative_to(HW.relative_to(ROOT))),ROOT/n)for n in native])
 save('fabrication-data-audit.json',dict(status='PASS_NATIVE_DRILL_AND_EXPORT_CONSISTENCY',PTH_unique_hits=len(expected['PTH']),NPTH_unique_hits=len(expected['NPTH']),drill_counts_native_and_export_match=True,drill_coordinate_max_rounding_mm=max(quantization),drill_coordinate_note='KiCadExcellondecimal3places(1um);maximumradialrounding<=0.00072mm,farbelowstandarddrillregistrationtolerance.',job_stackup_and_revision_match=True,job_size_note='Jobboundsinclude0.05mmedgepen;actualroutedoutlinecenter180x140mm.',Gerber_drill_E2_comparison=comparison,upload_archive_files=[f.name for f in sorted(files)],upload_archive_note='Reviewonly;exactly9Gerbers+2drills,nojobcustomstackmetadataoranalysisincluded. Do not uploadwithoutauthorization.',native_source_archive=True,all_hardware_tests='NOT_RUN',commercial_CAM_acceptance=None,actual_quote=None,uploaded=False))
 print('PASSnative/fabdata;',len(expected['PTH']),'PTH,',len(expected['NPTH']),'NPTH;9Gerbers/2drills;nativeandfabreviewarchivescreated')
if __name__=='__main__':main()
