#!/usr/bin/python3
"""Evidence-linked E5 review documents. No report substitutes for native checks."""
import collections,html,csv
from m5b_e5_common import *
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.strip()+'\n')
def svg(name,boxes,circles=(),notes=(),size=(190,200)):
 # Draw dimensioned envelopes with an automatic view box, including projections.
 xs=[x for _,x,y,w,h in boxes]+[x+w for _,x,y,w,h in boxes];ys=[y for _,x,y,w,h in boxes]+[y+h for _,x,y,w,h in boxes]
 x0=min(xs+[0])-12;y0=min(ys+[0])-12;x1=max(xs+[0])+12;y1=max(ys+[0])+12+5*len(notes);w=x1-x0;h=y1-y0
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*4}px" height="{h*4}px" viewBox="{x0} {y0} {w} {h}"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="white"/>','<style>text{font:2.4px sans-serif}.small{font-size:2.2px}</style>']
 colors=['#ddeedc','#dce9f8','#f6d4b6','#e9d9f3','#d5efee','#f4efb4']
 for i,(label,x,y,ww,hh)in enumerate(boxes):out.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="{colors[i%6]}" fill-opacity=".55" stroke="#333" stroke-width=".3"/><text x="{x+1}" y="{y+3}">{html.escape(label)}</text>')
 for label,x,y,d in circles:out.append(f'<circle cx="{x}" cy="{y}" r="{d/2}" fill="white" stroke="#333" stroke-width=".25"/><text x="{x+2}" y="{y-2}">{html.escape(label)}</text>')
 for i,n in enumerate(notes):out.append(f'<text x="{x0+2}" y="{y1-5*len(notes)+i*5}" class="small">{html.escape(n)}</text>')
 out.append('</svg>');write(OUT/name,'\n'.join(out))
def costs():
 rows=[]
 for qty in[5,10,20]:
  old=[15+200*qty*.0252,30+400*qty*.0252];new=[15+200*qty*.0165,30+400*qty*.0165]
  rows.append(dict(quantity=qty,E4R1_estimated_batch_EUR=old,E5_estimated_batch_EUR=new,delta_batch_EUR=[new[i]-old[i]for i in range(2)]))
 save('manufacturing-cost-comparison.json',dict(status='UNQUOTED_BUDGET_MODEL_NOT_JLCPCB_PRICE',area_mm2={'E4R1':25200,'E5':16500},area_reduction_percent=100*(1-16500/25200),formula='EUR15..30 setup + EUR200..400/m2 * quantity * actual board area; chosen budgeting assumptions, NOT published JLCPCB tariff',batches=rows,shipping_VAT_CAM_excluded=True,quotation=None,uploaded=False,component_delta_EUR=0,component_q10_EUR={'BOOST2S':50.27,'BUCK4S':49.03,'TRAIN_ONLY':14.11},component_unquoted_q10_EUR={'BOOST2S':28.09,'BUCK4S':27.95,'TRAIN_ONLY':10.02},cooling=dict(PA_SK81_bar_TIM='Retained E4R1 materials; no price saving claimed',pass_SK100='Retained E4 candidate MPN; reoriented with5mm stock spacer',pass_SK100_RS_observed_q1_q10_net_EUR=[16.48,15.17],pass_SK100_source='https://de.rs-online.com/web/p/kuhlkorper/1898088',observed_date='2026-10-19',stock_note='Listing showed51 additional available for dispatch; not reserved or a fleet commitment',spacer_allocated_q1_q10_EUR=[[.5,2],[.3,1]],spacer_first_stock_purchase_q1_EUR=[3,8],ordinary_support_hardware_q1_q10_EUR=[[1,3],[.7,2]],helper_FK213='Manufacturer catalogue dimensions/rating available; exact incoming pose and current fleet stock OPEN, cost remains unquoted'),platform_estimates=dict(carrier_q1_q10_EUR=[[3,8],[2,5]],posts_q1_q10_EUR=[[3,6],[2,4]],IDC_q1_q10_EUR=[[2,4],[1.5,3]],pigtails_q1_q10_EUR=[[3,8],[2,6]],status='Estimates, no invented supplier quantity breaks; minimum purchase cash may exceed allocated material'),source_assembly='Same .12mm source stencil, paste, initial X-ray/thermal qualification as E4R1; no new premium PCB process'))
