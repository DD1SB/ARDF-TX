# M5B-E6R2 final executed verification — 2026-10-21

Starting commit: `b48865fed332ced9257559e174f0b6fceaaec096` on
`m5b-e6-unified-heatsink`. The final local commit is recorded in Git history.
This report covers checks executed during this implementation, rather than
historical PASS results. [REPRODUCE.md](REPRODUCE.md) gives the exact final
commands and dependency versions; the development logs retain original failures.

Linux x86_64; Python 3.12.3; KiCad CLI/pcbnew 10.0.6; ngspice 42.
Mechanical/plot environment: CadQuery 2.8.0, NumPy 2.5.4, SciPy 1.18.1,
Matplotlib 3.11.2 and Pillow 13.0.0. The separately downloaded TI model ZIP is
hash-checked and is not redistributed.

| Executed check | Result |
|---|---|
| Complete native schematic ERC | 0 errors, 0 warnings |
| Native PCB DRC | 0 errors, 0 unrouted, 0 schematic/PCB parity issues |
| Inherited DRC warnings | 11 missing-courtyard warnings, exactly matching E5 |
| Project rules/exclusions | Configuration byte-identical to starting project |
| Native electrical checks | 352 footprints, 51 critical manufacturer maps, all 20 controller contacts |
| Safety and local keying | 4,096 enable combinations, 36 safety scenarios, 16 local truth-table rows |
| Negative electrical/native cases | 68 detected |
| Source-joint regression | 16 native/input mutations and 4 adverse thermal-model cases detected |
| Actual GND copper contact graph | One connected component, including C409 reservoir ground |
| High-current copper | All 12 checked paths connected |
| Standard-process DFM | PASS; 11 native mutations detected |
| Mechanical solid checks | PASS; 2 deliberately colliding configurations rejected |
| Ngspice | 8 transient cases and 2 AC return-ratio cases executed |
| Numerical unit tests | 14 passed |

The source thermal negatives exercise numerical assumptions; they do not prove
that hardware detects a bad solder joint. The ngspice models use generic ST BJT
bounds, an averaged PA load and finite-impedance prepared rails. They do not
model the 144 MHz RF waveform or converter switching-loop stability. The low
gain BF20 sensitivity clips the modeled crest; hot gain/headroom remains a
measurement priority. Loaded/unloaded modeled loop margins are 85.87°/68.92°.

The [fresh CAM comparison](final-reproduction.json) exported 9 Gerbers and
separate PTH/NPTH drills into a temporary directory without replacing archived
files. All 11 files have identical geometry after removing only creation-time
records. Exported netlist component/pin/net semantics also match. Five source
paste windows total 6.765 mm² and the source mask remains unchanged.

The [fabrication audit](fabrication-data-audit.json) checks the actual native
drill locations against 953 PTH and 6 NPTH hits. ZIP CRCs and every archived
entry agree with the final CAM directory. ZIP entry metadata is fixed for
repeatable packaging. The bare-board archive contains 11 files; the stencil
archive contains full F.Paste and Edge.Cuts. [SHA256SUMS](SHA256SUMS) inventories
the complete review package. Native project inputs and all verification scripts
are separately hashed in the input manifests.

Manufacturing remains 150 × 110 mm, two-layer FR4, 1.6 mm, 1 oz, green mask,
white legend and lead-free HASL, with ordinary PTH vias and two routed cutouts.
No filled/capped vias or special stackup is required. Nominal 0.15 mm via
annuli remain explicit margin exceptions relative to the preferred 0.25 mm
land target; they are not concealed by exclusions. Commercial CAM upload,
supplier quotation and board ordering were not performed.

The preservation guard confirms unchanged M6-L2 controller, RF80, historical
RF2M review/manufacturing archives, prior tools and milestone evidence. Protected
RF tracks, matching/filter placement, Q501 source geometry and 98 thermal vias
are unchanged. Q401/Q402 and local modulator/control routing are revised. The
initial mirrored BD139 flat footprint, clamp-current issue and isolated C409
ground pour were corrected; rejected drafts and failure logs remain under
`development/`, which must never be used for fabrication.

**GO for five bare RF2M E6R2 evaluation PCBs, subject to independent review.**
The native cooling arrangement is implemented and dimensioned. Plastic/fin
details and the preserved upper controller/carrier are identified mechanical
envelopes. Incoming dimensions, source-joint quality, insulation, actual contact
performance, RF/AM/spectrum, thermal protection and outdoor behavior require
the [first-article procedure](../../../../docs/M5B_E6R2_FIRST_ARTICLE_TEST.md).
Continuous 1 W MO has only 0.49°C modeled Q401 margin; the adverse 134.72°C
source-contact scenario remains documented. Target firmware integration is
incomplete. Powered and operational qualification are **NOT_RUN**. No hardware
was energized, ordered or published.
