"""Replay unchanged E5 checks ONLY in a disposable clone, never frozen evidence.

Output path/preservation start are the only harness adaptations. Native checks,
thresholds, package maps, electrical and DFM mutations are not changed.
"""
import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
import m5b_e5_common as c

BASE='256c64888b680f5152e92f035e2ea0676a83630a'


def main():
    assert str(c.ROOT).startswith('/tmp/'), 'Disposable clone required; no active or historical output writes'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.ROOT,text=True).strip()==BASE
    action=sys.argv[1]
    c.OUT=c.HW/'review/M5B-E6/baseline-regression'
    def preserved():
        names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=c.ROOT,text=True).splitlines()
        return {n:c.sha(c.ROOT/n) for n in names if n.startswith(('hardware/controller/','hardware/80m/','hardware/2m/review/'))}
    c.preserved=preserved
    c.guard()
    (c.OUT/'development').mkdir(exist_ok=True)
    for name in ['JLCPCB-standard-profile.json','development/E4R1-baseline.kicad_pcb']:
        shutil.copyfile(c.HW/'review/M5B-E5'/name,c.OUT/name)
    names=subprocess.check_output(['git','ls-files','hardware/2m/RF2M.*'],cwd=c.ROOT,text=True).splitlines()
    original={n:c.sha(c.ROOT/n) for n in names}
    if action in ['checks','verify','models','dfm','thermal']:
        mod=importlib.import_module('m5b_e5');sys.argv=[sys.argv[0],action];mod.main()
    else:
        mod=importlib.import_module('m5b_e5_'+action);mod.main()
    final={n:c.sha(c.ROOT/n) for n in names}
    assert original==final, ('Replay changed native inputs',action)
    c.guard()
    c.save('replay-'+action+'.json',dict(status='PASS_UNCHANGED_E5_BASELINE_REPLAY',starting_commit=BASE,
        action=action,adaptations='Output path only; preservation guard starts at current public baseline rather than pre-publication RF80 commit',
        native_sha256=original,not_an_E6_CAD_candidate=True))


if __name__=='__main__':main()
