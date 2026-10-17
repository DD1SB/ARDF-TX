#!/usr/bin/python3
"""E4R1 candidate paths. E4 and all earlier tracked evidence are immutable."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E4R1'
BASE='920da7b6326764980cd4a9e2d4d2135d6635a5d0';REV='M5B-E4R1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
def gitfile(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
def preserved():
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
 return {x:sha(ROOT/x)for x in tracked if x!='README.md'and not(x.startswith('hardware/2m/')and'/review/'not in x)}
def guard():
 OUT.mkdir(parents=True,exist_ok=True);p=OUT/'preserved-baseline.json';now=preserved()
 if not p.exists():save(p.name,now)
 assert json.loads(p.read_text())==now,'Frozen historical or unrelated tracked file changed'
SOURCE=(110.65,52.5,113.35,57.5)
SOLDER=(110.95,52.5,113.05,57.5)
INNER=[(111.175+.55*c,y)for c in range(4)for y in[53.5,54.5,55.5,56.5]]
SIDE=[(x,52.75+.5*r)for x in[110.5,113.5]for r in range(10)]
NEAR=[(110.8+.8*c,y)for c in range(4)for y in[52.,58.]]
OUTER=[(109.6+.8*c,y+.8*r)for c in range(7)for r in range(4)for y in[49.1,58.5]if not(y==49.1 and r==3 and c in[0,6])]
VIAS=INNER+SIDE+NEAR+OUTER
TOP_RECTS=[(110.2,51.9,113.8,58.1),(109.2,48.7,114.8,51.),(110.,51.,114.,51.9),(109.2,58.1,114.8,61.3)]
WINDOW=(105,47,119,63);BAR=(104.5,28,119.5,72)
# Five separate, easily released windows. No paste printed at nominal holes.
PASTE=[(110.975,a,113.025,z)for a,z in[(52.55,53.3),(53.7,54.3),(54.7,55.3),(55.7,56.3),(56.7,57.45)]]
def via_specs():
 return [(x,y,.3,.8,'joint')for x,y in INNER]+[(x,y,.3,.6,'side')for x,y in SIDE]+[(x,y,.3,.8,'near')for x,y in NEAR]+[(x,y,.5,1.1,'wing')for x,y in OUTER]
