# ARDF-TX 80 m RF electrical design — M3A-R1

Date: 2026-10-14. **Review schematic, unbuilt and unvalidated. No PCB layout.**

Open [RF80.kicad_pro](RF80.kicad_pro) in KiCad 10, then [RF80.kicad_sch](RF80.kicad_sch). The root links thirteen circuit sheets, using explicit global nets and native multiunit gates/transistor/passive drawings. [PDF](review/RF80.pdf), [exported netlist](review/RF80.xml), [ERC report](review/ERC.json) and [pin/population manifest](RF80.electrical.json) are included. Local ARDF_TX symbol and footprint libraries resolve through the two project library tables; no reference-repository checkout is needed.

Normal population: protected4S input, approximately3 W full/1.2 W extended and calibrated Sprint. Fox-only: same RF PCB concept, protected2S/controller3.3 V, normal converter/driver/final/transformer/filter DNP. Fox-only omits U312/PA thermal/reference branches; R228/R348/R349 bias unused watt logic/comparator nodes. R336 is removed. Common S3/RTC/optionalLoRa and the separate2 m genuineAM module are retained elsewhere.

Read [R1 logic audit](../../docs/M3A_R1_LOGIC_AUDIT.md), [verification](../../docs/M3A_R1_VERIFICATION.md), [cost delta](../../docs/M3A_R1_COST_DELTA.md) and [R1 review decision](../../docs/M3A_R1_REVIEW_DECISION.md). R0 is preserved in Git tag `m3a-r0`.

Read [circuit review](../../docs/M3_80M_SCHEMATIC_REVIEW.md), [BOM](../../docs/M3_80M_BOM.md), [test plan](../../docs/M3_80M_TEST_PLAN.md) and [review decision](../../docs/M3_80M_REVIEW_DECISION.md) before preparing a prototype. ERC passes without reported errors/warnings; it cannot establish voltage margins, RF performance, SOA or component availability. Package/winding geometry is specified; custom wound-component lead forming and ancillary mechanical selection remain review gates.

Reproduce checks from repository root:

```sh
kicad-cli sch erc hardware/80m/RF80.kicad_sch --output hardware/80m/review/ERC.json --format json --severity-all --exit-code-violations
kicad-cli sch export netlist hardware/80m/RF80.kicad_sch --output hardware/80m/review/RF80.xml --format kicadxml
python3 tools/m3a_r1_logic.py
python3 tools/m3a_r1_driver_fault.py
python3 tools/m3a_r1_report.py
python3 tools/m3_80m_checks.py
```

The initial schematic was assembled by [m3_80m_design.py](../../tools/m3_80m_design.py), preserving actual pin assignments and a cost manifest. It produces ordinary editable KiCad files. **Do not regenerate after manual CAD edits without reconciling those edits with the manifest/generator**; regeneration replaces the schematic/library/workbook files. No board/placement/routing or production firmware is generated.

No components may be ordered or PCBs fabricated under this milestone. Electrical review and separate authorization for a small evaluation layout come next. [Attribution and licences](LICENSES.md).
