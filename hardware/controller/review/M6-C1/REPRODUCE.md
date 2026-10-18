# Reproduce the candidate checks and exports

Run from repository root with KiCad10.0.6 CLI, `/usr/bin/python3` including pcbnew, a C11 compiler and the supplied project libraries. Python checks reuse frozen repository RF tools without modifying those tools or their historical reports. No network, manufacturer upload or hardware access occurs.

The strict RF re-extraction/preservation checks require the supplied RF80-V1 production working tree and RF2M-E4R1 baseline. RF80 production was untracked input when this controller was developed and is deliberately not added by the M6 commit. Frozen fresh RF netlists are in `inputs/`; `frozen-RF-files.json` records the complete supplied source-tree hashes. On a checkout without those inputs, KiCad controller checks and host fixtures still run, but a missing RF baseline must be reported rather than relabeled as a successful whole-project regression.

```sh
set -e
/usr/bin/python3 tools/m6_c1_contracts.py
/usr/bin/python3 tools/m6_c1_exports.py checks
/usr/bin/python3 tools/m6_c1_verify.py
/usr/bin/python3 tools/m6_c1_analysis.py
/usr/bin/python3 tools/m6_c1_route_audit.py
/usr/bin/python3 tools/m6_c1_dfm.py
/usr/bin/python3 tools/m6_c1_rf_protocols.py
/usr/bin/python3 tools/m6_c1_mechanical.py
/usr/bin/python3 tools/m6_c1_exports.py exports --render
/usr/bin/python3 tools/m6_c1_review.py
/usr/bin/python3 tools/m6_c1_exports.py manifest
```

Actual3D rendering requires a working local X display. The export command uses `DISPLAY=:97` with software GL in this environment; use a local display/Xvfb with that number or adapt only that environment setting. Missing display is a render failure, not a thermal/fit result. Stock KiCad3D libraries are required. RTC and IDC models are explicitly dimension-only envelopes; optional LoRa has no qualified model.

The final native PCB is the routed authority. Do **not** rerun `m6_c1_pcb.py --place` or import an old routing session to reproduce validation: those regenerate construction steps, not checks. Intermediate DSN/SES files in `analysis/` precede localized USB, fuse, ground and power-width corrections. The final checker reads actual geometry after zone refill and does not infer it from old router output.

`m6_c1_design.py` regenerates deterministic editable capture/metadata. If deliberately recapturing, export its netlist, run `m6_c1_finish.py --sync --stack --settings` to update board fields/pad assignments, then rerun every check/export above. Review any resulting net or footprint change before fabrication. Footprint/library-generation and placement tools are construction utilities, not necessary validation steps; do not overwrite a reviewed landing with a draft generator output.

The final audit repeats32 Python host tests and compiles/runs the C waveform/GPIO fixture with `-std=c11 -Wall -Wextra -Werror`. No target firmware or real-time peripheral test is implied. KiCad's SWIG property-enum diagnostics may appear on stderr; they are preserved in logs and are distinct from DRC/ERC violation counts. The pipeline must exit nonzero on failed checks.

`SHA256SUMS` covers review files except itself/inventory. `inventory.json` additionally hashes native sources, local landings/models and specifications. After a check/export legitimately regenerates timestamps or metadata, regenerate the inventory; do not compare timestamped Gerber hashes to an older export while claiming byte identity. Native electrical/geometry consistency is checked separately.
