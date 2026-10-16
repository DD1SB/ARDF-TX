#!/usr/bin/python3
"""Audit final native files and produce the M5B review index/cost decision.
Does not modify the electrical design or waive DRC warnings. All hardware
acceptance entries remain NOT_RUN until real measurements are recorded.
"""
import collections,csv,hashlib,json,subprocess,datetime
from pathlib import Path
import pcbnew as p
from m5b_design import HW,OUT,ROOT,preserved

def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---'for _ in headers)+' |',*['| '+' | '.join(map(str,r))+' |'for r in rows]])+'\n'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 assert preserved()==json.loads((OUT/'preserved-baseline.json').read_text())
 drc=json.loads((OUT/'DRC.json').read_text());erc=json.loads((OUT/'ERC.json').read_text());v=json.loads((OUT/'verification.json').read_text());cost=json.loads((OUT/'costs.json').read_text());parts=json.loads((HW/'RF2M.electrical.json').read_text())['parts'];pr={x['ref']:x for x in parts}
 # There is no zero-DRC claim. Keep all warnings visible and dispositioned.
 assert not drc['unconnected_items']and not drc['schematic_parity']
 assert not any(x['severity']=='error'for x in drc['violations'])
 assert all(x['type']in ['missing_courtyard','copper_sliver']for x in drc['violations'])
 erc_items=[x for s in erc['sheets']for x in s['violations']];assert not erc_items,erc_items
 pro=json.loads((HW/'RF2M.kicad_pro').read_text());ds=pro['board']['design_settings'];assert not ds['drc_exclusions']
 coverage=dict(tool=subprocess.check_output(['kicad-cli','version'],text=True).strip(),rules=ds['rules'],rule_severities=ds['rule_severities'],exclusions=ds['drc_exclusions'],disabled={k:val for k,val in ds['rule_severities'].items()if val=='ignore'},disabled_rationale='Only tuning_profile_track_geometries is irrelevant: no tuning profiles, delay lines or differential pairs are used. Courtyard, footprint filters/type, via centering, mask, silk, drill, thermal, copper and parity checks are enabled.',results=collections.Counter(x['type']for x in drc['violations']),dispositions=[])
 for x in drc['violations']:
  if x['type']=='missing_courtyard':
   assert all(i['description'].split()[-1]in {'TL603','TL604','TL605','TL606','TL607','TL608','TL609','TP601','TP602','TP603','TP604'}for i in x['items'])
  why='Bare copper transmission-line/probe feature, no purchased body or assembly collision volume. Relevant copper/mask/edge checks stay enabled.'if x['type']=='missing_courtyard'else'Unlocated F.Cu sliver warning: KiCad JSON/report provides no item UUID or coordinate. Not waived or called false-positive. Independent native/Gerber CAM inspection must close it before ordering; do not alter RF copper without review.'
  coverage['dispositions'].append(dict(type=x['type'],severity=x['severity'],items=x['items'],disposition=why))
 coverage['supplemental_marker_API']='KiCad10.0.6 pcbnew.WriteDRCReport read-only localization attempt failed with missing Pgm process/context (exit139). Not used for final acceptance. CLI DRC is the reproduced authoritative check;GUI/CAM localization still needed.'
 save('DRC-coverage.json',coverage)
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));assert p.ToMM(b.GetDesignSettings().m_SolderMaskMinWidth)>=.1;fs={f.GetReference():f for f in b.GetFootprints()};bb=b.GetBoardEdgesBoundingBox();assert abs(p.ToMM(bb.GetWidth())-180)<.1 and abs(p.ToMM(bb.GetHeight())-140)<.1
 pads=[];drills=collections.Counter()
 for f in fs.values():
  for pa in f.Pads():
   if not pa.GetNumber():continue
   pads.append(dict(ref=f.GetReference(),pad=pa.GetNumber(),net=pa.GetNetname(),x_mm=p.ToMM(pa.GetPosition().x),y_mm=p.ToMM(pa.GetPosition().y),drill_x_mm=p.ToMM(pa.GetDrillSize().x),drill_y_mm=p.ToMM(pa.GetDrillSize().y),footprint=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())))
   if pa.GetDrillSize().x:drills[round(p.ToMM(pa.GetDrillSize().x),3)]+=1
 with(OUT/'pad-connectivity.csv').open('w')as fp:w=csv.DictWriter(fp,fieldnames=list(pads[0]));w.writeheader();w.writerows(pads)
 # Verify explicit source vias; no drain/gate thermal slug substitution.
 source_vias=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)and p.ToMM(t.GetPosition().x)in [111.35,112.65]and 52.9<p.ToMM(t.GetPosition().y)<57.1]
 assert len(source_vias)==12 and all(x.GetNetname()=='GND'for x in source_vias)
 widths=json.loads((OUT/'power-path-widths.json').read_text());assert widths['pass_all']
 stack=dict(revision='M5B-E1',outline_mm=[180,140],layers=2,finished_thickness_mm=.8,dielectric_mm=.64,copper_each_um=70,mask_each_um=10,material='FR4 Dk4.3/tand.02 ASSUMED;fabricator actual stackup confirmation required',finish='ENIG proposed',minimum_track_clearance_mm=[.15,.15],ordinary_via_diameter_drill_mm=[.6,.3],min_annular_ring_mm=.15,copper_edge_mm=.5,hole_clearance_mm=.25,finished_component_holes_mm=dict(drills),mounts=[dict(ref='H'+str(i),x_mm=x,y_mm=y,NPTH_mm=3.2)for i,(x,y)in enumerate([(25,25),(195,25),(195,155),(25,155),(112,32),(112,68)],1)],thermal='See thermal-contact.json and M5B_E1_POWER_AND_THERMAL.md;external independent sinks/40mm bench support;not a qualified thermal assembly',manufacturer_confirmation='0.8mm2oz stackup,0.15mm features,0.30mm PTH/annular ring,0.1mm mask webs,finished connector holes/tolerances,via tents/stencil and electrical-test net aliases')
 save('stackup-mechanical.json',stack)
 # Intentional net ties become aliases in the fabrication electrical-test data.
 parent={}
 def find(x):
  parent.setdefault(x,x)
  if parent[x]!=x:parent[x]=find(parent[x])
  return parent[x]
 for part in parts:
  if part['ref'].startswith('TL'):
   a,bb=list(part['pins'].values());parent[find(bb)]=find(a)
 aliases={x:find(x)for x in parent};save('fabrication-net-aliases.json',dict(reason='Physical copper TL net ties intentionally connect logical schematic segments. Preserve logical netlist for CAD checks;use physical IPC for bare-board E-test.',aliases=aliases))
 ipc=OUT/'RF2M-logical.ipc'
 if ipc.exists():
  out=[]
  for line in ipc.read_text().splitlines():
   if line[:3]in ['317','327','367']:
    net=line[3:17].strip();line=line[:3]+aliases.get(net,net).ljust(14)+line[17:]
   out.append(line)
  (OUT/'RF2M-physical-netties.ipc').write_text('\n'.join(out)+'\n')
 # Full itemized ledger is CSV; these tables are generated, not manually patched.
 rows=[]
 for pop in ['BOOST2S','BUCK4S','TRAIN_ONLY']:
  ss=[x for x in cost['summary']if x['population']==pop];q10=next(x for x in ss if x['fleet']==10)
  rows.append([pop,*[f"€{next(x for x in ss if x['fleet']==q)['component_net_EUR']:.2f}"for q in [6,10,20]],q10['physical_components'],q10['IC_count'],f"€{q10['unquoted_net_EUR']:.2f}",f"€{q10['delta_net_EUR']:+.2f}"])
 budget=table(['Population','6 each','10 each','20 each','Fitted parts','ICs','Unquoted at10','Delta/R4 at10'],rows)
 q10s={x['population']:x for x in cost['summary']if x['fleet']==10};allblocks=sorted(set().union(*(x['blocks']for x in q10s.values())))
 blocks=table(['Functional block','2S at10','4S at10','Training at10'],[[k,*[f"€{q10s[pop]['blocks'].get(k,0):.3f}"for pop in ['BOOST2S','BUCK4S','TRAIN_ONLY']]]for k in allblocks])
 (ROOT/'docs/M5B_E1_BOM.md').write_text('''# M5B-E1 material budget

2026-10-16. EUR net, VAT/shipping/labor separate. These are candidate material budgets, not purchase quotations. No procurement is authorized. The complete per-position, MPN, footprint, population, supplier, MOQ, pooled-order, price-break and evidence ledger is [RF2M_BOM.csv](../hardware/2m/review/M5B-E1/RF2M_BOM.csv); the three population CSVs provide quantity-ten assembly lists. Do not count test pads, TL copper features or footprint assignments as purchased ICs.

'''+budget+'''
The original R4 quantity-ten baselines are€43.32/€42.03/€11.28. Normal populations add eight fitted parts and one IC: the preregulator, divider/bypass parts, liftable driver/RF links and selected local converter reservoir. R651 is DNP and optional test-only. No component is counted twice because two footprints share an MPN. Price pooling and MOQ rounding use the actual fleet demand; no speculative discount is booked. Deltas are calculated before displayed-cent rounding.

The increase also includes the exact MMCX rather than an unspecified cheap connector, the low-DCR RF choke and corrected current shunt/divider. The two-stage driver protection costs more than the old marginal circuit. It is not hidden in a blanket allowance. The full RF/source/matching/AM/driver-supply core is approximately€28.56 at ten; that is not the complete transmitter.

'''+blocks+'''
Current indexed observations include Panasonic C409, Coilcraft33 nH/150 nH feeds, Wurth MMCX and the Bourns power inductors. Earlier distributor observations remain HISTORICAL; unquoted passives, protection and control positions remain ESTIMATE_UNQUOTED. At ten the unquoted amounts above remain visible rather than being treated as verified procurement. Exact priced observations can be stale by ordering time.

**Supply holds:** L301 has indexed zero stock/backorder; L6340603HC-47NXJRW is a documented current manufacturer configuration with a cut-MOQ1 non-stocked distributor offering and approximately9-week indicated factory lead time. Its€0.75 budget is an estimate, not a EUR quotation. U950's regional inventory caches conflict and require confirmation. The active PD54008 and PHA-1+ baseline sourcing evidence is retained; verify all final suffixes, authenticity, temperature grades and spares before purchase. No broker substitution is assumed.

Bare-board estimate: **five180×140 mm,0.8 mm,2oz two-layer boards:€60–100 net per batch**, shipping approximately€10–25. This is an engineering estimate, not an uploaded fabrication quote or promotion. Production-context estimates per board at6/10/20 are€12/€9/€7, conditional on actual stack-up and panel rules. Obtain a supplier quote after independent review.

External thermal material allowance is€12 net per full board for two independent sinks, spreader, insulation and mounting hardware. A Fischer SK48 50SA comparator was indexed at€3.7128 gross individually/€3.4391 gross at ten, approximately€3.12/€2.89 net using19% German VAT; the remaining hardware is estimated. Harness allowance€3, antenna/feeder€12 are separate. At ten a4S installed-module allowance is therefore€73.03 including€9 PCB,€12 thermal and€3 harness, or€85.03 including the provisional antenna/feeder. Controller, battery/BMS, charging, enclosure and labor are excluded. Training-only does not need PA heat hardware.

The optional driver load is approximately€0.025 plus temporary coax/probes, all estimated and reusable. The26 probe contacts are bare-board features with no separately purchased component cost. RF instruments/dummy loads belong to shared commissioning equipment. Measure actual assembly/alignment time before assigning labor or claiming savings. Manufacturing VAT is jurisdiction-dependent; a19% illustration is not a tax-inclusive procurement commitment.
''')
 summary=dict(date='2026-10-16',revision='M5B-E1',baseline_commit='b44fe3b',baseline_tag='m5a-r4',KiCad=coverage['tool'],ERC_errors=0,ERC_warnings=0,DRC_errors=0,DRC_warnings=len(drc['violations']),unrouted=0,schematic_parity_issues=0,logic_combinations=v['logic']['combinations'],state_scenarios=len(v['logic']['scenarios']),original_mutations=len(v['mutation_tests']),additional_mutations=len(v['M5B_additional_mutations']),critical_pin_maps=len(json.loads((OUT/'pinout-audit.json').read_text())['devices']),native_pad_packages=v['native_PCB_package_checks'],power_path_widths='PASS',physical_acceptance='NOT_RUN',review='GO for independent integrated evaluation PCB review',order='NO_GO until independent CAM/sliver disposition and stackup/finished-hole confirmation,then explicit user authorization',preservation_files=len(preserved()))
 save('final-checks.json',summary)
 (ROOT/'docs/M5B_E1_REVIEW_DECISION.md').write_text(f'''# M5B-E1 review decision

2026-10-16. **GO for independent review of one integrated evaluation PCB. NO_GO for an order until the remaining CAM warning and fabrication confirmations are closed, followed by explicit user authorization.** No purchasing, fabrication, assembly, power-up or RF operation occurred. All hardware acceptance is NOT_RUN.

The editable [schematic](../hardware/2m/RF2M.kicad_sch) and [180×140 mm PCB](../hardware/2m/RF2M.kicad_pcb) preserve the selected Si5351/PHA-1+/PD54008 chain, ST output matching/elliptic filter, drain-sine AM, autonomous fail-off, captured mode and separateµW training port. The board supports mutually exclusive2S boost/4S buck and training-only populations. R4 is preserved at `m5a-r4`/`b44fe3b`; RF80 and historical references are unchanged. No ADR is silently accepted.

The seven missing landings are resolved. Additional corrections fix the unreachable current-trip threshold, high-DCR MMIC choke, marginal driver switch and converter input bypassing. Two independent regulators and a rated isolation switch replace reliance on an unmeasured20µs fault assumption. The initial50Ω interstage includes the33nH gate-bias feed;47nH/22pF/22pF is a documented tunable starting population, not measured device matching. The final output network values remain unchanged. Thermal construction has separate insulated pass/helper mounting and a grounded lower PA spreader/contact window.

KiCad {coverage['tool']}: **ERC0 errors/0 warnings; DRC0 errors,0 unrouted,0 parity issues, {len(drc['violations'])} visible warnings.** Eleven warnings concern bodyless TL/probe copper features; one is an unlocated F.Cu copper sliver. No exclusions are installed. Full coverage/dispositions are in [DRC-coverage.json](../hardware/2m/review/M5B-E1/DRC-coverage.json). The sliver is not falsely declared harmless: independent native/Gerber CAM inspection must locate/dispose it before ordering. Do not globally disable the checker or change matching copper without review.

The actual exported netlist/native pad regression passes **4096 combinations,39 state scenarios,19 original mutations plus{len(v['M5B_additional_mutations'])} new mutations**, {summary['critical_pin_maps']} manufacturer pin maps,26 ST network positions and all {summary['native_pad_packages']} schematic package/pad sets. Main current paths retain≥0.5mm copper or short pad necks on70µm copper. Static checks do not qualify analog startup/reset races, overvoltage transients, RF stability, AM or thermal performance.

'''+budget+'''
The complete unquoted amounts remain substantial. Buck-inductor delivery,47nH matching-inductor lead time and preregulator inventory require procurement confirmation; they do not make bare-board evaluation layout impossible. Five-board fabrication budget€60–100 net plus estimated€10–25 shipping is not a supplier quote. Populate only one first, after separate approval.

The [review package](../hardware/2m/review/M5B-E1/README.md) contains final-native references, PDF, copper/assembly/3D views, review Gerbers/drills, logical and physical-net-tie IPC, pin/pad reports, variants and checksums. Custom3D geometry is identified as dimensional envelopes; missing standard connector visualization is explicitly listed rather than treated as package qualification. Actual footprints/holes are separately audited.

Before a small bare-PCB batch: independently inspect native RF/thermal layout and the unlocated sliver, confirm the0.64mm dielectric/70µm copper stack and0.15mm rules/connector finished holes, confirm buildable source/spreader/stencil assembly and obtain a real quote, then request explicit manufacturing authorization. No nonexistent RF measurement is demanded before this evaluation-board review. Before MMIC fitting or RF activation, follow [one staged bring-up procedure](M5B_E1_BRINGUP.md): bounded logic/power tests, both regulator-fault cases with MMIC absent, modulator/thermal checks, driver alignment, full RF acceptance, training/isolation and endurance. Actual gain, clean70–80%AM/PEP/ERP, harmonics, off-slot silence, hot SOA and12h/24h results remain NOT_RUN. This is an evaluation candidate, not production release.
''')
 (OUT/'MANUFACTURING.md').write_text('''# RF2M M5B-E1 review-only manufacturing notes

NOT AN ORDER / NOT A PRODUCTION RELEASE. Use final-native files and checksums; do not reuse R4 exports. One integrated two-layer180×140mm board. Proposed0.8mm finished,0.64mm FR4 dielectric,70µm copper each side,ENIG,mask both sides. No blind/buried vias or impedance premium is assumed. Confirm Dk/tolerance,2oz0.15mm features,0.3mm PTH with0.15mm annular rings and0.1mm mask webs. Copper-edge≥0.5mm;NPTH mounts3.2mm. Finished holes:IDC1.1mm,SMA center1.5mm/ground1.7mm;confirm manufacturer drawings and hole tolerance±0.1mm candidate. See drill report for all exact sizes. Dimensions are millimeters.

Review GerberX2 layers/drills and outline as one matched set. The B.Mask thermal window exposes GND with two mask strips retained over source-via columns. Do not remove these tents or merge RNW center pads. Source stencil is a proposal;100µm initial stencil and segmented apertures need assembler review. No via-fill premium assumed. Do not resize RF traces or shorten TL603–609. Confirm intentional net ties against fabrication-net-aliases.json and use RF2M-physical-netties.ipc for E-test; RF2M-logical.ipc retains schematic nets and will otherwise report intentional ties as shorts.

Independent CAM must close the visible unlocated F.Cu sliver warning before an order. Eleven courtyard warnings are non-component TL/probe features. All other manufacturing/connectivity checks remain enabled; no DRC exclusion is present. Do not silently apply CAM edits to RF, thermal or safety nets. Request a real five-board quote;€60–100net/batch plus shipping is an estimate only. Procurement, assembly, controlled power-up and RF activation each need separate authorization.
''')
 (OUT/'README.md').write_text('''# RF2M M5B-E1 independent review package

**REVIEW ONLY — NOT RELEASED — HARDWARE TESTS NOT_RUN.** Native project: `../../RF2M.kicad_pro`, `../../RF2M.kicad_sch`, `../../RF2M.kicad_pcb`; prior electrical baseline tag `m5a-r4`, commit `b44fe3b`. RF80 is unchanged.

Start with `final-checks.json`, `DRC.rpt`, `DRC-coverage.json` and `MANUFACTURING.md`. Zero DRC errors/unrouted/parity is accompanied by12 visible warnings, not a clean-checker claim. The unlocated F.Cu sliver needs independent CAM closure before ordering. Courtyard warnings concern eleven bodyless copper features.

- `RF2M.pdf`: complete editable-source schematic export.
- `top-copper.svg`, `bottom-copper.svg`, assembly PDFs/SVGs and actual KiCad `RF2M-3D*.png`: placement/routing review. Dimensional-envelope and missing visualization status is in `3D-model-status.json`; renders do not qualify footprints or thermal performance.
- `gerbers/`: fresh GerberX2, separate PTH/NPTH Excellon,PDF drill maps and job file; no files were submitted anywhere.
- `RF2M.net.xml`, `pad-connectivity.csv`, `pinout-audit.json`, `verification.json`, `power-path-widths.json`: electrical/physical assertions and mutations.
- `RF2M-logical.ipc`, `RF2M-physical-netties.ipc`, `fabrication-net-aliases.json`: schematic versus actual net-tie E-test definitions.
- `BOM_*.csv`, `RF2M_BOM.csv`, `costs.json`: explicit2S/4S/training populations and6/10/20 fleet costs, observed versus unquoted positions.
- `stackup-mechanical.json`, `thermal-contact.json`, `transmission-lines.csv`, `calculations.json`, `input-match-sensitivity.csv`, power/thermal/endurance tables: estimates and fabrication assumptions.
- `SHA256SUMS`, `file-inventory.json`, `native-inputs.json`: exact local revision identity; `preserved-baseline.json` protects historical/RF80 files. `development/` contains non-final routing history; its intermediate DRC reports are not final acceptance results.

Reproduce final checks from repository root with KiCad10.0.6/systemPython: `tools/m5b_exports.py --checks`, `tools/m5b_verify.py`, `tools/m5b_power_widths.py`, `tools/m5b_models.py`, then `tools/m5b_exports.py --render` with a local X display and `tools/m5b_review.py`. Prefix Python tools with `/usr/bin/python3`; model-only script also works with `python3`. DRC code5 means retained warnings, not zero violations. Inspect reports. Rendering uses local softwareGL/Xvfb. Routing/construction helper scripts are development tools, not an instruction to regenerate or overwrite the reviewed native PCB.

Read the seven `docs/M5B_E1_*.md` documents for corrections, packages, input matching, safety, costs, commissioning and decision. GO for independent evaluation-board review; no procurement, manufacture, assembly or energizing is authorized. Commercial/source rights are inherited from the documented reference provenance; no third-party datasheets or historical articles are redistributed here.
''')
 native=[HW/'RF2M.kicad_pro',HW/'RF2M.kicad_pcb',HW/'RF2M.electrical.json',HW/'ARDF_2M.kicad_sym',HW/'sym-lib-table',HW/'fp-lib-table',*HW.glob('*.kicad_sch'),*(HW/'ARDF_2M.pretty').glob('*'),*(HW/'ARDF_2M.3dshapes').glob('*')]
 save('native-inputs.json',{str(x.relative_to(ROOT)):sha(x)for x in sorted(set(native))if x.is_file()})
 print('Final review audit:',summary)

if __name__=='__main__':main()
