# M3B-E2 — physical pinout and mechanical audit

Date: **2026-10-15**. [Machine report: 55 critical devices](../hardware/80m/review/M3B-E2/critical-pinouts.json), [native mechanical/drill/model report](../hardware/80m/review/M3B-E2/mechanical-stackup.json), [updated BOM](M3B_E2_COMPONENT_WORKBOOK.md). “Verified” below means document/CAD comparison, never incoming inspection, stock reservation or hardware validation.

The report lists each exact MPN, manufacturer package source, physical pin roles, local symbol pin names/types, approved footprint, actual PCB x/y/rotation and exported net assignments. Role expectations are independent of the electrical manifest. Logic gate pins also use the retained physical-pin logic model. Q403/U311 application nets are independently fixed expectations. Ten incorrect-pin/vendor/footprint/symbol/E1 mutations must fail.

## Critical devices

| References / exact MPN | Manufacturer-specific physical mapping and landing | Status / constraint |
| --- | --- | --- |
| Q403 **ST BD140** | ST May2008 Rev5 Fig1/p7 drawing0016114E: **1B 2C 3E**, SOT32. Custom native-numbered 1.30 mm drill, 1.90 mm lands, 2.28 mm pitch; installed180°, illustrated face toward board+Y. Maximum body7.8×2.9×11.05 mm | **Verified with assembly constraint**: ST-only identity, 1:1 lead/face check, form leads without body stress, stand body2 mm above board. Own labeled model; no alternate-vendor fit approval |
| Q402 **Vishay IRF610PBF-BE3** | Vishay [91023 RevC, 2Aug2021](https://www.vishay.com/docs/91023/irf610.pdf): **1G 2D 3S**, tabD. Custom TO220 vertical2.54 mm pitch/1.30 mm holes/1.905 mm lands | **Requires incoming dimensional inspection**: the exact IRF610 lot's detailed lead/body drawing is not established by the generic TO220 outline. Existing conservative hole and standard body model retained. Insulate drain tab/heatsink/temperature probe from ground; no heatsink may obstruct adjacent circuitry |
| U401 **LM5134BMF/NOPB** | TI DBV0006A, SNVS808C:1VDD2PILOT3OUT4VSS5INB6IN; SOT23-6,0.95 pitch. Pad5 high inhibits | **Verified** mapping/landing; pilot NC. Driver supply/fault timing is an OPEN electrical gate |
| U302 **TPS22810DBVR** | TI DBV:1VIN2GND3EN/UVLO4CT5QOD6VOUT; native SOT23-6 | **Verified**. Actual physical switch response and18/20 V limits remain OPEN |
| U301 **TPS54302DDCT** | TI DDC0006A thin SOT23:1GND2SW3VIN4FB5EN6BOOT; native TSOT23-6, not a six-pin generic substitution | **Verified**. 28 V operating class is not permission to expose the downstream18 V switch to that voltage |
| U311 **TL431AIDBZR** | TI DBZ, SLVS543S Table5-1: **1K2REF3A**, 1+2VREF,3GND. SOT23 | **Verified**, E1 application corrected; threshold/cold-start/load checks required |
| U313 **INA180A1IDBVT**, R330 **WSL2512R0500FEA** | TI DBV5:1OUT2GND3IN+4IN−5VS; Vishay2512 50mΩ. Actual sense-positive/negative nets checked | **Verified**. Two-terminal shunt sense takeoffs need measured offset/RF rejection; not a four-terminal Kelvin resistor |
| U312/U314 **LM339BIDR/LM393BIDR** | TI SOIC14/8; physical +/−, open-collector outputs and supplies verified individually in machine report | **Verified**. Correct reference now provided by U311; no measured threshold/propagation result |
| U202 **74HC123D,653**, U224 **74HC174D,653** | Nexperia SOT109-1 SO16. Q1=13,/Q1=4,Q2=5,/Q2=12; HC174MR1/CP9/GND8/VCC16, six actual D/Q pairs checked | **Verified**; corrected R1 physical logic remains. Analog reset/RC/ARM races OPEN |
| Other **Nexperia74HC…D,653**, U501 **SN74AC00DR** | Exact SO14/SO16 MPNs. AC00 physical NAND pairs1/2→3,4/5→6,9/10→8,12/13→11,7GND14VCC | **Verified**. No direct output paralleling; Fox summing resistors remain. Below2 V shaped-rail logic/backpower unqualified |
| U101 **SI5351A-B-GT** | Skyworks MSOP10:1VDD2XA3XB4SCL5SDA6CLK27VDDO8GND9CLK110CLK0;3×3 mm/0.5 pitch | **Verified**; original programmable-source and reference circuit retained |
| U201 **MCP100T-300I/TT** | Microchip DS11187F p1 SOT23 top view:1RESET_N2VDD3VSS, package p9 | **Verified** actual picture, not garbled PDF text extraction; rail startup remains measured gate |
| **MMBT3904,215 / MMBT3906,215** | Nexperia SOT23:1B2E3C | **Verified** each occurrence; these are not ST BD140 pin order |
| **BSS138BK,215 / DMN2056U-7** | Nexperia/Diodes SOT23:1G2S3D. Gate ratings±20 V /±8 V respectively | **Verified**; DMN gate is3.3 V logic, not raw pack |
| D301 **SS34-E3/57T**, D302 **LittelfuseSMBJ17A**, BAT54WS devices | Vishay SMC/DO214AB, Littelfuse SMB/DO214AA, Diodes SOD323. **1K2A**, cathode band→pad1 | **Verified** package/polarity. Generic SS34 in a smaller SMA package is not selected. TVS pulse rating is not a DC surge guarantee |
| F301 **Littelfuse046701.5NR** | Maker467 **0603**, nonpolar. Local manufacturer reflow land outer2.54/gap0.36/width1.02 mm | **Verified**; 1.5 A32 V/35 A interrupt coordination is an OPEN power gate |
| Y101 **ABM3B-25.000MHZ-10-1-U-T** | Abracon5032,5×3.2/h1.1 mm max;1/3active2/4GND. 10pF CL variant | **Verified with assembly constraint**: actual marking, not chamfer alone. Own5.1×3.3×1.3 conservative envelope |

Package drawings/source links for every row and each occurrence are in the machine report; retained [E1 dated sources](M3B_SOURCES.md) remain attributed. Newly fetched documents and access failures are in [E2 source identities](../hardware/80m/review/M3B-E2/source-identities.json). ST's official binary was inaccessible; a real ST-authored mirror was used. No fabricated official retrieval or fresh distributor stock observation is asserted.

## Connectors, holes and assembly

| Part | Actual board / manufacturer basis | Disposition before order/assembly |
| --- | --- | --- |
| J101 Wurth **61201621621** | IDC2×8/2.54 mm, body27.98±0.2 mm. Maker finished hole1.10±0.15 mm; PCB1.20 | **Verified with assembly constraint**: require finished **1.20±0.05 mm**; ordinary±0.10 would permit1.30, outside maker recommendation. Verify quote and actual shrouded housing/IDC key, pin1 and cable continuity |
| J301 JST **B2P-VH(LF)(SN)** | 3.96 mm pitch/1.70 mm holes; header7.86×8.5×10.9 envelope.1VBAT2GND | **Verified with assembly constraint**: exact VHR-2N housing and compatible SVH crimp contact/wire variant must be selected for harness; series name does not qualify a crimp. Own envelope, not supplier3D |
| J502 JST **B3B-XH-A(LF)(SN)** | 2.50 mm pitch/0.95 mm holes; maker [XH PCB3+circuits](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf) specifies0.90+0.10/−0 mm.1RF_FOX2GND3FOX_ID | **Verified with assembly constraint**: finished **0.95±0.05 mm**, supplier confirmation mandatory. XHP-3 housing/compatible SXH contact exact wire variant pending. Maker note4 permits substrate-dependent changes only after consultation; no unsupported tolerance waiver |
| J401 Phoenix **1727010** | MKDS1/2-3.81,3.81 pitch/1.10 mm holes, horizontal cable exit | **Verified with assembly constraint**: do not buy3.50 mm1751248. Short coax/load adapter, wire ferrules/gauge and screw access checked at assembly |
| Mounts | Four3.20 mm NPTH, no plating; locations in mechanical report | **Verified** CAD clearances; ≥10 mm insulating standoffs/open bench support. Cut/trim bottom leads. Conductive heatsinks must not bridge drain/collector to ground |

**Bare-board order blocker:** no manufacturer has yet confirmed finished-hole tolerances (including Q402/Q4031.30±0.05mm), stack-up or price. If it cannot meet the J101/J502 limits, change those local holes/landings after review; do not send these files with an incompatible tolerance assumption.

## Magnetics, thermal attachment and models

Original **FT-50A-43**, nominal12.7/7.92/6.35 mm core, **9+9 turns AWG24 enamel**, same sense/bifilar: Astart1(dot),Afinish2,Bstart3(dot),Bfinish4;2+3drain,1VPA_SHAPED,4RF_RAW. Leads formed to inline5.08 mm pitch/1.0 mm holes. AL480nH starting calculation gives38.9µH per winding; no inductance measurement exists. Confirm phasing at low energy. Own envelope includes winding allowance; lead forming, glue/strain relief and winding-to-probe clearance need dry-fit.

L410/L411 retain **T60-2,20 turns AWG24**, original2.7µH label; AL6.5nH calculation gives2.60µH pending measurement/trimming to reference response. Nominal core15.24/8.53/5.94 mm; conservative wound envelope used. One flat/one upright orthogonal. Fox axial **78F2R7J-RC** remains independent. No RF filter values changed. All magnetics: **requires incoming dimensional inspection and measured inductance/phasing**, not a reason to redesign the RF stage now.

BD140 case/heatsink and IRF610 drain tab must have insulated thermal attachments wherever a conductive support/probe could ground them. Exact sink/mount hardware remains a prototype allowance; verify full body/bolt/washer clearance before mounting. The remote NTC must be bonded to the intended PA case with electrical insulation and strain relief. An electrically sound but detached NTC is not detected as an open circuit: mechanical bond inspection and temperature correlation remain mandatory.

All referenced model files resolve (199 placements). Nine local **own dimensional envelopes**, including E2 BD140, are identified as such; they are not qualified production models. Actual KiCad top/isometric/bottom views are supplied. The BD140 envelope has a gold **illustrated-face marker**, not a device logo or guaranteed real marking. Standard KiCad bodies are also visual aids. There is no unresolved known pin-mapping defect after this audit; exact stock/lot fit, mating cables, thermal hardware and fabrication capability remain **OPEN**. They must not be silently converted into “verified stock” or hardware qualification.
