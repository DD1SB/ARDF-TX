#!/usr/bin/python3
"""Final read-only design/document checks plus R1 inventories; never writes historical data."""
import csv,hashlib,json,re,subprocess,copy
from pathlib import Path
from m5a_r1_verify import main as verify,load,revised_checks,freeze
from m5a_r1_design import parse,walk
R=Path(__file__).resolve().parents[1];H=R/'hardware/2m';O=H/'review/M5A-R1'
NAMES=['ST_REFERENCE_AUDIT','RF_SELECTION','AM_FEASIBILITY','POWER_THERMAL','COST_DELTA','SCHEMATIC_REVIEW','PA_TEST_PLAN','REVIEW_DECISION']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 verify()
 saved=json.loads((O/'r0-preservation.json').read_text())
 for name,digest in saved['files'].items():assert sha(R/name)==digest,('R0 changed',name)
 assert subprocess.check_output(['git','rev-parse','m5a-r0'],text=True).strip().startswith(saved['commit'])
 parts,nets=load();changed=copy.deepcopy(parts);changed['Q501']['footprint']='UNVERIFIED_GENERIC_POWER_PAD'
 try:revised_checks(changed,nets)
 except AssertionError:pass
 else:raise AssertionError('Invented final footprint accepted')
 docs=[R/'docs'/('M5A_R1_'+name+'.md')for name in NAMES]+[R/'docs/decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md',H/'README.md',O/'README.md']
 links=0
 for path in docs:
  assert path.is_file()
  for url in re.findall(r'\]\(([^\s)]+)',path.read_text()):
   if url.startswith(('https:','http:','mailto:','#')):continue
   assert(path.parent/url.split('#')[0]).resolve().exists(),(path,url);links+=1
 active={'RF2M.kicad_sch'}
 for sh in walk(parse((H/'RF2M.kicad_sch').read_text()),'sheet'):
  for p in sh:
   if isinstance(p,list)and p[:2]==['property','Sheetfile']:active.add(p[2])
 assert active=={p.name for p in H.glob('*.kicad_sch')},'Orphan/missing active sheet'
 for name in active:assert'M5A-R1'in(H/name).read_text()
 assert not list(H.rglob('*.kicad_pcb'))and not list(H.rglob('*.gbr'))
 # Existing footprint existence and physical pad inventory; geometry is NOT thereby qualified.
 fps=[]
 for ref,p in parts.items():
  fp=p['footprint']
  if not fp:continue
  lib,name=fp.split(':',1);path=Path('/usr/share/kicad/footprints')/(lib+'.pretty')/(name+'.kicad_mod')
  assert path.is_file(),('Missing footprint file',ref,fp)
  pads=sorted(set(str(n[1])for n in walk(parse(path.read_text()),'pad')))
  needed={str(n)for n in p['pins']if p['pins'][n]is not None}
  assert needed<=set(pads),('Missing required footprint pad',ref,needed,pads)
  fps.append(dict(ref=ref,footprint=fp,pads=pads,status='LIBRARY_PAD_INVENTORY_ONLY_NOT_MECHANICAL_QUALIFICATION'))
 (O/'footprint-pad-inventory.json').write_text(json.dumps(fps,indent=2)+'\n')
 rows=list(csv.DictReader((O/'RF2M_BOM.csv').open()));costs=json.loads((O/'costs.json').read_text())
 for s in costs['summary']:
  rr=[x for x in rows if x['variant']==s['variant']and int(x['fleet'])==s['fleet']]
  assert len(rr)==s['fitted_physical']
  assert abs(sum(float(x['per_board_net_eur'])for x in rr)-s['component_allowance_net_eur'])<1e-8
  for x in rr:assert int(x['fleet_component_demand'])==s['fleet']*sum(y['mpn']==x['mpn']for y in rr)
  if s['variant']=='TRAIN_ONLY':assert not({'Q501','Q401','U501','U303','U302','U301'}&{x['ref']for x in rr})
 baskets=json.loads((O/'comparison-baskets.json').read_text());br=list(csv.DictReader((O/'comparison-baskets.csv').open()))
 for s in baskets['summary']:
  rr=[x for x in br if x['basket']==s['basket']and int(x['fleet'])==s['fleet']]
  assert len(rr)==s['parts']and abs(sum(float(x['unit_net_eur'])for x in rr)-s['net_eur'])<1e-8
 calc=json.loads((O/'calculations.json').read_text());assert len(calc['endurance'])==60 and len(calc['sensitivity'])==288
 assert abs(calc['erp']['pep80_w']-4.078918334213102)<1e-12
 assert any(x['current_trip_risk']for x in calc['sensitivity'])
 gates=json.loads((O/'physical-gates.json').read_text());assert all(x==dict(status='NOT_RUN',evidence=None)for x in gates.values())
 tools={}
 for n,cmd in [('kicad',['kicad-cli','version']),('python',['python3','--version']),('pdfinfo',['pdfinfo',str(O/'RF2M.pdf')])]:
  p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0;tools[n]=(p.stdout+p.stderr).strip()
 assert re.search(r'Pages:\s+16\b',tools['pdfinfo'])
 tools['git_baseline']=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
 tools['R0_tag']='m5a-r0';tools['cad_scope']='Schematic only; no PCB/DRC/Gerbers';tools['ngspice']='NOT_RUN for R1; analytical model only'
 (O/'tool-versions.json').write_text(json.dumps(tools,indent=2)+'\n')
 result=dict(status='PASS limited CAD/netlist/cost/document checks; NO_GO physical package/reference trace',documents=len(NAMES),local_links_checked=links,active_sheets_including_root=len(active),pdf_pages=16,R0_files_preserved=len(saved['files']),HF_baseline_files_preserved=freeze(),physical_gates_not_run=len(gates),footprint_pad_inventory_refs=len(fps),negative_final_footprint_assertion='PASS: unverified numeric land rejected',pcb_created=False,procurement=False)
 (O/'review-checks.json').write_text(json.dumps(result,indent=2)+'\n')
 paths=[p for p in H.iterdir()if p.is_file()]+[p for p in O.rglob('*')if p.is_file()]+docs+list((R/'tools').glob('m5a_r1*.py'))+list((R/'analysis/m5a_r1').rglob('*'))
 inventory={str(p.relative_to(R)):sha(p)for p in sorted(set(paths))if p.is_file()and p.suffix not in('.pyc','.kicad_prl')and p.name not in('SHA256SUMS','file-manifest.json')}
 (O/'file-manifest.json').write_text(json.dumps(dict(revision='M5A-R1',status='REVIEW CANDIDATE, NOT RELEASED',files=inventory),indent=2)+'\n')
 (O/'SHA256SUMS').write_text(''.join(digest+'  '+name+'\n'for name,digest in inventory.items()))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
