# M5B-E1 review decision

2026-10-16. **GO for independent review of one integrated evaluation PCB. NO_GO for an order until the remaining CAM warning and fabrication confirmations are closed, followed by explicit user authorization.** No purchasing, fabrication, assembly, power-up or RF operation occurred. All hardware acceptance is NOT_RUN.

The editable [schematic](../hardware/2m/RF2M.kicad_sch) and [180×140 mm PCB](../hardware/2m/RF2M.kicad_pcb) preserve the selected Si5351/PHA-1+/PD54008 chain, ST output matching/elliptic filter, drain-sine AM, autonomous fail-off, captured mode and separateµW training port. The board supports mutually exclusive2S boost/4S buck and training-only populations. R4 is preserved at `m5a-r4`/`b44fe3b`; RF80 and historical references are unchanged. No ADR is silently accepted.

The seven missing landings are resolved. Additional corrections fix the unreachable current-trip threshold, high-DCR MMIC choke, marginal driver switch and converter input bypassing. Two independent regulators and a rated isolation switch replace reliance on an unmeasured20µs fault assumption. The initial50Ω interstage includes the33nH gate-bias feed;47nH/22pF/22pF is a documented tunable starting population, not measured device matching. The final output network values remain unchanged. Thermal construction has separate insulated pass/helper mounting and a grounded lower PA spreader/contact window.

KiCad 10.0.6: **ERC0 errors/0 warnings; DRC0 errors,0 unrouted,0 parity issues, 12 visible warnings.** Eleven warnings concern bodyless TL/probe copper features; one is an unlocated F.Cu copper sliver. No exclusions are installed. Full coverage/dispositions are in [DRC-coverage.json](../hardware/2m/review/M5B-E1/DRC-coverage.json). The sliver is not falsely declared harmless: independent native/Gerber CAM inspection must locate/dispose it before ordering. Do not globally disable the checker or change matching copper without review.

The actual exported netlist/native pad regression passes **4096 combinations,39 state scenarios,19 original mutations plus18 new mutations**, 42 manufacturer pin maps,26 ST network positions and all 320 schematic package/pad sets. Main current paths retain≥0.5mm copper or short pad necks on70µm copper. Static checks do not qualify analog startup/reset races, overvoltage transients, RF stability, AM or thermal performance.

| Population | 6 each | 10 each | 20 each | Fitted parts | ICs | Unquoted at10 | Delta/R4 at10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOOST2S | €54.33 | €50.27 | €49.94 | 272 | 25 | €28.09 | €+6.95 |
| BUCK4S | €52.76 | €49.03 | €48.71 | 268 | 25 | €27.95 | €+7.01 |
| TRAIN_ONLY | €14.11 | €14.11 | €14.11 | 103 | 13 | €10.02 | €+2.83 |

The complete unquoted amounts remain substantial. Buck-inductor delivery,47nH matching-inductor lead time and preregulator inventory require procurement confirmation; they do not make bare-board evaluation layout impossible. Five-board fabrication budget€60–100 net plus estimated€10–25 shipping is not a supplier quote. Populate only one first, after separate approval.

The [review package](../hardware/2m/review/M5B-E1/README.md) contains final-native references, PDF, copper/assembly/3D views, review Gerbers/drills, logical and physical-net-tie IPC, pin/pad reports, variants and checksums. Custom3D geometry is identified as dimensional envelopes; missing standard connector visualization is explicitly listed rather than treated as package qualification. Actual footprints/holes are separately audited.

Before a small bare-PCB batch: independently inspect native RF/thermal layout and the unlocated sliver, confirm the0.64mm dielectric/70µm copper stack and0.15mm rules/connector finished holes, confirm buildable source/spreader/stencil assembly and obtain a real quote, then request explicit manufacturing authorization. No nonexistent RF measurement is demanded before this evaluation-board review. Before MMIC fitting or RF activation, follow [one staged bring-up procedure](M5B_E1_BRINGUP.md): bounded logic/power tests, both regulator-fault cases with MMIC absent, modulator/thermal checks, driver alignment, full RF acceptance, training/isolation and endurance. Actual gain, clean70–80%AM/PEP/ERP, harmonics, off-slot silence, hot SOA and12h/24h results remain NOT_RUN. This is an evaluation candidate, not production release.
