# Foxoring-only cost audit and reconciliation

Date: **2026-10-13**. **Candidate material/cash budgets, not orders, validated hardware or assembly quotations.** The ESP32-S3 controller with RTC, unpopulated optional Silicontra SX1262 footprint, existing 80 m PCB and its M1 Fox-only population are preserved. No fourth transmitter PCB, replacement MCU or complete-set manufacture is proposed.

The current recommendation is approximately **€55.24/€55.20 per complete unit in material and functional provisions at 10/20 units**, plus separately purchased shared charging/provisioning equipment and fleet freight. With a €60 freight budget retained, the fleet cash budgets are **€63.34/€60.05 per unit**, before VAT, labor, instruments and spares. These are mixed observed-price/estimated budgets, not proven attainable prices. The lowest candidate BMS price gives €53.53/€53.49 unit material, but it is **not safety-qualified**; the recommended budget keeps a replacement reserve.

The historical €77.11 figure was not a new RF-board BOM price. It allocated a charger to every transmitter, freight and tooling, in addition to missing external materials. Its scope was insufficiently prominent in the earlier review. There is **no €48 electronics increase**. Only €0.75 was added as an unquoted RF guard/input-limiting provision.

## Exact €48.05 bridge at ten units

The [M1 itemized workbook](M1_COSTED_BOM.md) establishes **€29.06** for controller + reduced-population RF + complete compact antenna. It already includes the antenna coil, tuning element, voltage-rated RF capacitors, compact radiator/return, keyed cartridge plug, protection/damping and cartridge support. It excludes bare PCB fabrication, external battery, transmitter sockets/harness and the outer transmitter enclosure. Pooled purchasing means the complete configuration is slightly cheaper than adding independent board totals.

| Scope | Addition beyond €29.06 | Classification in old M2 estimate |
| --- | ---: | --- |
| Low-source guard/input-limit provision | 0.75 | Essential functional reserve, no quoted incremental parts |
| Two reference cells | 8.00 | Unquoted €4/cell allowance |
| Pack BMS | 3.00 | Unquoted protection/balancing allowance |
| Pack fuse/tabs/insulation/restraint material | 4.00 | Unquoted material allowance; no assembly labor |
| Pack-side mating connector | 0.60 | Unquoted material allowance |
| Transmitter battery half, module power pair and low RF socket | 2.20 | Unquoted material allowance |
| Transmitter wiring/crimps/strain relief | 2.50 | Unquoted material allowance |
| Two bare common PCBs | 6.00 | Unquoted €3/board fabrication allowance |
| Outer enclosure/seals/mounting | 4.50 | Unquoted material allowance |
| One external charger for **each** transmitter | 10.00 | Deployment choice; unquoted equipment allowance |
| Shared provisioning fixture allocation | 0.50 | €5 **one-time fleet** equipment, divided by ten |
| Fleet freight allocation | 6.00 | €60 fleet shipping estimate, divided by ten |
| **Total addition** | **48.05** | |
| **Old M2 complete-system allocation** | **77.11** | 29.06 + 48.05 |

There is no second €8.38 antenna charge in this bridge. M2 started with PCB components (€20.68 + €0.75), then added the same €8.38 antenna. The main enclosure is distinct from the small cartridge support. Pack shrink/restraint is distinct from the main enclosure. The four power connector halves account for both sides of the battery connection and both sides of the detachable RF-board feed. Harness mating contacts are distinct from M1's PCB logic headers. None is removed merely by relabeling scope.

At twenty units, the same historical bridge is €44.80 above the €29.02 baseline: freight and fixture divide across twenty. The [generated BOM](FOXORING_COST_BOM.md) and [JSON](FOXORING_COST_TOTALS.json) reproduce both bridges directly from the preserved workbooks.

## Revised itemization and economically justified changes

