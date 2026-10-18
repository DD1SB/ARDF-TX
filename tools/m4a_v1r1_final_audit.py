#!/usr/bin/python3
"""Final native/export/test-package consistency. No physical qualification inferred."""
import re,zipfile,xml.etree.ElementTree as ET,csv,math
from m4a_v1r1_common import *
def main():
 frozen();board=P/(NAME+'.kicad_pcb');b=pcb.LoadBoard(str(board));native={};ipc={}
 for f in b.GetFootprints():
  if f.GetReference().startswith('H'):continue
  for a in f.Pads():native[(f.GetReference(),a.GetNumber())]=dict(net=a.GetNetname(),pos=[pcb.ToMM(v)for v in a.GetPosition()])
 for line in(D/(NAME+'.ipc')).read_text().splitlines():
  z=re.match(r'^(?:317|327)(\S+)\s+(\S+)\s+-(\d+)\s+.*?X([+-]\d+)Y([+-]\d+)',line)
  if z:ipc[(z[2],z[3])]=dict(net=z[1],pos=[int(z[4])*.00254,-int(z[5])*.00254])
 assert set(ipc)==set(native),(len(native),len(ipc),set(native)^set(ipc));maxerror=0
 for k,x in native.items():
  got=ipc[k];want='N/C'if not x['net']else x['net'][-14:].upper();assert got['net']==want,(k,got,want)
  dist=max(abs(a-z)for a,z in zip(x['pos'],got['pos']));maxerror=max(maxerror,dist);assert dist<=.001271,(k,dist)
 assert len(native)==604
 emitted={}
 for x in native.values():
  if x['net']:
   key=x['net'][-14:].upper();assert key not in emitted or emitted[key]==x['net'],('AmbiguousIPCnettruncation',key);emitted[key]=x['net']
 tree=ET.parse(D/(NAME+'.xml'));nn={(a.get('ref'),a.get('pin')):n.get('name')for n in tree.findall('nets/net')for a in n.findall('node')}
 assert all(nn.get(k,'')==v['net']for k,v in native.items())
 for file in ['finished-hole-audit.json','V1-layout-preservation.json','JLCPCB-DFM.json']:
  x=json.loads((D/file).read_text());assert x['native_sha256']==sha(board),('Stale native evidence',file)
 drc=json.loads((D/'DRC.json').read_text());erc=json.loads((D/'ERC.json').read_text());assert drc['kicad_version']=='10.0.6'and not drc['violations']and not drc['unconnected_items']and not drc['schematic_parity']and not drc['ignored_checks'];assert not [v for s in erc['sheets']for v in s['violations']]
 jlc=json.loads((D/'JLCPCB-DFM.json').read_text());assert not jlc['errors']
 logic=json.loads((D/'logic-results.json').read_text());eq=json.loads((D/'electrical-equivalence.json').read_text());assert logic['truth_cases']==256 and len(logic['state_scenarios'])==31 and len(logic['timing_corners'])==16;assert eq['physical_pad_memberships']==604 and len(eq['critical_devices'])==55 and len(eq['negative_cases_rejected'])==12
 negativecounts={'existing':12}
 for file,key in [('hole-regression.json','tests'),('DFM-regression.json','mutations'),('interface-regression.json','mutations')]:
  x=json.loads((D/file).read_text());assert x['status']=='PASS';negativecounts[file]=len(x[key])
 assert sum(negativecounts.values())==40
 expected={'FULL':196,'FOX_ONLY':115}
 for pop,n in expected.items():
  rr=list(csv.DictReader((D/('BOM-'+pop+'.csv')).open()));assert len(rr)==n*4 and {int(z['batch'])for z in rr}=={1,5,10,20}
 plan=json.loads((D/'physical-qualification.json').read_text());assert len(plan['tests'])==17 and all(x['status']=='NOT_RUN'and x['measurement_record']is None for x in plan['tests'])
 matrix=json.loads((D/'three-board-order-readiness.json').read_text());archives=[]
 for x in matrix['records']:
  f=D/x['archive'];assert sha(f)==x['sha256']
  with zipfile.ZipFile(f)as z:
   assert len(z.namelist())==11 and not any('/'in n for n in z.namelist())
   for a in x['entries']:assert z.read(a['name'])==(R/a['source']).read_bytes()
  archives.append(dict(board=x['PCB'],archive=x['archive'],sha256=sha(f),entries=11))
 # Actual proposed specification must contain no special process demand.
 profile=json.loads((D/'JLCPCB-standard-profile.json').read_text());assert profile['order']['quantity']==5 and profile['order']['individual_boards']and all(not profile['order'][k]for k in ['controlled_impedance','special_drilling','press_fit','premium_via_treatment'])
 for textfile in ['README.md','manufacturing-notes.md','BRINGUP.md','REPRODUCE.md','CHANGE_REPORT.md','verification.md']:
  assert(D/textfile).stat().st_size>100
 for n in [NAME+'.pdf','assembly.pdf','assembly-bottom.pdf']:assert(D/n).read_bytes().startswith(b'%PDF')
 for n in [NAME+'-3D.png',NAME+'-3D-top.png',NAME+'-3D-bottom.png']:assert(D/n).read_bytes().startswith(b'\x89PNG')
 report=dict(revision=REV,date=DATE,status='PASS_NONPHYSICAL_REVIEW_GATES',native_sha256=sha(board),logical_and_IPC_pin_nets_verified=len(native),maximum_IPC_coordinate_quantization_mm=maxerror,IPC_netname_encoding='KiCad IPC-D356 emits uppercase rightmost14characters; full logical names preserved in XML. All distinct names checked against truncation collisions; named no-connect pads retain individual nets, empty nets emit N/C.',ERC=dict(errors=0,warnings=0,inherited_informational_defaults=3),DRC=dict(errors=0,warnings=0,unrouted=0,parity=0,exclusions=0,ignored_checks=0),electrical=dict(manufacturer_devices=55,logic_cases=256,states=31,timing_corners=16,negative_mutations=negativecounts),archives=archives,physical='17gatesNOT_RUN; no authorization/qualification inferred',prototype_transition='PROPOSED_PENDING_REVIEW, original M4A E2-first restriction preserved',other_designs='1421 frozen evidence files and every tracked E2 hardware file verified unchanged',source_commit='Record final Git commit externally; source and artifact hashes identify exact candidate without circular self-hash')
 save('final-verification.json',report);print('PASS current CAD,604native/XML/IPC pads,40negativecases,3isolated11-fileZIPs; physicalNOT_RUN')
if __name__=='__main__':main()
