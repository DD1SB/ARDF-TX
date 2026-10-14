# M3B — evaluation materials and production context

Date: **2026-10-14**. All EUR **net**, VAT excluded; if19% VAT applies, multiply taxable totals by1.19. **No component/PCB quote or order has been placed.** The itemized [workbook](M3B_COMPONENT_WORKBOOK.md), [CSV](M3B_BOM.csv), [machine baskets](M3B_COSTS.json) and current [electrical manifest](../hardware/80m/RF80.electrical.json) are the purchase-candidate ledger. Historical M3A inputs remain unchanged; they are not current M3B exports.

## Component-only baskets

Same-MPN purchases are pooled within each population, MOQ/multiple rounding applied. Cash for unused minimum quantities is included; no reel-sized MOQ is assumed. “Observed” means the retained **dated distributor observation**, not verified current stock or a reserved basket. Every unquoted price/supplier code remains ESTIMATE/OPEN in the ledger. Labor, commissioning, tax, shipping, bare PCB and shared tools are separate.

| Population | Purchased physical parts / ICs | 1 board | 3 boards, each | 5 boards, each | 6 boards, each | 10 | 20 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
|Full80 m, normal +Fox |196 /18 |32.317 |32.065 |31.981 |31.896 |27.311 |27.311 |
|Fox-only |115 /13 |13.759 |12.273 |12.081 |12.081 |10.815 |10.468 |

Full default population excludes the three Fox-only bias links. Fox-only excludes every NORMAL part, including converter/driver/IRF610/shaper/transformer/watt LPF/output connector and watt thermal/current guard hardware. The **same PCB** retains both paths. All74 pads, schematic flags and four holes are fabrication features, not purchased ICs/components. TH301 is one remote purchased NTC in the normal basket; it is not a second sensor on the PCB. [Population CSV](../hardware/80m/review/M3B-E1/population-map.csv) is the assembly authority; default KiCad DNP flags describe full assembly, not automatic Fox variant manufacture.

| Necessary change from R1 | Material addition per full board | Fox impact |
| --- | ---: | --- |
|R350CRCW25121R50FKEG |0.150 **estimate** |Absent |
|C350EEUFR1V101 |0.450 **estimate** |Absent |
|C405GRM21BR71H104KA01L |0.100 **estimate** |Absent |
|C31450 V replacement |0.011 unit-price change at ten; pooled breaks determine other batches |Retained;0.011 at ten |
|Fuse/IDC/IRF610 footprint corrections |No new purchased part; existing MPN retained |Fuse/IDC retained; IRF610 absent |
|52 extra probe pads, labels, holes |No separate purchased component |No separate purchased component |

| Component scope | R1 at6 /10 /20 | M3B-E1 at6 /10 /20 | Delta at10 |
| --- | --- | --- | ---: |
|Full |31.185 /26.600 /26.600 |31.896 /27.311 /27.311 |+0.711 |
|Fox |12.006 /10.804 /10.457 |12.081 /10.815 /10.468 |+0.011 |

The larger Fox change at six includes a changed pooled price break for the remaining old100 nF MPN; it is computed, not a manual adjustment. The reference€25.35 full/€10.55 Fox/€59.18 complete figures in the R1 task were **R0**; actual R1 was€26.60/€10.804 at ten. The previous [R1 reconciliation](M3A_R1_COST_DELTA.md) remains intact. M1's€29.06 material subset and€55.24/€63.34 complete/fleet scopes must not be recast as this evaluation board's cost.

## Prototype bare PCB and external materials

These are **engineering allowances**, not distributor observations or fabrication quotes. The board is210×160 mm,2layer1.6 mmFR4/1oz,ordinary0.15/0.15 mm and0.30 mm plated drill. No100×100 mm promotional price is applied. A fabricator's exact stack/finished-hole/annular-ring capabilities and actual quote must be reviewed before ordering.

| Scope | Net EUR allowance | Accounting treatment |
| --- | ---: | --- |
|Small batch of5 identical **bare evaluation PCBs** |45–90 total |Unquoted estimate;9–18 per bare board only if all five are used. It does not make a one-populated-board experiment cost only9–18 in PCB cash |
|PCB freight |10–25 per shipment |Separate unquoted shared batch expense; no import/VAT assumption hidden in board price |
|One full populated board's components |32.317 |Calculated candidate basket above; uncertain/dated sourcing retained |
|One-board experiment: five bare boards +one component basket +PCB freight |**87.32–147.32** |Material/shipment cash allowance; four bare spares remain; excludes labor, instruments, component freight and items below |
|Nylon standoffs/screws/open bench base |1–4 per assembly |Evaluation-only allowance; no final field enclosure |
|Temporary PA clip sink/electrical insulator/NTC bond and strain relief |2–6 per normal assembly |Unquoted fixture materials; exact thermal hardware selected after SOA review |
|Mating power/control/RF harness and short coax adapters |8–20 per bench fixture |Shared reusable fixture allowance; board-side connectors are already included in component total |
|Gate-load/rail dummy-load/fault-injection fixture consumables |5–15 shared |Unquoted allowance, not another primary product PCB; active test instrument cost separate |
|Calibration resistor and winding spares |2–5 per experiment |Explicit allowance; not hidden in nominal per-board BOM |
|50 Ω loads, attenuators, active probes, scope/analyzer/VNA, PSUs |Existing equipment or obtain quote |Shared laboratory tooling; **unpriced**, not silently counted as free product materials |
|Hand assembly, inspection, winding, commissioning |Unpriced labor |No claimed labor saving; manual prototype assembly assumed |
|Shipping for components / customs / tax |Unquoted |Separate from the bare-PCB freight allowance |

No separate prototype connector is permanently bought for any of the new probe pads. The stage-isolation link R403 and buck inductor L301 may be temporarily removed in testing. Ordinary pads/clip adapters are preferable here to permanently populated SMA tees on switching/clock nodes. The normal/Fox output connectors remain functional product parts. Test pads, generous spacing, some silkscreen and bench supports may disappear after qualification; there is **no validated saving** from a future compact layout yet.

## Prospective production comparison

M3A-R1 component baselines remain€26.60 full/€10.804 Fox at ten. If the M3B corrections qualify and are retained, prospective components become€27.311/€10.815; **the210×160 mm evaluation PCB cost is not the projected compact production PCB cost**. No new controller, RTC, LoRa module, battery, antenna or enclosure has been added by M3B.

For retained complete Fox accounting only: R1 quantity-ten materials€59.434 become approximately**€59.445** after the€0.011 RF component change, with the same€8.10 fleet allocation outside materials (≈€67.545 including fleet). This bridge retains the earlier production-PCB/pack/accessory allowances; it is **not** a quote for assembling Fox transmitters on this large evaluation PCB. The complete2S1P protected pack, compact30 cm antenna/counterpoise/matcher and controller/RTC remain mandatory in that scope. No fourth PCB or alternate MCU is introduced.

Ordering **bare** evaluation boards can be considered after independent CAD review and explicit user approval. Component procurement additionally needs the open supply/package checks in [qualification](M3B_COMPONENT_QUALIFICATION.md). Nothing in this ledger is a manufacturing release.
