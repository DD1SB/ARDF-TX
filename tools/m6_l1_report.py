#!/usr/bin/python3
"""Finalize a source-backed M6-L1 review, never a physical acceptance report."""
import json,hashlib,re,csv,subprocess,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-L1'
def load(n):return json.loads((D/n).read_text())
def save(n,x):(D/n).write_text(json.dumps(x,indent=2)+'\n')
def write(n,s):(D/n).write_text(s.strip()+'\n')
def doc(n,s):(ROOT/'docs'/n).write_text(s.strip()+'\n')
def canonical(f):
 # Drop only non-geometric X2 provenance/net/component attributes and comments.
 # Aperture definitions, masks, polarity, coordinates and drawing order remain.
 return '\n'.join(s for s in f.read_text().splitlines() if not s.startswith(('G04','%TF.','%TO.','%TA.','%TD')))
def drill_geometry(f):
 return '\n'.join(s for s in f.read_text().splitlines() if not s.startswith(('; DRILL file KiCad','; #@! TF.CreationDate,')))
def main():
 cad=load('CAD-results.json');assert all(cad[k]==0 for k in ['ERC_violations','DRC_errors','DRC_warnings','unrouted','parity']) and not cad['exclusions']
 assert cad['ignored_categories']==['tuning_profile_track_geometries']
 dfm=load('JLCPCB-DFM.json');assert not dfm['errors']
 e=load('electrical-regression.json');assert e['native_pad_instances']==704 and e['RF_baseline_files_unchanged']==1220 and len(e['native_mutations'])==20 and e['hardware_enable_combinations']==4096
 assert len(load('DFM-regression.json')['mutations'])==7 and len(load('protection-regression.json')['native_and_numeric_checks'])==16
 host=load('host-test-results.json');assert all(x['exit_code']==0 for x in host['commands']) and 'Ran 46 tests' in host['commands'][0]['stderr']
 sha=hashlib.sha256((P/'CTRL.kicad_pcb').read_bytes()).hexdigest()
 for n,k in [('native-preservation.json','current_sha256'),('antenna-native-geometry.json','native_sha256'),('JLCPCB-DFM.json','native_sha256'),('artifact-audit.json','board_sha256')]:assert load(n)[k]==sha,(n,'stale native evidence')
 assert len(load('LoRa-negative-geometry.json')['tests'])==21
 fab=[]
 for f in sorted((D/'fabrication').iterdir()):
  old=P/'review/M6-C1R1/fabrication'/f.name
  if not f.is_file() or not old.exists():continue
  raw=f.read_bytes()==old.read_bytes();geom=None
  if f.suffix in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1']:geom=canonical(f)==canonical(old)
  if f.suffix in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1'] and f.suffix not in ['.gtl','.gto']:assert geom,f.name
  drill=None
  if f.suffix=='.drl':
   drill=drill_geometry(f)==drill_geometry(old);assert drill,f.name
  fab.append(dict(file=f.name,baseline_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),current_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),byte_identical=raw,drill_geometry_identical_ignoring_generation_timestamps=drill,Gerber_graphics_identical_ignoring_only_X2_attributes_and_comments=geom))
 save('fabrication-equivalence.json',dict(status='PASS',files=fab,method='Freshly generated from final native board. Full raw hashes recorded. For nonidentical Gerbers only comments/X2 attributes removed; aperture/polarity/draw stream must match. PTH/NPTH drills retain every tool/hole/format command; only generation-timestamp comment lines differ.',copper='F.Cu: only local Hirose underbody GND-fill strip removed, bounded by native boolean comparison. F.Silkscreen: board revision marking updated. Signal tracks, all vias/pads/mask/paste/drills/outline and B.Cu geometry retained.'))
 rf=load('RF-analysis.json');rows=rf['nominal'];summary=rf['summary'];cost=load('LoRa-costs.json')['variants']
 before=load('analysis/before-keepout-RF.json')
 assert rows==before['nominal']
 save('RF-change-comparison.json',dict(status='PASS_CALCULATED_COMPARISON_ONLY',before='analysis/before-keepout-RF.json',after='RF-analysis.json',native_board_sha256=sha,nominal_results_identical_at_extraction_resolution=True,interpretation='The small ground-fill deletion is outside the resolved transverse sections. This does not prove physical launch or parasitic equivalence; physical VNA/RF commissioning NOT_RUN.'))
 pins=load('module-22-pin-audit.json')['pins']
 with (D/'module-pin-matrix.csv').open('w') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['pin','TR4_V2','TR8_V1','TR8_V2','native_net','disposition']);w.writerows([x['pin'],x['TR4_V2'],x['TR8_V1'],x['TR8_V2'],x['net'],x['disposition']] for x in pins)
 table='| Band | Electrical length | Delay | Calculated line RL | Calculated line IL | Worst material/model IL |\n|---|---:|---:|---:|---:|---:|\n'+'\n'.join(f"| {int(x['frequency_Hz']/1e6)} MHz | {x['electrical_length_deg']:.2f}° | {x['delay_ps']:.1f} ps | {x['return_loss_dB']:.1f} dB | {x['insertion_loss_dB']:.3f} dB | {summary[str(int(x['frequency_Hz']))]['line_only_insertion_loss_max_dB']:.3f} dB |" for x in rows)
 doc('M6_L1_MODULE_COMPATIBILITY.md','''# M6-L1 module and connector compatibility

The existing single U70 landing is nominally compatible with **SX1262TR4-GC / SX1262ZTR4-GC** and **SX1262TR8-GC / SX1262ZTR8-GC**. This is a documented supplier alias, not an inference from the SX1262 chip name. LCSC C42381681 links a manufacturer ZTR4 V2.0 PDF byte-identical to the official download. C42381682 links ZTR8 V2.0, also byte-identical to Silicontra's newer official download. The requested ZTR8 V1.0 has the same pin/land topology. Revision V2.0 versus V1.0 is a document revision; no TR-prefix-specific alternate package is indicated. The source URLs and exact downloaded hashes are in [manufacturer-evidence.json](../hardware/controller/review/M6-L1/manufacturer-evidence.json).

Normalize **TR4 V2 and TR8 V2 by a 90° counterclockwise rotation**, with no reflection, to the native F.Cu/top-side view: pin 1 lower-left, pins 1–11 left-to-right on the lower row, pins 12–22 right-to-left on the upper row. TR8 V1 is already drawn in that orientation. The older blank outline alone does not explicitly label its viewing side; the later component-side/pin-function drawings supply the cross-check. A bottom PCB/service view is mirrored for viewing only, not a different footprint. See [normalized drawing](../hardware/controller/review/M6-L1/normalized-module-views.svg).

| Dimension | Manufacturer evidence | Implemented carrier land |
|---|---|---|
| Body | 15 × 15 mm, no mechanical tolerance or height specified | F.Fab corrected from 15 × 16.7 to 15 × 15 mm; position unchanged |
| Terminal count / pitch | 22 / 1.27 mm | All 22 verified; 1.27 mm |
| Terminal width | 0.80 mm nominal | 0.80 mm copper width |
| Terminal depth | 1.37 mm nominal | 2.20 mm land length; 1.35 mm nominal inner overlap, 0.85 mm outer toe |
| First terminal offset | 1.12 mm callout | First centre X = −6.38 mm; last +6.32 mm |
| Row spacing | Body outer edges 15 mm; no recommended carrier pad-centre spacing | Pad centres Y = ±7.25 mm, separation 14.50 mm |
| Hole / castellation | Illustrated, diameter/tolerances not dimensioned | No carrier drilled holes or via-in-pad |
| Mask / stencil | Not prescribed by Silicontra | Mask expansion 0.03 mm, nominal mask web 0.41 mm; standard paste lands |
| Assembly clearance | Not prescribed | Conservative existing 16 × 18.1 mm courtyard retained |

Ten pitches plus twice 1.12 mm equal 14.94 mm, not exactly 15 mm: a 0.06 mm drawing/rounding residual. The carrier's 0.03 mm row-centroid offset is retained, rather than inventing a tighter package tolerance. The 14.50 mm number is **our carrier land placement**, not a manufacturer-specified terminal-centre distance. First incoming modules must be checked against these dimensions and pin 1 before soldering. Absence of manufacturer tolerances remains explicit; it is not evidence of a different TR4/TR8 package.

All 22 native pad numbers, nets and functions pass [the pin matrix](../hardware/controller/review/M6-L1/module-pin-matrix.csv). Pins 6/7/9 are NC. Pin 8 is **DIO3, unused configurable IO**, with a no-connect usage marker; its old generic IO label is clarified to DIO3, not reclassified as a required NC. No external TCXO driven from DIO3 is fitted. Pins 5/10 carry DIO1/BUSY, 14/15/16/17 are SCK/MISO/MOSI/NSS, 18 reset, 21 antenna; all specified ground contacts and VCC 13 remain.

J7 remains **Hirose U.FL-R-SMT-1(10)**. Its nominal recommended PCB pattern is verified from Hirose's drawing/catalog: signal 1.05 × 1.00 mm at (−1.525, 0), ground 2.20 × 1.05 mm at (0, ±1.475), in the native rotated orientation. The ground separation derives from the 4.00/1.90 mm outer/inner pattern dimensions. Native rounded corners are retained; these are ordinary land shapes, not a claim that the maker specifies those radii. The maker uses SIG/GND terminology; carrier pad numbers 1 and duplicated 2 map those contacts explicitly. The underbody top-copper keep-out is corrected to the full 2.20 × 1.90 mm rectangle, permitting the explicitly intended SIG land. The old 0.11 mm trimming left unintended GND fill; it is removed. Bottom ground remains. Solder mask over the insulating underbody is allowed; unnecessary exposed-mask windows are not added.

The historical Hirose catalog explicitly includes (10), 2500/reel. The current series catalog corroborates the pattern, while newer packing options differ. Mouser's exact (10) listing offers individual cut tape, MOQ 1: a full reel is not required. The (01) bag version uses the same landing but its observed MOQ 100 is less practical here; no substitution is needed. Sources and procurement limitations are in [SOURCING.md](../hardware/controller/review/M6-L1/SOURCING.md).

Copper lands, pitch, RF signal feed, solder mask, paste and drills are retained. A narrow top-ground strip inside the full Hirose no-traces rectangle is removed by a localized keep-out correction. Bottom ground and the ground stitch remain. The body drawing, optional-population/symbol metadata and PCB revision legend also change. These are CAD compatibility findings; actual module identity, solder fit and RF performance remain physical acceptance tasks.
''')
 doc('M6_L1_ANTENNA_FEED.md',f'''# M6-L1 antenna-feed analysis

Retain the existing **0.45 mm × 5.25 mm** straight F.Cu route, (97.89,33.75) to (97.89,28.50) mm. There are no series components, signal vias or RF stubs. The endpoints are U70 antenna pin 21 and J7 signal pad 1. Neither module nor connector moves. The native geometry audit identifies the local top-ground correction and unchanged signal/pad/mask/paste/drill geometry in [native-preservation.json](../hardware/controller/review/M6-L1/native-preservation.json) and [fabrication-equivalence.json](../hardware/controller/review/M6-L1/fabrication-equivalence.json).

This is a **locally discontinuous grounded-coplanar/microstrip hybrid**. The middle section has approximately 0.255 mm top-ground gaps; the module land widens to 0.80 mm and the U.FL land to 1.05 mm. At the connector the right top-ground gap grows to about 2.4 mm because of the required underbody keep-out. Bottom GND is continuous under the route and the sampled ±1 mm corridor. The local GND stitch is at (95,29) mm, roughly 3 mm from the launch; top ground also joins the module's ground terminals. That is not zero-inductance grounding. Native 5 µm transverse / 50 µm longitudinal sections and the actual via geometry are exported in [antenna-native-geometry.json](../hardware/controller/review/M6-L1/antenna-native-geometry.json), with [an annotated view](../hardware/controller/review/M6-L1/antenna-feed-detail.svg).

The model uses Qucs' conductor-backed CPW conformal mapping (equations 12.10–12.17, elliptic integrals evaluated by AGM), cascaded lossy ABCD sections, with a conventional narrow microstrip comparison. Larger measured gaps bracket the asymmetric launch. Nominal substrate separation is 1.53 mm after two nominal 35 µm copper layers; ordinary finished-board thickness is 1.6 mm. Nominal FR4 Er = 4.5. The independent sensitivity sweep includes substrate separation 1.37–1.69 mm, Er 4.0–5.0, copper 30–45 µm, width ±20%, extra gap ±0.05 mm, loss tangent 0.015–0.030, conductor-loss allowance and effective-permittivity mask increment 0–0.25. These are engineering ranges, not a factory RF-material guarantee. JLCPCB publishes ±10% finished thickness, ±20% track-width tolerance, nominal two-layer Er 4.5 and mask Er 3.8; no controlled impedance is ordered. [JLCPCB](https://jlcpcb.com/capabilities/pcb-capabilities/), [Qucs model](https://qucs.github.io/tech/node86.html).

{table}

Nominal local characteristic impedance varies approximately **52–105 Ω** over the pads/launch; the whole-line arithmetic mean is about **65.5 Ω** in the segmented model. It is not a uniform 50 Ω line. Nominal effective Er is about 2.88–3.19. Calculated dissipative line loss alone is 0.022/0.035 dB at 433/868 MHz; the table adds matched-port mismatch. The full material/model sweep gives minimum line-only return loss about {summary['433000000']['line_only_return_loss_min_dB']:.1f}/{summary['868000000']['line_only_return_loss_min_dB']:.1f} dB. The worst calculated line insertion loss corresponds to less than 4% power loss. The short line is therefore credible for this evaluation PCB without adding a matching network or widening it into adjacent module ground lands.

Reference planes are explicitly the **module terminal-21 carrier solder-land centre and U.FL signal solder-land centre**, with nominal 50 Ω module/load assumptions. To relate those to the internal module antenna port and the mated cable, a separate sensitivity adds 0–1.5 nH series and 0–0.35 pF shunt at each end. Its nominal-material minimum calculated return loss is about 19.9/14.1 dB at 433/868 MHz. Those parasitics are illustrative, not measured or guaranteed bounds. Infinite equipotential grounds, HASL roughness, mask fields, the finite ground plane and unequal return geometry limit the model. The microstrip comparison is a topology sensitivity, not a statement that actual top copper disappears. It does not replace a 3D EM model or VNA measurement, and does not bound an arbitrarily mismatched antenna.

The same connector/feed serves both bands; external antennas differ. A band-correct 50 Ω antenna and commissioned pigtail are mandatory. No dual-band antenna is assumed. Preserve the ESP32 antenna all-layer keep-out; route the coax north along the J7 side, away from its printed antenna and the RF-module heatsinks. RF2M harmonics can fall near both LoRa bands, so initial LoRa TX uses quiet/off-slot windows. Receiver blocking, actual antenna match, emissions and coexistence are NOT_RUN. See [variant and power contract](M6_L1_LORA_VARIANTS.md).
''')
 total='| Base | NO_LORA | LORA_433 | LORA_868 |\n|---|---:|---:|---:|\n'+'\n'.join('| '+b+' | '+' | '.join(f"€{cost[b+'_'+v]['netEUR_per_unit']['10']:.2f}" for v in ['NO_LORA','LORA_433','LORA_868'])+' |' for b in ['FOX_MIN','RF80_FULL','RF2M_FULL','UNIVERSAL'])
 doc('M6_L1_LORA_VARIANTS.md',f'''# M6-L1 optional radio, power and assembly contract

One PCB and one U70/J7 footprint support these independent radio options on any of the four existing base-controller populations:

| Assembly option | Trusted configuration | U70 | Antenna |
|---|---|---|---|
| NO_LORA | NONE | DNP | None; J7/R70/R71/C70/C71 DNP |
| LORA_433 | SX1262TR4_GC_433 | SX1262TR4-GC, C42381681 | Commissioned 433 MHz system |
| LORA_868 | SX1262TR8_GC_868 | SX1262TR8-GC, C42381682 | Commissioned 868 MHz system |

The native master retains an 868 MHz orderable MPN as its **DNP default**, with the 433 alternate selected in its own assembly BOM. All six optional positions must be fitted together for either radio option. Both options share identical copper; no GPIO, IDC connector, RTC, battery protection, USB or RF enable changes. [Twelve complete population BOMs and costs](../hardware/controller/review/M6-L1/LoRa-populations.json) cover the orthogonal choices; the old UNIVERSAL_LORA_OPEN name is superseded.

Do not infer the RF band from GetStatus or an SX1262 response. Establish it from the fitted-part/lot and trusted commissioning record; inspect supplier label and pin-1 geometry against the source register. An unknown, contradictory, uncommissioned or unresponsive radio leaves LoRa TX disabled. NONE is normal. A radio failure must not stop otherwise valid autonomous RTC-controlled ARDF operation. The host contract in `firmware/controller_hw/lora.py` requires a trusted exact population, matching antenna band, commissioning, stable power/main-pack validation, initialized response, approved frequency/power policy and an airtime authorization. It performs no RF probing. Its synthetic test policies are not legal country settings. Production firmware must independently enforce actual regional bands, EIRP/antenna gain and duty/airtime limits; the module's 22 dBm capability is not permission to use it.

Both modules are nominal 3.3 V / 120 mA at maximum stated RF power, with about 5 mA receive current. Common supply operation is within their 2.0–3.7 V / 1.8–3.7 V documented ranges. Reserve **150 mA** for radio TX as an engineering allowance; 120 mA is a published operating point, not a guaranteed all-corner transient maximum. Existing C70 100 nF and C71 10 µF remain near the module, on the common V3V3 domain. The native full-segment copper model gives roughly 0.149 Ω from regulator output to U70.13 at 80°C; a 150 mA radio contribution drops about 22 mV. The C70/C71 local paths add about 6.3/7.6 mΩ (roughly 1 mV at 150 mA). Shared rail load/ground effects still need oscilloscope tests. No new regulator or active switch is justified.

An effective local 4 µF capacitance scenario supporting a 150 mA step for 1 µs gives approximately 38 mV capacitive droop; 10 µs would give 375 mV if the regulator did not respond. This demonstrates the need for measurement, not a promised transient response. The previous 0.4 A steady-controller budget remains: 40 mA host + one 150 mA RF logic port + 150 mA LoRa allowance = 340 mA. Wi-Fi/BLE stays off. Do not convert the earlier 0.92 A short-burst allowance into a continuous rating. Initial LoRa TX is disabled on USB-only power and during ARDF RF slots; RX/diagnostics can be commissioned separately. NO_LORA has none of the six optional loads.

SPI is shared with the control shift registers. Keep NSS high except for a deliberate radio transaction, and SHIFT_LATCH low throughout it. Every control update must reload all 16 shift bits and latch atomically under a bus lock; radio data must never be latched as a control word. Direct key/slot/progress GPIO ownership is unchanged. Hold/reset/init the radio deliberately and validate BUSY/response before commands. DIO3 remains unused; do not select an external-TCXO mode based on another vendor's module. Selected module oscillator/RF-switch/SPI initialization is a commissioning/driver task; this milestone supplies no LoRa protocol stack. Remote commands retain all local pack, RTC, frequency, interlock and deliberate-rearm checks.

Use a short 50 Ω U.FL/MHF-I-compatible to normal-SMA bulkhead pigtail; **Taoglas CAB.011**, 95 mm, is a documented example. Separate antenna examples are **TE ANT-433-CW-HWR-SMA** (433 MHz quarter-wave; needs its specified counterpoise) and **ANT-868-CW-HWR-SMA** (868 MHz half-wave). These examples have manufacturer documentation; direct-store/distributor availability and prices remain unquoted, so band-correct equivalents may be used after their own data review. Never confuse SMA with RP-SMA. Cable loss and antenna gain enter regional EIRP limits. No generic whip is assumed dual-band. [Pigtail](https://www.taoglas.com/product/cab011-ipex-mhfiu-fl-to-95mm-1-13-cable-to-smafbkst/), [433 antenna](https://www.te.com/fr/product-ANT-433-CW-HWR-SMA.html), [868 antenna](https://www.te.com/en/product-ANT-868-CW-HWR-SMA.html).

Reserve the previous 15 mm top service envelope around J7; its roughly 2.4 mm mated height does not establish a final enclosure. Strain-relieve the coax to an independent support; do not pull the connector sideways or use it as a panel anchor. Keep the cable out of the ESP32 antenna keep-out and RF2M cooling envelope. U70 and J7 have no validated complete manufacturer 3D models in this project; the actual KiCad views show the default DNP lands, not proof of fitted module/cable height. There is no final enclosure acceptance.

Quantity-ten component estimates, net EUR, exclude freight/VAT/antenna/pigtail:

{total}

LCSC observations are USD 5.5656/4.7161 (433, q1/q10) and USD 5.6375/4.7854 (868). The EUR model uses an explicit **0.90 EUR/USD planning factor**, not an exchange-rate observation or supplier EUR quote; no unobserved q20 discount. J7 uses an indexed EUR 1.11/0.946 observation; another regional listing differs. Significant base material remains unquoted. A PCB/stencil process change is unnecessary. See [sourcing](../hardware/controller/review/M6-L1/SOURCING.md), [cost JSON](../hardware/controller/review/M6-L1/LoRa-costs.json).
''')
 doc('M6_L1_REVIEW_DECISION.md',f'''# M6-L1 engineering review decision

**GO for independent evaluation-board manufacturing review and optional LoRa prototype assembly preparation**, for NO_LORA, LORA_433 and LORA_868 on the same PCB. This is not procurement, fabrication, assembly, RF operation or physical qualification authorization. No acceptance tag.

A: **PASS nominal module compatibility.** The current distributor-linked TR4/TR8 PDFs are byte-identical to their official Silicontra ZTR4/ZTR8 versions. The older TR8 V1.0 package is also compatible. All 22 terminals are checked in the common top-side orientation. The existing 0.80 × 2.20 mm lands, 1.27 mm pitch and 14.50 mm host-row spacing remain. The body F.Fab outline is corrected to 15 × 15 mm; DIO3 is clarified as unused IO. Missing manufacturer tolerances/height are disclosed and incoming-part checks retained. [Compatibility](M6_L1_MODULE_COMPATIBILITY.md).

B: **PASS credible RF-feed evaluation design.** The 5.25 × 0.45 mm signal feed and bottom reference remain; the Hirose underbody top-ground intrusion is removed. Calculated nominal line loss is about {rows[0]['insertion_loss_dB']:.3f}/{rows[1]['insertion_loss_dB']:.3f} dB and return loss {rows[0]['return_loss_dB']:.1f}/{rows[1]['return_loss_dB']:.1f} dB at 433/868 MHz. Wider material/geometry/topology sensitivities give line loss up to {summary['868000000']['line_only_insertion_loss_max_dB']:.2f} dB at 868 MHz. Transition parasitics and actual antenna matching remain unmeasured. No unnecessary matching network or reroute. [RF analysis](M6_L1_ANTENNA_FEED.md).

C: **PASS local standard JLCPCB manufacturability.** 100 × 100 mm, two-layer standard FR4, 1.6 mm, 1 oz, green mask, white legend, lead-free HASL and ordinary through vias. No controlled impedance or premium process. ERC/DRC errors/warnings = 0/0, unrouted/parity = 0/0. No exclusions; the inherited unused tuning-profile category alone is ignored. Native geometry DFM passes. Fresh fabrication data includes the localized F.Cu ground-clearance correction and L1 revision legend. All signal/other copper, mask, paste and drill geometry remains; exact hashes and the local native boolean difference are recorded.

D: **PASS population/configuration readiness.** Twelve explicit base/radio assembly records, correct alternate U70 MPNs and antennas, fail-disabled unknown/absent-radio behavior. The 704 numbered pad assertions (715 lands including unnumbered mechanical contacts), 38 base critical maps plus two R1 diode maps, all 36 RF pins, 4096 enable combinations, 20 baseline electrical mutations, 16 R1 protection checks, seven DFM mutations, 21 new native/model LoRa mutations, 46 host tests and strict C11 fixture pass. RF80/RF2M read-only protocol coverage and all 1220 frozen RF-file hashes are preserved. [Validation](../hardware/controller/review/M6-L1/final-checks.json).

E: **NOT_RUN physical RF qualification.** Incoming module fit/identity, solder quality, supply step/ground noise, oscillator/RF-switch driver initialization, VNA return loss, actual conducted/radiated power, harmonics, receiver sensitivity, antenna match, coexistence and immunity remain. Earlier R1 pack-ID/negative-clamp/ADC calibration, USB/ESD, RTC and fail-off commissioning gates remain mandatory. Their absence does not imply another PCB architecture study.

UNIVERSAL q10 component estimates are €{cost['UNIVERSAL_NO_LORA']['netEUR_per_unit']['10']:.2f} without LoRa, €{cost['UNIVERSAL_LORA_433']['netEUR_per_unit']['10']:.2f} at 433 MHz and €{cost['UNIVERSAL_LORA_868']['netEUR_per_unit']['10']:.2f} at 868 MHz, net, with unquoted/Fx uncertainty visible. Bare-PCB process and unquoted planning allowance are unchanged. No supplier quotation or CAM acceptance has occurred.

The RF80/RF2M connectors, GPIOs, RTC, USB and R1 battery protection are preserved. No placement, RF signal-track, via, pad, solder-mask, paste or drill geometry changes. The only functional copper correction removes the small top-ground strip inside Hirose's underbody no-traces region; native boolean comparison bounds it locally and confirms unchanged bottom GND. The board revision legend now reads L1. The PCB master remains DNP for LoRa by default; choose the explicit assembly BOM. M6-C1 and M6-C1R1 review artifacts remain immutable. [Review package](../hardware/controller/review/M6-L1/README.md). Stop for independent review before any external manufacturing action.
''')
 write('README.md','''# M6-L1 dual-band LoRa CAD closure

Active native sources remain ../../CTRL.kicad_pro, ../../CTRL.kicad_sch and ../../CTRL.kicad_pcb. Electrical/physical copper baseline is M6-C1R1, commit742159d363dd8dd8b8ff653d01238af9a49ef2aa. M6-L1 clarifies optional part/population metadata, unused DIO3 labeling and the 15 mm module body drawing. It retains the RF signal geometry and corrects only a small Hirose underbody ground-fill intrusion; the board revision mark is L1.

Read the [decision](../../../../docs/M6_L1_REVIEW_DECISION.md), [module compatibility](../../../../docs/M6_L1_MODULE_COMPATIBILITY.md), [feed calculation](../../../../docs/M6_L1_ANTENNA_FEED.md), [population contract](../../../../docs/M6_L1_LORA_VARIANTS.md), [sourcing](SOURCING.md), [assembly/qualification](BRINGUP.md) and [reproduction](REPRODUCE.md).

module-22-pin-audit.json and module-pin-matrix.csv cover all terminals. The normalized-module-views.svg is an original dimension reconstruction; LoRa-native-overview.svg and antenna-feed-detail.svg use actual copper/lands/vias. Manufacturer-evidence hashes identify reference downloads; copyrighted full datasheets are linked, not redistributed. The native-preservation and fabrication-equivalence reports distinguish unchanged geometry from changed metadata and byte hashes. The SHA inventory binds final sources and outputs.

Fresh fabrication/ contains the proposed bare-board Gerbers and separate PTH/NPTH drills. Analysis files, annotated views and BOMs are review data. Default native population is NO_LORA; choose the exact base/radio BOM. Both radio options use one PCB. The original M6-C1/R1 directories are preserved.

Gates A–D pass for independent evaluation review. Gate E and earlier controlled electrical commissioning remain NOT_RUN. No acceptance tag, factory CAM/quote, supplier upload, purchase or hardware operation has occurred.
''')
 write('BRINGUP.md','''# M6-L1 staged option assembly and qualification — NOT_RUN

Retain the R1 [controller procedure](../M6-C1R1/BRINGUP.md) without bypassing pack-ID/USB/power/RTC/default-off tests. No activity below is authorized by this CAD review. RF80/RF2M packs and antennas stay disconnected during controller-only tests.

1. Select the exact base/radio BOM. NO_LORA leaves all six optional positions absent and must pass normal standalone RTC operation. For 433/868, record the purchased label, LCSC code/lot, supplier-linked datasheet hash and actual package measurements. Check pin 1, pitch, 15 mm body, row contact edges, pad depth, height and courtyard fit. Do not mirror the module. Reject an unexplained variant rather than probing RF frequencies.
2. Inspect ordinary HASL flatness and clean/dry flux residue. The castellated lands have no hidden centre solder pad. Use fresh compatible lead-free paste, a standard 0.10 mm stainless stencil and controlled reflow, or controlled edge soldering where the module supplier permits it. Native module aperture area ratio is about2.93 at0.10 mm thickness; nominal deposited volume is0.176 mm³ per land, before metal-content/shrinkage. No source-joint-style filled vias are needed. Inspect each visible castellation for wetting/bridges and continuity; there is no invented guaranteed void fraction. The module's complete assembly profile is not specified: use a profiled initial build within component/paste limits and retain thermal/process records before fleet reproduction.
3. For J7, a practical manual-assembly route is to mask its stencil apertures during paste application and solder its three lands separately with controlled minimal solder. Hirose publishes manual350°C/5s and0.10–0.12 mm metal-mask guidance. Its newer recommended metal apertures are smaller than full native copper lands; do not assume a full-pad paste file exactly reproduces that recommendation. If J7 is reflowed, use the maker's aperture pattern/profile instead of blindly increasing paste. Inspect seating and signal/ground separation with magnification. This stencil/hand-assembly choice uses ordinary processes and changes no PCB fabrication geometry.
4. After the R1 power gates pass, verify3.3 V at U70.13 and local C70/C71 with a scope and bounded source. Exercise a150 mA load-step scenario before relying on the module. Record minimum voltage, ringing, RF-board rail offsets and buck temperature. The local10 µF nominal capacitance is not a transient guarantee. USB-only LoRa TX remains inhibited in the initial contract.
5. With the correct radio identified, hold NSS inactive, reset deliberately and check BUSY/DIO1 and SPI response without transmitting. A chip response cannot determine433 versus868. Configure the selected oscillator/RF-switch/image-calibration settings using its actual supplier driver. Confirm shared-SPI locking: radio clocks never latch595 control bits; control words always reload16 bits atomically before SHIFT_LATCH. Failure of the option must leave autonomous ARDF operation available.
6. Fit a matching50 Ω dummy load/attenuator before any separately authorized RF test. Validate the trusted assembly/antenna/region/airtime record and start at bounded power. Measure actual frequency, power, harmonics, receiver sensitivity and TX current at the selected band; do not discover the band by transmission. VNA checks need calibrated module/connector reference planes, fixtures and de-embedding; do not call a sweep through an energized PA a passive S11 test.
7. Commission the chosen pigtail/antenna in its installation. Keep coax outside the ESP32 antenna keep-out, provide independent strain relief and vertical U.FL insertion/extraction access. Do not load the soldered receptacle with cable tension. Verify LoRa immunity/blocking/coexistence with RF80/RF2M using their existing acceptance procedures. Initial LoRa TX stays in RF-off slots. Record all results; CAD simulation does not close physical Gate E.
''')
 save('gate-status.json',dict(A='PASS_NOMINAL_MODULE_COMPATIBILITY',B='PASS_CREDIBLE_CALCULATED_EVALUATION_FEED',C='PASS_LOCAL_STANDARD_JLCPCB',D='PASS_EXPLICIT_POPULATIONS_AND_FAIL_DISABLED_CONFIGURATION',E='NOT_RUN',manufacturing='GO_INDEPENDENT_REVIEW_ONLY',physical_commissioning='NOT_RUN',acceptance_tag='NOT_AUTHORIZED'))
 final=load('final-checks.json');final['LoRa']={
  'native_module_pins':len(pins),'geometry_model_negative_tests':len(load('LoRa-negative-geometry.json')['tests']),
  'native_preservation':load('native-preservation.json'),'UFL_audit':load('UFL-landpattern-audit.json')['status'],
  'RF_model_summary':summary,'assembly_variants':list(cost),'gates':load('gate-status.json')}
 save('final-checks.json',final)
 print('M6-L1 final decision/equivalence/docs generated from verified results')
if __name__=='__main__':main()
