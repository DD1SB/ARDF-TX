#!/usr/bin/python3
"""Compact RF2M candidate. Frozen RF2M/RF80/controller evidence is never output."""
from pathlib import Path
import hashlib,json,subprocess
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E5';BASE='2f9982c1b72cd97ba4dad6c992143032b309cca7';START='f86684b9ef45eec3ca4ce52edcb62896a847f1d7';REV='M5B-E5';DATE='2026-10-18'
DX=-20.;DY=0.
from m5b_e3_common import LENGTHS,WIDTH,POWER_INPUT,POWER_RAIL,aliases
MM=p.FromMM
def pt(x,y):return p.VECTOR2I(MM(x),MM(y))
def xy(v):return(p.ToMM(v.x),p.ToMM(v.y))
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def save(name,data):
 q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def gitfile(path,revision=BASE):return subprocess.check_output(['git','show',revision+':'+str(path)],cwd=ROOT)
def preserved():
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',START],cwd=ROOT,text=True).splitlines()
 return {n:sha(ROOT/n)for n in paths if n!='README.md'and not(n.startswith('hardware/2m/')and'/review/'not in n)}
def guard():
 OUT.mkdir(parents=True,exist_ok=True);f=OUT/'preserved-baseline.json';now=preserved()
 if f.exists():assert json.loads(f.read_text())==now,'Historical or unrelated tracked source changed'
 else:save(f.name,now)
def translate_board(b,dx,dy):
 v=pt(dx,dy)
 for f in b.GetFootprints():f.Move(v)
 for t in b.GetTracks():t.Move(v)
 for g in b.GetDrawings():g.Move(v)
 for z in b.Zones():z.Move(v)
 return b
