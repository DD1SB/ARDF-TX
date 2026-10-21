"""E6R2 implementation paths and immutable historical/controller/RF80 guard."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E6R2'
START='b48865fed332ced9257559e174f0b6fceaaec096';REV='M5B-E6R2';DATE='2026-10-21'
MM=p.FromMM
def pt(x,y):return p.VECTOR2I(MM(x),MM(y))
def xy(q):return tuple(p.ToMM(v) for v in [q.x,q.y])
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def save(name,data):
 q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def gitfile(path):return subprocess.check_output(['git','show',START+':'+str(path)],cwd=ROOT)
def guard():
 OUT.mkdir(parents=True,exist_ok=True)
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',START],cwd=ROOT,text=True).splitlines()
 def allowed(n):
  return n in ['README.md','docs/README.md','hardware/2m/README.md','hardware/2m/RF2M.electrical.json','hardware/2m/RF2M.kicad_pro','hardware/2m/RF2M.kicad_pcb','hardware/2m/ARDF_2M.kicad_sym'] or (n.startswith('hardware/2m/') and n.count('/')==2 and n.endswith('.kicad_sch'))
 hashes={n:sha(ROOT/n) for n in paths if not allowed(n)}
 f=OUT/'preserved-start.json'
 if f.exists():assert hashes==json.loads(f.read_text()),'Unrelated/historical source modified'
 else:save(f.name,hashes)
 baseline=OUT/'baseline-E5-native.zip'
 if not baseline.exists():
  selected=[n for n in paths if n.startswith('hardware/2m/') and '/review/' not in n and '/archive/' not in n and not n.endswith('.kicad_prl')]
  with zipfile.ZipFile(baseline,'w',zipfile.ZIP_DEFLATED) as z:
   for n in selected:z.writestr(n,gitfile(n))
def fps(b):return {f.GetReference():f for f in b.GetFootprints()}
def manifest():return json.loads((HW/'RF2M.electrical.json').read_text())
