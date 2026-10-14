# M3B — RF80 evaluation PCB layout review

> **2026-10-15 correction notice:** This is a historical pre-E2 record. E1/R1 ST BD140 pin/orientation claims and the E1 manufacturing recommendation are superseded by [M3B-E2 corrections](M3B_E2_CORRECTIONS.md) and the [E2 decision](M3B_E2_REVIEW_DECISION.md). Use E2 assembly/netlist files: Q403 **1B/2C/3E**, illustrated ST face toward **PCB+Y**, and U311 TI DBZ **1K/2REF/3A**. E1 drawings are not build instructions. Frozen historical checks are not current E2 verification.


Date: **2026-10-14**. Revision **M3B-E1**. Engineering review, **unbuilt and unenergized**. Baseline: M3A-R1 commit `0dfd224`; R0 remains at `m3a-r0`. The [R1 CAD/PDF/netlist snapshot](../hardware/80m/review/M3A-R1/) is preserved. This milestone authorizes an evaluation layout and review exports; it does not accept pending ADRs or authorize an order.

## Native design and stack-up

Open [RF80.kicad_pro](../hardware/80m/RF80.kicad_pro), [schematic](../hardware/80m/RF80.kicad_sch) and [PCB](../hardware/80m/RF80.kicad_pcb) in KiCad **10.0.6**. The current [15-page schematic PDF](../hardware/80m/review/M3B-E1/RF80.pdf) supersedes the archived R1 drawing for this evaluation. All 273 electrical footprints have schematic paths and physical pad nets; four additional mounting holes are board-only. Full assembly has 196 purchased parts/18 ICs; Fox-only has 115/13. Test pads and power flags are not purchases.

| Fabrication parameter | Evaluation specification |
| --- | --- |
| Outline | Rectangular **210 × 160 mm**, no slots; absolute coordinates (20,20) to (230,180) mm |
| Construction | Two copper layers, **1.6 mm FR-4**, ordinary Tg ≥135°C, nominal 35 µm/1 oz copper both sides |
| Finish/mask | Lead-free HASL or ENIG; solder mask both sides, white top legend; no impedance-control premium |
| Minimum routed width / ordinary clearance | **0.15 / 0.15 mm**; explicit project rule, no smaller auto-neckdowns remain |
| Drain clearance | **0.60 mm** from `DRAIN_PA` to other nets; electrical spacing is not a measured RF-voltage qualification |
| Vias | Ordinary through vias, **0.60 mm land / 0.30 mm finished drill**, tented both sides; no SMD via-in-pad, blind/buried vias or filled vias |
| Mounting | Four **3.2 mm NPTH** at (25,25), (225,25), (225,175), (25,175) mm: 200 × 150 mm centers |
| Holes | Separate metric PTH/NPTH Excellon; 371 PTH including 328 vias, four NPTH; see drill report |
| Sourcing | Ordinary prototype capability requested; finished-hole tolerance ±0.10 mm or better and minimum annular ring ≥0.15 mm must be confirmed by the selected fabricator |

Four layers would provide an uninterrupted inner ground plane and easier digital routing but add two copper layers without eliminating any RF qualification gate. This deliberately roomy board uses two layers: top RF/power loops, bottom ground return with local low-current crossings and ground stitching. Its filled planes and local connections pass DRC. A plane split by routing is still a possible RF impedance problem; RF rail ripple, clock-to-port leakage and return-current behavior must be measured. A final compact production board has not been laid out or costed as this large evaluation panel.

## Placement, routing and return paths

The connector/lease/arming logic occupies the left side. The pack barrier/damper/buck occupy the upper middle. The normal driver/IRF610/transformer occupy the upper right; the original normal elliptic filter continues down the right edge. The Si5351/reference lies between the logic and RF branches. The Fox buffer, shaper, padding, LPF and separate connector occupy the lower right, with a wide copper/air-space interval from the watt filter. No watt net is routed to the Fox connector.

RF and high-current trees were constrained on top copper before local digital routing. **FreeRouting 2.5.0 ran locally with telemetry/API/MCP disabled**; no design was uploaded. Its result was corrected in native KiCad for minimum track width, ground connectivity and probe labels. Ground planes are filled on both sides with solid pad connections. Multiple local return vias avoid a series digital-ground trace in the driver/source return. Through-hole leads and connectors may require preheat for hand soldering; solid ground attachment is intentional for the evaluation.