| Scope | Old M2, ten units | Audited budget, ten units | Evidence / reason |
| --- | ---: | ---: | --- |
| M1 controller/RF/complete compact antenna | 29.06 | 29.06 | Preserved populations and price catalog |
| Additional guard provision | 0.75 | 0.75 | Keep provision pending exact component-count review |
| Two cells | 8.00 | 3.46 | NKON new regular 25R listing, €1.73 net at ≥10 cells; 20/40 cells do not reach its 50-cell break |
| Pre-welded tabs plus pack assembly material | 4.00 | 2.74 | €1.24 supplier tag service + €1.50 explicit fuse/barrier/shrink/restraint/leads allowances |
| Protected/balanced circuit budget | 3.00 | 3.00 | Observed LA123112 €1.29 + €1.71 replacement reserve; no unqualified safety saving credited |
| Pack-side connector | 0.60 | 0.60 | Retained |
| Transmitter connector material | 2.20 | 2.20 | Retained; all halves/sockets counted |
| Transmitter harness | 2.50 | 2.50 | Retained, split into power/logic/RF/restraint sets |
| Two bare PCBs | 6.00 | 6.00 | Retain allowance; no unsupported size or promotional-fab saving |
| Outer enclosure/mechanics | 4.50 | 4.43 | Regular-price shell net €3.28 + €1.15 internal mounting/penetration/sealing allowances |
| Solder/flux/cleaning and labels | not explicit | 0.50 | Added visible assembly material; labor remains separate |
| **Unit hardware/material budget** | **60.61** | **55.24** | Before external charging, tooling and freight |
| Charging equipment allocation | 10.00 | 1.60 | One €15 charger + €1 adapter **per ten packs**, both unquoted qualified-equipment budgets |
| Provisioning equipment allocation | 0.50 | 0.50 | Same €5 fleet allowance, not an instrument budget |
| Freight allocation | 6.00 | 6.00 | Retain old €60 fleet budget; exact supplier baskets open |
| **Fleet cash budget per transmitter** | **77.11** | **63.34** | Savings **€13.77**, no MCU/RTC/RF requirement removed |

The figures are rounded for presentation; calculations use exact batch purchasing allocations. At twenty units the corresponding hardware/material budget is €55.20 and fleet allocation €60.05. The full bill includes **every M1 component row in the selected population**, all external materials and shared equipment, with supplier codes, actual batch demand, observed quantity breaks and explicit estimate flags.

All values are EUR ex VAT planning. For a German private purchase, applying 19% to every budget line as a simple illustration gives roughly **€65.74/€65.69 unit material** and **€75.37/€71.46 fleet cash allocation** at 10/20. Actual invoice VAT/destination treatment must replace that illustration. Do not compare net ARDF-TX values with unqualified gross retail kit figures.

## Pack and charging scope

Use two **new, matched standard 18650 cells** in a protected external 2S1P pack. The candidate changes capacity from the earlier 3.4 Ah reference to 2.5 Ah typical/2.45 Ah conservative supplier basis, **not RF output**. Supplier-attached tabs are priced; subsequent tab connections, insulation, fuse, restraint, short leads and mating connector are separate. There is no assumed free spot welder or soldering directly to bare cells. If a holder or factory pack is selected instead, replace this pack scope rather than adding or deleting unexplained components.

LA123112 is a purchased-module candidate for the **external pack's protection**, not a fourth ARDF-TX product board. The seller lists 25 units, per-cell over/undervoltage protection, overcurrent/short protection and balancing. It also states no manufacturer datasheet is available. Those are **publisher claims**, not proof of a qualified pack. Keep the €3 protection budget until exact-lot tests verify trip/recovery, both cell sense inputs, balancing and leakage. If worst-case voltage thresholds are incompatible with the selected cell limits, reject this candidate; the replacement reserve is not evidence that a qualified substitute exists at that price. Thermal/current coordination and charge temperature restrictions remain required. A 20 A marketing rating does not qualify the pack or its leads. The discontinued NKON €1.20 board is excluded.

Charging uses an independent, qualified **8.4 V CC-CV charger**, proposed 0.5–1 A for this pack; a BMS alone is not a charger. Per-cell charging must comply with the selected cell specification; the listing's high emergency trip threshold is not the normal charge target. Balancing must be provided by the qualified pack circuit or an independently verified charging arrangement. Charge termination, individual cell voltage, temperature and leakage require measurement before release. A plain 8.4 V power adapter and an undocumented charger module are not accepted substitutes.

The observed €12.50 gross charger is only a sourcing comparator: VAT jurisdiction and CC-CV/termination evidence are incomplete. The budget uses **€15 net per qualified charger**, plus a €1 keyed adapter. No conversion of that gross offer into a fictitious net quote occurs. One charger per ten packs is an explicit fleet operating proposal. At 1 A, ten fully discharged 2.5 Ah packs can require roughly 30–40 h including CV tail and handling, rather than overnight replenishment. Sequential charging only; no parallel-pack charging harness. More chargers increase costs transparently: the same audited unit with an individual €15 charger/€1 adapter costs **€77.74/€74.45 per unit including current freight/tool allocations** at 10/20. Sharing is an equipment-utilization saving, not a safety shortcut.

