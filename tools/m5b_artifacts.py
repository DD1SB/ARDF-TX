#!/usr/bin/python3
"""Validate final M5B artifact/population consistency and write checksums.
Gerber syntax/header/outline/drill checks are not a commercial CAM DFM pass.
"""
import csv,hashlib,json,re,subprocess
from pathlib import Path
from m5b_design import HW,OUT,ROOT,preserved

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 native=json.loads((OUT/'native-inputs.json').read_text())
 assert all(sha(ROOT/path)==digest for path,digest in native.items()),'Native changed after report'
 assert preserved()==json.loads((OUT/'preserved-baseline.json').read_text())
 checks=[]
 for f in sorted((OUT/'gerbers').glob('*.g*')):
  if f.suffix=='.gbrjob':continue
  t=f.read_text();assert '%MOMM*%'in t and 'M02*'in t and 'M5B-E1'in t,(f,'header/footer/revision')
  checks.append(dict(file=f.name,size=f.stat().st_size,check='GerberX2 mm/header/revision/end present'))
 edge=(OUT/'gerbers/RF2M-Edge_Cuts.gm1').read_text();xs=list(map(int,re.findall(r'^X(-?\d+)',edge,re.M)));ys=list(map(int,re.findall(r'^X-?\d+Y(-?\d+)',edge,re.M)))
 assert min(xs)==20000000 and max(xs)==200000000 and min(ys)==-160000000 and max(ys)==-20000000
 for kind in ['PTH','NPTH']:
  f=OUT/'gerbers'/('RF2M-'+kind+'.drl');t=f.read_text();assert t.startswith('M48')and'METRIC'in t and'M30'in t and('NonPlated'if kind=='NPTH'else'Plated')in t
  checks.append(dict(file=f.name,check='Excellon metric/separate plating/header/end present'))
 raw=list(csv.DictReader((OUT/'RF2M_BOM.csv').open()))
 for pop in ['BOOST2S','BUCK4S','TRAIN_ONLY']:
  expected={x['ref']:x for x in raw if x['population']==pop and x['fleet']=='10'}
  actual={x['Ref']:x for x in csv.DictReader((OUT/('placement-'+pop+'.csv')).open())}
  assert set(expected)==set(actual),('Actual purchased population/placement mismatch',pop,set(expected)^set(actual))
  for ref,part in expected.items():assert actual[ref]['Val']==part['value'],('Variant assembly value mismatch',pop,ref,actual[ref]['Val'],part['value'])
  checks.append(dict(population=pop,placed_purchased_parts=len(actual),check='Exact BOM reference/value set matches native variant export'))
 for f in [OUT/'RF2M.pdf',*OUT.glob('assembly-*.pdf'),*list((OUT/'gerbers').glob('*map.pdf'))]:
  r=subprocess.run(['pdfinfo',str(f)],capture_output=True,text=True);assert r.returncode==0 and'Pages:'in r.stdout
  if f.name=='RF2M.pdf':assert re.search(r'Pages:\s+20\b',r.stdout)
 for f in OUT.glob('RF2M-3D*.png'):assert f.stat().st_size>10000 and f.read_bytes().startswith(b'\x89PNG')
 assert len(list(OUT.glob('RF2M-3D*.png')))==3
 # Physical E-test merges only intended copper-net-tie logical aliases.
 aliases=json.loads((OUT/'fabrication-net-aliases.json').read_text())['aliases'];logical=(OUT/'RF2M-logical.ipc').read_text().splitlines();physical=(OUT/'RF2M-physical-netties.ipc').read_text().splitlines();assert len(logical)==len(physical)
 for a,b in zip(logical,physical):
  if a[:3]in ['317','327','367']:
   assert b[:3]==a[:3]and b[17:]==a[17:]and b[3:17].strip()==aliases.get(a[3:17].strip(),a[3:17].strip())
  else:assert a==b
 data=dict(revision='M5B-E1',status='PASS_FILE_AND_POPULATION_CONSISTENCY',checks=checks,scope='Local export consistency and syntax markers;NOT independent CAM/physical/RF acceptance. DRC retained warnings remain in final-checks.json.',native_SHA_matches=True,historical_RF80_preserved=True)
 (OUT/'artifact-audit.json').write_text(json.dumps(data,indent=2)+'\n')
 files=[p for p in OUT.rglob('*')if p.is_file()and p.name not in ['SHA256SUMS','file-inventory.json']]
 docs=sorted((ROOT/'docs').glob('M5B_E1_*.md'));assert len(docs)==7
 inventory=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,SHA256=sha(p),role='NON_FINAL_DEVELOPMENT'if'development'in p.parts else'FINAL_REVIEW')for p in sorted(files+docs+[ROOT/n for n in native]+list((ROOT/'tools').glob('m5b*.py')))]
 (OUT/'file-inventory.json').write_text(json.dumps(dict(revision='M5B-E1',authority='Review only,no manufacture authorization',files=inventory),indent=2)+'\n')
 (OUT/'SHA256SUMS').write_text(''.join(x['SHA256']+'  '+x['path']+'\n'for x in inventory)+sha(OUT/'file-inventory.json')+'  '+str((OUT/'file-inventory.json').relative_to(ROOT))+'\n')
 print('PASS artifact/BOM/placement/native hashes;',len(inventory),'inventoried review/doc files')
if __name__=='__main__':main()
