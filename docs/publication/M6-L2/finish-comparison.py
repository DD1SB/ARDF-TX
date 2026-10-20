import collections,copy,difflib,hashlib,json,pathlib,re
E=pathlib.Path('/tmp/ardf-m6-l2-final-evidence');A=pathlib.Path('/home/stefan/src/ardf-tx/hardware/controller/review/M6-L2');B=pathlib.Path('/tmp/ardf-m6-l2-final-reproduction/hardware/controller/review/M6-L2')
j=json.loads((E/'artifact-comparison.json').read_text());notes=[]
def paths(s):return s.replace('/home/stefan/src/ardf-tx','<REPOSITORY>').replace('/tmp/ardf-m6-l2-final-reproduction','<REPOSITORY>')
def elapsed(s):return re.sub(r'Ran 75 tests in [0-9.]+s','Ran 75 tests in <elapsed>s',s)
for row in j['files']:
 if row['category']!=0:continue
 name=row['path'];a=(A/name).read_text();b=(B/name).read_text();aa=paths(a);bb=paths(b)
 if name.endswith('.svg'):
  def norm(s):return re.sub(r'(<title>SVG Image created as [^<]* date )[^<]*(</title>)',r'\1<DATE>\2',s).strip()
  assert norm(aa)==norm(bb),name
  reason='Only SVG creation-title timestamp and/or final newline differs; all geometry/text identical'
 elif name in ['DRC.rpt','drill-report.rpt']:
  def norm(s):return re.sub(r'^(?:\*\* )?Created on [^\n]*\n','',s,flags=re.M)
  assert norm(aa)==norm(bb),name
  reason='Only report creation timestamp differs'
 elif name=='host-test-results.json':
  assert elapsed(aa)==elapsed(bb),name
  reason='Same 75 passing tests and strict C11 commands; elapsed test runtime differs'
 elif name=='electrical-regression.json':
  x=json.loads(aa);y=json.loads(bb);assert x.pop('RF_baseline_files_unchanged')==1538 and y.pop('RF_baseline_files_unchanged')==1534;assert x==y
  reason='Only corrected inventory count: 1534 committed files, four unpublished ignored UI/lock records excluded; all electrical results identical'
 elif name=='L1-L2-change-audit.json':
  x=json.loads(aa);y=json.loads(bb);assert x.pop('frozen_files')==1869 and y.pop('frozen_files')==1865;assert len(y.pop('ignored_unpublished_personal_state'))==4;assert x==y
  reason='Only corrected inventory count and explicit four-file personal-state provenance; native/pad/copper results identical'
 elif name=='RF80-protocol-regression.json':
  x=json.loads(aa);y=json.loads(bb);assert x.pop('source')=='inputs/RF80-interface.xml';assert y.pop('source')=='../M6-L1/inputs/RF80-interface.xml';assert x==y
  reason='Only corrected reference path to committed immutable M6-L1 input; RF80 truth/state/timing results identical'
 elif name=='L2-render-commands.json':
  x=json.loads(aa);y=json.loads(bb);assert len(x)==len(y)==5
  def norm(s):return '\n'.join(v for v in s.splitlines() if not re.fullmatch(r'Rendering: \d+ %|(?:Rendering|Reload) time [\d.]+ s',v))
  for q,z in zip(x,y):
   assert q['command']==z['command'] and q['returncode']==z['returncode']==0
   assert norm(q['stdout'])==norm(z['stdout'])
   assert not z['stderr']
   assert not q['stderr'] or re.fullmatch(r"\d\d:\d\d:\d\d: Error: Failed to remove lock file '/tmp/org.kicad.kicad/instances/kicad-cli-10.0' \(error 2: No such file or directory\)\n",q['stderr'])
  reason='Same renderer commands, models and successful exit codes; progress/runtime differ and historical KiCad temporary-lock cleanup stderr is absent in this run'
 elif name=='fabrication-package-audit.json':
  x=json.loads(aa);y=json.loads(bb);assert x['status']==y['status']=='PASS' and x['native_sha256']==y['native_sha256'];assert not y['remote_upload'] and not y['order']
  for q,z in zip(x['packages'],y['packages']):
   assert q['file']==z['file'];assert [v['path'] for v in q['entries']]==[v['path'] for v in z['entries']]
   rr=next(v for v in j['files'] if v['path']==q['file']);assert rr['category']==2
   assert q['sha256']==rr['archived_sha256'] and z['sha256']==rr['regenerated_sha256']
  reason='Archive/export hashes and byte sizes reflect the separately verified creation-metadata differences; contents, geometry and native hash unchanged'
 elif name in ['inventory.json','SHA256SUMS']:
  for folder in [A,B]:
   inv=json.loads((folder/'inventory.json').read_text());assert len(inv['review_files'])==189
   for r in inv['review_files']:assert hashlib.sha256((folder/r['path']).read_bytes()).hexdigest()==r['sha256']
   expected=''.join(r['sha256']+'  '+r['path']+'\n' for r in inv['review_files']);assert (folder/'SHA256SUMS').read_text()==expected
  if name=='inventory.json':
   old={r['path']:r['sha256'] for r in json.loads(a)['sources']};new={r['path']:r['sha256'] for r in json.loads(b)['sources']}
   changed={k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
   assert changed=={'tools/m6_l2.py','tools/m6_l2_audit.py','tools/m6_l2_frozen.py'},changed
  reason='Both complete 189-file inventories validate; downstream export/log hashes and three explicitly corrected tooling inputs differ, no native source differences'
 else:raise AssertionError(name)
 row.update(category=2,basis=reason);notes.append(dict(path=name,reason=reason,diff=list(difflib.unified_diff(a.splitlines(),b.splitlines(),n=1))))
assert not j['extra_files'];assert all(v['category'] in [1,2] for v in j['files'])
j['counts']=dict(collections.Counter(str(v['category']) for v in j['files']));j['status']='PASS_NO_MANUFACTURING_OR_ELECTRICAL_DIFFERENCE';j['PNG_qualification']='Same 70 native/library/manifest inputs, verified manufacturer model hash and matching renderer commands. Five stochastic ray-traced views differ by at most 0.142 mean channel levels on a 0..255 scale; BOTH top visually compared. Not a physical fit measurement.'
(E/'artifact-comparison.json').write_text(json.dumps(j,indent=2)+'\n');(E/'classification-review.json').write_text(json.dumps(notes,indent=2)+'\n')
print(j['status'],j['counts'])
for v in j['files']:
 if v['path'].endswith('.zip'):print(v['path'],v['entry_count'],v['archived_sha256'],v['regenerated_sha256'])
