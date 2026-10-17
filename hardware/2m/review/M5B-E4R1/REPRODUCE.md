# Reproduce the candidate checks and review exports

Run from the repository root with KiCad 10.0.6 and its /usr/bin/python3 pcbnew binding. Thermal calculations use the Python standard library. Rendering requires an existing X display and software OpenGL; replace :97 with the available display. Commands do not submit data externally. Checks refill/save the active PCB, then all subsequent reports bind that final native file.

```bash
/usr/bin/python3 tools/m5b_e4r1.py checks
/usr/bin/python3 tools/m5b_e4r1.py verify
/usr/bin/python3 tools/m5b_e4r1.py dfm
/usr/bin/python3 tools/m5b_e4r1.py models
/usr/bin/python3 tools/m5b_e4r1.py thermal
/usr/bin/python3 tools/m5b_e4r1.py engineering
DISPLAY=:97 LIBGL_ALWAYS_SOFTWARE=1 /usr/bin/python3 tools/m5b_e4r1.py exports --render
/usr/bin/python3 tools/m5b_e4r1.py reports
/usr/bin/python3 tools/m5b_e4r1.py delivery
sha256sum -c hardware/2m/review/M5B-E4R1/SHA256SUMS
```

Actual KiCad command vectors and return codes are preserved in check-commands.json, export-commands.json, before-after-evidence.json and stencil-export-audit.json. Geometry implementation is tools/m5b_e4r1_design.py; it deliberately reconstructs from920da7b and must not be run over unrelated edits. The normal check sequence above operates on the already implemented candidate. No physical test is performed by these commands.
