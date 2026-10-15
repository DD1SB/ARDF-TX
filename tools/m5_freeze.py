#!/usr/bin/python3
"""Freeze/check the existing HF/controller/reference work without modifying it."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'hardware/2m/review/M5A-R0';F=D/'preserved-baseline.json'
def snapshot():
    paths=[R/'README.md']+list((R/'hardware/80m').rglob('*'))+list((R/'docs/decisions').glob('*'))
    return{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(paths)if p.is_file()and p.suffix not in('.kicad_prl','.pyc')}
def check():
    old=json.loads(F.read_text());now=snapshot();assert old['files']==now,'Existing RF80/ADR/README data changed during M5';return len(now)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--initialize',action='store_true');arg=a.parse_args()
    if arg.initialize:
        assert not F.exists(),'Never replace the starting snapshot';F.write_text(json.dumps(dict(date='2026-10-15',classification='Existing 80m, decision and M4A README preservation; not hardware validation',files=snapshot()),indent=2)+'\n')
    print('PASS frozen files',check())
