#!/usr/bin/python3
"""M4A local documentation/artifact/scope checks; no network or old-file writes."""
import csv,hashlib,json,re,tarfile
from pathlib import Path
from urllib.parse import unquote
from m4a_design import R,E,P,D,NAME,frozen

def main():
    names=frozen();h=E/'handoff/M4A-E2';docs=list((R/'docs').glob('M4A*.md'))+[P/'README.md',D/'README.md',D/'manufacturing-notes.md',D/'verification.md',D/'routing-history/README.md',h/'README.md',R/'README.md'];links=[];external=set()
    for doc in docs:
        assert doc.is_file(),doc
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
            target=raw.strip().strip('<>')
            if target.startswith(('https://','http://','mailto:')):external.add(target);continue
            target=unquote(target.split('#',1)[0])
            if not target:continue
            p=Path(target)if target.startswith('/')else doc.parent/target;assert p.exists(),('Broken local documentation link',str(doc.relative_to(R)),raw);links.append([str(doc.relative_to(R)),raw])
    archive=h/'ARDF-TX_E2_1245023_source.tar.gz'
    with tarfile.open(archive)as tar:
        for n in names:assert tar.extractfile(n).read()==(R/n).read_bytes(),('Frozen archive mismatch',n)
    copied=[]
    for q in(E/'review/M3B-E2').rglob('*'):
        if q.is_file():
            n=q.relative_to(E/'review/M3B-E2');assert(h/'reference-package'/n).read_bytes()==q.read_bytes();copied.append(str(n))
    for dest in(h,D):
        x=json.loads((dest/'physical-qualification.json').read_text());assert len(x['tests'])==17 and all(t['status']=='NOT_RUN'and t['measurement_record']is None for t in x['tests'])
    gates=json.loads((h/'handoff.json').read_text());assert gates['initial_bare_quantity']==5 and gates['initial_assembled_quantity']==1 and len(gates['authorizations'])==5 and all(t['status']=='NOT_AUTHORIZED'for t in gates['authorizations'])
    c=json.loads((R/'docs/M4A_COSTS.json').read_text());old=json.loads((R/'docs/M3B_E2_COSTS.json').read_text());assert c['PCB_model']['critical_hole_process_surcharge'].startswith('OPEN')
    for n,bb in c['batches'].items():
        for pop,x in bb.items():assert x['component_eur']==old['scopes'][pop]['batches'][n]['per_board_eur']
    for name in[NAME+'.pdf','assembly.pdf','assembly-bottom.pdf']:
        assert(D/name).read_bytes().startswith(b'%PDF'),name
    for name in[NAME+'-3D.png',NAME+'-3D-top.png',NAME+'-3D-bottom.png']:
        assert(D/name).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),name
    for name in['DRC.json','ERC.json','fabrication-audit.json','drc-coverage.json','electrical-equivalence.json','ground-connectivity.json','mechanical-stackup.json','routing-summary.json','population.csv','production-test-pads.csv','mechanical-interface.svg','source-status.json','logic-results.json']:
        assert(D/name).stat().st_size>0,name
    rr=json.loads((D/'logic-results.json').read_text());assert rr['truth_cases']==256 and len(rr['state_scenarios'])==31 and len(rr['timing_corners'])==16
    meta=json.loads((D/'logic-source.json').read_text());assert meta['netlist_sha256']==hashlib.sha256((D/(NAME+'.xml')).read_bytes()).hexdigest()
    for result in json.loads((D/'historical-version-regressions.json').read_text()):assert result['exit_code']==0
    report=dict(date='2026-10-15',status='PASS local documents/identity/cost/artifact/scope checks',local_links_checked=len(links),links=links,external_links_not_rechecked_by_this_offline_tool=sorted(external),external_evidence_record='source-status.json / retained E2/M1-M3 logs, not HTTP PASS invented here',frozen_hardware_files_checked=len(names),archived_hardware_files_checked=len(names),byte_identical_E2_review_copies=len(copied),physical_tests='All17 per design NOT_RUN',purchasing_and_activation_gates='All5 NOT_AUTHORIZED',prices='Component baskets match dated E2 scopes; no quote or achieved PCB saving',original_ADR_files='Not modified or automatically accepted')
    (D/'documentation-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(links),'local links;',len(names),'frozen/archive hardware files;',len(copied),'E2 review copies; costs and all NOT_RUN/NOT_AUTHORIZED gates')
if __name__=='__main__':main()