def docs():
 d=json.loads((OUT/'DRC.json').read_text());errors=[x for x in d['violations']if x['severity']=='error'];warnings=[x for x in d['violations']if x['severity']=='warning'];counts=dict(collections.Counter(x['type']for x in warnings));opens=len(d['unconnected_items']);parity=len(d['schematic_parity'])
 gates={}
 for name in['compact-engineering.json','JLCPCB-DFM.json','verification.json','fabrication-data-audit.json','compact-power-and-return.json','source-assembly-DFM.json']:
  path=OUT/name;report=json.loads(path.read_text())if path.exists()else{};binding=report.get('native_sha256',report.get('native_SHA256',sha(HW/'RF2M.kicad_pcb')));gates[name]=str(report.get('status','')).startswith('PASS')and binding==sha(HW/'RF2M.kicad_pcb')
 ready=not errors and not opens and not parity and all(x['type']=='missing_courtyard'for x in warnings)and all(gates.values())
 decision='GO for independent evaluation-board review'if ready else'HOLD: native CAD or evidence closure remains incomplete'
 save('review-gates.json',dict(decision=decision,CAD_errors=len(errors),unrouted=opens,parity=parity,warnings=counts,required_reports=gates,physical='NOT_RUN',optional_dual_stack='HOLD',acceptance_tag=False,manufacturing_authorized=False))
 prefix='../hardware/2m/review/M5B-E5/'
 texts={
 'COMPACT_LAYOUT':f'''# M5B-E5 compact layout

The native RF2M candidate is 150 × 110 mm, reduced from 180 × 140 mm by 34.52% in area. Native origin is (20,20) mm. Four 3.2 mm NPTH centres are (25,25), (165,25), (165,125), (25,125); normalized centres (5,5), (145,5), (145,105), (5,105) match the actual RF80-V1R1 board. The controller and RF80 files are unchanged.

E4R1 `{BASE}` remains the electrical/source-joint baseline. The driver, PA, matching/filter, normal connector, source contact and bar move rigidly (−20,0) mm. Other blocks are placed and rerouted around them. [Every component displacement]({prefix}component-displacement.json) and [initial impact extraction]({prefix}initial-placement-and-impact.json) identify the actual arrangement. All values, MPNs, electrical package pads and population memberships are compared against E4R1.

J101 is at (27,80), battery J301 (35,120), normal SMA J501 (165,52.206), training MMCX J701 (165,116). J302 rotates 90° without changing pole numbering. Q401 moves to (115,26); R506 follows to (115,32). C401 rotates 180° for a short boost switch connection. C402 moves locally to (80.7,104); C307 rotates 180° for a ground escape, and reference-divider R810 moves to (125.5,97.5). These retain their original values and terminal nets. DC probes TP502 and TP303 move outside the helper cooling envelope; their final positions are in the displacement map. RF probes retain their positions relative to the matching network.

The routing audit identified a real washer hazard: new KEY copper crossed H6's exposed ground contact and inherited VPA copper lay under H5's metal washer. Explicit ground annuli, OD9.5/ID4.3 mm, and two additional ordinary ground vias now define the washer contacts. Those vias are outside the original 98-via source structure and receive no thermal-model credit. The affected DC/control conductors are rerouted around the contacts. Corner supports use insulating M3 posts/washers. See [washer evidence]({prefix}ground-washer-correction.json).

Nonessential footprint silk moves to assembly layers. Required board revision, connector/polarity, normal/training and mutually exclusive supply markings use 1 mm / 0.15 mm lettering. Current checks, rather than the initial autorouter result, determine review readiness.
''',
 'RF_PRESERVATION':f'''# M5B-E5 RF preservation

The seven ST-derived TL603–TL609 structures retain their actual 2.741 mm widths, pad-to-pad lengths, orientations, L/C values and internal placement. The PHA-1+, PD54008L-E and normal matching/filter group translates 20 mm left. This preserves its analytical distributed network; it does not prove physical gain, stability, AM or spectrum. [Native assertions]({prefix}compact-engineering.json) verify each line and package, not only schematic equality.

The recalculated nominal model at 144.7 MHz uses H=1.50 mm, Er=4.5, copper=0.035 mm: Z0≈50.005 Ω, effective Er≈3.3947. Broad ordinary-FR4 thickness/material/etch sensitivity spans approximately 39.4–63.4 Ω. Dielectric loss is about 0.044 dB/100 mm plus a conductor lower bound about 0.020 dB/100 mm. Solder mask and component transitions remain model uncertainties. Exact line delays, electrical lengths, input match and elliptic response are in [RF analysis]({prefix}RF-analysis.json) and its CSVs. No controlled-impedance service is required or claimed.

A local bottom-layer control corridor opens between X29 and X35.5 under the synthesizer/buffer periphery. This permits the isolated slow I²C branch to escape congested clock/power fanouts. No controlled matching line or PA ground return is moved. The resulting narrow control slot and source-clock return require spectral/jitter/immunity commissioning; see source-control-corridor.json.

Si5351-to-buffer clock wiring and the independent training clock are rerouted; they are not ST matching lines. CLK_NORMAL total copper shortens 15.956→13.258 mm (minimum width 0.20→0.15 mm, no vias); CLK_TRAIN increases 190.839→210.954 mm and 5→9 vias. NORMAL_CLOCK_BUF remains 2 mm / 0.35 mm, and TRAIN_CLOCK_BUF 3.280 mm / 0.20 mm. These totals include branches. An ideal uniform 0.15 mm microstrip over 1.5 mm FR4 is about 142 Ω / effective Er2.985, not a 50 Ω port. The additional training wire contributes roughly 6° at 144.7 MHz in that comparison. Actual mixed-layer returns, via transitions, CMOS source impedance and high-impedance buffer loading require waveform/ringing and off-path emission tests; these simple line estimates do not establish S11 or clock noise margins. Their full widths, lengths, via counts and nominal phase comparisons are reported separately. Clock ringing, buffer loading, source harmonics and local returns require commissioning. Training connector and filter membership remain unchanged. Normal/training connector centre separation decreases from approximately 87.94 mm to 63.794 mm; measured port isolation remains NOT_RUN.

One bottom-layer routing corridor changes: the matching-region track keepout ends at X168.6 instead of X170, allowing the modulator control conductor near X169 beyond the matching structures. Continuous ground beneath the distributed line bodies and all SMA ground contacts is retained. A simple infinite-plane estimate assigns about 0.4% of return-current density to a 0.15 mm slot at 4 mm lateral offset and 1.5 mm height; this is a locality estimate, not an EM solution or measured S11. See [peripheral return change]({prefix}RF-peripheral-return-change.json). RF pickup/stability and harmonics must be measured with the new placement.

The final native audit additionally compares all 36 original normal RF signal copper tracks/vias under the rigid translation; redundant autorouter additions are removed, not treated as matching improvements. All 26 ST component poses are preserved.

The complete source → PHA → final → filter → output path must be accepted at controlled dummy-load commissioning, including 144.500–144.900 MHz and configured legal training frequencies. Physical gain, carrier/PEP/ERP, sinusoidal AM depth, compression, oscillation, harmonics and port isolation remain NOT_RUN.
''',
 'THERMAL_MECHANICAL':f'''# M5B-E5 thermal and mechanical review

The E4R1 source joint is retained: 16 intentionally open source vias + 20 side + 8 end + 54 wing = 98. Source copper is 2.7 × 5 mm, continuous mask opening 2.1 × 5 mm, five paste windows total 6.765 mm², local stainless stencil 0.12 mm. No mask islands, filled/capped vias, guaranteed tenting or solder-fill conduction credit. [Source geometry/assembly gate]({prefix}source-assembly-DFM.json) and the Gerber/drill region audit bind this to the final board. The preserved controlled print/reflow, first-article X-ray and thermal process still applies. Edge inspection cannot establish hidden wet area.

PA cooling retains the 15 × 44 × 10 mm bar and Fischer SK81 100 SA (100 × 100 × 15 mm). The square sink rotates in plane so its channels run along board X; bar/contact/mount coordinates do not change relative to Q501. Sink native bounds X42..142/Y20..120, bar X84.5..99.5/Y28..72; holes H5/H6 (92,32)/(92,68). Extrusion-local taps are (12,50)/(48,50) after rotation. Minimum SK81-to-OD9 corner washer clearance is 12.5 mm. Underside projection is 25.2 mm; lowest Z=−26.8 relative to RF top. No package pressure or mounting load through solder joints.

Same-boundary FVM predictions at 40°C/4 W remain approximately 91°C nominal, 122°C conservative and 138°C with poor joint/contact. The conservative 110°C target remains NOT_MET. The 125°C engineering limit is conditional and physically OPEN. Selected mesh 0.1→0.05 mm changes source-to-bar resistance about 0.021 K/W; the retained 1 K/W allowance is not a bound on physical assembly uncertainty. All 2/3/4/5 W, 25/40°C, barrel 10/15/18/25 µm, solder/TIM/contact and lost-via sensitivities are retained. Fin rotation adds an explicit +0.25 K/W (+1°C at 4 W) sensitivity, not an asserted measurement. A 5°C inlet rise adds 5°C; sink 4→6 K/W adds 8°C. A sealed warm box is unsupported.

The existing Fischer SK10075SA pass heatsink is retained, rotated in its mounting plane: 75 mm along X, 40 mm forward projection, 66 mm along Z. A simple 15 × 20 × 5 mm stock aluminum spacer with one 4 mm clearance hole separates it from D45H11. Native sink box X80.04..155.04/Y−22.5..17.5/Z−20..46 leaves 2.5 mm from the PA sink. Both fin channels are upright with UP=−boardX. Independently support the heavy sink using ordinary brackets; do not hang it from transistor leads. [Manufacturer-authored drawing](https://docs.rs-online.com/0660/0900766b80f3d711.pdf).

Insulate the VPA collector tab with GS220P mica/grease and correctly installed IB6 shoulder hardware, M3×12 with verified thread engagement. At 4.24 W pass loss, catalogue sink 1.9 K/W + 1 K/W interface predicts case 52.3°C at 40°C. Conservative 2.85 + 1.5 K/W predicts 58.4°C. The 60°C case stop is unchanged; raised inlet temperature or 5.5 W can violate it. Hot SOA, sensor contact/lag, interface pressure and airflow remain unqualified.

BD139 remains at its original compact location, with an 8.5 mm body standoff and separately insulated MOD_SINK tab. Fischer FK213SA32 SOT32 catalogue dimensions 25.4 × 18 × 13 mm / 21 K/W support a reserved installed envelope X126.28..144.28/Y22.55..37.55/Z2..42. Verify exact incoming hole pattern, pose, lead protrusion and small-quantity supply before assembly. GS32P and suitable nylon hardware; do not force a TO220 shoulder washer into BD139. At 1.1 W, the conservative case/junction estimates are about 76/87°C, not measurements. [Manufacturer-authored catalogue](https://www.farnell.com/datasheets/17590.pdf).

Native 3D additions are explicitly clearance envelopes, not manufacturer STEP or proof of enclosure fit. Copper, source joint and PA values remain unchanged; real assembly fit and all thermal qualifications remain OPEN.
''',
 'COMMON_ENCLOSURE':'''# M5B-E5 common enclosure study

The mandatory controller+RF80 and controller+RF2M configurations share 150 × 110 mm RF boards and the 140 × 100 mm mounting pattern. Read-only controller dimensions remain 100 × 100 mm with asymmetric holes. Rotate it 180°, local origin (65,20), independent posts (160,78),(70,115),(70,25),(160,25). Controller bottom Z=53 mm. A 170 × 120 × 3 mm insulating carrier, bottom Z45, uses 40 mm nylon posts + 5 mm spacers and 5 mm controller posts. It is simple drilled/cut stock sheet, not a fourth electrical PCB.

The primary internal envelope study is 180 × 200 × 125 mm, external protected battery, UP=−boardX. Reserve separate open inlet/exhaust paths for the rear PA plenum and front pass sink; do not seal both into a shared warm air volume. Begin thermal qualification on the supported open frame, then measure the actual case inlet temperature. A weatherproof final enclosure is not qualified. The front bay supports the pass heatsink outside the RF outline; the underside PA sink has a vented plenum. Fin channels must remain upright and inlet temperature must be measured. RF80 retains its own thermal/service envelope unmodified. This is a dimensioned compatible envelope study, not a selected or thermally qualified final enclosure.

The carrier has a rear antenna cutout X109..162/Y110..120. ESP antenna keepout is approximately X111..159/Y111.75..132.75, with 15 mm surrounding clearance, no metal/battery/cable and 53 mm separation from RF PCB. USB near X165/Y100 needs an open service bay and accessible plug opening. LoRa pigtail routes left/rear outside ESP clearance, using the controller's band-specific antenna. Follow Espressif guidance; RF immunity and cable fit remain NOT_RUN.

RF2M initially uses a 150 mm keyed, continuity-tested IDC; RF80 220 mm. Pin 1 remains straight-through, with a cable half-twist where connector orientation requires. Start I²C at 100 kHz: 4.7 kΩ/200 pF illustrative rise ≈0.80 µs; measure actual cable capacitance and fail-off. Normal/training outputs use side-access right-angle pigtails and strain relief. Separate fused battery harnesses carry PA current. Four corner supports are insulating; only grounded bar fixings use metal washers.

Beside the RF board, the controller needs at least 260 × 110 mm board plane with a 10 mm gap; a wider case is the alternative, not a claimed fit in the RF footprint. Optional dual-RF study places RF2M top Z0, RF80 top Z55 and controller bottom Z100, requiring at least 170 mm case depth, separate vent paths and verified RF shielding/service access. It remains HOLD for thermal/EMC integration. Neither simultaneous transmission nor acceptance of this taller arrangement is required for the two mandatory configurations.

See dimensioned top, bottom and section SVGs and common-mechanical-platform.json in the E5 review. Actual plug fit, cooling, insulator integrity and mounting preload must be verified before operation.
''',
 'MANUFACTURING':'''# M5B-E5 manufacturing and cost

After independent review and explicit authorization, request five individual 150 × 110 mm boards: two layers, standard FR4, 1.6 mm, 1 oz, green mask, white legend, lead-free HASL, ordinary PTH vias. No impedance service, custom core, precision-hole service, filled/capped vias, premium plating or panelization. Edge.Cuts centreline defines the outline; the Gerber stroke does not enlarge it. JLCPCB CAM, quotation and purchasing remain separate, NOT_RUN activities.

The revisioned E5 fabrication ZIP contains only nine Gerbers and separate PTH/NPTH drills. Source stencil, drawings, analysis and historical datasets stay outside it. The native CAD and final exports must have matching hashes, drill counts and netlists. Intentional bodyless TL/probe courtyard warnings are individually documented; manufacturing failures are not excluded. Current published capabilities, local native-geometry DFM and factory CAM are different evidence.

The VMOD main copper is locally broadened up to 2 mm where native clearances permit, retaining short local necks. At 80°C copper resistivity, the contact-resolved sheet model predicts a worst PCB-path drop about 0.250 V at the stated 3/2/1.8 A envelopes; 30 µm face copper / 10 µm barrel sensitivity is about 0.294 V. A 1→0.5 mm analysis mesh changes the largest drop by about 1.1 mV. This is a model, not a measurement; thin long sense branches are excluded. The raw whole-segment estimate remains separately visible.

Electronics remain E4R1: quantity-ten estimates BOOST2S €50.27, BUCK4S €49.03, TRAIN_ONLY €14.11, containing €28.09/€27.95/€10.02 unquoted material. Complete quantity 6/10/20 BOMs remain in the review. No component savings follow from board area alone.

The bare-board budget model uses €15–30 setup plus €200–400/m² × area × quantity, explicitly chosen estimates, not JLCPCB tariffs or a quotation. Five E4R1 boards estimate €40.20–80.40 versus E5 €31.50–63.00; shipping/VAT/CAM excluded. Ten: €65.40–130.80 versus €48–96. Twenty: €115.80–231.60 versus €81–162. Obtain a fresh supplier quote; no prior cart price is transferable.

TRAIN_ONLY omits the PA, normal converter and all watt-level cooling hardware; its independent protected output remains. PA heatsink/bar/TIM and pass SK100 MPN are retained for the full populations. New stock spacer allocation €0.5–2 at quantity one / €0.3–1 at ten, with first stock purchase perhaps €3–8; support hardware €1–3 / €0.7–2, all unquoted. Common carrier/posts/IDC/pigtails are separate estimated materials. The source stencil, paste and first-article inspection process are inherited. Helper heatsink fleet stock remains a sourcing check. See manufacturing-cost-comparison.json for observed listing versus estimates.

The three-board readiness matrix names controller M6-L1, RF80 V1R1 and this E5 candidate. Other fabrication archives remain byte-for-byte unchanged. E5 supersedes E4R1 for ordering only after independent review and explicit authorization. No upload, order, assembly, power-up or RF transmission is performed by this milestone.
''',
 'REVIEW_DECISION':f'''# M5B-E5 review decision

**{decision}.** No acceptance tag, manufacture or transmitter release is authorized.

Native board: 150 × 110 mm, common 140 × 100 mm pattern, standard two-layer 1.6 mm / 1 oz FR4. E4R1 component values, manufacturer pad mappings, 20-pin controller contract, protections and all three populations are retained. The driver/PA/matching/filter/source/bar group translates rigidly 20 mm left; support circuits and connectors are placed and rerouted. Local washer-ground hazards are explicitly corrected. RF80 and controller CAD are unchanged.

Current CAD report: {len(errors)} DRC errors, {opens} unrouted, {parity} parity differences. Warning categories: {counts}. Native equivalence, full logic/package/ST regression, source assembly, actual copper DFM, power returns and fabrication consistency are separate mandatory gates in review-gates.json. A missing/failed gate keeps HOLD; an old PASS is not substituted.

Mandatory single-RF/controller arrangements have dimensioned envelopes. The optional dual-RF stack remains HOLD for enclosure/thermal/EMC integration. Source-joint and cooling geometry are retained; same-boundary 40°C/4 W predictions are about 91/122/138°C nominal/conservative/poor contact. The conservative 110°C target is unmet, and the 125°C physical thermal gate stays OPEN. Enclosure heating may exceed it. The initial source joint, contact flatness, convection and temperature must be qualified before RF use.

Electronics budget is unchanged with substantial unquoted material. Bare-board savings are only a setup/area budget estimate, not a quote. Supplier CAM, quote and purchasing require later authorization. All physical RF gain, PEP/ERP, true AM, stability, emissions, port isolation, controller immunity, protection timing, hot SOA and endurance tests remain NOT_RUN. Read the staged bring-up procedure before any population.
'''}
 for n,t in texts.items():write(ROOT/'docs'/('M5B_E5_'+n+'.md'),t)
 write(OUT/'README.md',f'''# RF2M M5B-E5 review candidate

**{decision}.** Active native authority: `hardware/2m/RF2M.kicad_pcb`. Baseline E4R1 `{BASE}` is archived. This package is for independent engineering review, not manufacturing release.

Read the six `docs/M5B_E5_*.md` reports, review-gates.json, current ERC/DRC/DFM, compact-engineering.json, thermal-model.json and dimensioned mechanical views. `development/` holds intermediate placement/routing analysis and is not a fabrication dataset. The revisioned fabrication ZIP is distinct from native source and stencil archives. Historical controller, RF80 and E4R1 packages are unchanged. All physical tests are NOT_RUN.
''')
 write(OUT/'MANUFACTURING.md',texts['MANUFACTURING'])
 write(OUT/'BRINGUP.md','''# E5 staged commissioning — all physical steps NOT_RUN

1. Verify bare-board outline/holes, package fit, pin maps, continuity and absence of shorts. Confirm exact BOOST2S or BUCK4S links; never both. TRAIN_ONLY excludes PA/converter/cooling.
2. On bench supports at least 40 mm high, apply current-limited low-voltage logic. Test ARM, SLOT, KEY, PROGRESS, both PREPARE signals, mute, reset, watchdog, faults and controller supply loss. No automatic rearming.
3. With driver/final absent, qualify selected converter and all rails on a bounded laboratory supply. Measure startup/shutdown/overvoltage/isolation, not with an unqualified Li-ion fault source.
4. Test modulator with a representative bounded load. Verify PWM reconstruction, crest/trough, disable and pass-device-short handling. Install independently supported insulated D45/BD139 heatsinks. Stop at D45 case 60°C; verify sensor contact/lag and hot SOA.
5. Follow E4R1 source print/reflow procedure using the local 0.12 mm stencil, five apertures and intentionally open vias. Record real profile. First assembly requires qualified X-ray/wetting assessment plus correlated thermal measurements. Inspect bottom for protrusion, clean/measure flat contact, install thin TIM and supported bar. Do not press the PA plastic or credit unverified solder-filled vias.
6. Fit a suitable 50 Ω dummy load and attenuated spectrum/envelope instruments. Start limited driver/PA supply and RF drive. Adjust only documented interstage alternatives. Check oscillation before increasing power. Measure gain, compression, carrier and PEP, actual 70–80% sinusoidal RF AM, harmonics and spurs across configured legal frequencies.
7. Calibrate independent µW training path. Measure normal/training isolation and verify the normal PA cannot energize the training connector. Check off-slot silence and faults.
8. Qualify at 25/40°C, 4 W continuous PA heat budget, declared passive orientation and actual enclosure inlet. Confirm source joint/TIM/case/junction inference with calibrated instruments; poor contact is a stop condition. 125°C is the PA engineering limit; conservative model target remains unmet until corrected/qualified evidence establishes the operating envelope.
9. Integrate controller using continuity-tested keyed IDC, separate fused pack harness and antenna keepouts. Test brownout, cable disconnect, power loss, rearming, schedules and profile calibration. Then endurance 12/24 h and continuous-beacon model; finally antenna ERP and field tests under separate authorization.

No current milestone report establishes a physical PASS for any step. Inspect live collector-tab insulation and source/ground continuity before applying power.
''')
 write(OUT/'REPRODUCE.md','''# Reproduction

Use installed KiCad 10.0.6 and `/usr/bin/python3` with pcbnew. Run from repository root. Do not run historical generators, which target frozen review directories.

```
/usr/bin/python3 tools/m5b_e5.py checks
/usr/bin/python3 tools/m5b_e5.py verify
/usr/bin/python3 tools/m5b_e5.py models
/usr/bin/python3 tools/m5b_e5.py dfm
/usr/bin/python3 tools/m5b_e5_engineering.py
/usr/bin/python3 tools/m5b_e5_ground.py
/usr/bin/python3 tools/m5b_e5_closure.py
/usr/bin/python3 tools/m5b_e5_mechanical.py
/usr/bin/python3 tools/m5b_e5.py thermal
DISPLAY=:97 LIBGL_ALWAYS_SOFTWARE=1 /usr/bin/python3 tools/m5b_e5.py exports --render
/usr/bin/python3 tools/m5b_e5_delivery.py
/usr/bin/python3 tools/m5b_e5_reports.py
/usr/bin/python3 tools/m5b_e5_final_audit.py
```

Commands that refill/save the native board must finish before another board writer starts. Final delivery binds native hashes, exported drills and revision. Verify the SHA256 manifest after reproduction; PDFs/3D can contain tool-dependent metadata. Layout construction scripts are development history; the committed native board is the routed source authority.
''')
def main():
 guard();from m5b_e5_mechanical import main as mechanical
 mechanical(svg);costs();docs();print('Wrote evidence-linked E5 review documents and mechanical drawings')
if __name__=='__main__':main()
