#!/usr/bin/env python3
"""Review-package/link/hash checks, including preserved R1 provenance."""
import argparse,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote
R=Path(__file__).resolve().parents[1];H=R/'hardware/80m';D=H/'review/M3B-E1'
def report():
 required=['M3B_PCB_LAYOUT_REVIEW.md','M3B_COMPONENT_QUALIFICATION.md','M3B_BRINGUP_PLAN.md','M3B_SAFETY_GATES.md','M3B_EVALUATION_BOM.md','M3B_REVIEW_DECISION.md','M3B_SOURCES.md','M3B_CHECKS.md']
 for name in required:assert '2026-10-14'in(R/'docs'/name).read_text(),name
 paths=[R/'README.md']+list((R/'docs').rglob('*.md'))+list(H.rglob('*.md'));n=0
 for path in paths:
  text=re.sub(r'```.*?```','',path.read_text(),flags=re.S)
  for link in re.findall(r'\[[^\]]*\]\(([^\n)]+)\)',text):
   if re.match(r'[a-z]+:',link):continue
   target,_,anchor=unquote(link.strip('<>')).partition('#');p=(path.parent/target).resolve()if target else path
   assert p.exists(),(str(path.relative_to(R)),link);n+=1
   if anchor:
    anchors={re.sub(r'[^\w\s-]','',h.lower()).replace(' ','-')for h in re.findall(r'^#+\s+(.+)$',p.read_text(),re.M)};assert anchor in anchors,(path,anchor)
 b=json.loads((H/'review/M3A-R1/RF80.electrical.json').read_text());m=json.loads((H/'RF80.electrical.json').read_text());bp={p['ref']:p for p in b['parts']};mp={p['ref']:p for p in m['parts']}
 assert set(bp)<=set(mp)
 pin_changes=[r for r in bp if bp[r]['pins']!=mp[r]['pins']];assert set(pin_changes)=={'D301','R313','C314'},pin_changes
 assert all(mp[r]['pins']==bp[r]['pins']for r in bp if r.startswith('U'))
 cost=json.loads((R/'docs/M3B_COSTS.json').read_text())['scopes'];assert cost['Full']['purchased_parts']==196 and cost['Fox']['purchased_parts']==115
 for scope in cost.values():
  for q in scope['batches'].values():
   assert abs(sum(l['allocated_per_board_eur']for l in q['lines'])-q['per_board_eur'])<.001
   assert all(l['ordered']>=l['needed']and l['ordered']%l['multiple']==0 for l in q['lines'])
 gerbers=list((D/'gerbers').glob('*.g*'));assert len(gerbers)==10 # nine layers and job manifest
 for file in gerbers:
  if file.suffix=='.gbrjob':continue
  text=file.read_text();assert '%TF.FileFunction,'in text and 'M02*'in text,file
 assert (D/'gerbers/RF80-NPTH.drl').read_text().count('T1C3.200')==1
 assert len(list((D/'gerbers').glob('*.drl')))==2
 for name in ['RF80.pdf','assembly.pdf','RF80-3D.png','RF80-3D-top.png','top-copper.svg','bottom-copper.svg','RF80.ipc','RF80.xml','DRC.rpt','ERC.json','DRC.json','RF80-position-full.csv','probe-map.csv','population-map.csv']:
  assert (D/name).stat().st_size>100,name
 files={}
 for p in sorted(H.rglob('*')):
  if p.is_file()and p.name not in('ARTIFACT_HASHES.json','DOCUMENTATION_RESULTS.json')and p.suffix not in('.lck','.bak'):
   files[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return dict(date='2026-10-14',revision='M3B-E1',status='CAD review only; no manufacturing release',markdown_files=len(paths),local_links=n,required_deliverables=len(required),R1_pin_changes=pin_changes,safety_IC_pin_changes=[],files=files)
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();out=D/'ARTIFACT_HASHES.json'
 if args.write and not out.exists():out.write_text('{}\n')
 r=report();s=json.dumps(r,indent=2)+'\n'
 if args.write:out.write_text(s)
 else:assert out.read_text()==s,'Review package hashes stale; run --write only after verified exports'
 print('PASS M3B documentation:',r['markdown_files'],'Markdown;',r['local_links'],'local links;',len(r['files']),'hashes; baseline safety IC nets unchanged')
if __name__=='__main__':main()
