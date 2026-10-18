# M4A — frozen E2 prototype handoff

Date: **2026-10-15**. Reference **1245023 / m3b-e2**. Intended quantity: **five bare evaluation PCBs; initially populate only one**, in stages. This prepares an engineering handoff; **all purchasing, manufacture, assembly, energizing and RF activation remain unauthorized**. Independent review is a CAD review, not a physical test result.

The [self-contained handoff directory](../hardware/80m/handoff/M4A-E2/) contains an exact Git source archive, byte-identical E2 fabrication/review artifacts, [critical procurement candidates](../hardware/80m/handoff/M4A-E2/critical-procurement-candidates.csv), [reference-by-reference assembly stages](../hardware/80m/handoff/M4A-E2/assembly-stages.csv), the one-board candidate material basket and a relative-path checksum inventory. Unpack the source archive to obtain native `hardware/80m/RF80.kicad_pro`, all hierarchical schematics, cached footprint geometry, local symbol/footprint/model libraries, original documents, licenses and provenance. KiCad10 with its standard model library is needed for interactive native3D; exported PDFs/PNGs can be reviewed without it. No cloud upload is needed. Original E2 source files, Gerbers and review exports are unchanged.

## Fabrication specification to confirm

| Parameter | Frozen E2 requirement |
| --- | --- |
| Quantity / profile | 5 bare boards, **210.00 ×160.00 mm edge centerline**; Gerber job210.05×160.05 includes0.05mm outline stroke |
| Stack | Two-layer FR4, nominal1.6mm, nominal35µm outer copper, ordinary plated through vias; no impedance-control premium |
| Copper | 0.15mm minimum width/spacing, drain-specific0.60mm clearance, copper-edge≥0.50mm |
| Drills | Separate **372PTH /4NPTH** files;329ordinary0.60/0.30mm vias; mounting holes3.20mm NPTH. Drill report is authoritative for all diameters |
| Critical finished holes | **J1011.20±0.05mm; J5020.95±0.05mm; Q402/Q4031.30±0.05mm**. These are finished holes, not unplated drill-tool diameters |
| Mask / legend | +0.025mm mask expansion, minimum0.075mm mask web, tented vias; legend≥0.8mm height/0.08mm stroke,0.10mm clearance. Confirm actual registration/web capability |
| Requested finish/color | **Lead-free HASL, green mask both sides, white top/bottom legend** for the initial hand-assembled prototype. Supplier must confirm solderability/land flatness for MSOP0.5mm/0603; if unsuitable, return an ENIG alternative quote for review, with no automatic substitution |
| Inspection | Supplier electrical test/AOI, outline/NPTH identity, finished-hole and copper/annular-ring capability, no unapproved CAM edits or part substitutions |

