# M3B — evaluation PCB review decision

> **2026-10-15 correction notice:** This is a historical pre-E2 record. E1/R1 ST BD140 pin/orientation claims and the E1 manufacturing recommendation are superseded by [M3B-E2 corrections](M3B_E2_CORRECTIONS.md) and the [E2 decision](M3B_E2_REVIEW_DECISION.md). Use E2 assembly/netlist files: Q403 **1B/2C/3E**, illustrated ST face toward **PCB+Y**, and U311 TI DBZ **1K/2REF/3A**. E1 drawings are not build instructions. Frozen historical checks are not current E2 verification.


Date: **2026-10-14**. Revision **M3B-E1**. **Proposed review disposition; no order or hardware operation authorized.** Baseline M3A-R1 commit`0dfd224` and R0 tag`m3a-r0` preserved.

**CONDITIONAL GO for a small bare evaluation-PCB batch after the review, sourcing/fit checks and explicit approval below. NO-GO for production release or unrestricted4S/driver/RF operation.** The board is ready to review as a staged experiment; it is not a validated transmitter. No parts have been ordered, Gerbers sent to a manufacturer, hardware fabricated, assembled or energized.

## Delivered

- One native, editable **210×160 mm two-layer KiCad evaluation PCB** in the existing RF80 project. Fifteen schematic pages,273 electrical footprints plus four mounting holes,74 measurement pads, existing separate normal/Fox outputs and population variants.
- Current **ERC0; all-severity DRC0; unrouted0; schematic-parity0**. No DRC exclusion used. Current-netlist regression preserves **256 logic combinations,31 state scenarios,16 timing corners** and both polarity-mutation rejection tests. Every664 physical pad/net membership checked. These are digital/CAD checks, not physical safety proof.
- Current [schematic PDF, copper/assembly previews, actual KiCad3D views, Gerbers, metric plated/nonplated drills, drill maps, placement, IPC connectivity and reports](../hardware/80m/review/M3B-E1/). Native [PCB](../hardware/80m/RF80.kicad_pcb), [logical checks](M3B_CHECK_RESULTS.json), [logic results](M3B_LOGIC_RESULTS.json), [layout review](M3B_PCB_LAYOUT_REVIEW.md), [qualification](M3B_COMPONENT_QUALIFICATION.md), [staged bring-up](M3B_BRINGUP_PLAN.md), [safety gates](M3B_SAFETY_GATES.md), [costed evaluation BOM](M3B_EVALUATION_BOM.md).

## Necessary electrical and package changes

1. Add **1.5 Ω damper/100 µF35 V bulk** on normal input, sense pack before it, retain reverse barrier/fuse and change upstream100 nF to50 V. A17 V-named TVS is **not** treated as an18/20 V clamp. The passive model supports the stated≤10 µH harness envelope, not arbitrary surges or wrong-source voltage.
2. Add **100 nF transformer-feed bypass**, without changing transformer turns/core/ratio or elliptic filter topology/values. Measure its RF and key-edge effect.
3. Correct467 fuse **1206→actual0603** landing; qualify IDC body/key and1.2 mm holes; conservatively enlarge IRF610 holes to1.3 mm. Form transformer leads inline with the same electrical polarity and connection. Missing two installed3D models are replaced by clearly identified dimensional envelopes; incoming fit still requires inspection.
4. No safety gates or R1 asynchronous permissions were removed or simplified for routing. Three-PCB architecture, ESP32-S3/RTC/optionalLoRa, separate2 m **true A2A1 W carrier ERP** and all independent antenna paths are unchanged. Proposed ADR-0012 has a separately marked M3B amendment; it remains proposed.

## Cost and readiness

Full component candidate **€32.32 for one /€27.31 each at ten**; Fox-only **€13.76 for one /€10.82 at ten**, net, excluding bare PCB/external accessories. Full quantity-ten change is+€0.711 from actual R1; Fox+€0.011. No material saving is claimed. The evaluation layout's extra pads/space add no separate purchased IC but do affect bare-PCB cost.

**Five bare boards:€45–90 net unquoted allowance**, freight€10–25 separately; one populated experimental board's component basket plus the five-board bare batch and PCB freight is€87.32–147.32 before fixtures/labor/component freight/tax. Exact prototype quote and critical component basket remain OPEN. Production6/10/20 context and legacy Fox complete/fleet scopes are kept separate in the BOM.

## Conditions before and after ordering

Before recommending an actual order: an independent reviewer must inspect the native board and review plots, exact stack-up/finished-hole tolerances, transistor/connector orientation, formed winding clearance and staged assembly boundaries. Obtain a bare-board quote for this actual outline and verify the exact critical MPN availability/package documents. **User approval is required before any order or file transfer to a manufacturer.** This task stops without one.

The first board must begin with Stage0/unpowered inspection, then isolated3.3 V logic. **U401/Q402 must remain absent until the power-only tests prove driver-fault withdrawal≤20 µs and VDRV≤12.6 V**. The100 µs passive counterexample exceeds12.6 V; calculations do not waive that gate. Verify reset/ARM pulse widths, held-ARM non-rearming, supply collapse, current-trip startup, input ringing/fuse coordination, remote NTC bond, BD140 hot SOA, normalRF power/efficiency/emissions/key shape, Fox nominal10 mW and measured port isolation. All physical results are **NOT_RUN**.

A failing stage requires a targeted correction before dependent tests. Existing12 h full/24 h reduced endurance figures remain models; R350 adds loss and usable4S1P margin must be rechecked with measured currents and the real dropout endpoint. No continuous-beacon or field-range performance has been established. The next engineering activity is review of this concrete evaluation PCB and, only after authorization, staged hardware qualification—not another architecture comparison.
