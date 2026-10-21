# Reproduce M5B-E6R2 from the committed native candidate

Run from repository root. The routed `hardware/2m/RF2M.kicad_pcb` and complete
schematic hierarchy are authoritative. Do not run the one-time design,
floorplan,clamp,relocation or routing-development helpers on the final board.
They record development provenance; regeneration starts from the reviewed
native project. Older E5/E6/E6R1 packages are immutable and their old generation
commands must not be directed at this updated project.

The reviewed implementation is commit `2fff32131dd0f7da3c46fef47c04713a55df89d8`.
The [publication record](../../../../docs/M5B_E6R2_FINAL_PUBLICATION.md) documents
the later independent-review conclusion and a separate fresh reproduction run.
The review generator writes implementation-time README/decision prose; run it
in the disposable checkout and preserve the current publication documentation.
Publication updates only documentation and its hash entries. Native sources,
manufacturing archives and original numerical/CAD evidence remain unchanged.

Executed environment: Linux x86_64,Python3.12.3,KiCad CLI/pcbnew10.0.6,
ngspice42. Geometry/plot venv: CadQuery2.8.0,NumPy2.5.4,SciPy1.18.1,
Matplotlib3.11.2,Pillow13.0.0,with system-site-packages for pcbnew.
A C++17 compiler is used only by the routing-development aid,not these checks.

Create an equivalent geometry environment if needed (outside the repository):

```sh
python3 -m venv --system-site-packages /tmp/m5b-e6r2-venv
/tmp/m5b-e6r2-venv/bin/python -m pip install cadquery==2.8.0 numpy==2.5.4 scipy==1.18.1 matplotlib==3.11.2 pillow==13.0.0
```

The TI model is an external copyrighted reference,not MIT project source.
Download it separately and retain its vendor license. This run used TI's
TLV9002 RevC per-amplifier model as TLV9004 family proxy,not a matched quad
package or characterized ST power-device model. The script checks this ZIP SHA:
`516e3f6405b699003d94840520966d7599c6c3af37f37c69541f9ed7ae211fe6`.
A different model revision requires review,not bypassing the check.

```sh
mkdir -p /tmp/m5b-e6r2/references
curl -fL --max-time 60 -o /tmp/m5b-e6r2/references/TLV9002-model.zip https://www.ti.com/lit/zip/sbomal2
sha256sum /tmp/m5b-e6r2/references/TLV9002-model.zip
```

Exact final verification/export entry points:

```sh
/usr/bin/python3 tools/m5b_e6r2_checks.py checks
/usr/bin/python3 tools/m5b_e6r2_verify.py
/usr/bin/python3 tools/m5b_e6r2_checks.py power
/usr/bin/python3 tools/m5b_e6r2_ground_audit.py
/usr/bin/python3 tools/m5b_e6r2_checks.py source
/usr/bin/python3 tools/m5b_e6r2_checks.py dfm
/tmp/m5b-e6r2-venv/bin/python tools/m5b_e6r2_simulation.py
/tmp/m5b-e6r2-venv/bin/python tools/m5b_e6r2_test_simulation.py
MPLCONFIGDIR=/tmp/m5b-e6r2-mpl /tmp/m5b-e6r2-venv/bin/python tools/m5b_e6r2_models.py
MPLCONFIGDIR=/tmp/m5b-e6r2-mpl /tmp/m5b-e6r2-venv/bin/python tools/m5b_e6r2_drawings.py
/usr/bin/python3 tools/m5b_e6r2_delivery.py bom
/usr/bin/python3 tools/m5b_e6r2_checks.py exports
kicad-cli pcb render --width 2000 --height 1550 --quality high --background opaque --rotate 325,0,25 -o hardware/2m/review/M5B-E6R2/RF2M-3D.png hardware/2m/RF2M.kicad_pcb
kicad-cli pcb render --width 2000 --height 1550 --quality high --background opaque -o hardware/2m/review/M5B-E6R2/RF2M-3D-top.png hardware/2m/RF2M.kicad_pcb
kicad-cli pcb render --width 2000 --height 1550 --quality high --background opaque --side bottom -o hardware/2m/review/M5B-E6R2/RF2M-3D-bottom.png hardware/2m/RF2M.kicad_pcb
/usr/bin/python3 tools/m5b_e6r2_reproduction.py
/usr/bin/python3 tools/m5b_e6r2_delivery.py fabrication
/usr/bin/python3 tools/m5b_e6r2_review.py
/usr/bin/python3 tools/m5b_e6r2_delivery.py inventory
```

Do not run concurrent writers to the native board. The check command refills
and saves zones,then exports ERC/netlist/DRC. DRC exit5 is expected for the11
preserved missing-courtyard warnings; it is not accepted blindly. Acceptance
requires zero errors,zero unconnected items,zero parity issues,no new exclusions,
and exactly the inherited warning set. ERC must have zero reported violations.
Use a disposable checkout when rerunning exporters so the committed evidence
remains available for comparison. The independent `reproduction.py` command
exports to `/tmp/m5b-e6r2-final-reproduction` and compares against the archived
CAM without replacing it. Inspect `final-reproduction.json` for per-file hashes
and classifications.
DFM and fabrication delivery assert actual geometry/drill counts and final native
hashes. No thresholds are relaxed to turn failed checks into PASS.

Rendering is headless in this environment; no X display was needed. Native
rendering must resolve project-relative STEP/WRL models and KiCad standard3D
libraries. Mechanical STEP fin/plastic details are identified approximations;
mounting planes,hardware,body envelopes and native cutouts are dimensioned.

Archive reproducibility: ZIP entries use fixed2026-10-21 metadata. Gerber and
Excellon export timestamps may differ. Compare all copper/mask/paste/silk/edge
and drill geometry after removing only creation/export timestamps. STEP/PDF
metadata can differ; do not treat actual geometry/netlist/paste differences as
metadata. The fabrication audit checks all9Gerbers,2drills,150×110outline and
standard job profile; source paste windows remain6.765mm². SHA256SUMS lists
this run's exact bytes. Never silently replace an independently reviewed archive.

Logs include original failures and corrections. TI model contents are not
redistributed. No command uploads/orders boards,creates a tag,pushes Git or
executes a physical test. Refer to the first-article plan before powered work.
