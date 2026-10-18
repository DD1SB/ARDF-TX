# Reproduce M6-C1R1

Run from the repository root using KiCad10.0.6 CLI, `/usr/bin/python3` with pcbnew, and a C11 compiler. These commands use the checked-in final native board; they do not regenerate placement or reroute it. Do not run the frozen `m6_c1_*.py` tools directly on R1: their original output directory belongs to the immutable M6-C1 evidence. The dedicated wrapper redirects output and updates only legitimate R1 assertions.

```sh
set -e
/usr/bin/python3 tools/m6_c1r1.py contracts
/usr/bin/python3 tools/m6_c1r1.py checks
/usr/bin/python3 tools/m6_c1r1.py verify
/usr/bin/python3 tools/m6_c1r1.py analysis
/usr/bin/python3 tools/m6_c1r1.py powerpaths
/usr/bin/python3 tools/m6_c1r1.py dfm
/usr/bin/python3 tools/m6_c1r1.py protocols
/usr/bin/python3 tools/m6_c1r1.py mechanical
/usr/bin/python3 tools/m6_c1r1_electrical.py
/usr/bin/python3 tools/m6_c1r1_usb.py
/usr/bin/python3 tools/m6_c1r1.py exports --render
/usr/bin/python3 tools/m6_c1r1.py review
/usr/bin/python3 tools/m6_c1r1_audit.py
/usr/bin/python3 tools/m6_c1r1_report.py
/usr/bin/python3 tools/m6_c1r1.py manifest
```

The strict RF preservation/re-extraction checks require the supplied RF80 production working tree and frozen RF2M-E4R1 sources. Their1,220 file hashes are retained; RF80 production was user working-tree input, not added to the controller commits. Fresh interface netlists live in inputs/. Missing source trees must be reported, not silently counted as successful tests.

Actual KiCad rendering uses DISPLAY=:97 and software GL in this environment. Start an appropriate local X/Xvfb display or adapt only that environment setting if necessary. No display means rendering failed. RTC/IDC models remain dimension-only envelopes and optional LoRa's package remains HOLD. Bottom-copper/assembly SVGs and assembly-bottom.pdf are explicitly mirrored for a bottom-side view. The top variant PDFs show the differing populations; all six underside positions are common to base variants.

The native schematic capture and sync actions are construction utilities for intentional future edits, not validation commands. Any recapture/net change requires complete parity, DRC, electrical and export replay; sync never repairs copper by deleting it. Frozen M6-C1 source tools and review evidence are preserved. No supplier upload, network service or hardware operation occurs in the reproduction pipeline.

check-commands.json/export-commands.json and host-test-results.json preserve exact commands/output. KiCad SWIG property-enum/image-handler diagnostics can appear on stderr and are distinct from ERC/DRC counts. All critical gates assert their numerical/native results. New source tests mutate actual pads/numerical inputs. Physical tests are NOT_RUN.

After legitimately regenerating timestamped artifacts, rerun the manifest. SHA256SUMS covers review files except itself/inventory; inventory.json also hashes native libraries/models, tools, specifications and the firmware foundation. Do not compare stale timestamped exports while claiming byte identity.
