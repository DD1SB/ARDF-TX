#!/usr/bin/python3
"""Read-only technical/document checks plus a new M5 review inventory; no CAD mutation."""
import csv,hashlib,json,re,subprocess,sys
from pathlib import Path
from m5_freeze import check as freeze
from m5_2m_verify import main as verify
R=Path(__file__).resolve().parents[1];H=R/'hardware/2m';D=H/'review/M5A-R0'
NAMES=['PA_SELECTION','AM_DESIGN','POWER_ARCHITECTURE','CONTROLLER_INTERFACE','BOM','SCHEMATIC_REVIEW','TEST_PLAN','REVIEW_DECISION']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 verify()
 docs=[R/'docs'/('M5_2M_'+n+'.md')for n in NAMES]+[R/'docs/M5_2M_SOURCES.md',R/'docs/M5_2M_TRACEABILITY.md']
 assert all(p.is_file()for p in docs)
 links=0
 for p in docs+[H/'README.md',D/'README.md']:
  for dest in re.findall(r'\]\(([^\s)]+)',p.read_text()):
   if dest.startswith(('http:','https:','mailto:','#')):continue
   target=(p.parent/dest.split('#')[0]).resolve();assert target.exists(),(p,dest);links+=1
 positions=json.loads((H/'RF2M.electrical.json').read_text())['parts'];parts={p['ref']:p for p in positions}
 assert parts['Q501']['mpn']=='PD55008-E'and parts['Q401']['mpn']=='D45H11'
 assert parts['C605']['value']=='56p'and parts['C610']['value']=='47p'and parts['L608']['value']=='24n'
 assert parts['U207']['population']=='NORMAL'and parts['R519']['population']=='TRAIN_ONLY'
 assert parts['L302']['value']=='4.7u'and parts['C409']['value']=='100u'
 assert parts['C615']['pins']=={'1':'DRIVER_PAD','2':'DRIVER_IN'}
 rows=list(csv.DictReader((D/'RF2M_BOM.csv').open()));costs=json.loads((D/'costs.json').read_text())
 for x in costs['summary']:
  selected=[p for p in rows if p['variant']==x['variant']and int(p['fleet'])==x['fleet']]
  assert len(selected)==x['fitted_physical'];assert abs(sum(float(p['per_board_net_eur'])for p in selected)-x['component_allowance_net_eur'])<1e-8
  for p in selected:
   assert int(p['fleet_component_demand'])==sum(y['mpn']==p['mpn']for y in selected)*x['fleet']
  refs={p['ref']for p in selected}
  if x['variant']=='TRAIN_ONLY':assert {'R517','R518','R519','U701','Q701'}<=refs and not({'Q501','Q401','U501','U302','U301','U303','U207','C208'}&refs)
  else:assert 'U207'in refs and'R519'not in refs
 c=json.loads((D/'calculations.json').read_text());assert len(c['packs'])==60 and len(c['sensitivity'])==144
 assert abs(c['erp']['conducted_carrier_w']-1.2589254117941673)<1e-12
 assert abs(c['erp']['pep_m80_w']-4.078918334213102)<1e-12
 assert any(x['current_trip_risk']for x in c['sensitivity'])
 # Read explicit physical test ledger from the plan; never promote an analysis to measured PASS.
 gates=[]
 for line in(R/'docs/M5_2M_TEST_PLAN.md').read_text().splitlines():
  if re.match(r'\| G\d+ ',line):
   fields=[x.strip()for x in line.strip('|').split('|')];assert fields[-1]=='NOT_RUN';gates.append(dict(id=fields[0].split()[0],name=fields[0],status='NOT_RUN',acceptance=fields[2]))
 assert len(gates)==16
 (D/'qualification.json').write_text(json.dumps(dict(revision='M5A-R0',physical_measurements=0,gates=gates),indent=2)+'\n')
 tools={}
 for name,cmd in [('kicad',['kicad-cli','version']),('python',['/usr/bin/python3','--version']),('ngspice',['ngspice','--version'])]:
  p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0;tools[name]=(p.stdout+p.stderr).strip()
 tools.update(scope='Schematic only; no PCB/DRC/manufacturing',git_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),m4a_state='Pre-existing working-tree design preserved by SHA256 snapshot',frozen_files=freeze())
 (D/'tool-versions.json').write_text(json.dumps(tools,indent=2)+'\n')
 result=dict(date='2026-10-15',required_documents=len(NAMES),additional_source_trace_documents=2,local_links_checked=links,physical_tests_not_run=len(gates),variant_baskets=len(costs['summary']),candidate_parts=len(positions),status='PASS limited CAD/document/calculation checks; OPEN hardware/package gates retained')
 (D/'review-checks.json').write_text(json.dumps(result,indent=2)+'\n')
 paths=list(H.rglob('*'))+docs+list((R/'tools').glob('m5*.py'))+list((R/'analysis/m5_2m').rglob('*'))
 inventory={str(p.relative_to(R)):sha(p)for p in sorted(set(paths))if p.is_file()and p.suffix not in('.pyc','.kicad_prl')and p.name not in('SHA256SUMS','file-manifest.json')}
 (D/'file-manifest.json').write_text(json.dumps(dict(date='2026-10-15',revision='M5A-R0',status='REVIEW ONLY / NOT HARDWARE VALIDATION',files=inventory),indent=2)+'\n')
 (D/'SHA256SUMS').write_text(''.join(v+'  '+k+'\n'for k,v in inventory.items()))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
