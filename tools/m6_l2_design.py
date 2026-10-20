#!/usr/bin/python3
"""Shared paths for M6-L2 native-source verification and exports.

Committed KiCad sources are authoritative. There is no regeneration entrypoint.
"""
import json,subprocess
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'hardware/controller';D=P/'review/M6-L2'
BASE='d94dabd0e40137dc44b2bb94f3707ad4636ca65f'
MM=p.FromMM
def pt(x,y):return p.VECTOR2I(MM(x),MM(y))
def save(n,x):(D/n).write_text(json.dumps(x,indent=2)+'\n')
def source(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
