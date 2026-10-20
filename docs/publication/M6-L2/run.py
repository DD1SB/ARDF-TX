import datetime, hashlib, json, pathlib, platform, subprocess, time
root=pathlib.Path('/tmp/ardf-m6-l2-final-reproduction')
out=pathlib.Path('/tmp/ardf-m6-l2-final-evidence')
reference_code="""import hashlib, json, pathlib, urllib.request
cache = pathlib.Path('/tmp/m6l2/references')
cache.mkdir(parents=True, exist_ok=True)
register = json.loads(pathlib.Path('hardware/controller/review/M6-L2/source-register.json').read_text())
for item in register['sources']:
    if not item['sha256']:
        continue
    target = cache / item['file']
    if not target.exists():
        request = urllib.request.Request(item['url'], headers={'User-Agent': 'ARDF-TX engineering reference review'})
        target.write_bytes(urllib.request.urlopen(request, timeout=30).read())
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256'], item['file']
    print('SHA256 PASS', item['file'], item['sha256'])
"""
(out/'validate-references.py').write_text(reference_code)
commands=[['/usr/bin/python3',str(out/'validate-references.py')]]
commands += [['/usr/bin/python3','tools/m6_l2.py',x] for x in ['checks','verify','protocols','protection','usb','powerpaths','dfm','host']]
commands += [['/usr/bin/python3','tools/'+x+'.py'] for x in ['m6_l2_audit','m6_l2_metrics','m6_l2_documents','m6_l2_bom']]
commands += [['/usr/bin/python3','tools/m6_l2_references.py','/tmp/m6l2/references']]
commands += [['/usr/bin/python3','tools/m6_l2_exports.py',x] for x in ['exports','render','package']]
commands += [['/usr/bin/python3','tools/m6_l2.py','manifest']]
rows=[]
for i,cmd in enumerate(commands):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
    stem=f'{i:02d}-'+pathlib.Path(cmd[1]).stem+'-'+(cmd[2] if len(cmd)>2 else 'run').split('/')[-1]
    print('START',stem,flush=True)
    with (out/(stem+'.log')).open('w') as log:
        r=subprocess.run(cmd,cwd=root,stdout=log,stderr=subprocess.STDOUT)
    rows.append(dict(command=cmd,cwd=str(root),started_utc=start,seconds=round(time.monotonic()-t,3),returncode=r.returncode,log=stem+'.log'))
    (out/'execution.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('END',stem,'returncode',r.returncode,'seconds',rows[-1]['seconds'],flush=True)
    print((out/(stem+'.log')).read_text()[-1500:],flush=True)
    if r.returncode: raise SystemExit(r.returncode)
print('ALL DOCUMENTED REPRODUCTION COMMANDS COMPLETED',flush=True)
