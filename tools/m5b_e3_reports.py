#!/usr/bin/python3
"""Assemble current E3 reviewevidenceanddocumentationfromfinalnativeinputs."""
import json,csv,collections,subprocess,math
import pcbnew as p
from m5b_e3_common import *
from m5b_e3_models import table

def doc(n,s):(ROOT/'docs'/('M5B_E3_'+n+'.md')).write_text(s.strip()+'\n')
def mdtable(headers,rows):return'\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---'for _ in headers)+' |',*['| '+' | '.join(map(str,r))+' |'for r in rows]])+'\n'
def main():
 guard();drc=json.loads((OUT/'DRC.json').read_text());erc=json.loads((OUT/'ERC.json').read_text());ver=json.loads((OUT/'verification.json').read_text());dfm=json.loads((OUT/'JLCPCB-DFM.json').read_text());assert not[v for s in erc['sheets']for v in s['violations']];assert not drc['unconnected_items']and not drc['schematic_parity'];assert all(v['type']=='missing_courtyard'and v['severity']=='warning'for v in drc['violations'])and len(drc['violations'])==11;assert dfm['status']=='PASS_AUTOMATED_NATIVE_GEOMETRY'and dfm['native_sha256']==sha(HW/'RF2M.kicad_pcb')
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};parts=json.loads((HW/'RF2M.electrical.json').read_text())['parts'];pro=json.loads((HW/'RF2M.kicad_pro').read_text());ds=pro['board']['design_settings'];assert not ds['drc_exclusions'];disabled={k:v for k,v in ds['rule_severities'].items()if v=='ignore'};assert disabled=={'tuning_profile_track_geometries':'ignore'}
 disp=[]
 for v in drc['violations']:
  r=v['items'][0]['description'].split()[-1];assert r in set(LENGTHS)|{'TP601','TP602','TP603','TP604'};f=fs[r];assert f.IsExcludedFromBOM()and f.IsExcludedFromPosFiles();disp.append(dict(ref=r,classification='B_INTENTIONAL_NON_COMPONENT',position_mm=[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)],geometry='Mask-coveredflat-ended2.741mmRFlinewithintentionalnettie'if r.startswith('TL')else'0.6mminlinebareprobecontactinsideRFconductor;nopaste',reason='No purchasedbodyorassemblyvolume. Acomponentcourtyardwouldbemisleading. Nativecopper/mask/hole/edgechecksremainactive;componentbodyclearancesarecheckedindependently.'))
 save('via-policy-exceptions.json',dict(counts=dfm['statistics']['via_land_counts'],preferred_land_drill_mm=[.8,.3],exceptions=dfm['preferred_margin_exceptions'],status='FINAL_NATIVE_GEOMETRY'));save('DRC-warning-dispositions.json',disp);save('DRC-coverage.json',dict(KiCad=drc['kicad_version'],rules=ds['rules'],severities=ds['rule_severities'],disabled=disabled,disabled_justification='Onlyunusedlength-tuningprofilecheck;allmanufacturing,copper,footprint,courtyard,maskandlegendcategoriesenabled.',exclusions=ds['drc_exclusions'],warnings=disp,ERC_default_ignored=erc['ignored_checks'],ERC_coverage_note='GlobaldefaultERCfootprintfilterignoreiscompensatedbyactivePCBfootprint_filters_mismatchandactual320package/padparity. No new ignoredcategory introduced.'))
 pads=[];holes=collections.Counter();vias=[]
 for f in fs.values():
  for a in f.Pads():
   d=a.GetDrillSize();pads.append(dict(ref=f.GetReference(),pad=a.GetNumber(),net=a.GetNetname(),x_mm=p.ToMM(a.GetPosition().x),y_mm=p.ToMM(a.GetPosition().y),drill_x_mm=p.ToMM(d.x),drill_y_mm=p.ToMM(d.y),footprint=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())))
   if d.x:holes[(round(p.ToMM(d.x),3),'NPTH'if a.GetAttribute()==p.PAD_ATTRIB_NPTH else'PTH')]+=1
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):vias.append(t)
 table('pad-connectivity.csv',pads);table('via-connectivity.csv',[dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),x_mm=p.ToMM(t.GetPosition().x),y_mm=p.ToMM(t.GetPosition().y),land_mm=p.ToMM(t.GetWidth(p.F_Cu)),drill_mm=p.ToMM(t.GetDrillValue()))for t in vias])
 save('stackup-mechanical.json',dict(revision=REV,board_mm=[180,140],finished_mm=1.6,finished_tolerance_fraction=.10,layers=2,nominal_copper_um=35,analytic_core_mm=1.50,core_is_not_purchase_specification=True,Dk_model=4.5,mask_model_each_mm=.015,finish='Lead-free HASL',factory_impedance_control=False,special_process=False,ordinary_via_land_counts=dfm['statistics']['via_land_counts'],source_vias=32,component_holes=[dict(diameter_mm=d,kind=k,count=n)for(d,k),n in sorted(holes.items())],mounting_NPTH_mm=3.2,corner_centers_mm=[[25,25],[195,25],[195,155],[25,155]],spreader_centers_mm=[[112,32],[112,68]],manual_assembly=True,no_customer_panel=True))
 # Physicalbare-boardelectricaltestmergesonlydocumentedTLaliases.
 from m5b_e3_common import aliases
 aa=aliases();save('fabrication-net-aliases.json',dict(reason='IntentionalTLcoppernetties;usephysicalIPCforbare-boardE-test',aliases=aa));logical=(OUT/'RF2M-logical.ipc').read_text().splitlines();physical=[]
 for line in logical:
  if line[:3]in['317','327','367']:line=line[:3]+aa.get(line[3:17].strip(),line[3:17].strip()).ljust(14)+line[17:]
  physical.append(line)
 (OUT/'RF2M-physical-netties.ipc').write_text('\n'.join(physical)+'\n')
 gates=[r['gate']for r in csv.DictReader((HW/'review/M5B-E1/acceptance-register.csv').open())]+['E3standardHASLhidden-padjointandmaskcoverage','E3thermalpathat35um/1.6mm','E3RFmatchingandnewSMAlaunch','E3connectorincomingfit']
 table('acceptance-register.csv',[dict(gate=g,status='NOT_RUN',serial='',conditions='',instrument='',result='',uncertainty='',operator_date='')for g in gates])
 audit=json.loads((OUT/'pinout-audit.json').read_text());save('critical-package-audit.json',dict(revision=REV,manufacturer_devices=audit['PCB_physical_devices'],native_package_count=ver['native_PCB_package_checks'],manufacturer_sources='../M5B-E1/source-log.json',source_SHA256=sha(HW/'review/M5B-E1/source-log.json'),E3_changes='Sourcepadmask/pasteandviaarray;J101/J301finishedholes;locallibrarylegendvariants. Othercopperpadlocations/shapes/numberspreserved.',incoming_mechanical_and_solder_qualification='NOT_RUN'))
 models=json.loads((HW/'review/M5B-E1/3D-model-status.json').read_text());models['E3']='FreshactualKiCadrendersinspectedtop/bottom/isometric;boardthickness1.6. LocallysourceddimensionalenvelopesarenotqualifiedvendorSTEP. Standardconnectorbodymodelsremainabsent;2Dpackage/holeauditstillapplies.';save('3D-model-status.json',models)
 summary=dict(revision=REV,baseline_commit=BASE,baseline_tag='m5b-e2',KiCad=drc['kicad_version'],ERC_errors=0,ERC_warnings=0,DRC_errors=0,DRC_warnings=11,unrouted=0,schematic_parity_issues=0,exclusions=0,disabled=disabled,logic_combinations=4096,state_scenarios=39,existing_mutations=37,critical_pin_maps=len(audit['devices']),ST_network_positions=26,native_package_pad_sets=ver['native_PCB_package_checks'],DFM_status=dfm['status'],DFM_mutations=len(json.loads((OUT/'DFM-regression.json').read_text())['mutations']),engineering_mutations=3,physical_tests='NOT_RUN',decision='GOforindependentfive-boardstandard-JLCquotation-datareview;NOupload/orderauthorization',preserved_files=len(preserved()))
 assert summary['critical_pin_maps']==42 and summary['native_package_pad_sets']==320;save('final-checks.json',summary)
 native=[HW/'README.md',HW/'RF2M.kicad_pro',HW/'RF2M.kicad_pcb',HW/'RF2M.electrical.json',HW/'ARDF_2M.kicad_sym',HW/'sym-lib-table',HW/'fp-lib-table',*HW.glob('*.kicad_sch'),*(HW/'ARDF_2M.pretty').glob('*'),*(HW/'ARDF_2M.3dshapes').glob('*')];save('native-inputs.json',{str(f.relative_to(ROOT)):sha(f)for f in sorted(set(native))if f.is_file()})
 profile=json.loads((OUT/'JLCPCB-standard-profile.json').read_text());save('source-log.json',dict(retrieved='2026-10-16',manufacturing_primary_sources=profile['sources'],retained_component_source_log='../M5B-E1/source-log.json',connector_update=['https://www.we-online.com/components/products/datasheet/61202021621.pdf','https://www.jst.com/wp-content/uploads/2025/06/eVH.pdf','https://www.amphenolrf.com/en-us/assets/file/4065861576/'],access_notes='WEcurrentmanufacturerPDFread;JSTcachedmanufacturerPDFfromE1readaftercurrentURL403. Amphenolmanufacturerindexcatalogdimensionsretained;nodistributorpreviewusedasnewdrawing.',commercial_quote=None,files_uploaded=False))
 cost=json.loads((OUT/'costs.json').read_text());budget=mdtable(['Population','6 each','10 each','20 each','Unquoted at10'],[[pop,*[f"€{next(x for x in cost['summary']if x['population']==pop and x['fleet']==q)['component_net_EUR']:.2f}"for q in[6,10,20]],f"€{next(x for x in cost['summary']if x['population']==pop and x['fleet']==10)['unquoted_net_EUR']:.2f}"]for pop in['BOOST2S','BUCK4S','TRAIN_ONLY']])
 lengths=mdtable(['Line','E2 mm','E3 mm','Width mm'],[[r,f'{LENGTHS[r]/LENGTH_SCALE:.4f}',l,WIDTH]for r,l in LENGTHS.items()])
 doc('ENGINEERING_CHANGE',f'''# M5B-E3 engineering change report

M5B-E3 replaces the E2 fabrication assumptions with ordinary two-layer **1.6 mm / 1 oz JLCPCB FR4, green mask, white legend and lead-free HASL**. This is an unbuilt evaluation design. E2 remains immutable at `m5b-e2` / `2ca4c8e`; its manufacturing-review GO is superseded. RF80, M4A, accepted ADRs and historical packages are hash-preserved.

The native project remains `hardware/2m/RF2M.*`. Initial inspection is recorded in [initial-change-impact.json](../hardware/2m/review/M5B-E3/initial-change-impact.json). The comparison baseline is Git, not an overwritten E2 export.

| Affected function | Actual implementation | Electrical impact |
| --- | --- | --- |
| Substrate | 0.8 mm/70 µm →1.6 mm/35 µm; no dielectric constraint | RF width/phase and power/thermal models recalculated |
| TL603–609 | Real flat-ended 2.741 mm copper; lengths scaled0.981206 | Preserves nominal E2 calculated phase; ordinary FR4 tolerance remains |
| Matching placement | Walked outward from fixed Q501 gate/drain | Small shifts, at most0.519 mm; all lumped values and topology retained |
| RF junctions/output | Replaced obsolete overlapping routes with direct junctions, flat copper and 8 mm SMA taper | New pad/stub/launch parasitics remain physical alignment gates |
| RF return | Bottom RF track keepouts retained; top fill-only channel widened to y46–62 | Avoids accidental coplanar loading; no bottom signal cut under matching |
| Power | Selectively enlarged existing main routes, mostly0.7–1.5 mm |35 µm native contact-graph voltage/drop model; short necks retained explicitly |
| Vias | Preferred0.80/0.30; local0.70/0.30 and 0.60/0.30 exceptions | All ordinary through-vias; list actual coordinates and nets inDFM report |
| PA source |12→32 ordinary0.80/0.30 GND vias;4×8 at 0.6 mm pitch | Thicker barrel path compensated partly; no solder-fill thermal credit |
| Source assembly | Copper landing unchanged; mask caps/paste grid; open bottom contact | Ordinary LPI tenting is neither plugging nor insulation |
| J101 |1.30 mm holes /1.90 mm lands | Standard hole tolerance clears maximum specified pin diagonal |
| J301 |1.80 mm holes, existing lands | More practical hole-fit margin on 1.6 mm board |
| Legend |≥1.0 mm /0.15 mm; thin library art moved toFab in real local variants | Some dense refs rely on complete assembly drawings; no DRC suppression |
| Local routing | Control/supply detours at widened RF strip and enlarged IDC | No net, pin contract, safety behavior or population change |

[engineering-regression.json](../hardware/2m/review/M5B-E3/engineering-regression.json) compares actual E2/E3 net membership and manufacturer pad geometry. Purchased MPNs, electrical values, population fields and prices are unchanged. Only the seven nonpurchased TL values/footprints change electrically descriptive metadata. Local symbol footprint filters now explicitly allow the connector footprints; pin definitions are unchanged.

The exact native track/placement and library deltas are available in Git and the JSON change reports. Development router/DRC investigations are isolated under `review/M5B-E3/development/`; only `gerbers/` is proposed fabrication data. No procurement, upload, manufacture or physical test occurred.
''')
 doc('RF_STACKUP',f'''# M5B-E3 RF and stackup redesign

The purchase configuration is ordinary **1.6 mm, two-layer FR4, 1 oz**, without controlled impedance or a named/custom core. The analytical nominal model is 1.50 mm copper-to-copper dielectric,35 µm copper, Dk4.5, tanδ0.02 and 15 µm mask per side. These sum to1.60 mm; they are **not separate fabrication tolerances**. Published finished thickness ±10% does not fix dielectric spacing. Ordinary outer1 oz copper includes plating;35 µm is nominal, not a minimum finished-thickness guarantee. [JLC capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/), [copper guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight) and [calculator guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator) were reviewed2026-10-16.

Finite-thickness Hammerstad/Jensen calculations give **2.741 mm width,50.005 Ω,εeff3.3947** uncoated. E2 was1.102 mm over0.64 mm/70 µm/Dk4.3. Scaling lengths by√(εeff_E2/εeff_E3)=**0.981206** preserves nominal144.7 MHz phase. Conventional microstrip fits; grounded coplanar geometry would add gap/fence/pad constraints without a demonstrated benefit, so no arbitrary CPW50 Ω claim is used.

{lengths}
All line bodies are real copper, not zero-length schematic wires. Butt ends prevent round-cap shorts across series pads. Q501 remains fixed; matching components move outward by fractions of a millimetre. The normal output is a flat conductor with a1 mm initial transition and 8 mm taper to1.0 mm at the fixed SMA. A100-section lossless taper model gives about 40 dB return loss between50 Ω planes at 144.7 MHz. It omits the connector pin/via and pad fringing, so it is not a measured launch result.

The top fill-only keepout x48–190/y46–62 mm retains local grounded components while keeping adjacent plane copper away from the wide matching lines. Bottom signal-routing keepouts beneath the RF strip and thermal contact remain. The native copper preview and DRC check the resulting returns. Grounded component pads/stubs make the local field nonideal microstrip; their effects remain alignment requirements.

[RF-tolerance-sweep.csv](../hardware/2m/review/M5B-E3/RF-tolerance-sweep.csv) sweeps h1.30–1.70 mm, Dk4.1–4.8, copper30–50 µm and width±20%, at 144/144.5/144.7/144.9/146 MHz. The deliberately combined extremes span **39.39–63.44 Ω**. This is ordinary-FR4 uncertainty, not a supplier impedance tolerance. These matching lines are short; their impedance error must be considered with electrical length, not treated as a long50 Ω cable. [input-match-comparison.csv](../hardware/2m/review/M5B-E3/input-match-comparison.csv) shows near-identical nominal E2/E3 ABCD behavior with the same illustrative3 Ω/80 pF gate plus33 nH feed model. That load is not a measured144 MHz PD54008 impedance.

A disclosed first-order thin-mask perturbation predicts about 49.88 Ω at 15 µm and 49.75 Ω at 30 µm; this is approximate fringe-energy sensitivity, not a full-wave solution. Estimated dielectric loss is 0.044 dB/100 mm; a conductor lower bound is 0.020 dB/100 mm. Surface roughness, solder, component Q and RF grounding can increase losses. At144.7 MHz35 µm copper is several skin depths; its RF loss does not simply double relative to70 µm.

Source/filter junctions remain short lumped0.35 mm conductors, not claimed50 Ω lines. [source-and-stub-parasitics.csv](../hardware/2m/review/M5B-E3/source-and-stub-parasitics.csv) quantifies changed equivalent L/C; an approximate source-filter cascade predicts0.456 dB versus E2's0.510 dB at 144.7 MHz. Branch stubs, driver/source impedances and Q/SRF are omitted. This supports retaining the values, not an achieved drive or harmonic claim. The elliptic filter topology and values remain identical; its ideal transfer is separately exported and is not an emissions result.

The Si5351/PHA-1+/PD54008L-E architecture, initial 10 dB source pad,19 dBm driver target, tunable C631/C633/L634 and independent training output remain. Final gain, AM depth/PEP, stability, harmonic rejection and port isolation are **NOT_RUN**. Use the bounded original adjustment set and one complete-device acceptance procedure; no separate coupon program is introduced.
''')
 doc('THERMAL_MECHANICAL','''# M5B-E3 thermal, power and mechanical review

The board remains180 ×140 mm with the six original3.2 mm NPTH mounts. The1.6 mm material adds0.8 mm to the clamping stack; do not bend the board to compensate. The source, flange and connector pad mappings remain manufacturer-specific. [critical-package-audit.json](../hardware/2m/review/M5B-E3/critical-package-audit.json) and [engineering-regression.json](../hardware/2m/review/M5B-E3/engineering-regression.json) verify actual nets and copper geometry, with the two documented connector-hole changes.

The PD source remains2.7 ×5 mm copper, electricalGND. Its array is now **32 ordinary0.80/0.30 vias**,4×8 on 0.6 mm pitch, with 1.6/0.3=5.33 nominal aspect ratio. The thermal calculation uses a copper barrel only, k385 W/mK. Parallel barrel resistance is approximately 7.66 K/W at 18 µm plating,9.19 K/W at 15 µm and 13.78 K/W at 10 µm. E2's12 vias at 0.8 mm/25 µm were approximately 7.35 K/W. JLC publishes **18 µm average**, not a guaranteed minimum at every barrel. No minimum-plating negotiation or solder-fill credit is required or claimed.

With RθJC3 K/W, spreading/contact2, TIM1 and sink3.5 K/W,4 W PA heat at 40°C ambient predicts approximately 109°C junction at 18 µm,115°C at 15 µm and 133°C at 10 µm. Thus the barrel model is not thermal qualification. The initial heat budget is≤4 W and engineering junction limit125°C; the real path must be measured on the first staged assembly. At1 W carrier ERP,−1 dBd gain,0.75 dB output loss and 80% AM, average PA-planeRF is approximately 1.98 W. Assumed PA efficiencies35–50% imply approximately 3.67–1.98 W heat;30% would exceed the budget. Measure averageV(t)I(t), RF power and temperature; do not infer efficiency from the ST fixed-supply reference.

Ordinary top mask caps are0.4 mm squares over0.3 mm holes. Segmented source mask/paste allows wetting around them; bottom holes/contact are open. Mask tenting is not a hermetic plug. It is not electrical insulation or proof against solder wicking. Inspect hidden-pad joint quality, mask coverage and solder loss during controlled manual reflow. No filled/capped via process is requested. The14 ×12 mm bottom window x105–119/y49–61 has no foreign copper. Use the retained16 ×44 ×8 mm spreader,0.15–0.25 mm insulatingTIM k≥3 W/mK and dielectric rating≥100 V, a separate GND strap, and the lower sink. Verify flatness, pressure and electrical isolation rather than assuming ideal contact.

D45H11 pin2/tab is liveVPA; BD139 pin2/tab is liveMOD_SINK. Keep their insulated thermal hardware separate from the grounded PA assembly. Retain pass-sink≤3.5 K/W plus≤1 K/W interface, measured case≤60°C, junction≤125°C and the approximately 66°C NTC trip. The insulated NTC must be bonded to the case and strain-relieved. The unchanged no-tone/high-current model can exceed60°C at continuous full power; competition duty and sine-AM average reduce heat, but **continuous full-carrier operation is unqualified**. Do not raise the trip threshold to hide this. Reduce energy and stop if the acceptance limits are exceeded.

[power-native-main-paths.json](../hardware/2m/review/M5B-E3/power-native-main-paths.json) finds actual contacting pad/track/via paths for all11 main-current connections. It charges every traversed track its full80°C resistance and excludes thin long sense branches. Input routes are evaluated at 3 A, regulator/pass rails2 A andPA supply1.8 A. Calculated worst individual connection drop is 0.290 V (VMOD); VPA is 0.130 V. These are conservative full-current bounds, not measured droop. Main routes are predominantly0.7–1.5 mm; the 0.3502 mm boost-pad necks are only1.56/0.77 mm. Their spreading estimate is separated from an inappropriate isolated-long-trace current rule. The all-branch net totals deliberately overcount branches and must not be read as actual full-load heating of sense stubs.

Copper30 µm would raise the 35 µm resistance estimates17%; inspect rail headroom under crest current. The nominal upstream9.02 V,7.2 V crest and series-pass operating point are unchanged. Include shunt, switch, inductor and connector drops separately. The0.068 Ω shunt dissipates0.272 W at 2 A; R413 dissipates0.152 W at 180 mA. Ground-plane resistance is modeled separately; actual return distribution and converter loops require current/temperature qualification.

J101's20 holes are now1.30 mm with 1.90 mm lands. The Wurth61202021621 drawing002.001 specifies square0.64±0.15 mm pins: maximum diagonal1.117 mm, below JLC's1.22 mm minimum finished hole. Its3±0.15 mm tail leaves≥1.09 mm below a1.76 mm board. J301's1.80 mm holes retain existing lands; its nominal1.14 mm square posts have1.612 mm diagonal versus 1.72 mm minimum holes. JST specifies1.6 mm boards. The normalSMA retains1.50/1.70 mm holes; its nominal1.02 mm square shell pins and 3.94 mm tails remain compatible with 1.6 mm construction. Confirm incoming plating/burrs, lead dimensions, fit and polarity before soldering. TRAINMMCX is SMT and thickness-independent.

Retain40 mm corner standoffs, trim leads≤2.5 mm and keep≥5 mm from unrelated conductive fixture parts. Adjust external sink mounting by 0.8 mm; do not use transistor leads as mechanical supports. Cable strain relief and open-bench support remain required. Actual KiCad top/bottom/isometric views were inspected; custom models are dimensional envelopes and three standard connector body models remain absent. The2D package audit is authoritative. No final enclosure fit is claimed. All physical thermal/mechanical tests are **NOT_RUN**.
''')
 doc('JLCPCB_DFM',f'''# M5B-E3 JLCPCB manufacturability audit

The versioned [JLCPCB-standard-profile.json](../hardware/2m/review/M5B-E3/JLCPCB-standard-profile.json) records official source URLs,2026-10-16 retrieval, hard capability limits, preferred margins and manual checks. It distinguishes nominal 1 oz from actual plated external copper. The requested old production-time URL is unavailable; the official equivalent is [PCB fabrication services and production time](https://jlcpcb.com/help/article/pcb-fabrication-services-and-production-time). No commercialCAM review, accepted quote or upload occurred.

`tools/m5b_e3_dfm.py` reads the **native PCB**: actual layer/thickness/stack properties, track shapes, copper graphics, pads, drill geometry, hole spacing, annuli, edge distances, mask apertures/webs, visible legend and filled-zone polygon slivers. It checks physical TL aliases instead of reporting intentional net ties as shorts. Its spatial pair tests do not merely read configured KiCad rule minima. Native KiCad's actual narrow-connection/thermal checker remains an additional mandatory gate. Combined coverage is recorded in `DRC-coverage.json`, `JLCPCB-DFM.json`, `engineering-regression.json` and `final-checks.json`.

| Constraint | Published capability / E3 policy |
| --- | --- |
| Layers/thickness/copper | Standard2L FR4 /1.6 mm±10% /nominal 1 oz |
| Track/space | Vendor1 oz0.10/0.10; actual policy≥0.15/0.15 |
| Via | Preferred0.80/0.30;0.70/0.30 and 0.60/0.30 where congested; all ordinary PTH |
| Annulus | ComponentPTH≥0.25; actual minimum 0.275 mm. Via preferred0.25; local0.20/0.15 exceptions explicitly inventoried |
| Holes | Via hole gap≥0.20; component hole gap≥0.45. Hole-to-foreignCu≥0.20 via/NPTH,≥0.28 componentPTH |
| Mask | Green1 oz web≥0.10; actual apertures inspected; ordinary tenting only |
| Legend | Visible height≥1.0, stroke≥0.15, mask gap≥0.15 |
| Routed edge | VendorCu≥0.20; board policy0.50 |
| Special process | None; no controlled impedance, custom core, filled/capped/blind/buried vias or factory assembly |

The final via sizes/counts and every preferred-margin exception are in `JLCPCB-DFM.json` and `via-connectivity.csv`. Smaller lands are intentional local congestion decisions, **not a supplier process exception**. They retain0.3 mm holes and lands well above JLC's small-via/premium thresholds. All32 PA source vias use the preferred0.8 mm land. No global enlarging or blanket DRC exclusion is used.

Final KiCad 10.0.6: **ERC0 errors/0 warnings; DRC0 errors;0 unrouted;0 parity;11 warnings;0 exclusions**. Every manufacturing category is enabled. Only `tuning_profile_track_geometries` is ignored because no tuning-profile geometry exists. ERC default informational ignores are disclosed, including footprint filters; the PCB's corresponding filter warning and actual package/pad comparison are active.

The11 retained warnings are TL603–609 and TP601–604. Each is classifiedB, intentional non-component. They have no purchased body, paste,3D body or assembly volume; a component courtyard would be fictitious. TLs are mask-covered copper net ties, and probes have intentional0.6 mm mask openings. The native copper/mask/edge checks remain enabled. Exact coordinates and individual dispositions are in `DRC-warning-dispositions.json`.

Regression testing rejects E2's thickness/copper/finish/legend under the E3 profile. Mutations detect wrong thickness, narrow tracks, insufficient annuli, blind vias, premium microdrills, undersized legend,2 oz copper, unsupported finish and an actual 0.05 mm copper gap. Three additional native RF/source mutations supplement the preserved37 electrical/physical mutations. The engineering gate also checks TL length/width,32 grounded source vias, source mask policy, thermal-window isolation, connector holes and unchanged purchased circuitry.

Manual reviews are explicit: HASL flatness and hidden-pad solder quality; mask coverage; incoming connector dimensions; TIM/heat-sink insulation and actual thermal contact; and independent finalCAM/assembly inspection. They are not fabricated automated PASS results. Ordinary drill/etch variation and measured RF/thermal behavior remain qualification gates. The locally verified result establishes standard-process design compatibility; it does not assert factory CAM acceptance.
''')
 doc('MANUFACTURING_COST',f'''# M5B-E3 standard manufacturing and cost

Select **5 pieces,2 layers, standardFR4,1.6 mm,1 oz, green mask, white legend, lead-free HASL**, one180 ×140 mm routed rectangle. Use ordinary plated through-vias, standard electrical test and no impedance control, via filling/capping, special laminate, castellations, edge plating or factory assembly. Do not substitute1.6 mm/2 oz: JLC's0.16 mm geometry requirement would conflict with existing0.15 mm signals. The1 oz power/thermal analysis provides no reason to select that alternative. Do not specify the analytical1.50 mm dielectric as a negotiated core tolerance.

The proposal is manually assembled in stages, with one of five boards initially populated. HASL is selected for ordinary cost and hand assembly. Its nonplanarity requires inspection/reflow care on the PHA, PD andRNW hidden contacts; see [JLC's HASL discussion](https://jlcpcb.com/blog/hasl-surface-finish-pcb). Their fine contacts are a solder-process risk, not an established incompatibility requiring ENIG. Do not silently change finish inCAM. If real incoming planarity or joint inspection fails, hold assembly and review ordinary ENIG as a separate quoted correction. A stencil/paste file is an assembly aid, not a required JLC assembly service.

Only `hardware/2m/review/M5B-E3/gerbers/` is proposed fabrication data. It contains nine copper/mask/paste/legend/outline Gerbers, job metadata, separatePTH/NPTH drills and maps. Retain the **physical-netties IPC** as a review reference; standard JLC electrical test derives connectivity from Gerber copper, so no special netlist service is required. the logicalIPC and alias table explain intentional RF net merges. Do not upload `development/` or analysis screenshots. `SHA256SUMS` and `native-inputs.json` bind the files to the final native project. No files have been uploaded.

Purchased parts and prices are unchanged fromE2. Full itemized6/10/20 budgets and source classifications are regenerated, not hand-patched:

{budget}
There are272 fitted purchased parts/25ICs inBOOST2S,268/25 inBUCK4S and 103/13 inTRAIN_ONLY. RF lines, test pads and footprint assignments are not extra purchased parts. The dated pricing observations remain observations, not current reservations. L301 zero-stock/backorder, L634 nonstocked cut-tape lead time and U950 conflicting regional stock remain visible. Unquoted material remains€28.09/€27.95/€10.02 respectively at 10. No new supplier quote is claimed.

`PCB-cost-estimate.csv` gives a deliberately transparent **engineering allowance**, not JLC pricing:€10–20 setup plus€250–500/m² at actual 0.0252 m² area. Five boards:€41.50–83; ten:€73–146; twenty:€136–272 net. Shipping€10–25 and destinationVAT are separate. The historicalE2 five-board allowance was€60–100 before shipping; the ranges overlap, so **no achieved PCB saving is booked**. An actual automated quote is still pending. Published capability, localDFM compatibility, budget estimate, quote and factory CAM acceptance are separate statuses.

The180 ×140 outline is retained because the RF return strip, separate ports, hand-rework access and two insulated thermal assemblies use the geometry. Blank evaluation area is acknowledged, but shrinking/panelizing this first board would add routing/mechanical risk unrelated to the manufacturing correction. No100 ×100 promotional price is assumed. External heatsinks/TIM/mounts remain approximately€12 per initially populated board, harness€3 and antenna/feed€12 estimates; controller, battery, charger, enclosure and labor remain separate. Measure actual commissioning time rather than booking fictitious labor savings.

The package is **GO for independent standard-option quotation-data review**, subject to user authorization before upload. It is not an order or manufacturing release. Normal automated pricing should require only the standard selections above; no exceptional fabrication agreement is part of the design.
''')
 doc('BRINGUP','''# M5B-E3 single-board bring-up considerations

All entries in `review/M5B-E3/acceptance-register.csv` begin **NOT_RUN**. No assembly or power-up is authorized by this CAD milestone. Preserve the detailed [E1 procedure](M5B_E1_BRINGUP.md) and [E2 sequence](M5B_E2_BRINGUP.md), with the E3 changes below. Use one integrated transmitter and one acceptance record; no separate RF coupons.

1. **Unpowered inspection.** Confirm the exact E3 revision,1.6 mm board and standard1 oz construction, connector holes/identity/polarity, all manufacturer-specific pins, mutually exclusive2S/4S links andTRAIN_ONLYDNP population. Inspect HASL planarity, source mask caps and hidden-pad reflow. Inspect source and RNW joints with suitable magnification and hidden-joint inspection/rework capability. Do not mistake tenting for filled vias. Verify spreader/TIM insulation, its separate GND strap, live pass/helper tabs and adjusted1.6 mm clamping stack. No board bending or conductive sink bridge is acceptable.
2. **Logic only.** Initially omit normal converters, MMIC and final. Apply3.3 V with 100 mA current limit, increasing only after explaining consumption. Verify reset, watchdog, captured ARM/path/profile, key-inactive arming, retuning inhibit, mutually exclusive ports and deliberate rearm. Both physical outputs must remain inactive outside permission. Use only bounded logic fixtures; Boolean tests do not qualify asynchronous pulse widths.
3. **Power only.** Fit exactly one converter population. Start with a current-limited lab input:2Svariant6.0 V/100 mA or4Svariant12.0 V/100 mA; raise current in documented steps with dummy loads. Confirm pack window and 9.02 V/full orselected reduced rail. KeepR952 open and driver/final absent until driver preregulation,5 V regulation and shutdown pass. Sweep normal input6–8.4 or12–16.8 V as applicable. Do not connect wrong-pack voltage as a trial. Test specified faults with bounded current/energy, not a Li-ion pack.
4. **Driver-supply qualification.** Retain E1's two regulators and 18 V-ratedTPS22810. Verify normal approximately 4.8–5.2 V and the defined fault acceptance≤5.7 V before fittingPHA. A bounded16.8 V upstreamfault can exceedTLV767's16 V recommended input while below18 V absolute maximum; this is a fault test, not normal operation or surge immunity. Measure isolation/inhibit timing and repetition. No sole20 µsRC guarantee is assumed.
5. **AM/dummy load.** Test D45H11/BD139 with bounded representative load and proper insulated sinks. Verify sine reconstruction, feedback sign/stability,7.2/4.0/0.8 V starting crest/center/trough and shutdown. These voltages do not establish RF modulation depth. Record crest droop and power-path temperature on 35 µm copper. Limit pass case 60°C and engineering junction 125°C; verify the approximately 66°C sensor trip/lag. Never raise the trip to overcome insufficient cooling.
6. **Normal RF.** Fit the verified RF parts, connect an adequately rated50 Ω load, attenuator/coupler and analyzer. Start with the 10 dB source pad, low bias and low PA supply/current. Use the retained C631/C633/L634 adjustment set only when needed. Measure source/driver level/compression, frequency/stability, carrier power, averageRF, PEP, true 70–80% RF sine AM, sidebands, harmonics and spurs. New microstrip/taper/FR4 behavior requires end-to-end alignment; no manufacturer2-stage power claim proves the derivative. Record off-slot silence and controlled fault withdrawal. Derive PA heat conservatively from averageV(t)I(t)+driveRF−connectorRF. Start below1 W heat; increase in steps only while case/junction estimates remain bounded. Qualify the E3 heat path up to its≤4 W initial budget; at 40°C ambient require inferredTj≤125°C and adequate margin. Stop on excessive heat, drift, instability or poor joints.
7. **Training/isolation.** Normal converter/PA remain absent inTRAIN_ONLY. Verify independentµW output, modulation, calibration, silence and measured normal-to-training isolation. Never infer isolation from separate schematic nets alone.
8. **Operational acceptance.** Verify permitted training frequencies and championship144.500–144.900 MHz configuration, slot timing, watchdog/fault/rearm and both power profiles. ERP calibration must include actual antenna/feed gain and uncertainty. At−1 dBd,1 W carrier ERP needs1.259 Wconductedcarrier and 4.079 WconnectorPEP at 80%AM; these are calculations, not outputs achieved. Assess12 hfull/24 hreduced competition duty separately from continuous beacons. Record RF/thermal/endurance results before any operational release.

Required shared instruments remain a current-limited supply, calibrated RF power/PEP measurement,50 Ω load, spectrum analyzer, oscilloscope/envelope detector, appropriate attenuation/probes and temperature/current logging. A VNA is useful for the bounded alignment if required. Ordinary passive probes can detune exposed RF contacts; prefer calibrated pickup or output-coupler measurements. Hardware qualification and antenna/field tests remain NOT_RUN.
''')
 doc('REVIEW_DECISION',f'''# M5B-E3 review decision

**GO for independent review and, after explicit user authorization, upload of the five-board standard-JLCPCB dataset for quotation.** No manufacturing release is granted. E2 remains frozen at `m5b-e2` / `2ca4c8e`; its manufacturing recommendation is superseded.

The completed native board is **180 × 140 mm, two-layer standard FR4, 1.6 mm, 1 oz, green mask, white legend and lead-free HASL**. It requires ordinary through-vias and no controlled impedance, custom core or premium process. The schematic architecture, purchased MPNs/values, controller contract, protection behavior and population variants are preserved.

Implemented changes include 2.741 mm RF lines with approximately 1.88% shorter lengths, matching placement shifts of at most 0.519 mm, flat junctions and a tapered SMA launch. Power routes are selectively wider. The PA source now has 32 ordinary preferred-size thermal/ground vias. Connector holes and legend have standard-process margins. Local control escapes and ground connections were repaired without moving the RF ports or mounting holes.

**KiCad 10.0.6 results:** ERC zero errors and warnings; DRC zero errors; zero unrouted connections; zero schematic/PCB parity issues; eleven individually justified bodyless-feature warnings; zero exclusions. No manufacturing category is suppressed. Preserved coverage passes: 4,096 logic combinations, 39 states, 37 mutations, 42 manufacturer pin maps, 26 ST network positions and 320 package/pad sets. The independent native-geometry DFM gate, eleven new DFM mutations and three additional RF/thermal geometry mutations pass. Exact results and commands are in the review package.

Calculated nominal microstrip impedance is 50.005 Ω. Combined ordinary-process extremes span 39.39–63.44 Ω; the short matching lines, component junctions and launch still need end-to-end RF alignment. These calculations do not establish gain, ERP, clean AM or emissions.

The source thermal model predicts approximately 109°C junction at 4 W heat and 40°C ambient with 18 µm average barrels, but approximately 133°C at 10 µm. No guaranteed minimum plating or filled-via process is hidden in the purchase specification. Staged assembly must establish joint quality and thermal margin, using the initial 4 W heat budget, 125°C junction engineering limit and retained 60°C pass-case limit. Live D45H11/BD139 tabs require insulated hardware. Continuous full no-tone carrier, actual RF/AM, isolation, antenna ERP and 12 h / 24 h endurance remain **NOT_RUN**.

Quantity-ten component budgets remain **€50.27 BOOST2S / €49.03 BUCK4S / €14.11 TRAIN_ONLY**. Their unquoted portions remain €28.09 / €27.95 / €10.02. Five bare boards have an unquoted engineering allowance of **€41.50–83 before shipping and VAT**. Actual JLCPCB pricing and factory CAM acceptance are pending. No achieved price saving or supplier stock reservation is claimed.

Fresh schematic, BOMs, copper/assembly/placement views, actual KiCad renders, logical/physical netlists, Gerbers, separate drills/maps, native and fabrication-review archives, and SHA-256 inventory are under `hardware/2m/review/M5B-E3/`. The fabrication ZIP contains only nine Gerbers and two drill files; analysis and development data are separate. Source and drill coordinates/counts are checked against the final native board.

There is no remaining identified CAD fabrication blocker. Next steps are independent review, explicit authorization before external submission or ordering, and separately authorized staged assembly/commissioning of one board. RF80, M4A, accepted ADRs and historical revisions are preserved. No upload, purchase, manufacturing, assembly, power-up or RF operation occurred.
''')
 (OUT/'README.md').write_text('''# M5B-E3 standard JLCPCB review package

**CAD milestone — NOT RELEASED.** Active native project: `../../RF2M.kicad_pro`, `../../RF2M.kicad_sch` and `../../RF2M.kicad_pcb`. Frozen comparison baseline: `m5b-e2` / `2ca4c8e`. Start with the [review decision](../../../../docs/M5B_E3_REVIEW_DECISION.md).

The proposed standard options are five boards, 180 × 140 mm, two-layer FR4, 1.6 mm, 1 oz, green mask, white legend and lead-free HASL. No controlled impedance or special process is required. The fabrication-review ZIP contains exactly nine Gerbers and two drill files. The native ZIP contains the editable project and libraries. Neither archive authorizes an upload or order.

Only `gerbers/` and the fabrication-review ZIP contain proposed fabrication data. Analysis reports and `development/` are not fabrication inputs. Logical and physical IPC files document intentional RF net aliases; ordinary factory electrical test can derive connectivity directly from the Gerber copper. No special netlist service is required.

Reproduce from the repository root with KiCad 10.0.6 and `/usr/bin/python3` providing pcbnew and Pillow:

```sh
/usr/bin/python3 tools/m5b_e3.py checks
/usr/bin/python3 tools/m5b_e3.py verify
/usr/bin/python3 tools/m5b_e3.py models
/usr/bin/python3 tools/m5b_e3_engineering.py
/usr/bin/python3 tools/m5b_e3.py dfm
DISPLAY=:97 /usr/bin/python3 tools/m5b_e3.py exports --render
/usr/bin/python3 tools/m5b_e3.py reports
/usr/bin/python3 tools/m5b_e3_delivery.py
/usr/bin/python3 tools/m5b_e3.py artifacts
sha256sum -c hardware/2m/review/M5B-E3/SHA256SUMS
```

Rendering needs an existing X display or Xvfb with software OpenGL. Exact CLI commands and rendering environment are recorded in `check-commands.json` and `export-commands.json`. Historical generators and archived implementation aids must not be run against the finished board.

The eleven DRC warnings describe intentional bodyless RF copper/probe features. No manufacturing category is suppressed. Manual HASL/hidden-joint inspection, thermal contact, RF/AM, supply-fault, antenna and endurance qualification remain **NOT_RUN**. Standard published capability and local DFM compatibility are separate from quotation and factory CAM acceptance. No files have been submitted externally.

The three fresh KiCad renders show all native component positions, including mutually exclusive converter alternatives. The population-specific assembly drawings and BOMs determine actual fitment. Custom models are dimensional envelopes; missing connector body models are disclosed in `3D-model-status.json`.
''')
 (OUT/'MANUFACTURING.md').write_text('''# Proposed standard web-order configuration

Select **5 individual PCBs, 180 × 140 mm, 2 layers, standard FR4, 1.6 mm, 1 oz, green mask, white legend and lead-free HASL**. Use ordinary through-vias and standard electrical test. Assembly is manual and staged.

No controlled impedance, custom core, filled/capped/plugged vias, special laminate, edge plating or factory assembly is requested. Do not substitute 2 oz or historical E2 fabrication files. The 1.50 mm dielectric / Dk 4.5 record is an analytical model, not a separately negotiated purchase tolerance.

After explicit authorization, the proposed upload file is `RF2M-M5B-E3-fabrication-review.zip`: nine Gerbers and separate PTH/NPTH drills. Job metadata, drill maps, source CAD, IPC references and analysis are deliberately outside that ZIP. Standard factory electrical test derives physical connectivity from the copper; keep the physical IPC/alias report as an independent reference.

Check SHA-256 inventory and ordinary automated checkout options/price before any order. No RF copper resizing is authorized. HASL planarity, ordinary mask tenting, connector fit and hidden solder joints require incoming/assembly inspection. Tenting is not plugging or insulation. No quotation, factory CAM acceptance, upload or order has occurred.
''')
 print('E3reviewdocuments,nativeauditandmanufacturinghandoffgenerated')
if __name__=='__main__':main()
