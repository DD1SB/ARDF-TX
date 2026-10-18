# M4A-V1R1 — proposed first evaluation article transition

Date: 2026-10-18. **PROPOSED — PENDING USER / INDEPENDENT ENGINEERING REVIEW.** This document requests a specific change to the original M4A sequence. It does not approve fabrication or erase historical decisions.

The retained [M4A review decision](M4A_REVIEW_DECISION.md) explicitly says V1 manufacture is NO-GO until E2 is physically qualified. Its “required next steps” 2, 4 and 5, and [M4A production test plan](M4A_PRODUCTION_TEST_PLAN.md) first-article steps 1–5, therefore conflict with treating V1R1 as the first 80 m hardware. That restriction remains historical evidence and is **not silently amended**. No physical E2 exists yet. This change proposal is for the user to approve before supplier upload/fabrication authorization.

## Proposed change

Use **five 150 × 110 mm RF80-V1R1 bare boards, with one initially populated in controlled stages**, as the first 80 m evaluation hardware, instead of first manufacturing five 210 × 160 mm E2 boards. Retain the frozen E2 schematic, manufacturer map checks and all physical acceptance methods as the electrical reference. Treat compact V1R1 as an evaluation board, not production-qualified hardware.

The accepted three-PCB architecture and existing controller contract are unchanged. No accepted ADR found mandates E2's dimensions or its first-hardware order. ADR-0012 remains **Proposed** and is not accepted here. The explicit M4A review/test-plan sequencing condition requires amendment by review, even though it is not an accepted ADR. No ADR has been edited.

## What carries forward and what must be measured

| Evidence / changed property | Treatment on V1R1 |
| --- | --- |
| E2 component values, RF core, transformer, filter, power modes | Same actual components/nets except prior classified test-pad removal; manufacturer checks inherited and rerun on new files |
| E2 corrected BD140 / TL431 manufacturer pinouts | Same physical mappings, checked in native pads, exported XML, copper Gerber and IPC |
| E2-to-V1 tests | All non-TP values/MPNs/populations/nets, 604 pad memberships and 55 critical devices still compared to frozen 1245023; legitimate PTH-size changes explicitly audited |
| Compact routing and return currents | Different from oversized E2; no physical equivalence asserted. Measure supply/ground bounce, gate/drain ringing, reset/feedback race, coupling, RF stability and port isolation on V1R1 |
| Changed parasitics | Compact trace/loop lengths, component coupling, shared ground and hot-device proximity remain unknown physical quantities; hole corrections do not waive them |
| E2 protection experiment | Perform driver-absent failed-buck/current-limited surrogate on V1R1 before fitting U401/Q402: board isolation ≤20 µs and VDRV≤12.6 V including uncertainty, hot capacitor ESR and realistic parasitics |
| E2 reset/rearm/watchdog tests | Run full real timing matrix, ≥500 MHz/low-capacitance reset method, quiet interval, deliberate rearm, fault priority; logic simulation is not a substitute |
| E2 RF/thermal tests | Repeat all normal/Sprint/Fox power, CW/harmonics, mismatch, hot SOA, sensor detachment, thermal and off-slot measurements directly on V1R1 |
| Endurance/antenna/independent assembly | Retain full 12 h / reduced 24 h targets, continuous-beacon distinction, normal/Fox separate antennas, field method and independent-build reproducibility sample |

No E2-to-V1 analog comparison can be measured when E2 does not exist. Instead record V1R1 waveforms against absolute existing safety and RF criteria, with E2 topology/calculations as reference only. Any failure stops progression and triggers a controlled local correction; it does not authorize a redesigned transmitter. Manufacturing the large board later remains an option only if a concrete failure makes comparison useful and the user separately approves it.

## Gates and requested decision

A: current CAD/electrical integrity; B: standard-process DFM; C: independent bare-board review can pass without physical RF tests. The **sequence change** itself remains pending. D: authorized supplier upload/CAM/quote; E: separately authorized purchase; F: separately authorized staged population/power/RF. All seventeen retained physical tests are **NOT_RUN**. No user approval, transmission permission or production release is inferred.

This proposal removes duplicated bare-board cost and transfers the complete experiment to the intended compact geometry. It removes **no protection experiment or commissioning requirement**. Accepting it would amend the M4A sequencing restriction only; it would not waive any measured acceptance bound. See [integrated bring-up plan](../hardware/80m/production/review/M4A-V1R1/BRINGUP.md).
