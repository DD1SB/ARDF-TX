# Frozen M3B-E2 prototype handoff — review only

Reference: **1245023**, tag **m3b-e2**. Intended scope: **five bare PCBs**,
with only **one initially populated in stages**. No purchase, supplier upload,
assembly, power-up or RF activation has been authorized.

`ARDF-TX_E2_1245023_source.tar.gz` is the exact Git archive. Unpack it into a
new directory to obtain the complete native E2 KiCad project, local libraries,
original documents, licenses and electrical evidence. `reference-package/`
copies the E2 exports byte-for-byte; these files have not been re-exported from
V1. Standard KiCad 10 libraries are needed to resolve standard interactive
3D models. Exported PDFs and PNGs can be inspected without KiCad.

Verify this self-contained handoff from its own directory:

```sh
sha256sum -c SHA256SUMS
```

The copied original E2 checksum files use repository-root paths: verify those
inside the unpacked original archive, not in `reference-package/`.
The handoff's `SHA256SUMS` uses paths relative to this directory.

Fabrication: **210 × 160 mm**, 1.6 mm nominal FR4, two layers, nominal 35 µm
outer copper; ordinary 0.60/0.30 mm vias. Use all nine fabrication Gerbers and
job metadata, separate PTH/NPTH drills and maps. Paste files support assembly;
they do not add copper layers. The 0.05 mm outline stroke is not an oversize
board profile. Requested process: **lead-free HASL, green mask both sides,
white legend**. Confirm solderability/flatness for MSOP0.5mm and0603; an ENIG
alternative requires a revised quote/review, not automatic substitution.
The frozen Gerber job retains its original unspecified-finish metadata.
Confirm electrical test, mask registration and actual
finished holes before ordering. Critical finished holes are:

- J101: **1.20 ± 0.05 mm**.
- J502: **0.95 ± 0.05 mm**.
- Q402/Q403: **1.30 ± 0.05 mm**; inspect real lead fit and body orientation.

Ordinary advertised PTH tolerances do not automatically meet these limits.
Tight-hole process availability and any surcharge remain **OPEN**. No vendor
has accepted these files or requirements. The retained five-board allowance
is €45–90 net plus €10–25 PCB freight, **not a quote or firm ceiling**.
One full component basket is €32.317 net before its freight, fixtures/labor/tax.

Critical assembly corrections: ST Q403 **1B→SHAPE_BASE, 2C→VPA_SHAPED,
3E→VPA_LOAD**, illustrated face toward PCB +Y; TI U311 DBZ
**1K/2REF→VREF_2V5, 3A→GND**. Read the archived E2 footprint/protection audits.
Exact manufacturer, suffix, approved dimensions and winding materials matter.
The procurement CSV is a candidate evidence list, not an authorized order.

The five separate gates in `handoff.json` are all **NOT_AUTHORIZED**:
bare fabrication; low-voltage procurement; high-energy population/procurement;
controlled power-up; RF activation. Approval of one grants none of the others.
Use `assembly-stages.csv` with the archived bring-up instructions and E2
power-protection restrictions. Begin with bounded laboratory supplies, never
an unrestricted Li-ion pack. Keep U401/Q402 absent during failed-buck tests.

All physical tests remain **NOT_RUN**, particularly ≤20 µs board isolation,
LM5134B rail ≤12.6 V, input/load-switch margins, actual reset/ARM races,
RF/thermal/SOA/isolation/field and 12 h full / 24 h extended endurance.
The compact V1 project is a separate, unqualified engineering candidate.
