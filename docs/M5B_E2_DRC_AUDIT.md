# M5B-E2 DRC audit

KiCad **10.0.6** was actually run. Fresh [DRC text](../hardware/2m/review/M5B-E2/DRC.rpt), [DRC JSON](../hardware/2m/review/M5B-E2/DRC.json), [ERC](../hardware/2m/review/M5B-E2/ERC.json) and exact command logs are retained.

| Result | Count |
| --- | ---: |
| ERC errors / warnings | 0 / 0 |
| DRC errors | 0 |
| Unrouted connections | 0 |
| Schematic/PCB parity issues | 0 |
| Warnings | 11 |
| Exclusions | 0 |

[DRC-coverage.json](../hardware/2m/review/M5B-E2/DRC-coverage.json) contains the full native severity map, numerical constraints and individual dispositions. All copper, clearance, annulus, drill, hole, mask, silkscreen, courtyard, footprint, via-connection, isolated-copper and thermal categories remain enabled. The sole ignored category is `tuning_profile_track_geometries`: no tuning-profile geometry exists. Enabled length/skew/creepage checks without corresponding constraints do not establish numerical limits or RF impedance.

E1's zero minimum connection-width threshold was ineffective coverage. E2 sets **0.15 mm**, corrects the five exposed findings and keeps the category visible. No severity was reduced. Minimum track/clearance are 0.15 mm, annulus 0.15 mm, copper-edge 0.50 mm, hole clearance 0.25 mm and mask web 0.10 mm.

All eleven remaining warnings are **B — intentional non-component footprints**. They are retained, not excluded. See [the per-feature native audit](../hardware/2m/review/M5B-E2/DRC-warning-dispositions.md) for exact positions and connections:

| References | Individual disposition |
| --- | --- |
| TL603, TL604, TL605, TL606, TL607, TL608, TL609 | Each is a real 1.102 mm F.Cu transmission line with intentional net-tie endpoints. No purchased body, assembly volume, paste or mask opening exists. A component courtyard is inapplicable. |
| TP601, TP602, TP603, TP604 | Each is a 0.60 mm inline bare probe contact within existing 1.102 mm copper. Its mask opening is intentional; it has no paste or mounted body. The copper margin is 0.251 mm per side. No added RF stub or decorative courtyard is needed. |

All eleven are excluded from purchased BOM/placement data. Adjacent mounted components retain their real courtyard checks. The four probe planes are nearby RF observation points, not intrinsic transistor-die voltages. Probe capacitance can detune them.

Reproduce sequentially from the repository root:

```sh
/usr/bin/python3 tools/m5b_e2.py checks
/usr/bin/python3 tools/m5b_e2.py verify
/usr/bin/python3 tools/m5b_e2.py evidence
DISPLAY=:97 LIBGL_ALWAYS_SOFTWARE=1 /usr/bin/python3 tools/m5b_e2.py exports --render
/usr/bin/python3 tools/m5b_e2.py reports
/usr/bin/python3 tools/m5b_e2.py artifacts
sha256sum -c hardware/2m/review/M5B-E2/SHA256SUMS
```

Use a working local X display for actual KiCad rendering. `correct` is the separate idempotent E1-to-E2 patch, unnecessary for verification of the final board. DRC exit code 5 represents retained warnings, not zero violations. Zone refill saves the board; run dependent steps sequentially.

The existing regression passes **4,096 combinations, 39 state scenarios and 37 mutations**, with 42 manufacturer pin maps, 26 ST network positions and 320 native schematic package/pad sets. Functional static checks do not prove analog reset timing, overvoltage response, AM, thermal behavior or RF performance. Local export validation is separate from independent fabricator CAM acceptance.
