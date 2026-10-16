# RF2M electrical candidates

The active editable project is **M5A-R4**, a lower-cost PD54008L-E/PHA-1+ true-AM schematic with traced ST output matching and elliptic filtering. **NOT RELEASED; pre-layout electrical/physical holds remain.** No RF2M PCB, DRC report, Gerbers or hardware results are claimed.

Start with the [review decision](../../docs/M5A_R4_REVIEW_DECISION.md), [schematic PDF](review/M5A-R4/RF2M.pdf), [reference audit](../../docs/M5A_R4_RF_STAGE.md), [costed population BOM](review/M5A-R4/RF2M_BOM.csv) and [controller/variant contract](../../docs/M5A_R4_MODERNIZATION.md). All prices are dated observations or explicit estimates; this is not a released order list.

R3 is preserved at tag `m5a-r3` (`daf994c`). R0/R1 tags and the [R1 native archive](archive/M5A-R1/README.md) remain intact. R2 produced no new CAD. Historical review exports are unchanged. To inspect/reproduce old CAD, use its tag/archive rather than running a historical generator against this active project. The old DL3BBX permission file applies to the historical derivative; manufacturer ST/Mini-Circuits documents retain publisher rights. R4 drawings are independently generated engineering schematics, not redistributed original artwork or a blanket commercial-rights claim.

Reproduce the complete current review, using installed KiCad 10.0.6 and Python 3.12:

```sh
python3 tools/m5a_r4_review.py
python3 tools/m5a_r4_review.py --check
```

The pipeline generates native sheets, exports XML/PDF, runs ERC, netlist-derived logic/pin/variant tests, recalculates costs and power, regenerates six review documents, checks local links and preserved history, and seals hashes. Its R1 template generation occurs only in a temporary directory. RF80, M4A, root README and accepted ADRs are hash-preserved.

Current blockers are the changed 50 Ω MMIC/ST interstage definition, drive margin and the listed exact physical landings/thermal implementation. All analog timing, RF, AM, thermal and endurance tests remain **NOT_RUN**. No manufacture, procurement or RF operation is authorized.
