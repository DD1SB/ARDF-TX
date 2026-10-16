# M5B-E3 engineering change report

M5B-E3 replaces the E2 fabrication assumptions with ordinary two-layer **1.6 mm / 1 oz JLCPCB FR4, green mask, white legend and lead-free HASL**. This is an unbuilt evaluation design. E2 remains immutable at `m5b-e2` / `2ca4c8e`; its manufacturing-review GO is superseded. RF80, M4A, accepted ADRs and historical packages are hash-preserved.

The native project remains `hardware/2m/RF2M.*`. Initial inspection is recorded in [initial-change-impact.json](../hardware/2m/review/M5B-E3/initial-change-impact.json). The comparison baseline is Git, not an overwritten E2 export.

| Affected function | Actual implementation | Electrical impact |
| --- | --- | --- |
| Substrate | 0.8 mm/70 µm →1.6 mm/35 µm; no dielectric constraint | RF width/phase and power/thermal models recalculated |
| TL603–609 | Real flat-ended 2.741 mm copper; lengths scaled0.981206 | Preserves nominal E2 calculated phase; ordinary FR4 tolerance remains |
| Matching placement | Walked outward from fixed Q501 gate/drain | Small shifts, at most0.519 mm; all lumped values and topology retained |
| RF junctions/output | Replaced obsolete overlapping routes with direct junctions, flat copper and 8 mm SMA taper | New pad/stub/launch parasitics remain physical alignment gates |
| RF return | Bottom RF track keepouts retained; top fill-only channel widened to y46–62 | Avoids accidental coplanar loading; no bottom signal cut under matching |
| Power | Selectively enlarged existing main routes, mostly0.7–1.5 mm |35 µm native contact-graph voltage/drop model; short necks retained explicitly |
| Vias | Preferred0.80/0.30; local0.70/0.30 and 0.60/0.30 exceptions | All ordinary through-vias; list actual coordinates and nets inDFM report |
| PA source |12→32 ordinary0.80/0.30 GND vias;4×8 at 0.6 mm pitch | Thicker barrel path compensated partly; no solder-fill thermal credit |
| Source assembly | Copper landing unchanged; mask caps/paste grid; open bottom contact | Ordinary LPI tenting is neither plugging nor insulation |
| J101 |1.30 mm holes /1.90 mm lands | Standard hole tolerance clears maximum specified pin diagonal |
| J301 |1.80 mm holes, existing lands | More practical hole-fit margin on 1.6 mm board |
| Legend |≥1.0 mm /0.15 mm; thin library art moved toFab in real local variants | Some dense refs rely on complete assembly drawings; no DRC suppression |
| Local routing | Control/supply detours at widened RF strip and enlarged IDC | No net, pin contract, safety behavior or population change |

[engineering-regression.json](../hardware/2m/review/M5B-E3/engineering-regression.json) compares actual E2/E3 net membership and manufacturer pad geometry. Purchased MPNs, electrical values, population fields and prices are unchanged. Only the seven nonpurchased TL values/footprints change electrically descriptive metadata. Local symbol footprint filters now explicitly allow the connector footprints; pin definitions are unchanged.

The exact native track/placement and library deltas are available in Git and the JSON change reports. Development router/DRC investigations are isolated under `review/M5B-E3/development/`; only `gerbers/` is proposed fabrication data. No procurement, upload, manufacture or physical test occurred.