The LM5134B is adjacent to R403 and the IRF610 gate; C404 and ceramic bypasses return locally. The drain node is short and wide to the center-connected transformer terminals and has no permanent coax connector or large probe island. T401's electrical 9+9-turn connection and original core/ratio are preserved; only the formed-lead landing geometry changes. C405 adds **100 nF at the transformer supply end**, not across the drain. C405 and all return planes introduce real parasitics that remain a hardware gate. The filter capacitor/inductor values and elliptic topology are unchanged.

The PA rail uses wider copper wherever space permits, with neckdowns at actual pads. [Machine geometry report](M3B_CHECK_RESULTS.json) states actual lengths/widths/layers rather than assuming every power connection is 1 mm wide. R330 remains a four-terminal **connection discipline on a two-terminal part**: separate sense traces leave the shunt land pair; load current enters/leaves the power lands. No ground-referenced instrument lead may bypass the shunt. Confirm the physical sense voltage using a differential probe before trusting current-trip calibration.

L410 is flat, L411 upright: their magnetic axes differ and centers are 28 mm apart. The transformer uses its own formed-lead fixture. The [3D rendering](../hardware/80m/review/M3B-E1/RF80-3D.png) was generated by KiCad and inspected for body/connector/coil clearance. Wound components use explicitly identified **winding-envelope models**, not verified supplier CAD. Their actual lead forming, insulation and windings still need a dry-fit against the printed assembly drawing.

## Thermal and mechanical provisions

IRF610 is upright at the top RF edge with access above the board for a removable heatsink, thermocouple and insulated mounting. **The tab is drain potential**, not ground. No grounded copper heatsink is assumed. The BD140 shaper is accessible separately; no continuous-beacon thermal rating follows from the target's 20% contest schedule. A free-air/clip fixture must keep grounded metal away from the PA tab and nearby transformer.

TH301 is a **remote NTC bonded through electrical insulation to the PA case**, connected to its landing pads/test access. Do not fit a second board NTC in parallel. It is excluded from automatic placement but remains one required material item. A physically detached sensor with intact wires is not detected by the electrical open-sensor comparator. Bond retention and correlation with actual case/junction temperature are mandatory tests.

Use four nylon standoffs ≥10 mm in a simple open bench base; keep underside copper away from metal. Final weatherproof enclosure design is outside this milestone. The evaluation board needs no additional primary PCB. Shared controller/test-fixture wiring is permitted.

## Probe access and separation

There are **74 fabricated test pads**, including 52 new 0.8 mm pads. [Probe map](../hardware/80m/review/M3B-E1/probe-map.csv) gives net/absolute X/Y; [population map](../hardware/80m/review/M3B-E1/population-map.csv) gives all parts/variants. The exported assembly sheet identifies references even where silk spacing prevents a long net label. Raw ARM, raw/captured modes, ARM_ACCEPT, ARM_CLK, reset, lease, quiet, ARMED, permits, key tail, PA_INB, rail nodes and sense nodes are independently accessible.

Use ≤1 pF active probing for the asynchronous reset chain and drain, with nearby spring ground or suitable isolated differential measurement. Probe capacitance must be included in the timing comparison. Do not use an ordinary grounded scope clip on a drain/tab or high-side node. Normal and Fox RF connectors remain their different original types; temporary coax/dummy-load adapters are external fixtures. Large permanent SMA tees were avoided on clocks/gate/drain.

## Electrical changes and checks

R350/C350 damp the normal supply input; pack sensing stays ahead of R350. C314 is now 50 V. F301's erroneous 1206 mapping was corrected to the actual 0603 fuse lands. J101 hole geometry is matched to its manufacturer recommendation. IRF610 holes were enlarged conservatively to 1.3 mm while retaining pin order, pad spacing and body/model. No R1 permission/state logic, normal filter values or Fox filter values were deleted or changed. [Qualification](M3B_COMPONENT_QUALIFICATION.md) and [safety gates](M3B_SAFETY_GATES.md) explain the limits.

Current ERC: **0 reported violations**. Current all-severity DRC: **0 violations, 0 unrouted, 0 schematic-parity differences**, with no DRC exclusion. [Reports and copper/assembly/3D artifacts](../hardware/80m/review/M3B-E1/). The R1 pin-derived suite passes on the **current** netlist: 256 truth combinations, 31 scenarios, 16 timing corners, including polarity mutations. These are CAD/ideal-event results, not physical RF, startup or thermal validation.
