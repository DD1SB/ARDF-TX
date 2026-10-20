"""M5B-E6 evidence paths. No historical package is an output."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / 'hardware/2m'
OUT = HW / 'review/M5B-E6'
BASE = '256c64888b680f5152e92f035e2ea0676a83630a'
REV = 'M5B-E6'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def frozen():
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
    return {n: sha(ROOT/n) for n in names if n.startswith(('hardware/controller/', 'hardware/80m/', 'hardware/2m/review/', 'docs/M5B_E5'))}


def guard():
    path = OUT/'preserved-baseline.json'
    now = frozen()
    if path.exists():
        assert json.loads(path.read_text()) == now, 'Protected controller/RF80/RF2M historical evidence changed'
    else:
        save(path.name, now)


def parts():
    return {p['ref']: p for p in json.loads((HW/'RF2M.electrical.json').read_text())['parts']}


def number(value):
    return float(value[:-1])*{'k': 1000, 'n': 1e-9, 'u': 1e-6, 'p': 1e-12}[value[-1]] if value[-1] in 'knup' else float(value)
