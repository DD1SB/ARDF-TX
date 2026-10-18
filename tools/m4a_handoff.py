#!/usr/bin/python3
"""Frozen five-bare-board / one-staged-assembly handoff, never a purchase.
Copies byte-identical E2 review data; archives exact1245023 source locally.
"""
import csv,hashlib,json,shutil,subprocess
from pathlib import Path
from m4a_design import E,R,frozen
H=E/'handoff/M4A-E2'
def stage(p):
    if p['group']=='fox':return '5_Fox_RF'
    if p['group']in('normal_filter','normal_rf_bypass')or p['ref']in('Q402','T401','J401'):return '4_normal_RF'
    if p['group']in('normal_driver','normal_shaper'):return '3_driver_shaper_AFTER_gate_D'
    if p['population']=='NORMAL'or p['ref']in('J301','F301','D301'):return '2_power_conversion_driver_absent'
    return '1_low_voltage_logic_source'
def main():
    names=frozen();H.mkdir(parents=True,exist_ok=True)
    archive=H/'ARDF-TX_E2_1245023_source.tar.gz'
    if not archive.exists():subprocess.run(['git','archive','--format=tar.gz','--output='+str(archive),'1245023'],cwd=R,check=True)
    src=E/'review/M3B-E2';dest=H/'reference-package'
    copied=[]
    for q in sorted(src.rglob('*')):
        if not q.is_file():continue
        target=dest/q.relative_to(src);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,target)
        assert target.read_bytes()==q.read_bytes();copied.append(str(q.relative_to(src)))
    m=json.loads((E/'RF80.electrical.json').read_text());parts=[p for p in m['parts']if not p['ref'].startswith(('#','TP'))]
    with(H/'assembly-stages.csv').open('w')as out:
        w=csv.writer(out,lineterminator='\n');w.writerow(['reference','MPN','footprint','population','full_fit','Fox_fit','planned_stage','authorization','physical_test'])
        for p in parts:w.writerow([p['ref'],p['mpn'],p['footprint'],p['population'],p['population']in('NORMAL','BOTH'),p['population']in('FOX','BOTH'),stage(p),'NOT_AUTHORIZED','NOT_RUN'])
    crit=json.loads((src/'critical-pinouts.json').read_text());critical={p['reference']for p in crit['devices']}
    with(H/'critical-procurement-candidates.csv').open('w')as out:
        w=csv.writer(out,lineterminator='\n');w.writerow(['reference','MPN','manufacturer','footprint','full_quantity','Fox_quantity','stage','supplier','supplier_identifier','MOQ','multiple','price_provenance','availability_evidence','source','blocker'])
        for p in parts:
            if p['ref']not in critical and p['ref']not in('C404','C350','R410','R330','R350','L301','L410','L411','TH301'):continue
            d=next((x for x in crit['devices']if x['reference']==p['ref']),{})
            w.writerow([p['ref'],p['mpn'],d.get('manufacturer',p.get('manufacturer','See exact MPN/source')),p['footprint'],int(p['population']in('NORMAL','BOTH')),int(p['population']in('FOX','BOTH')),stage(p),p['supplier'],p['supplier_part_number'],p['moq'],p['multiple'],p['evidence'],p['availability'],p['source_url'],'Fresh stock/price and exact suffix/fit required; no automatic substitute'])
    # Original itemized one-board cash basket; no manual scope adjustment.
    costs=json.loads((R/'docs/M3B_E2_COSTS.json').read_text())
    (H/'one-board-material-budget.json').write_text(json.dumps(costs['scopes']['Full']['batches']['1'],indent=2)+'\n')
    gates=[dict(gate=i,name=n,status='NOT_AUTHORIZED',hardware_tests='NOT_RUN',scope=s)for i,n,s in[(1,'Bare PCB fabrication','Exactly five bare M3B-E2 PCBs; vendor confirmations and user approval required'),(2,'Low-voltage component procurement','Only approved Stage1 BOM quantities; no implied power/RF procurement'),(3,'High-energy power-stage population','Only specifically approved later stage/parts, after prior measurements pass'),(4,'Controlled power-up','Named stage, bounded lab supply, instruments and operator conditions; not RF activation'),(5,'RF activation','Named path, calibrated rated dummy load and bounded initial voltage/current/duty; no unqualified radiation')]]
    report=dict(date='2026-10-15',reference_commit_full=subprocess.check_output(['git','rev-parse','1245023'],cwd=R,text=True).strip(),source_archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),reference_commit='1245023',reference_tag='m3b-e2',reference_files_checked=len(names),copied_review_files=copied,source_archive=archive.name,initial_bare_quantity=5,initial_assembled_quantity=1,requested_finish='Lead-free HASL; green mask both sides; white legend. Supplier must confirm land flatness/solderability; any ENIG alternative requires quote/review. Frozen job unspecified-finish metadata unchanged.',authorizations=gates,all_physical_tests='NOT_RUN',budget_eur_net=dict(bare_five=[45,90],PCB_freight=[10,25],one_full_component_basket=32.317,subtotal_before_fixture_labor_tax_component_freight=[87.317,147.317],classification='Unquoted E2 allowance; tight-hole process surcharge/quote OPEN'))
    (H/'handoff.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Prepared byte-identical E2 handoff; five bare boards / one staged population; all five authorizations NOT_AUTHORIZED')
if __name__=='__main__':main()
