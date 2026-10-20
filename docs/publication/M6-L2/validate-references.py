import hashlib, json, pathlib, urllib.request
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