The M2 high-power 5 A planning requirement remains applicable when the pack/connector is offered for full-family interchangeability. Foxoring's smaller load does not prove that rating. If only a lower-current pack is qualified, its current capability must be explicitly reported and controller operation restricted accordingly; it cannot be labeled an unrestricted common-family pack. No lower rating or protection function is silently assumed here.

## What costs are still estimates or excluded

The [part/allowance catalog](FOXORING_COST_PARTS.json) distinguishes observed supplier values from material sets, reserves and shared equipment. **No materials have actually been purchased.** M1's passive/coil/connector counts and price allowances remain candidates. PCB dimensions/layers/finish, enclosing the common boards and pack, environmental seals and calibrated antenna construction are not yet proven, so €6 fabrication and the mechanical fit are still open. Quote the unchanged boards; a Fox-only population does not justify a smaller outline or an unverified PCB discount.

Freight remains a separate **€60/fleet estimated** cash row. A €40 consolidated-freight case gives **€61.34/€59.05 per unit** at 10/20, but is a sensitivity, not an observed route saving. Do not assume free shipping, zero lithium-cell freight, coupons or a promotional first-order PCB service. Checkout transport/tax/handling/minimum-order costs and unused bulk material must be reconciled before any ordering release.

Assembly assumptions: amateur self-assembly, supplier-tabbed pack cells, hand winding/tuning, shared service-pad programming access and individual RF calibration. Solder/flux/cleaning/labels are counted. Board assembly, tab connections, coil winding, case drilling/harness construction, programming, bench calibration and field qualification are **labor OPEN**, not included/free vendor services. No measured build time or yield is available. A paid-build price is `material cash + N × per-unit labor hours × rate + shared setup/field labor + tools/instrument access + reject/spare material`. No numeric labor saving is claimed.

The shared €5 programming fixture covers a passive service-pad cable/probe only; computer, calibrated RF measurement equipment, cell/pack testers and workshop tooling are not included. Tool purchases are reusable capital and cannot be hidden in RF silicon prices. The BOM assumes one accepted unit per planned material set; rejected boards/parts, spares and development coupons are additional. No full fleet is ordered to establish those yields.

## TinyFox and Fixle comparison

| Attribute | ARDF-TX Fox-only audit | TinyFox | Fixle |
| --- | --- | --- | --- |
| Cost evidence | €55.24/€55.20 budgeted complete unit material, plus shared fleet equipment/freight; observed values + explicit allowances | **€15–30/unit**, author report in QSP July–August **2019**; no current price or available kit quote obtained | **€5.65 itemized / about €6** author material calculation for larger quantities; not a distributor basket quote |
| Material boundary | Two common boards, protected rechargeable 2S1P, compact match/radiator/return, case and harness; labor/instruments separate | Historical build cost scope not fully normalized for taxes/labor/battery/transport | Published table includes PCB/case/holder/wires; **CR2032 cell not priced in that table**, and labor/shipping/programming tools not priced |
| Control/source/power | Locked ESP32-S3 + RTC, programmable local Si5351, optional unpopulated LoRa, independent hardware fail-off | Documented 2011 hardware uses ATtiny13, fixed crystal/logic RF and one AA with boost | ATtiny25, fixed crystal/single-transistor RF and CR2032 |
| Antenna / field evidence | ~30 cm radiator and defined compact counterpoise/matching; 10 mW reference + 30/250 m qualification **not measured** | Primary manual describes 30 cm antenna and installation tuning. 2019 author reports audibility around **500 m without grounding**, hence no 250 m compliance proof | Default longer wires; author suggests ~75 cm antenna + ~75 cm return for beginners. Reported ~300 m with Spätzle; author says international operation needs shorter antennas |
| Equivalence to current ARDF-TX requirements | Target retained; all relevant measured gates still open | Conducted nominal 10 mW, current spectra/stability and autonomous hardware fail-off not established by inspected material | Conducted 10 mW, compact 30 cm recipe, RTC timing/fail-off and calibrated emissions not established by inspected material |

