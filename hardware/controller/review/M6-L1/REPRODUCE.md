# Reproduce M6-L1

Run from the repository root with `/usr/bin/python3`, KiCad **10.0.6**, its
`pcbnew` Python bindings, a C11 compiler and the installed standard libraries.
SVG previews additionally use the ordinary `librsvg-2`, `libcairo` and
`libgobject` shared libraries. No source or fabrication data is uploaded.

The immutable comparison is commit
`742159d363dd8dd8b8ff653d01238af9a49ef2aa`. Keep M6-C1 and M6-C1R1 review
directories intact. Do not run their capture/sync/route utilities on the active
design. `m6_l1.py` redirects the frozen check implementations into this directory;
it deliberately offers no automatic recapture or reroute operation.

Full RF integration replay also requires the existing RF80-V1/M4A working inputs
and RF2M-E4R1 sources enumerated in `frozen-RF-files.json`. Some RF80-V1 files
were pre-existing uncommitted work at the start of M6-L1; this milestone does
not stage or modify them. A fresh clone without those inputs cannot claim all
1,220 RF-file preservation checks. The interface XML snapshots in `inputs/`
freeze the contracts used by this controller candidate; they are not a
replacement for the complete RF-module physical review packages.

```bash
set -e
/usr/bin/python3 tools/m6_l1.py contracts
/usr/bin/python3 tools/m6_l1.py checks
/usr/bin/python3 tools/m6_l1.py verify
/usr/bin/python3 tools/m6_l1.py analysis
/usr/bin/python3 tools/m6_l1.py dfm
/usr/bin/python3 tools/m6_l1.py protocols
/usr/bin/python3 tools/m6_l1.py powerpaths
/usr/bin/python3 tools/m6_l1.py mechanical
/usr/bin/python3 tools/m6_l1.py protection
/usr/bin/python3 tools/m6_l1.py usb
/usr/bin/python3 tools/m6_l1_geometry.py
/usr/bin/python3 tools/m6_l1_ufl.py
/usr/bin/python3 tools/m6_l1_rf.py
/usr/bin/python3 tools/m6_l1_views.py
/usr/bin/python3 tools/m6_l1_variants.py
/usr/bin/python3 tools/m6_l1.py exports --render
/usr/bin/python3 tools/m6_l1.py review
/usr/bin/python3 tools/m6_l1_report.py
/usr/bin/python3 tools/m6_l1.py manifest
```

KiCad rendering needs an available graphical display. The recorded run used
`DISPLAY=:97` with `LIBGL_ALWAYS_SOFTWARE=1`; a normal local desktop display or
ordinary Xvfb server can provide it. `check-commands.json` and
`export-commands.json` retain the exact successful KiCad commands and outputs.
KiCad's Python bindings print their existing enum/image-handler debug messages;
the actual ERC/DRC and subprocess exit results are recorded separately.

The reference register is `manufacturer-evidence.json`. To repeat the commercial
alias comparison, download each listed manufacturer and distributor PDF into a
temporary directory, compute SHA-256 and compare each band pair. Full copyrighted
PDFs are linked rather than redistributed. The mechanical function tables were
manually transcribed from the cited pages; the native-geometry tests check that
transcription against all actual lands, not an automated reading of a PDF image.
Stock/prices are dated indexed observations and must be rechecked at procurement.

Gerber and drill export timestamps will change. `fabrication-equivalence.json`
records raw hashes and separately compares geometric commands, stripping only
the documented metadata/comments. Do not expect byte equality after regeneration
and do not remove drawing commands to force a comparison to pass.

Validate the retained review dataset without regeneration:

```bash
cd hardware/controller/review/M6-L1
sha256sum -c SHA256SUMS
```

`inventory.json` separately binds the exact native sources, scripts and firmware
fixtures. The manifest excludes itself and `inventory.json` to avoid circular
hashes. Physical commissioning remains NOT_RUN.
