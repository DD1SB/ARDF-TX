# Reproduce M6-L2

The committed native KiCad files are authoritative. Do not regenerate them from older milestone capture/layout scripts. Run from the repository root with KiCad10.0.6, its system Python pcbnew bindings, Pillow, a C11 compiler and Python3. Third-party DF1FO references remain outside this MIT repository; source-register.json records their official URLs and retrieved hashes.

Retrieve the originally cached references into a private temporary directory and verify their recorded hashes. A changed upstream file requires engineering review, not silently accepting a different reference. This downloads technical references only; it does not upload or order anything.

```sh
/usr/bin/python3 - <<'PY'
import hashlib, json, pathlib, urllib.request
cache = pathlib.Path('/tmp/m6l2/references')
cache.mkdir(parents=True, exist_ok=True)
register = json.loads(pathlib.Path('hardware/controller/review/M6-L2/source-register.json').read_text())
for item in register['sources']:
    if not item['sha256']:
        continue
    target = cache / item['file']
    if not target.exists():
        request = urllib.request.Request(item['url'], headers={'User-Agent': 'ARDF-TX engineering reference review'})
        target.write_bytes(urllib.request.urlopen(request, timeout=30).read())
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256'], item['file']
PY
```

```sh
/usr/bin/python3 tools/m6_l2.py checks
/usr/bin/python3 tools/m6_l2.py verify
/usr/bin/python3 tools/m6_l2.py protocols
/usr/bin/python3 tools/m6_l2.py protection
/usr/bin/python3 tools/m6_l2.py usb
/usr/bin/python3 tools/m6_l2.py powerpaths
/usr/bin/python3 tools/m6_l2.py dfm
/usr/bin/python3 tools/m6_l2.py host
/usr/bin/python3 tools/m6_l2_audit.py
/usr/bin/python3 tools/m6_l2_metrics.py
/usr/bin/python3 tools/m6_l2_documents.py
/usr/bin/python3 tools/m6_l2_bom.py
/usr/bin/python3 tools/m6_l2_references.py /tmp/m6l2/references
/usr/bin/python3 tools/m6_l2_exports.py exports
/usr/bin/python3 tools/m6_l2_exports.py render
/usr/bin/python3 tools/m6_l2_exports.py package
/usr/bin/python3 tools/m6_l2.py manifest
```

References and the Espressif STEP/DXF files are downloaded separately from the URLs in source-register.json. Before rendering, set M6_L2_MODEL_DIR to their local directory, containing ESP32-S3-WROOM-1U.step. The tool defaults to /tmp/m6l2/references. Original ASM/DOC files and the manufacturer STEP are not redistributed or relicensed as project MIT material. Renders use the actual manufacturer module geometry and native component models; physical fit remains NOT_RUN.

The checks command refills and saves native zones before ERC/DRC/parity reporting. Required counts are zero; packaging refuses nonzero CAD results and stale native source hashes. DFM includes the inherited native geometry mutations. The manufacturer DXF comparison reads both independent land drawings and the actual native module pads/paste. The host simulator compiles the C11 core and tests it against an independently written timed peer. Outputs go to M6-L2 and temporary compiler/reference files. Population exports temporarily write boards beside the project and remove them afterward. No command refreshes a historical review or RF board.

The native copper is committed; no autorouter or exploratory placement script is required for reproduction. No hosted routing, fabrication upload, purchase or physical measurement is part of reproduction. SHA256SUMS inventories review files; inventory.json also identifies source inputs. Generated PDF/render metadata may vary by tool build; native geometry, reports, package contents and checks must remain reviewable.
