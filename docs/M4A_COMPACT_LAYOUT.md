# M4A — compact RF80 layout

Date: **2026-10-15**. **M4A-V1 — PRODUCTION-INTENT, NOT RELEASED.** The separate [editable project](../hardware/80m/production/RF80_V1.kicad_pro), [schematic](../hardware/80m/production/RF80_V1.kicad_sch) and [PCB](../hardware/80m/production/RF80_V1.kicad_pcb) derive from1245023/E2. The evaluation project and its exports remain unchanged. This is a replacement 80m module candidate within the same three-PCB system, not an additional fourth primary board.

## Physical allocation

The outline is **150×110mm**,16,500mm² versus E2's33,600mm²: **50.9% area reduction**. Two outer copper layers, nominal1.6mm FR4/35µm,0.15mm general rules,0.60mm drain clearance and ordinary0.60/0.30mm vias are retained. The geometry accommodates the original connectors, two wound T60-2 toroids, FT-50A-43 transformer and through-hole power devices. It does not force the transformer or coils into unverified smaller packages. Height/thermal/cable assumptions are in the [mechanical interface](M4A_MECHANICAL_INTERFACE.md).

| Region | Placement purpose |
| --- | --- |
| Left | Keyed controller header, watchdog/quiet timers and captured ARM/path/mode logic, local bypassing |
| Top/center | Raw4S connector, fuse/reverse barrier, damper/bulk and buck. Feedback and switch loops remain local |
| Top/right | Driver and IRF610 near the board edge for insulated cooling access; phased transformer follows drain |
| Right/middle | Original elliptic LPF, orthogonal toroids and separate normalRF connector |
| Lower/center | Si5351/crystal with local reference return, separated from the buck switching node |
| Lower/right | Independent Fox shaped rail/buffer/LPF/pad and keyed compact-antenna port |

Critical RF/power trees are routed first; remaining low-current nets use a local offline router with telemetry/API disabled, followed by actual KiCad checks and return-plane inspection. This is not blind reliance on a router's “zero violations” message. Final copper views, DRC/parity/unrouted data and measured native path lengths are in the [V1 review package](../hardware/80m/production/review/M4A-V1/README.md). All components remain top-side for repeatable assembly/rework; no fine-pitch reduction or hidden vias are introduced.

## Electrical scope and test access

No purchased component, electrical value, non-test pin connection or full/Fox population changed. Manufacturer-specific Q403/U311 corrections are preserved. The original transformer9+9turns and elliptic filter values are unchanged; supply selection and independent hardware latches remain. **60 of74 probe pads are removed,14 retained**. [Every test-feature disposition](../hardware/80m/production/review/M4A-V1/test-feature-disposition.json) distinguishes essential production access, optional service access via existing pins and evaluation-only features.

Retained access covers3.3V, local grounds, both source clocks, PA/shaped/driver rails, Fox supply, ARMED/reset/watchdog/PA guard. RF calibration uses **J401/J502 into defined50Ω fixture loads**, rather than redundant RF pads/stubs. Optional detailed gate/drain/key-tail/comparator/race measurements use accessible component leads/pads on qualification units. The shared controller connector provides I²C/control/status; there is no new MCU, RTC or programming subsystem on RF80.

## Returns, thermal behavior and coupling

Both layers have ground pours with local ordinary-via fanout; no via-in-SMD-pad is accepted. RF/driver/buck loops require local return paths rather than long serial digital-ground tracks. Source/crystal are kept away from SW_PA. Normal supply/current-sense routing must retain adequate width and separate sense takeoffs; solid return copper and stitching must not be mistaken for characterized RF impedance or cooling.

Final native copper has **354 ordinary vias,112 on GND**, and one connected
network across41filled ground polygons. Local stitching at the driver, Fox
buffer and comparator returns required four short reroutes; those connections
were closed and checked rather than excluding isolated copper findings.
Nearest-via straight distances are1.85mm for U401GND and1.0mm for its C401
return. They are geometry metrics, not loop-inductance measurements. Some
low-current digital ground bridges remain0.15mm; measure their ground bounce
and common-impedance coupling before accepting the compact layout. See the
actual ground/routing reports. Summed native GATE_DRV/GATE_PA/DRAIN_PA trace
lengths are6.214/10.113/20.834mm, with no vias; these include branches and are
not claims of equal RF loop lengths. The source PA clock sum is72.172mm with
four vias; edge/ringing/spur checks remain mandatory.

Four layers could provide a less interrupted internal return plane, but no measured need justifies extra fabrication cost at this stage. The two-layer candidate must pass connectivity/manufacturing checks and then actual ground-bounce/spectrum/isolation comparisons. If those physical results fail, review a targeted layout/stack-up correction rather than declaring two layers qualified by DRC.

Compaction brings normal/Fox ports, magnetics and digital returns closer than E2. New risks include common-impedance coupling, clock harmonics, gate/drain ringing, increased regulator/driver-rail parasitics, local heating of capacitors/sense circuits and more difficult rework. Distinct connector nets and mutually exclusive permissions prevent a logical path transfer; they do **not** establish47dB RF isolation. Repeat E2's≤66µW leakage test at maximum normal power, all channels/key edges/faults, on V1. Requalify R410/C404 fault peak/delay on V1 **before fitting its driver**, even if E2 subsequently passes.

The board is ready only for the review status recorded in [M4A decision](M4A_REVIEW_DECISION.md). Native layout, ERC/DRC and electrical-equivalence evidence are separate from the **NOT_RUN** RF, thermal, safety and endurance tests.
