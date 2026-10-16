# M5B-E2 supplier-neutral manufacturing review

**Not an order or production release.** Five bare boards; one initially populated in stages after separate approval.

Use only `gerbers/`, its separate PTH/NPTH Excellon files/maps, `RF2M-physical-netties.ipc` and SHA256SUMS. Native authority is RF2M.kicad_pcb plus native-inputs.json. Files under copper-investigation/ are comparison data and must never be ordered.

- Single 180 ×140 mm two-layer FR4 board; nominal0.8 mm finished thickness, finished70 µm copper per side, ENIG proposed.
- Core model0.64 mm; request±0.05 mm and actual laminate/Dk/copper/mask details. Do not infer core thickness from the overall-thickness checkbox.
- Minimum track/clearance/connection0.15 mm; ordinary vias0.60/0.30 mm, annulus0.15 mm; copper-edge0.50 mm; hole constraints0.25 mm; mask web0.10 mm.
- Critical finished holes: IDC1.10 mm; SMA center1.50 mm/shell1.70 mm; six NPTH mounts3.20 mm. Confirm tolerances and lead fit.
- Preserve source-via tents, bottom thermal window, segmented source paste and isolated RNW6/7/8 contacts. Initial100 µm stencil requires assembly review.
- No1.6 mm substitution, RF-line resizing or unsolicited CAM cleanup. Confirm the combined process in writing; catalog options are not an accepted quote. JLCPCB's published2oz minimum0.16 mm is above this design's0.15 mm rule.
- Electrical test must account for intentional TL net ties using the physical IPC/alias file; retain logical IPC for schematic comparison.

DRC:0 errors,0 unrouted,0 parity,11 retained bodyless-courtyard warnings,0 exclusions. The original sliver and five findings exposed by the active connection-width rule are corrected. Review docs/M5B_E2_FABRICATION.md, COMPONENT_FIT.md and BRINGUP.md before approving a quote or order.
