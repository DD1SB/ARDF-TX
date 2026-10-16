#!/usr/bin/python3
"""E4 review paths and immutable E3/history guard."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E4';BASE='95f189c6063b1814f89c1b6c528b67831466abc5';REV='M5B-E4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def gitfile(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
def preserved():
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
 return {x:sha(ROOT/x) for x in tracked if x!='README.md' and not(x.startswith('hardware/2m/') and '/review/' not in x)}
def guard():
 OUT.mkdir(parents=True,exist_ok=True);p=OUT/'preserved-baseline.json';now=preserved()
 if not p.exists():save(p.name,now)
 assert json.loads(p.read_text())==now,'Frozen history or unrelated tracked file changed'
INNER=[(110.8+.6*c,52.9+.6*r) for c in range(5) for r in range(8)]
NEAR=[(110.8+.6*c,y) for c in range(5) for y in [52.3,57.7]]
OUTER=[(109.6+.8*c,y+.8*r) for c in range(7) for r in range(4) for y in [49.1,58.5] if not(y==49.1 and r==3 and c in[0,6])]
VIAS=INNER+NEAR+OUTER
TOP_RECTS=[(110.4,51.9,113.6,58.1),(109.2,48.7,114.8,51.0),(110.,51.,114.,51.9),(109.2,58.1,114.8,61.3)]
WINDOW=(105,47,119,63)
BAR=(104.5,28,119.5,72)
