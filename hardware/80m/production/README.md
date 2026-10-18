# RF80 V1 — PRODUCTION-INTENT, NOT RELEASED

This separate KiCad 10 project derives from the frozen `1245023 / m3b-e2`
electrical reference. Open **RF80_V1.kicad_pro**. The original project one
directory above is unchanged. Do not regenerate the evaluation board from V1.

The 150 × 110 mm, two-layer candidate preserves every non-test component,
value, manufacturer mapping and connection. Fourteen of the evaluation
board's 74 probe pads remain. Full Classic/Sprint/Fox and Fox-only are
population variants of this same PCB; the three-PCB system is unchanged.

- [Engineering decision](../../../docs/M4A_REVIEW_DECISION.md)
- [Layout](../../../docs/M4A_COMPACT_LAYOUT.md)
- [Mechanical assumptions](../../../docs/M4A_MECHANICAL_INTERFACE.md)
- [Variant BOM and installed-cost scope](../../../docs/M4A_VARIANT_BOM.md)
- [Electrical equivalence](../../../docs/M4A_ELECTRICAL_EQUIVALENCE.md)
- [Production test plan](../../../docs/M4A_PRODUCTION_TEST_PLAN.md)
- [Review exports](review/M4A-V1/README.md)

Native DNP flags describe the **full** assembly: the three Fox-only bias links
R228/R348/R349 are DNP. Use the explicit Fox population and placement files
for the reduced assembly; do not interpret a full-board render as its assembly
instruction. TH301 is one remote insulated PA-case sensor in the full build.

The electrical protections, analog timing, RF output/spectrum/port isolation,
compact antenna field range, thermal behavior and endurance remain **NOT_RUN**.
CAD equivalence does not qualify altered layout parasitics. E2 must be built
and measured first under separately approved staged conditions, and any
resulting electrical corrections must flow into V1 before its physical review.
No order, upload, assembly, power-up or production release is authorized.

Local generator commands that replace routing input (`m4a_design.py --place`,
`--derive`) are **not verification commands**. Use the checked-in PCB for review;
read the review README before running export/audit tools. Local dimensional
WRL envelopes retain E2's limitations; they are not certified supplier CAD.
See [licenses](LICENSES.md) and retained source attribution.
