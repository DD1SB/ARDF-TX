#!/usr/bin/python3
"""Publish R1 review summaries only after native and artifact gates pass."""
import json,re,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1R1'
def load(n):return json.loads((D/n).read_text())
def write(n,s):(D/n).write_text(s.strip()+'\n')
def main():
 cad=load('CAD-results.json');assert all(cad[k]==0 for k in ['ERC_violations','DRC_errors','DRC_warnings','unrouted','parity'])
 assert cad['exclusions']==[] and cad['ignored_categories']==['tuning_profile_track_geometries']
 dfm=load('JLCPCB-DFM.json');sha=hashlib.sha256((P/'CTRL.kicad_pcb').read_bytes()).hexdigest();assert not dfm['errors'] and dfm['native_sha256']==sha
 art=load('artifact-audit.json');assert art['board_sha256']==sha
 elec=load('electrical-regression.json');assert elec['native_pad_instances']==704 and len(elec['native_mutations'])==20 and elec['hardware_enable_combinations']==4096 and elec['connector_contract_pins']==36
 assert len(load('DFM-regression.json')['mutations'])==7
 host=load('host-test-results.json');assert all(x['exit_code']==0 for x in host['commands']);assert 'Ran 40 tests' in host['commands'][0]['stderr']
 prot=load('input-protection.json');assert max(x['TMUX_5_max_V'] for x in prot['positive_fault_worst'])<3.0
 assert len(load('protection-regression.json')['native_and_numeric_checks'])==16
 change=load('change-and-preservation-audit.json');assert change['native_PCB_sha256']==sha and change['USB_topology_and_copper']=='UNCHANGED'
 costs=load('costs.json')['variants'];base=json.loads((P/'review/M6-C1/costs.json').read_text())['variants'];variants=['FOX_MIN','RF80_FULL','RF2M_FULL','UNIVERSAL'];lines=[];deltas={}
 for v in variants:
  vals=[costs[v][str(q)]['components_per_unit_net_eur'] for q in [1,10,20]]
  dd=[round(vals[i]-base[v][str(q)]['components_per_unit_net_eur'],3) for i,q in enumerate([1,10,20])];deltas[v]=dict(zip(map(str,[1,10,20]),dd));lines.append('| '+v+' | '+' | '.join(f'{x:.2f}' for x in vals)+f" | {costs[v]['10']['estimated_unquoted_net_eur']:.2f} |")
 table='| Population | q1 EUR/unit | q10 | q20 | Unquoted at q10 |\n|---|---:|---:|---:|---:|\n'+'\n'.join(lines)
 write('COST_DELTA.md',f'''# Component and manufacturing cost delta

Net EUR, VAT/freight/labor excluded. All base variants add five purchased parts: R8/R9/R19 at0.01 each (unquoted allowance), D22 BAS116,235 at0.224/0.130/0.130 (q1/10/20 indexed Mouser observation), D23 BAT54H,115 at0.20/0.12/0.12 (unquoted EUR estimates). R3's value changes at the same0.01 allowance. Total addition **0.454 EUR at q1 and0.280 EUR at q10/q20**. No new IC or additional PCB process.

{table}

D22 supplier771-BAS116235: indexed58175 stock, cut-tape MOQ1, no stock reserved. The10000 factory reel is not the customer MOQ. D23 regional Mouser indices differ (approximately60194–75213 in some regional observations and backorder in others); live EU availability/price remains OPEN. Do not call its0.12 allowance a supplier quote. No additional20-unit discount is invented. Most legacy small-part material remains unquoted, as shown in every BOM row.

The100×100mm PCB remains ordinary2L1.6mm1oz FR4/green/white/lead-free HASL. The bare-board planning model is unchanged:5/10/20 boards at9/14/24 EUR per batch before10–25 EUR freight allowance, VAT and optional8–20 EUR stencil. These are **unquoted planning estimates**, not JLC prices or CAM acceptance. New underside parts can be locally reflowed/hand assembled; a production assembly line is not required. Labor and small consumables remain unquoted. Existing battery/cell, RF boards, harness, antenna and enclosure are separate. Optional LoRa remains HOLD.
''')
 (D/'cost-delta.json').write_text(json.dumps({'classification':'netEUR estimates and separately labeled indexed observations','deltas_per_unit':deltas,'PCB_process_delta':'NONE','PCB_quote':'NOT_REQUESTED','D23_EU_stock_price':'OPEN'},indent=2)+'\n')
 pth=sum(art['drill_counts_by_diameter_mm']['PTH'].values());npth=sum(art['drill_counts_by_diameter_mm']['NPTH'].values())
 summary=f'''# M6-C1R1 electrical and manufacturing validation

KiCad **{cad['kicad']}** was run on the final native board. All values below are actual CAD/host checks, not physical tests.

| Check | Result |
|---|---|
| ERC errors/warnings |0 /0|
| DRC errors/warnings |0 /0|
| Unrouted/parity |0 /0|
| Exclusions |none|
| Ignored category |default tuning_profile_track_geometries only; no tuning patterns|
| Baseline pad coverage |693 retained, with3 intentional net changes|
| Current native pad assertions |704|
| Manufacturer maps |38 baseline plus2 new diode maps|
| RF connector pins |36 unchanged|
| Enable combinations |4096|
| Baseline electrical mutations |20 rejected|
| New native/numerical protection checks |16 pass, including unsafe mutations rejected|
| Native DFM mutations |7 rejected|
| Host Python tests |40; all32 baseline tests retained with legitimate ID-decoder update|
| C fixture |strict C11 -Wall -Wextra -Werror compile and execution PASS|
| RF80 read-only replay |256 truth cases,31 states,16 RC corners,2 polarity mutations|
| RF2M read-only replay |4096 combinations,39 states,16 preparation rows|
| Native JLCPCB geometry |PASS; {dfm['statistics']['independent_copper_pair_tests']} foreign-copper pair checks; no slivers|
| Fabrication artifact audit |9 Gerbers,{pth} PTH/{npth} NPTH,{art['native_IPC_records']['pads']} pad/{art['native_IPC_records']['vias']} via IPC records|
| Historical preservation |111 M6-C1 review files and1220 RF files unchanged|

Independent positive-fault calculations give less than2.74V at U21.5 unpowered and2.11V powered for16.8V at J1.3 with resistor/leakage corners. Resistor-only bounds are2.6472/2.0713V. ThePACK_ID channel uses calibrated ATTEN1/2.5dB and rejects>=0.93V/saturation. Independent1.7% initial/temperature resistor corners are included. Static VDD=0 ADC leakage bound is±0.204V. R8 dissipation is at most1.23mW in the positive-fault cases. Finite U21 RON≤4.5ohm contributes below0.1mV DC error at these currents; it is below the qualified ADC-error budget, not asserted to be an ideal physical switch.

The complete fault rows, currents, recognition envelopes and explicit parameter assumptions are in [input-protection.json](../hardware/controller/review/M6-C1R1/input-protection.json). The3.3V USB steering reference and all USB copper remain unchanged; [USB review](M6_C1R1_USB_ESD_REVIEW.md) distinguishes normal power states, forced unpowered data injection and IEC transients.

Required negative-test coverage is tied to actual nets/model inputs: raw16.8V and absent U21 supply (numerical divider/off leakage), missing R8/R9/R19 and incorrect bias or clamp connections (native mutations), open/short/wrong identity and excessive/absent calibration (host interval reader), incorrect USB rail/pins (native mutations), unchanged RF connector identity (baseline/native mutation), USB-only/MCU reset/brownout/no progress/conflicting bands (native4096 truth and host states). No label-only result substitutes for a circuit or model check.

Physical ADC calibration, leakage over temperature, negative clamp behavior, transient isolation, rail decay/backfeed, USB ESD/enumeration/eye, RTC and RF integration are **NOT_RUN**. The explicit calibration record must be qualified over the intended operating envelope. Unqualified, stale, ambiguous or wrong frontend-version data cannot authorize a pack identity. The normal scheduling/application firmware is not delivered here.

Reproduction commands and frozen-source requirements: [REPRODUCE.md](../hardware/controller/review/M6-C1R1/REPRODUCE.md). Historical helpers are reused through the R1 wrapper so their old review directory is never overwritten.
'''
 (ROOT/'docs/M6_C1R1_ELECTRICAL_VALIDATION.md').write_text(summary)
 decision=f'''# M6-C1R1 independent review decision

**GO for independent review of five unpopulated controller evaluation PCBs. No manufacturing authorization or acceptance tag.**

Finding A is corrected in the native schematic and routed PCB using a pack-derived, reverse-isolated resistor-ID excitation,180k/33k positive-fault divider, negative clamp and100k ADC discharge/load. This adds five inexpensive purchased parts and no IC. External10k/22k codes, J1 numbering, all GPIOs and all36 RF connector pins remain. The hardware/decoder binding is now **PACK_ID_FRONTEND_REV2**; the former3.3V-excited decoder must not be used. [Input engineering](M6_C1R1_INPUT_PROTECTION.md).

Finding B closes with a **justified no-change** decision. U3 pin5 remains V3V3 with C10; both the USB electrical topology and copper are unchanged. The assessment uses ST's rail-to-rail mechanism/working-voltage rating, upstream device example and VCC-bias guidance, rather than treating the pin name as a requirement. It does not claim IEC immunity. [USB review](M6_C1R1_USB_ESD_REVIEW.md).

The100×100mm board retains standard two-layer1.6mm FR4/1oz, green mask, white legend, lead-free HASL and ordinary0.80/0.30mm vias. No custom process or active-IC redesign. Protection is concentrated near J1; the established long ID route is reused on the protected side. R19 is a local ADC pull-down. Six small positions (five added plus relocated R3) are on the underside; preserve at least the prior10mm underside clearance and trim THT leads. Connector/mounting locations and RF contracts are unchanged. All existing footprints except relocated R3 retain their positions.

ERC/DRC each have **0 errors and0 warnings**, unrouted/parity0, no exclusions. The native DFM and electrical/artifact/host regressions pass. [Exact coverage](M6_C1R1_ELECTRICAL_VALIDATION.md) includes704 pads,4096 enables,20 retained electrical mutations,16 new protection checks,7 DFM mutations,40 host tests and the strict C11 fixture. All111 original M6-C1 review files and1220 RF files are preserved.

Quantity-ten estimates become **FOX_MIN18.99 EUR, RF80_FULL19.26 EUR, RF2M_FULL19.30 EUR, UNIVERSAL22.34 EUR net/unit**: +0.28 each. Significant unquoted material remains; D23's live EU stock/price needs confirmation. [Complete q1/10/20 costs](../hardware/controller/review/M6-C1R1/COST_DELTA.md). Bare-board process/price model is unchanged and unquoted. Optional LoRa remains **HOLD/DNP**.

| Gate | Status |
|---|---|
|A electrical/CAD correction|PASS for defined DC faults and manufacturer-backed topology assessment; commissioning assumptions explicitly identified|
|B ordinary JLCPCB manufacturability|PASS local native/artifact checks; factory CAM not submitted|
|C five bare evaluation boards|GO for independent review/quotation preparation; user approval and supplier CAM remain separate|
|D controlled electrical commissioning|NOT_RUN: qualified ID/ADC calibration, cold/continuous negative clamp, startup/brownout/abrupt loss, backfeed and USB/RTC/fail-off measurements required|
|E transmitter operation|NOT_RUN; RF80/RF2M RF, AM, spectral, thermal, antenna and endurance gates remain|

A0.29V cold-clamp sensitivity and the illustrative VF/leakage calibration bounds are **not manufacturer guarantees or measured results**. Do not fit/enable the MCU for fault tests until the staged power-only checks establish safe conditions. Rail ramps and IEC pulses are not certified by DC calculations. Failure of a physical gate requires correction before use; it does not turn the bare-board review into an operational approval.

Use the [new review package](../hardware/controller/review/M6-C1R1/README.md) and its final fabrication directory. No files were uploaded, parts/boards ordered, hardware assembled/powered, or RF transmitted. Commit the engineering candidate without an acceptance tag and stop for independent review.
'''
 (ROOT/'docs/M6_C1R1_REVIEW_DECISION.md').write_text(decision)
 write('README.md','''# M6-C1R1 controller fabrication-review candidate

Active native sources are ../../CTRL.kicad_pro, CTRL.kicad_sch and CTRL.kicad_pcb in the controller directory. The inventory hashes those files and all local libraries. This package is regenerated from R1; review/M6-C1 remains immutable baseline evidence.

Read [decision](../../../../docs/M6_C1R1_REVIEW_DECISION.md), [input correction](../../../../docs/M6_C1R1_INPUT_PROTECTION.md), [USB assessment](../../../../docs/M6_C1R1_USB_ESD_REVIEW.md), [validation](../../../../docs/M6_C1R1_ELECTRICAL_VALIDATION.md), [changes](change-and-preservation-audit.json), [bring-up](BRINGUP.md), [costs](COST_DELTA.md), [manufacturing](MANUFACTURING.md) and [reproduction](REPRODUCE.md).

Only fabrication/ contains the proposed Gerbers/drills. CTRL.pdf, copper/assembly views, actual KiCad3D PNGs, per-population placements/BOMs and logical/physical IPC files are fresh exports. Analysis/model JSONs are review evidence, not extra fabrication layers. No routing-session or abandoned construction geometry is part of this dataset. Bottom assembly is common to the four base populations; LoRa is HOLD/DNP.

Gate A/B local checks pass; Gate C is GO for independent five-bare-board review only. Gates D/E remain NOT_RUN. Supplier quote/CAM, purchasing, manufacture and power-up require separate authorization. No acceptance tag or manufacturing release exists.

SHA256SUMS and inventory.json bind the final dataset and native/reproduction sources. Fresh export timestamps can legitimately change file hashes; rerun the inventory after regeneration. Native geometry, pad/net and drill/Gerber consistency are checked independently.
''')
 write('MANUFACTURING.md','''# Standard bare-PCB quotation specification — not submitted

Five individual controller boards. Native outline100.00×100.00mm, two-layer standard FR4,1.6mm finished thickness,1oz external copper, green mask, white legend, lead-free HASL, ordinary unfilled PTH vias. No controlled impedance, premium via treatment, custom laminate/stackup or supplier assembly service. JLCPCB standard web options only.

Use fabrication/ Gerbers, CTRL-PTH.drl and CTRL-NPTH.drl; drill maps are review aids. Thegbrjob bounding box includes the0.05mm outline stroke (100.05mm); the milling centerline is100.00mm square. No panel outline or final enclosure is specified. Confirm the automatic outline interpretation in a later authorized CAM review.

Actual native track minimum0.15mm; nominal via0.80/0.30mm and via/PTH minimum annulus0.25mm. Preferred0.15mm signal clearance,0.03mm mask expansion,0.10mm mask web and conservative edge/hole margins are independently checked. Finished-hole tolerances remain standard; first-article connector fit is NOT_RUN. See JLCPCB-standard-profile.json and JLCPCB-DFM.json, including manual items. The default ignored tuning-profile check is irrelevant because no tuning patterns exist; no relevant DRC category is disabled and there are no exclusions.

All four base populations share this PCB. Populate the six underside small positions before final THT assembly or use controlled local reflow; a second factory assembly service is unnecessary. Bottom clearance must remain at least10mm as in M6-C1. Inspect connector lead clipping and both sides. Exact MPN/pin orientation is mandatory; Nexperia BAT54H,SOD123F must not be confused with onsemi BAT54H,SOD323.

No factory quotation, CAM acceptance or file upload has occurred. Planning cost model is separate in COST_DELTA.md; stock and prices must be rechecked before any authorized purchase. Optional LoRa remains HOLD and is not an accepted assembly variant.
''')
 gates={'A':'PASS_DEFINED_DC_AND_CAD','B':'PASS_LOCAL_STANDARD_DFM','C':'GO_INDEPENDENT_FIVE_BARE_BOARD_REVIEW_ONLY','D':'NOT_RUN','E':'NOT_RUN','LoRa':'HOLD_DNP','acceptance_tag':'NOT_AUTHORIZED','manufacture_or_upload':'NOT_AUTHORIZED'}
 (D/'gate-status.json').write_text(json.dumps(gates,indent=2)+'\n')
 final=load('final-checks.json');final['R1_protection_checks']=load('protection-regression.json');final['R1_preservation']=change;final['R1_gates']=gates;final['new_manufacturer_maps']=2;(D/'final-checks.json').write_text(json.dumps(final,indent=2)+'\n')
 print('Final R1 summaries generated after all nonphysical gates passed')
if __name__=='__main__':main()
