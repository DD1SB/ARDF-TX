"""Assemble the analysis HOLD evidence without writing any native/historical CAD."""
import datetime
import shutil
import sys
from zoneinfo import ZoneInfo
from m5b_e6_common import *


def main():
    guard()
    clone=Path(sys.argv[1])
    logs=Path(sys.argv[2])
    assert (clone/'.git').exists() and clone.resolve()!=ROOT
    source=clone/'hardware/2m/review/M5B-E6/baseline-regression'
    target=OUT/'baseline-regression';target.mkdir(exist_ok=True)
    # Retain results, not temporary mutated board fixtures or duplicated old
    # preservation inventories. Frozen originals are already in the repository.
    for f in source.iterdir():
        if f.is_file() and f.name!='preserved-baseline.json':
            shutil.copyfile(f,target/f.name)
            if f.suffix=='.csv':
                # CSV semantics unchanged; do not retain CRLF as Git trailing WS.
                (target/f.name).write_text((target/f.name).read_text())
    (OUT/'logs').mkdir(exist_ok=True)
    for f in logs.glob('*.log'):shutil.copyfile(f,OUT/'logs'/f.name)
    d=json.loads((target/'DRC.json').read_text());e=json.loads((target/'ERC.json').read_text())
    v=json.loads((target/'verification.json').read_text());dfm=json.loads((target/'JLCPCB-DFM.json').read_text())
    test=json.loads((OUT/'analysis-test-results.json').read_text())
    assert test['successful'] and not test['failures'] and not test['errors']
    assert not [x for sheet in e['sheets'] for x in sheet['violations']]
    assert not d['unconnected_items'] and not d['schematic_parity']
    assert all(x['severity']=='warning' and x['type']=='missing_courtyard' for x in d['violations'])
    assert not dfm['errors']
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines()
    native={n:sha(ROOT/n) for n in names if n.startswith('hardware/') and '/review/' not in n and '/handoff/' not in n}
    for n,digest in native.items():
        raw=subprocess.check_output(['git','show',BASE+':'+n],cwd=ROOT)
        assert hashlib.sha256(raw).hexdigest()==digest, ('Native source changed',n)
    save('native-preservation.json',dict(starting_commit=BASE,all_native_unchanged=True,files=native,
        history='No reset, rebase, amend, tag or push; local development branch only',
        existing_tags=subprocess.check_output(['git','show-ref','--tags'],cwd=ROOT,text=True).splitlines()))
    audited=['power-audit.json','transient-results.json','E6-source-path-FVM.json','source-interface-alternatives.json',
             'stress-ripple-beacon.json','native-fault-envelope.json','thermal-path-closure.json','mechanical-concept.json','analysis-test-results.json']
    save('phase-C-selection.json',dict(disposition='HOLD_BEFORE_NATIVE_PCB_EDITS',
        preferred_concept='A: one SK81 100 SA below PCB, horizontal insulated Q401/Q402 tabs, source bar on same supported structure',
        manufacturing_selection_released=False,PCB_modified=False,
        blockers='Local PA source/interface and RF-loss/protection bound not closed; native common mounting assembly not implemented',
        result_hashes={n:sha(OUT/n) for n in audited},physical='NOT_RUN'))
    save('execution-results.json',dict(date=datetime.datetime.now(ZoneInfo('Europe/Berlin')).isoformat(),
        starting_commit=BASE,branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        final_disposition='HOLD_FOR_FIVE_BARE_RF2M_E6_EVALUATION_BOARDS',
        baseline=dict(ERC_errors=0,ERC_warnings=0,DRC_errors=0,DRC_warnings=len(d['violations']),
            unrouted=0,parity=0,enable_combinations=v['logic']['combinations'],state_scenarios=len(v['logic']['scenarios']),
            native_package_checks=v['native_PCB_package_checks'],electrical_mutations=len(v['mutation_tests'])+len(v['M5B_additional_mutations']),
            compact_mutations=len(json.loads((target/'compact-engineering.json').read_text())['negative_tests']),
            source_geometry_mutations=len(json.loads((target/'source-assembly-regression.json').read_text())['native_tests']),
            source_thermal_negatives=len(json.loads((target/'source-assembly-regression.json').read_text())['thermal_tests']),
            DFM_mutations=len(json.loads((target/'DFM-regression.json').read_text())['mutations']),DFM_status=dfm['status']),
        numerical_tests=test,
        native_E6='NOT_IMPLEMENTED',E6_fabrication_ZIP='NOT_CREATED',E6_native_3D='NOT_CREATED',
        physical='NOT_RUN',note='Fresh unchanged E5 replays are baseline evidence, not zero-warning E6 acceptance.'))
    inputs=[ROOT/'tools'/n for n in ['m5b_e4r1_thermal.py','m5b_e4r1_common.py','m5b_e5.py','m5b_e5_common.py']]
    inputs+=list((ROOT/'tools').glob('*m5b_e6*.py'))+list((ROOT/'docs').glob('M5B_E6*.md'))
    save('calculation-inputs.json',{str(p.relative_to(ROOT)):sha(p) for p in sorted(inputs)})
    # Hash scope includes review, documentation and calculation sources, with
    # manifest itself excluded. PDF metadata may differ on regeneration.
    paths=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    paths+=sorted((ROOT/'docs').glob('M5B_E6*.md'))+sorted((ROOT/'tools').glob('*m5b_e6*.py'))
    (OUT/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+str(p.relative_to(ROOT))+'\n' for p in paths))
    print('HOLD evidence assembled; native and historical files unchanged; numerical tests',test['tests_run'])


if __name__=='__main__':main()
