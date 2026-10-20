#!/usr/bin/python3
"""Replay accepted checks into M6-L2 only, with explicit legitimate ECO changes.
No historical review file is an output. No RF source is mutated.
"""
import sys,types,json,subprocess,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-L2'

def legacy():
    code=(ROOT/'tools/m6_l1.py').read_text().replace('review/M6-L1','review/M6-L2')
    m=types.ModuleType('m6_l2_replay');m.__file__=str(ROOT/'tools/m6_l1.py');exec(compile(code,m.__file__,'exec'),m.__dict__)
    l=m.legacy();orig=l.adapted
    def adapt(name,replace=()):
        extra=[]
        if name=='m6_c1_verify':
            extra=[("'ESP32-S3-WROOM-1-N4'","'ESP32-S3-WROOM-1U-N4'"),
              ("'J3':{'1':'GND','2':'UART_TX','3':'UART_RX'}","'J3':{'1':'GND','2':'REC_TX','3':'REC_RX'}"),
              ("if not n['U10'][pin].startswith('unconnected-'):errors.append('strap:'+pin)","if not (n['U10'][pin].startswith('unconnected-') if pin=='26' else n['U10'][pin]=={'15':'STRAP3','16':'STRAP46'}[pin]):errors.append('strap:'+pin)"),
              ("(ROOT/'firmware/controller_hw/pins.h').write_text(h)","# Read-only replay: keep accepted generated GPIO/pack-ID header unchanged")]
            extra.append(("json.loads((D/'frozen-RF-files.json').read_text()) if (D/'frozen-RF-files.json').exists() else None",
                          "__import__('m6_l2_frozen').committed_frozen(ROOT,D/'frozen-RF-files.json')"))
        if name=='m6_c1_analysis':extra=[('M6-C1R1','M6-L2')]
        if name=='m6_c1_dfm':extra=[("'revision':'M6-C1'", "'revision':'M6-L2'"), ('REV="M6-C1"', 'REV="M6-L2"')]
        if name=='m6_c1_rf_protocols':
            extra=[("'inputs/RF80-interface.xml'", "'../M6-L1/inputs/RF80-interface.xml'")]
        result=orig(name,[*replace,*extra])
        if name=='m6_c1_dfm':
            result.PROFILE['revision']='M6-L2'
            result.mod.REV='M6-L2'
        return result
    l.adapted=adapt
    return l

def adapted(name,replace=()):return legacy().adapted(name,replace)
def replay(action):
    # Read-only source evidence copied into the new review, never refreshed in
    # the historical directory. Frozen RF checks are checked against new CAD.
    for name in ['RF-interface-contracts.json','frozen-RF-files.json']:
        f=P/'review/M6-L1'/name
        if not (D/name).exists():shutil.copyfile(f,D/name)
    if action in ['protection','usb']:
        name='m6_c1r1_electrical' if action=='protection' else 'm6_c1r1_usb'
        code=(ROOT/'tools'/(name+'.py')).read_text().replace('review/M6-C1R1','review/M6-L2').replace('import m6_c1r1 as wrapper','import m6_l2 as wrapper')
        m=types.ModuleType(name+'_l2');m.__file__=str(ROOT/'tools'/(name+'.py'));exec(compile(code,m.__file__,'exec'),m.__dict__);m.main();return
    # Prevent the C1R1 verify wrapper from rewriting a historical GPIO header.
    if action=='verify':
        adapted('m6_c1_verify',[("'5':'PACK_ID_RAW','6':'PACK_ID_ADC'","'5':'PACK_ID_SAFE','6':'PACK_ID_ADC'")]).main();return
    l=legacy();sys.argv=[sys.argv[0],action]+sys.argv[2:];l.main()

def host():
    logs=[]
    for cmd in [['/usr/bin/python3','-m','unittest','discover','-s','.','-p','test_*.py','-v'],
                ['cc','-std=c11','-Wall','-Wextra','-Werror','contract.c','test_contract.c','-lm','-o','/tmp/m6-l2-contract'],['/tmp/m6-l2-contract']]:
        r=subprocess.run(cmd,cwd=ROOT/'firmware/controller_hw',capture_output=True,text=True)
        logs.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
        (D/'host-test-results.json').write_text(json.dumps(dict(status='PASS' if all(x['returncode']==0 for x in logs) else 'FAIL',commands=logs,physical='NOT_RUN'),indent=2)+'\n')
        print(r.stdout[-2000:]+r.stderr[-4000:]);assert r.returncode==0

def manifest():
    rows=[]
    for f in sorted(D.rglob('*')):
        if f.is_file() and f.name not in ['inventory.json','SHA256SUMS']:
            rows.append(dict(path=str(f.relative_to(D)),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    sources=[]
    for folder in [P,ROOT/'tools',ROOT/'firmware/controller_hw',ROOT/'docs']:
        for f in sorted(folder.rglob('*') if folder==P else folder.glob('*')):
            if not f.is_file() or 'review' in f.relative_to(folder).parts or '__pycache__' in str(f):continue
            if f.suffix in ['.kicad_prl','.lck']:continue
            if folder==ROOT/'tools' and not f.name.startswith('m6'):continue
            if folder==ROOT/'docs' and not f.name.startswith('M6_L2'):continue
            sources.append(dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    for f in [ROOT/'README.md',ROOT/'THIRD_PARTY_NOTICES.md',ROOT/'docs/README.md']:
        sources.append(dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    (D/'inventory.json').write_text(json.dumps(dict(review_files=rows,sources=sources),indent=2)+'\n')
    (D/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in rows))

if __name__=='__main__':
    action=sys.argv[1]
    if action=='host':host()
    elif action=='manifest':manifest()
    elif action in ['capture','sync','route','review']:raise SystemExit('Edit the native KiCad sources; use L2 audit/export commands. No broad regeneration.')
    else:
        replay(action)
        if action=='checks':
            f=D/'CAD-results.json';j=json.loads(f.read_text())
            j['native_sha256']=hashlib.sha256((P/'CTRL.kicad_pcb').read_bytes()).hexdigest()
            f.write_text(json.dumps(j,indent=2)+'\n')
