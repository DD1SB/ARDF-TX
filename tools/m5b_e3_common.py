#!/usr/bin/python3
"""M5B-E3 paths, immutable-history guard and analytical line model."""
import hashlib,json,subprocess,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E3';BASE='2ca4c8e';REV='M5B-E3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):
 (OUT/name).parent.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def gitfile(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
def preserved():
 from m5b_design import preserved as old
 d=old();d.pop('README.md',None)
 for rev in ['M5B-E1','M5B-E2']:
  for p in (HW/'review'/rev).rglob('*'):
   if p.is_file():d[str(p.relative_to(ROOT))]=sha(p)
 for pattern in ['M5B_E1_*','M5B_E2_*']:
  for p in (ROOT/'docs').glob(pattern):
   if p.is_file():d[str(p.relative_to(ROOT))]=sha(p)
 for p in (ROOT/'tools').glob('m5b*.py'):
  if not p.name.startswith('m5b_e3'):d[str(p.relative_to(ROOT))]=sha(p)
 tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines())
 return dict(sorted((k,v)for k,v in d.items()if k in tracked))
def guard():
 OUT.mkdir(exist_ok=True);f=OUT/'preserved-baseline.json'
 if not f.exists():save(f.name,preserved())
 assert json.loads(f.read_text())==preserved(),'Historical/RF80/M4A file changed'
from m5b_footprints import microstrip
H=1.50;T=.035;ER=4.5
# Nominal1.6mm model includes70um Cu and30um mask;ordinary process tolerances
# are swept,not negotiated as a custom core specification.
def width50(h=H,t=T,er=ER):
 lo,hi=.1,8
 for _ in range(70):
  w=(lo+hi)/2
  if microstrip(w,h,t,er)[0]>50:lo=w
  else:hi=w
 return (lo+hi)/2
WIDTH=round(width50(),3);LENGTH_SCALE=math.sqrt(microstrip(1.102,.64,.07,4.3)[1]/microstrip(WIDTH,H,T,ER)[1])
LENGTHS={f'TL{r}':round(l*LENGTH_SCALE,4)for r,l in zip(range(603,610),[6.23,6.62,5.8,2.2,11,12.4,2])}
POWER_INPUT={'BAT_RAW','BAT_FUSED','VIN_PROT','VIN_CONV'}
POWER_RAIL={'VBOOST','VBUCK','VREG_RAW','VREG_SWITCH','VMOD','VPA'}

def aliases():
 parts=json.loads((HW/'RF2M.electrical.json').read_text())['parts'];par={}
 def find(a):
  par.setdefault(a,a)
  if par[a]!=a:par[a]=find(par[a])
  return par[a]
 for f in parts:
  if f['ref'].startswith('TL'):
   a,z=f['pins'].values();par[find(z)]=find(a)
 return{a:find(a)for a in par}
