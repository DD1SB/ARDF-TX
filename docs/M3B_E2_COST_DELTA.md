# M3B-E2 — material cost delta

Date: **2026-10-15**. EUR **net**, VAT excluded. At19% VAT multiply taxable amounts by1.19; shipping/customs depend on the eventual order. **No quote, reservation or order was placed.** Exact candidate MPNs, footprints, supplier identifiers, MOQ/multiples, price classifications and open stock fields are in the [E2 workbook](M3B_E2_COMPONENT_WORKBOOK.md), [itemized CSV](M3B_E2_BOM.csv) and [machine baskets](M3B_E2_COSTS.json). [Machine E1/E2 delta](../hardware/80m/review/M3B-E2/cost-delta.json) is computed from both ledgers, not patched summary totals.

## Same material populations, corrected electrical implementation

| Population / identical-board quantity | E1 components/unit | E2 components/unit | Delta | E2 historical observations / estimates |
| --- | ---: | ---: | ---: | ---: |
|Full1|32.317|32.317|0.000|13.524 /18.793|
|Full6|31.896|31.896|0.000|13.103 /18.793|
|Full10|27.311|27.311|0.000|9.346 /17.965|
|Full20|27.311|27.311|0.000|9.346 /17.965|
|Fox-only1|13.759|13.759|0.000|5.469 /8.290|
|Fox-only6|12.081|12.081|0.000|4.759 /7.322|
|Fox-only10|10.815|10.815|0.000|3.593 /7.222|
|Fox-only20|10.468|10.468|0.000|3.558 /6.910|

The task's quantity-ten baselines **€27.31 /€10.82** are rounded versions of **€27.311 /€10.815**. “Historical observations” are retained dated M2/M3 observations with their original limitations, **not stock/prices reverified on2026-10-15**. More than half the quantity-ten full budget is estimated; zero modeled delta is not a firm purchase-price guarantee. Same-MPN requirements are pooled, quantity breaks and MOQ/leftovers included; no reel-only assumption is added.

| Count | E1 | E2 |
| --- | ---: | ---: |
| Full fitted purchased physical parts / ICs |196 /18|196 /18|
| Fox-only fitted purchased physical parts / ICs |115 /13|115 /13|
| Schematic electrical footprint positions |273|273|
| Total board footprints incl.4 mounts |277|277|
| Test pads (not separately purchased ICs) |74|74|
| Through vias |328|329|

The remote NTC is a purchased part despite being bonded off-board. Test pads, graphical footprints, DNP/optional positions and nonphysical symbols are not extra purchases. The production/normal population, Fox DNP rules and separate controller/battery architecture are unchanged.

| Correction | Material delta and scope |
| --- | --- |
| Q403 ST pin-correct symbol/180° placement | Same ST BD140, same estimated price. No substitute vendor or new transistor |
| Q4031.30mm holes/1.90mm lands, own mechanical envelope | No purchased component added; exact fabrication impact pending quote |
| U311 proper K/REF/A connections/local tracks/GND via | Same TI TL431AIDBZR, same estimated price. One extra ordinary via; no new comparator/reference |
| D302 specify LittelfuseSMBJ17A | Same unquoted€0.35 allowance, exact supplier code/stock still **OPEN**; not a verified new quote |
| Rule/mask/metadata/assembly corrections | No added components; +0.025mm mask expansion/0.075mm web and critical hole tolerances must be accepted by fabricator |

No hardware protection has been deleted to conceal cost. No component-level material saving is claimed from these necessary corrections. Engineering/review labor is one-time work and not a “free assembled transmitter” allowance.

## Bare boards and prototype-only costs

Retain the E1 **unquoted allowance** for five210×160mm,2layer1.6mmFR4/35µm ordinary through-hole evaluation PCBs: **€45–90 net total**, PCB freight **€10–25 separately**. If all five are used this allocates€9–18 per bare board; a one-populated-board experiment still pays for the five-board lot. **E2 actual fabrication price is PENDING**, particularly finished J101/J502 holes±0.05mm and agreed mask web. No claim of zero fabrication-price increase or repeatable promotion pricing is justified.

One full component basket plus five bare PCBs plus PCB freight remains an indicative **€87.32–147.32 net** before component freight/tax, inspection/labor and fixtures. E2 does not assume those boards are ordered. Bare-board cost at1/6/10/20 is **unquoted**, not extrapolated from a five-board promotion. Component counts/costs above do not include fabrication.

Prototype-specific allowances remain separate: **€2–6** heatsink/insulation/thermal attachment; **€8–20** reusable mating harness/coax fixture; **€2–5** calibration resistor/winding spares per experiment. Instruments, lab supplies, rated loads, pulse fixture and low-capacitance probes are shared equipment with no fabricated purchase price. Existing test pads need no purchased connectors. No new expensive permanently fitted measurement connector was introduced; many pads/spacings can disappear after qualification.

Controller, cells/BMS/charger, compact antenna loading/counterpoise, enclosure and wiring remain outside the RF80 component total. The [Fox cost audit](FOXORING_COST_AUDIT.md) and [M3B accounting bridge](M3B_EVALUATION_BOM.md) remain separate historical scopes; this revision makes **no change to complete-unit materials or shared fleet allocations**. It does not revive the earlier€77.11 accounting error or silently equate a corrected RF board with a complete Fox transmitter.

Before procurement, re-quote all estimated/dated rows and confirm exact LM5134B cut tape, ST identity, TI suffixes, custom core availability, C404 hot ESR, resistor pulse rating and harness contacts. Only a quote can resolve supplier/stock blockers; no components are authorized for purchase here.
