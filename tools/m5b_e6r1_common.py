"""E6R1 analysis paths; every starting tracked source except indexes is immutable."""
import hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware/2m'
OUT=HW/'review/M5B-E6R1'
START='85186204619edec32ad1bb2a3044bb55ea399658'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def save(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')

def guard():
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',START],cwd=ROOT,text=True).splitlines()
    now={n:sha(ROOT/n) for n in names if n not in ['README.md','docs/README.md']}
    path=OUT/'preserved-start.json'
    if path.exists():assert json.loads(path.read_text())==now,'Starting native/history/analysis changed'
    else:save(path.name,now)

def parts():return {p['ref']:p for p in json.loads((HW/'RF2M.electrical.json').read_text())['parts']}
