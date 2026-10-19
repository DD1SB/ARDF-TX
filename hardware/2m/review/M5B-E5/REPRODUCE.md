# Reproduction

Use installed KiCad 10.0.6 and `/usr/bin/python3` with pcbnew. Run from repository root. Do not run historical generators, which target frozen review directories.

```
/usr/bin/python3 tools/m5b_e5.py checks
/usr/bin/python3 tools/m5b_e5.py verify
/usr/bin/python3 tools/m5b_e5.py models
/usr/bin/python3 tools/m5b_e5.py dfm
/usr/bin/python3 tools/m5b_e5_engineering.py
/usr/bin/python3 tools/m5b_e5_ground.py
/usr/bin/python3 tools/m5b_e5_closure.py
/usr/bin/python3 tools/m5b_e5_mechanical.py
/usr/bin/python3 tools/m5b_e5.py thermal
DISPLAY=:97 LIBGL_ALWAYS_SOFTWARE=1 /usr/bin/python3 tools/m5b_e5.py exports --render
/usr/bin/python3 tools/m5b_e5_delivery.py
/usr/bin/python3 tools/m5b_e5_reports.py
/usr/bin/python3 tools/m5b_e5_final_audit.py
```

Commands that refill/save the native board must finish before another board writer starts. Final delivery binds native hashes, exported drills and revision. Verify the SHA256 manifest after reproduction; PDFs/3D can contain tool-dependent metadata. Layout construction scripts are development history; the committed native board is the routed source authority.
