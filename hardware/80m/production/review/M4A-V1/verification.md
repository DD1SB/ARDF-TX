# M4A verification record

Date: **2026-10-15**. Native KiCad/pcbnew **10.0.6**, Python **3.12.3**
(system interpreter; see command record for actual version), local software
Mesa/X display `:93`. No external router service, manufacturer upload or
physical equipment operation was used. FreeRouting 2.5.0/OpenJDK 25 was used
locally as a routing aid, with GUI/API/telemetry disabled. Its intermediate
completion message was not treated as zero-unrouted evidence.

## Reproducible checks

```sh
/usr/bin/python3 --version
kicad-cli version
/usr/bin/python3 tools/m4a_exports.py --render
/usr/bin/python3 tools/m4a_verify.py --logic
/usr/bin/python3 tools/m4a_artifact_audit.py
/usr/bin/python3 tools/m4a_geometry_review.py
/usr/bin/python3 tools/m4a_costs.py
/usr/bin/python3 tools/m4a_document_checks.py
/usr/bin/python3 tools/m4a_artifact_audit.py --manifest
sha256sum -c hardware/80m/production/review/M4A-V1/SHA256SUMS
```

Exports act only on the separate V1 project. The CLI command log contains
explicit `--severity-all`, `--all-track-errors`, `--schematic-parity`, zone
refill/save, netlist/PDF and Gerber/drill/position/render options. Do not run
placement/derive/import/ground-repair tools as read-only verification.

Results: ERC **0**; DRC **0 violations/0 unrouted/0 parity**; no DRC exclusions
or ignored checks, all **62** configured native DRC categories enabled. ERC
retains exactly the reference's three informational defaults:
`single_global_label` (intentional named test/observation nets),
`four_way_junction` (explicit junction connectivity), `simulation_model_issue`
(no complete transistor/logic SPICE model claimed). Their identities are
recorded in `ERC.json`/`drc-coverage.json`. No functional ERC error is hidden.

Every non-TP manifest record and XML connection matches E2. All **604 native
pad memberships**, component values/footprint IDs/full-population DNP flags
and footprint-local pad/lead/drill geometry are checked. **55 maker-specific
devices**, source drawings and actual physical pin/net mappings are audited;
**12 regression mutations rejected**, including a real native in-memory PCB
mutation restored without saving. The R1 engine uses the current V1 XML:
**256 combinations,31 state scenarios,16 timing corners**. Its retained engine
revision label is explained by `logic-source.json`, which records the exact
candidate XML SHA256; the result is not an archived-R1 netlist test.

The nine current Gerber layers/job carry M4A-V1 identity. All **401 native
holes** match separate PTH/NPTH exports within **0.0005 mm** quantization.
Q403/U311's six physical pins match both copper flashes and IPC output.
195 full board placements (plus external TH301) and 115 Fox placements agree
with the population scope. There are **354 ordinary vias**, including112GND;
no via center lies in an SMD pad. Native minimum trace is0.15mm. Filled-ground
analysis finds **one network across41polygons**, not just two shared zone
labels. All1993D model references resolve; E2 dimensional-envelope limitations
and incoming fit/thermal inspections remain.

Archived version-specific suites were executed in temporary directories:
R1 `m3_80m_checks`, `m3a_r1_logic`, `m3a_r1_driver_fault`, `m3a_r1_report`,
`m3a_r1_documentation`; E1 `m3b_verify`, `m3b_documentation`. All exited0.
`historical-version-regressions.json` identifies exact versions/commands.
These historical passes **do not** validate E1's known BD140/TL431 errors.
Current V1 uses corrected E2 manufacturer assertions and immutable E2 data.

The local Python KiCad binding emitted `PROPERTY_ENUM` assertion diagnostics
at import and duplicate image-handler debug messages when loading two boards;
raw verification output records them. The commands completed successfully;
native CLI ERC/DRC and independent Python assertions produced the results
above. These tool diagnostics are not hardware test evidence.

## Boundary

All physical test entries in `physical-qualification.json` are **NOT_RUN**.
Static polarity/state tests do not establish asynchronous reset pulse widths,
comparator behavior, ground bounce, driver fault isolation or analog startup.
No loop-inductance/thermal/RF calculation is presented as a measurement.
The compact board must repeat layout-dependent qualification after E2; its
changed parasitics/coupling are a separate risk. Supplier quote, exact current
stock, tight-hole capability and any surcharge remain open. Neither package
is an authorized order or production release.