A generic “standard PCB service” is insufficient evidence for the hole limits. Public [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/) list ordinary PTH +0.13/−0.08mm and a separate±0.05mm controlled-hole process; [PCBWay standard capabilities](https://www.pcbway.com/capabilities.html) list ordinary PTH±0.08mm. Neither ordinary tolerance meets all frozen requirements. [PCBWay's advanced table](https://www.pcbway.com/advanced-pcb-capabilities.html) describes tighter diameter-dependent tolerances, but is not a quote or confirmation for this board. Obtain explicit supplier confirmation **after authorization to communicate/send files**. No supplier has been contacted or selected.

This is the M4A handoff process request; the frozen E2 Gerber job retains its original unspecified-finish metadata. Confirm the requested process in the quote rather than silently rewriting that job. No finishing process is claimed already qualified.

Review the nine current Gerber layers/job, separate plated/nonplated drills/maps, native source, schematic PDF, top/bottom assembly/copper drawings, actual3D views, placement/population maps, ERC/DRC, manufacturer pin report and exact copper/drill/net comparisons. Their inventory/checksums are in the handoff. Do not substitute E1 drawings: ST Q403 **1B→SHAPE_BASE,2C→VPA_SHAPED,3E→VPA_LOAD**, ST illustrated face toward **PCB+Y**; TI U311 DBZ **1K+2REF→VREF_2V5,3A→GND**. ST Rev5 drawing0016114E and TI SLVS543S evidence are retained in [E2 footprint audit](M3B_E2_FOOTPRINT_AUDIT.md).

## Five distinct authorization gates

| Gate | Exact scope | Current status |
| --- | --- | --- |
| A1 bare-PCB fabrication | Five **E2**, not V1, bare boards; accepted supplier confirmations/quote and specified files | **NOT_AUTHORIZED** |
| A2 low-voltage procurement | Only approved Stage1 logic/source/reference/passive quantities; exact MPNs and current basket needed | **NOT_AUTHORIZED** |
| A3 high-energy population | Named later stage, associated procurement/population explicitly approved, prior measurement gates passed | **NOT_AUTHORIZED** |
| A4 controlled power-up | Named board/stage, bounded PSU/current/duty, instruments and procedure | **NOT_AUTHORIZED** |
| A5 RF activation | Named path, rated calibrated dummy load, bounded settings; no unqualified radiation | **NOT_AUTHORIZED** |

Approval of one gate grants none of the others. A PCB order alone never authorizes buying the full component basket, soldering a PA or powering logic. The assembly-stage CSV is a proposed allocation, not an order list. A3 procurement may be scoped separately in its approval; do not infer it from a stage name.

## Procurement and staged assembly

Use exact ST BD140, TI TL431AIDBZR, LM5134BMF/NOPB, TPS54302DDCT/TPS22810DBVR, Vishay IRF610, actual HC123/HC174/AC00 packages, C404 ESR/pulse-resistor evidence, exact IDC/VH/XH contacts and original FT-50A-43/T60-2 materials. Check incoming leads, winding polarity and insulated thermal attachments. TH301 is **one remotely bonded sensor**, not a second board-fitted parallel NTC. The complete196-part full basket is a budget reference; it is not permission to purchase all stages at A2.

[TI's exact LM5134BMF/NOPB page](https://www.ti.com/product/LM5134/part-details/LM5134BMF/NOPB) currently identifies an active part but publicly reports out of stock; this is not assured small-quantity fulfillment. The new DigiKey page retrieval failed. Retained distributor observations remain dated, not newly verified stock. [ST's BD140 page](https://www.st.com/en/power-transistors/bd140.html) identifies active volume production; only ST's qualified pinout is permitted. Exact baskets and unavailable items remain procurement blockers; do not buy an unverified substitute merely to unblock assembly.

After separate approvals: inspect unpowered board and1:1 fits; Stage1 isolated3.30V logic/source (initial100mA); Stage2 input/buck/dummy loads with **U401/Q402 absent**; bounded driver-fault qualification; Stage3 driver/shaper and dummy gate; Stage4 low-energy normalRF; Stage5 independent FoxRF; bounded faults/thermal/field/endurance afterward. The [retained bring-up procedure](M3B_BRINGUP_PLAN.md) must be read with the overriding [E2 corrections and bounded power restrictions](M3B_E2_POWER_PROTECTION.md), never its superseded E1 transistor instruction.

## Required measurements — all NOT_RUN

Input insertion/disconnect/ground bounce and TPS22810 margins; real reference startup/thresholds; **≤20µs isolation and VDRV≤12.6V** under the defined fault; capacitor ESR/temperature and driver discharge; asynchronous ARM/reset widths/propagation; heartbeat/fault/rearm; BD140/IRF610 hot SOA;3W/1.2W/Sprint conducted output; CW edges/clicks; harmonics/spurs; independent9–11mW Fox reference-load calibration; normal→Fox isolation≤66µW at maximum normal power; compact30cm antenna/return/loading and reproducible30m-audible/250m-not-audible evaluation; **12h full /24h competition-appropriate reduced** profiles and continuous beacons separately. Every result starts **NOT_RUN**. Prior Boolean/passive-model results do not change that status.

Keep no unrestricted4S pack connected during initial qualification. Stage2 starts with current-limited laboratory supply and conservative voltage, progresses12/14.4/16.8V only after records pass. Driver-absent failed-buck injection isolates the buck, uses independently bounded≤18V pulses, and must not confuse the fixture's timeout with the board opening. No24/28V board injection or destructive Li-ion fault. Preserve all E2 gates and uncertainty margins.

## Cash scope

Retained unquoted net allowance: five bare E2 boards **€45–90**, PCB freight **€10–25**, one full component basket **€32.317**: subtotal **€87.32–147.32**, excluding component freight, thermal/harness fixtures, labor and tax. Tight-hole process/finish surcharges and exact stock/price are **OPEN**, so this is not a firm ceiling or supplier offer. The four remaining boards are unpopulated spares. V1 manufacturing estimates are a separate scope and do not silently replace this frozen evaluation order.
