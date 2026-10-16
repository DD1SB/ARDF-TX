# M5B-E2 review decision

2026-10-16. **GO for independent final manufacturing review and preparation of a five-board bare evaluation-PCB quote. No order or manufacturing release is authorized.** Populate one first only after separate approval.

The original F.Cu sliver is located at **(55.991446,68.075) mm on PACK_OK_N** and removed by shortening a doubled-back control route to its existing via. Activating E1's previously zero connection-width threshold at0.15 mm exposed five further manufacturing findings. Four localized control/power junction corrections and one0.4 ×0.4 mm fill-only GND notch clear them. [The correction report](M5B_E2_COPPER_CORRECTION.md) includes coordinates, object IDs, before/after images, native/Gerber evidence and controlled DRC comparisons.

The board remains **180 ×140 mm, two layers**, nominal0.8 mm/finished70 µm copper with a0.64 mm dielectric model. Si5351/PHA-1+/PD54008L-E, ST output matching/elliptic LPF, D45H11/BD139 sine-drain AM, fail-off, exclusive2S/4S populations and the independent training port are preserved. No component, value, footprint, via, RF conductor, connector position or thermal contact changed. Only localized PCB copper, revision marking and the minimum connection-width rule changed. The fresh PDF retains the unchanged E1 electrical schematic title; E2 identifies the PCB revision.

Actual **KiCad10.0.6** results:

- ERC: **0 errors, 0 warnings**.
- DRC: **0 errors, 0 unrouted, 0 parity issues**, **11 retained intentional courtyard warnings**, **0 exclusions**.
- The0.15 mm connection-width threshold is active; no sliver or narrow-connection warning remains. Only unused tuning-profile geometry checking is ignored.
- Regression: **4,096 combinations, 39 states, 37 mutations**,42 manufacturer pin maps,26 ST network positions and320 native schematic package/pad sets pass.

The [individual warning dispositions](M5B_E2_DRC_AUDIT.md) concern seven bodyless microstrip features and four inline probe contacts. No decorative courtyards or blanket waivers were added. RF80, M4A, historical designs and ADRs remain unchanged. E1 is preserved at tag `m5b-e1`, commit `6931260`.

Critical package maps are CAD-ready with documented assembly constraints: grounded PD source/vias/paste, PHA ground flange, isolated RNW central contacts, exact ST pinouts/live tabs, keyed connectors and finished holes. Separate insulated pass/helper mounting and the lower grounded spreader are specified. Incoming dimensions, exact TIM, solder voids, flatness and thermal behavior remain assembly/commissioning gates. Custom3D models are dimensional envelopes; three connector bodies remain unavailable in the installed model library. No final enclosure compatibility is claimed.

Component costs are unchanged: at10, **BOOST2S€50.27 / BUCK4S€49.03 / TRAIN_ONLY€14.11 net**. Unquoted amounts remain **€28.09 / €27.95 / €10.02** respectively. [Cost reconciliation](M5B_E2_COST_DELTA.md) contains6/10/20 totals and sourcing holds. Five bare boards remain an estimated **€60–100 net per batch plus€10–25 shipping**, not a quotation.

The required0.15 mm/70 µm process, core/Dk, annulus, holes and mask webs need written fabricator confirmation. Published catalog options are not combined-process acceptance; JLCPCB's stated0.16 mm minimum for2oz does not automatically accept this board. A compatible fabricator/process must be confirmed before ordering. No generic1.6 mm stack substitution is allowed. L301/L634/U950 sourcing holds and other estimated material remain visible.

The fresh [E2 package](../hardware/2m/review/M5B-E2/README.md) contains schematic PDF, native hashes, copper/assembly/placement views, actual KiCad3D, review Gerbers, separate PTH/NPTH/maps, logical/physical IPC, ERC/DRC, pin/pad and regression reports, BOM, geometry evidence and checksums. Analysis copies are separated from the final fabrication set. Local consistency checks are not independent commercial CAM acceptance.

Before an order: independently review the localized corrections and RF/thermal construction; confirm a compatible stack/process, finished holes and stencil/tents; obtain a real five-board quote; then obtain explicit user manufacturing authorization. Low-voltage procurement, power-stage population, controlled power-up and RF activation remain separate gates. No orders, uploads, fabrication, assembly, power-up or transmission occurred.

All physical tests remain **NOT_RUN**: input transients and wrong-pack protection, driver voltage/isolation, reset races and rearming, current/thermal/hot SOA, actual gain/stability, carrier/PEP/true AM/emissions, off-slot silence, port isolation, antenna ERP/field behavior and12 h/24 h endurance. Follow [one integrated bring-up procedure](M5B_E2_BRINGUP.md). Those measurements are required before transmitter use, not before fabricating a controlled evaluation PCB. This is a manufacturing-review candidate, not a released transmitter.
