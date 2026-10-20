# M6-L2 controller manufacturing candidate

Current native sources are `hardware/controller/CTRL.kicad_pro`, `CTRL.kicad_sch`, its referenced sheets, `CTRL.kicad_pcb`, `ARDF_CTL.kicad_sym` and `ARDF_CTL.pretty`. The new independently reviewable package is `hardware/controller/review/M6-L2/`. M6-L1 and earlier reviews are immutable historical baselines.

The fabrication profile remains 100×100 mm, two copper layers, standard FR4, 1.6 mm, 1 oz copper, green mask, white legend, lead-free HASL. Four original mounting holes, USB-C, battery and RF IDC positions are preserved. Ordinary 0.8/0.3 mm ground/power and 0.6/0.3 mm signal unfilled through-vias and separately exported PTH/NPTH drills require no premium process. New through-hole option connectors use ordinary soldered finished holes and audited annuli. The full top-paste export is regenerated because the module footprint/body and optional top-side positions change the assembly/stencil evidence.

Review outputs include fresh schematic PDF, native top/bottom copper and assembly views, real KiCad 3D renders, native pad/package and module matrices, electrical calculations and mutation results, host test logs, ERC/DRC/parity/unrouted counts, standard-JLCPCB geometry/DFM results, population BOMs, component sourcing/cost delta, exact reproduction commands, Gerbers, separate drills and a revision-specific five-bare-board ZIP. SHA-256 inventories identify both deliverables and source inputs. The ZIP is local; no supplier CAM upload, order, purchase, main-branch push, acceptance tag or production release is authorized.

Use an explicit BOM for every assembly. All FoxPro/GPIO components may remain DNP. A base assembly fits recovery R300/R301 and omits R302/R303; FoxPro assembly reverses that choice. GPIO3/46 service links remain open; GPIO45 remains NC without breakout. Preserve the three explicit LoRa variants, exact trusted RF band/antenna identity and M6-C1R1 protected battery-ID calibration policy. Both RF branch constructions remain unchanged.

Source prices are either dated indexed distributor observations in their original currency or explicitly marked estimates. Cost tables include quantities 1,5,10,20, MOQ/multiple rounding, unused purchase quantities and the module replacement delta against M6-L1. A planning conversion is not a foreign-exchange quote. Taxes, freight, assembly, panel jack/cable/contacts, external 2.4 GHz antenna, enclosure, batteries and RF modules are not included unless individually listed. No fixed procurement total is claimed; recheck exact order codes, stock and MOQ before any separately authorized purchase.

All physical assembly, electrical, ESD, RTC, RF, thermal, USB and FoxPro interoperability checks are NOT_RUN. Controlled bare-board evaluation does not require those measurements to have already happened. The actual GO/HOLD decision and any remaining engineering blockers are in [M6_L2_REVIEW_DECISION.md](M6_L2_REVIEW_DECISION.md); a document's existence is not acceptance.


The module replacement and added components have the following per-controller planning deltas against the same M6-L1 RF/LoRa population. Values mix dated indexed prices and explicitly marked estimates, using a planning factor of 1 EUR/USD, not current exchange rates. These are not quotations and exclude MOQ excess; the separate purchase model includes rounding and unused parts.

| Population | 1 board | 5 boards | 10 boards | 20 boards |
|---|---:|---:|---:|---:|
| Base | −€0.0654 | −€0.0654 | +€0.0414 | +€0.0414 |
| GPIO | +€4.0955 | +€3.4155 | +€3.0281 | +€2.9721 |
| FoxPro | +€3.0589 | +€2.0379 | +€1.7487 | +€1.7487 |
| Both | +€6.3698 | +€5.5188 | +€4.6654 | +€4.6654 |

The delta contains the exact U10 replacement plus 47 added purchased references: two default recovery links and 45 optional interface references (FoxPro/GPIO options replace the recovery links when needed). Two normally open PCB service links and two service probe pads are copper features, not purchased items. The full reference-by-reference delta, exact order codes, supplier MOQ/stock evidence and all48 populations are in the revision review's BOM and sourcing files. Shared resistor quantities are combined before selecting price tiers.
