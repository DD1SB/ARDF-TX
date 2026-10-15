# M5A-R2 review decision

2026-10-15. **NO-GO for module-specific PCB commitment and manufacturing. M5A-R2 remains incomplete at the user's mandatory sourcing gate.** The requested Mitsubishi schematic/PCB was not fabricated on paper by assuming stock, a suitable modulator or a qualified footprint. No purchase, fabrication, assembly, power-up or RF operation occurred.

## Findings and recommendation

Mitsubishi's current official lineup lists RA07M1317M in production, and the manufacturer explicitly permits fixed-quiescent-bias/input-controlled linear modulation. It is a credible technical direction for reducing RF matching/development risk. RA07M1317M-501 remains the primary **candidate**, not the accepted replacement for R1. No guaranteed linear-AM crest or required low-Iq performance is documented.

The specific commercial stop is unresolved6/10/20-unit supply terms. RF Parts offers individual/ten-unit pricing and says In Stock without a quantity; GLYN lists RA07 without price/MOQ/lead time. The allowed RA08N-502 alternative has40 listed at GLYN, but no price/customer minimum/delivery offer. The concrete MAAV-011017 input-AM route also lacks current EU stock. These are actionable sourcing gaps, not evidence that the products are unavailable everywhere. A single complete supplier confirmation can close them; another broad architecture study cannot.

At the current retail comparator, the provisional4S accounting bridge is **EUR69.25/66.40/66.40 at6/10/20**, before freight/import/VAT/PCB/cooling. At10 this is **EUR15.70 above R1 EUR50.70**, although EUR6.36 below R0 EUR72.77. The training-only R1 allowance remains EUR16.37. A circa EUR36 complete module and a new completed ordering BOM are unsupported. Full2S totals remain additionally open because a7.2 V regulated rail cannot be made by simply retargeting the existing boost below8.4 V input.

For1 W carrier ERP/assumed−1 dBd, actual connector PEP is4.079 W at80% AM and capability target5.135 W. With the retained0.75 dB filter-loss scenario, module capability must be6.103 W: only0.274 dB below RA07's6.5 W **nonlinear** specification. This does not establish clean linear margin. RA08N's8 W rating provides another0.90 dB rating distance, but cannot be silently substituted or treated as an AM guarantee.

The conditional model favors4S buck for regulated normal power and leaves2S normal regulation unresolved. Four M35A cells calculate17.4 h full/26.8 h reduced at Iq0.30 A and assumed efficiencies; the reduced case lacks20% planning reserve. Eight cells improve margin. If the required linear bias is near the roughly2 A shown by the manufacturer's fixed3.5 V typical curves,24 h reduced fails even on eight M35A cells. Bias/clean crest/cooling/endurance are therefore coupled acceptance items. They are not reasons to invent measured efficiency.

## Direct comparison

| Scope | Preserved M5A-R1 | Mitsubishi candidate |
| --- | --- | --- |
| Main RF chain | PHA-1+ /PD54008L-E; source/matching/package OPEN | Internally matched two-stage module; direct filtered-clock drive plausible but unqualified |
| AM | D45H11/BD139 drain modulation | Input-voltage-envelope control with fixed VGG; actual complete circuit not yet implemented |
| Quantity10 4S component allowance | EUR50.70 | EUR66.40 incomplete accounting scenario; delivered prices OPEN |
| Fitted physical count/ICs |258 /23 | Unknown until real R2 schematic;52 old positions removed only in accounting |
| RF construction | Discrete final landing and device matching/tuning unresolved | Fewer external device-match structures; grounded flange/heatsink construction essential |
| Risk removed | None claimed validated | Potential reduction in device-level matching/stability work; no guaranteed whole-system AM result |
| Effort saved | No measured labor baseline | Potentially simpler assembly/commissioning; no invented minutes or EUR credit |
| Training |104 positions/14 ICs, separate output, EUR16.37 allowance | Must retain independent bounded branch; no completed new population/layout |

## Delivered review evidence

- [Manufacturer/reference and exact pin drawing](M5A_R2_MITSUBISHI_REFERENCE.md), [input-AM review](M5A_R2_AM_IMPLEMENTATION.md), [power/thermal/endurance](M5A_R2_POWER_THERMAL.md), [sourcing/itemized cost bridge](M5A_R2_SOURCING_COST.md).
- [Controller contract disposition](M5A_R2_CONTROLLER_INTERFACE.md), [artifact/PCB stop report](M5A_R2_PCB_REVIEW.md), [one-board acceptance process](M5A_R2_ACCEPTANCE_TEST.md).
- [Machine-readable review](../hardware/2m/review/M5A-R2/README.md): source dates/hashes/actual supplier observations, calculations,6/10/20 itemized accounting CSV, pin-drawing transcription, preservation and fresh R1 regression reports.
- R1 preserved by commit`4785057`, tag`m5a-r1`;440 baseline files unchanged including all existing80 m/M4A hardware and accepted decisions. KiCad10.0.6 R1 ERC0 errors/3 existing OPEN warnings;4096 combinations/36 scenarios and pin/logic mutation regressions pass. **No R2 ERC/DRC/pad-to-net PASS is claimed.**

## Explicit remaining acceptance items

| User criterion | Status |
| --- | --- |
| 1–2. Selected module and actual fleet source | Current-production candidate verified; selection/delivery gate **OPEN** |
| 3. Manufacturer-guided linear AM | Guidance verified; whole-chain AM **NOT_RUN** |
| 4. Concrete implemented input-AM circuit | Route identified with real device/pins; complete schematic **NOT_CREATED** |
| 5. Carrier/PEP arithmetic | **CALCULATED**, filter/antenna/linearity remain unmeasured |
| 6–9. LPF, separate ports, schematic, routed PCB | Preserved in R1; Mitsubishi implementation **NOT_CREATED** |
| 10–11. Pinout and protections | Drawing inspected; actual R2 CAD/physical checks **NOT_RUN** |
| 12.6/10/20 complete costs | Itemized bridge delivered; actual R2 BOM/delivered price **OPEN** |
| 13. End-to-end acceptance | Procedure prepared, all physical steps **NOT_RUN** |
| 14. Unverified remains unverified | Maintained |

Keep R1 as fallback unchanged. Do not approve a PCB order from this packet. The smallest next input is exact module and amplitude-control delivery/price/MOQ confirmation, preferably including spares; no communication/order was sent. Once that closes, resume the authorized **single integrated-board** electrical/layout task, resolve its bounded supply/bias/control implementation and physical lead/heatsink geometry, then obtain independent review. No extra coupon program or controller redesign is proposed. Any later accepted architectural change must be recorded explicitly; no ADR was silently accepted here.
