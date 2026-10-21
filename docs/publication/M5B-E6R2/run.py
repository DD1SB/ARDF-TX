from pathlib import Path
import subprocess,json,os,datetime,sys,hashlib,platform
ROOT=Path('/tmp/ardf-tx-e6r2-main-reproduction-20261021')
OUT=Path('/tmp/m5b-e6r2-main-evidence');OUT.mkdir(exist_ok=True)
V='/tmp/m5b-e6r2-venv/bin/python'
commands=[
 ['/usr/bin/python3','tools/m5b_e6r2_checks.py','checks'],
 ['/usr/bin/python3','tools/m5b_e6r2_verify.py'],
 ['/usr/bin/python3','tools/m5b_e6r2_checks.py','power'],
 ['/usr/bin/python3','tools/m5b_e6r2_ground_audit.py'],
 ['/usr/bin/python3','tools/m5b_e6r2_checks.py','source'],
 ['/usr/bin/python3','tools/m5b_e6r2_checks.py','dfm'],
 [V,'tools/m5b_e6r2_simulation.py'],
 [V,'tools/m5b_e6r2_test_simulation.py'],
 [V,'tools/m5b_e6r2_models.py'],
 [V,'tools/m5b_e6r2_drawings.py'],
 ['/usr/bin/python3','tools/m5b_e6r2_delivery.py','bom'],
 ['/usr/bin/python3','tools/m5b_e6r2_checks.py','exports'],
]
for name,extra in [('RF2M-3D.png',['--rotate','325,0,25']),('RF2M-3D-top.png',[]),('RF2M-3D-bottom.png',['--side','bottom'])]:
 commands.append(['kicad-cli','pcb','render','--width','2000','--height','1550','--quality','high','--background','opaque',*extra,'-o','hardware/2m/review/M5B-E6R2/'+name,'hardware/2m/RF2M.kicad_pcb'])
commands.extend([
 ['/usr/bin/python3','tools/m5b_e6r2_reproduction.py'],
 ['/usr/bin/python3','tools/m5b_e6r2_delivery.py','fabrication'],
 ['/usr/bin/python3','tools/m5b_e6r2_review.py'],
 ['/usr/bin/python3','tools/m5b_e6r2_delivery.py','inventory'],
])
model=Path('/tmp/m5b-e6r2/references/TLV9002-model.zip')
assert hashlib.sha256(model.read_bytes()).hexdigest()=='516e3f6405b699003d94840520966d7599c6c3af37f37c69541f9ed7ae211fe6'
env=os.environ.copy();env['MPLCONFIGDIR']='/tmp/m5b-e6r2-main-mpl'
rows=[]
for i,cmd in enumerate(commands,1):
 name=f'{i:02d}-'+(Path(cmd[1]).stem if cmd[0].endswith('python3')or cmd[0]==V else 'kicad-render')+('-'+cmd[2]if cmd[0].endswith('python3')and len(cmd)>2 else '')+'.log'
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 print(f'START {i}/{len(commands)} '+ ' '.join(cmd),flush=True)
 with (OUT/name).open('wb')as log:
  result=subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
 row=dict(number=i,command=cmd,cwd=str(ROOT),started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),returncode=result.returncode,log=name,log_SHA256=hashlib.sha256((OUT/name).read_bytes()).hexdigest())
 rows.append(row);(OUT/'execution.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(f'END {i} rc={result.returncode}',flush=True)
 if result.returncode:print((OUT/name).read_text(errors='replace')[-6000:],flush=True);sys.exit(result.returncode)
print('ALL 19 DOCUMENTED COMMANDS COMPLETED',flush=True)