Sources: [TinyFox author manual mirrored by ARDF-France](https://ardf.r-e-f.org/ressources/vente/Tinyfox-Documentation-fr-site.pdf), [OE6AVD's first-person QSP report](https://www.oevsv.at/export/shared/.content/.galleries/qsp_downloadgallery/2019_qsp_downloadgallery/QSP_07-08_2019.pdf), and [DF1FO Fixle documentation](https://df1fo.darc.de/DOC/Fixle.doc). The TinyFox website itself could not be accessed; no current kit price is invented. The cost advantage of both specialized designs is credible, but their published figures are not like-for-like released competition-qualified quotations. They provide minimal-circuit and mechanical references without replacing the common ARDF-TX platform. No third-party circuits, code or drawings are copied.

## Preserved RF, timing and go/no-go constraints

The audit makes **no power, antenna, timing or safety reduction**. Keep the nominal **10 mW A1A mark** at the defined post-filter 50 Ω plane, programmable competition frequencies, approximately 30 cm vertical radiator, compact counterpoise and dedicated loading/coupling network. Reference tolerance requires referee agreement. Retain G0/G1/G6/G7/G8/G9: stable frequency, suitable CW edges/emissions, autonomous POR/health lease/persistent latch, source power-off and bus-backfeed prevention, bounded low source plus measured drive/backfeed/transients, retune inhibit, correct identity/interlock and fixed low-power calibration. The absent watt PA/boost/driver/normal port cannot be energized by software. Repopulating the full HF board reinstates its physical low-port interlocks and RF isolation tests.

Keep the **reference-load power test independent of field reach**: audible at the mapped point/30 m, not audible at 250 m in reproducible wet/dry tests with representative receivers and azimuths. The loading coil may have tens of volts RF despite 10 mW; capacitor insulation/Q/SRF and clamp capacitance are not traded away. Preserve all €8.38 antenna functions pending qualification. In particular, the unquoted €3 antenna trimmer is a real cost driver: an adjustable loading tap or low-voltage coupling adjustment might reduce it later, but no saving is credited until voltage, channel tuning, repeatability and field tests pass. The expensive HF/VHF watt components and heat sinks are absent from this population.

Using the retained 0.350 W full-key-down M2 allowance, the new 2.5 Ah pack gives **33.3 h modeled** after the same 64.8% usable-energy factors; the conservative 2.45 Ah basis gives **32.7 h**, or **28.9 h** with +0.045 W continuous LoRa RX. No LoRa is populated in this cost basket. The conservative 24 h ceiling is now **0.476 W**, replacing the larger reference-pack ceiling for this specific cell choice. Actual aging/cold/imbalance and total input power must close this target; the 90% temperature factor is not a guarantee. Optional LoRa population and antenna geometry/stock choices require recosting and energy checks. Smaller cell capacity does not make Classic/VHF 24 h claims.

## Audit requirement trace

| ID | User requirement | Evidence / cost response | Closure |
| --- | --- | --- | --- |
| FOX-001 | Keep ESP32-S3, RTC, unpopulated Silicontra option | Unchanged M1 controller rows S3/RTC/BUCK/POR; LoRa population zero | Controller/timebase and no-LoRa tests |
| FOX-002 | Existing 80 m PCB, Fox-only population | M1 population reused exactly; watt groups excluded; two bare common PCB lines | Common-outline fit and low-source RF gates |
| FOX-003 | Protected 2S1P, two standard 18650 | 25R new cells/tabs; external protection/balance candidate + reserve, fuse/barriers/restraint/leads | Exact-lot pack/BMS/charger tests |
| FOX-004 | Itemize all remaining material | Complete CSV/Markdown/JSON, connector halves, fabrication, case/mechanics and assembly consumables | Fresh quote/count closure |
| FOX-005 | Separate materials, allowances, equipment, one-time costs and labor | Unit/equipment/freight/reserve classifications; labor/capital/yield explicitly open | Measured build times and cash basket |
| FOX-006 | Optimize ten/twenty units | Actual 20/40-cell quantities, same-MPN pooling, shared charging, no invented price breaks | Quantity availability and logistics review |
| FOX-007 | Compare TinyFox/Fixle without replacing platform | Primary comparator cost/scope/evidence table; no third-party implementation | Comparator evidence remains source-specific |
| FOX-008 | Preserve RF/compact match/field/safety/timing; no fourth PCB/MCU | Original rule trace and measured gates retained, €8.38 antenna untouched | G0/G1/G6–G9; no hardware passes claimed |

The principal remaining costs are **€29.06 common electronics/antenna**, roughly **€9.80 protected-pack material budget**, **€6 bare-board fabrication**, **€4.43 outer mechanics**, **€4.70 transmitter connectors/harness**, and external equipment/freight. ESP32-S3/RTC and the antenna tuner are visible drivers; no hidden VHF/MMIC/IRF610 premium explains the difference. Shared charging and sourced new cells give useful savings, but **€29.06 is not a complete powered, enclosed, fabricated-unit cost**. [ADR-0009](decisions/ADR-0009-foxoring-fleet-cost-scope.md) proposes the fleet accounting/charging policy; complete layout, buying a transmitter set and hardware validation remain gated.
