#!/usr/bin/python3
"""Seal/check the R3 review artifacts, never a manufacturing release."""
import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path
from m5a_r3_design import ROOT,DEST,OUT

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args()
    mf=OUT/'file-manifest.json'
    if a.check:
        manifest=json.loads(mf.read_text())
        for name,h in manifest['files'].items():assert digest(ROOT/name)==h,name
        r=subprocess.run(['sha256sum','-c',str(OUT/'SHA256SUMS')],cwd=ROOT,capture_output=True,text=True)
        assert r.returncode==0,r.stderr+r.stdout
        print('PASS',len(manifest['files']),'artifact/source hashes and SHA256SUMS; review only, no PCB')
        return
    (OUT/'README.md').write_text('''# M5A-R3 review package — NO_GO for PCB commitment

The active project is a complete, editable **private DL3BBX-derived candidate schematic**, not a qualified/buildable production design. No RF2M PCB, DRC report, Gerbers or3D manufacturing files exist: exact RF-device supply/manufacturer and physical landings are unresolved. Upper-power sineAM headroom is not proved. No purchases, fabrication, assembly or RF operation occurred.

Start with [review decision](../../../../docs/M5A_R3_REVIEW_DECISION.md), [reference audit](../../../../docs/M5A_R3_PROVEN_TRANSMITTER_AUDIT.md), [selection/controller contract](../../../../docs/M5A_R3_RF_SELECTION.md), [AM/power](../../../../docs/M5A_R3_AM_AND_POWER.md), [modernization](../../../../docs/M5A_R3_COMPONENT_MODERNIZATION.md), [BOM](../../../../docs/M5A_R3_BOM.md) and [one-board build plan](../../../../docs/M5A_R3_BUILD_PLAN.md).

CAD: [native project](../../RF2M.kicad_pro), [schematic](../../RF2M.kicad_sch), [PDF](RF2M.pdf), [netlist](RF2M.net.xml), [manifest](../../RF2M.electrical.json). The three RF pages are wired circuit drawings; named nets cross supply/control sheets. All hardware measurements are NOT_RUN.

Evidence: erc.json; verification.json (static logic, state, pin/value mutation tests); pinout-audit.json; final-checks.json; sources.json (including native-Eagle import failure); fallback-r1-* read-only regression; costs.json and per-reference RF2M_BOM.csv; RF/thermal/endurance CSV/JSON models. Footprint warnings are visible, not waived. Missing custom-symbol landings are separately listed because ERC does not warn on all of them.

R1 remains at Git tag m5a-r1 (4785057) and ../../archive/M5A-R1/. R0/R1/R2 review exports, RF80/M4A/controller/accepted ADRs remain unchanged; preserved-baseline.json records the starting467-file snapshot. Starting Git HEAD was1d8d88f; this package describes the working-treeR3 revision, not a claimed new commit.

Reproduction commands are in [RF2M README](../../README.md). Run `python3 tools/m5a_r3_package.py` after exports/checks to reseal; then `python3 tools/m5a_r3_package.py --check` from the repository root. SHA256SUMS paths are root-relative. Manufacturer and third-party source permissions remain separate from project code licensing; see ../../LICENSE-REFERENCE-DL3BBX.md.
''')
    versions={}
    for name,cmd in [('KiCad',['kicad-cli','--version']),('Python',['python3','--version']),('Poppler',['pdftotext','-v']),('Git',['git','rev-parse','HEAD'])]:
        r=subprocess.run(cmd,capture_output=True,text=True);versions[name]=(r.stdout+r.stderr).strip();assert r.returncode==0
    (OUT/'tool-versions.json').write_text(json.dumps(versions,indent=2)+'\n')
    rows=[
      ('RF2-001/RF2-004','CarrierERP,70-80% sineAM,PEP margin','OPEN','RFpower JSON, original>3W lower bound, one end-to-end RF acceptance required'),
      ('RF2-002/RF2-005','Independent low-power training output','SCHEMATIC_RETAINED_PHYSICAL_OPEN','Separate CLK2/buffer/BJT/filter/MCX; radiation/isolation NOT_RUN'),
      ('RF2-006/CTRL-005','Independent fail-off and rearm','STATIC_PASS_TIMING_OPEN','4096 combinations/36scenarios, real POR/reset/RC/driver withdrawal not measured'),
      ('RF2-007','Programmable legal frequencies','CONTRACT_ONLY_NO_FIRMWARE','CLK0=RF/2; CLK2=RF; country/championship restrictions require controller validation'),
      ('PWR-003/SYS-008','12h full24h reduced','MODELED_ONLY','Actual output,current,cell energy and4Swindow NOT_RUN'),
      ('COST-001/COST-002','Low-cost6/10/20 reproducible source','NO_GO','Legacy device price/maker/stock; coil quotes OPEN;93.16EUR at10 conditional2S'),
      ('M5A-R3 CAD','Editable schematic and integrated PCB','SCHEMATIC_DONE_PCB_BLOCKED','Exact manufacturer/landings unresolved; no guessed PCB'),
      ('Change control','RF80/R1/ADRs preserved','HASH_PASS','Starting467files, R1archive and review retained'),
      ('Permissions','Private construction; no commercial rights assumed','DOCUMENTED','DL3BBX written permission needed before commercial exploitation')]
    with (OUT/'requirements-trace.csv').open('w')as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['requirement','meaning','status','evidence']);w.writerows(rows)
    paths=list(OUT.rglob('*'))+list((ROOT/'docs').glob('M5A_R3_*.md'))+list((ROOT/'tools').glob('m5a_r3_*.py'))
    paths += [p for p in DEST.iterdir()if p.is_file()and(p.suffix in ['.kicad_sch','.kicad_sym','.kicad_pro','.json']or p.name in ['README.md','LICENSE-REFERENCE-DL3BBX.md','LICENSE-KICAD-SYMBOLS.md','sym-lib-table','fp-lib-table'])]
    files={str(p.relative_to(ROOT)):digest(p)for p in sorted(set(paths))if p.is_file()and p.name not in ['file-manifest.json','SHA256SUMS']}
    mf.write_text(json.dumps(dict(revision='M5A-R3',status='REVIEW_ONLY_NO_PCB_NO_MANUFACTURING',files=files),indent=2)+'\n')
    sums=files|{str(mf.relative_to(ROOT)):digest(mf)}
    (OUT/'SHA256SUMS').write_text(''.join(h+'  '+name+'\n'for name,h in sorted(sums.items())))
    print('Sealed',len(files),'R3 CAD/document/model/check files; manufacturing status NO_GO')
if __name__=='__main__':main()
