# M3B-E2 — electrical corrections

Date: **2026-10-15**. Baseline **55a5b3f**, annotated tag **m3b-e1**. E1 review files remain byte-identical. E2 is an unbuilt evaluation revision; the earlier E1 recommendation and transistor/reference pin assertions are withdrawn by this review.

## Q403: confirmed ST base/emitter reversal

The actual ST-authored **BD140 May 2008, Rev 5**, Figure 1/page 1 and SOT-32 mechanical drawing **0016114E/page 7**, specify **1 BASE, 2 COLLECTOR, 3 EMITTER**. The drawing shows **3–2–1 left-to-right when viewed from the illustrated package face**. This is the viewing convention used for assembly; an unspecific “front” label is insufficient. The [official ST endpoint](https://www.st.com/resource/en/datasheet/bd140.pdf) timed out twice. The actual [ST-authored PDF recovered from Electrokit](https://www.electrokit.com/upload/quick/12/96/0eac_40320006-tds.pdf) was inspected, including the mechanical picture; [source identities and SHA-256](../hardware/80m/review/M3B-E2/source-identities.json) record provenance. Another manufacturer's BD140 is not an approved substitution.

| Physical pin | ST function | E1 net — wrong | E2 net — required |
| --- | --- | --- | --- |
| 1 | Base | VPA_LOAD | **SHAPE_BASE** |
| 2 | Collector | VPA_SHAPED | **VPA_SHAPED** |
| 3 | Emitter | SHAPE_BASE | **VPA_LOAD** |

The new local symbol **ARDF_TX:BD140_ST** changes physical pin numbers, retaining base input and collector/emitter passive electrical types. It is not a graphical relabeling. The footprint retains native pad numbers **1/2/3**, at local x=0/2.28/4.56 mm. The actual numbered footprint is rotated **180° about the unchanged collector**, now with origin (160.56,69.00) mm. In PCB top view: west **3/E** (156,69), center **2/C** (158.28,69), east **1/B** (160.56,69). The illustrated ST face points toward **PCB +Y/bottom edge**. From that side the physical order is 3/E,2/C,1/B. Verify the actual ST part before soldering.

This rotation reuses the existing emitter/base tracks; **no PA shaping, drain, gate or RF track was rerouted**. A separate manufacturing defect was also corrected: a 1.00 mm hole cannot accommodate the maximum 0.88×0.63 mm ST lead diagonal, **1.082 mm**. The explicit **ST_BD140_SOT32_1p3Drill** landing uses 1.30 mm nominal holes/1.90 mm lands. Lead forming to the 2.28 mm PCB pitch and a 2 mm body stand-off are assembly constraints. The new own dimensional-envelope model follows the ST maximum body; it is not certified supplier CAD. The Q403 silkscreen reference was moved clear of the enlarged pads. Assembly orientation is also annotated on F.Fab.

## U311: additional critical TL431 application error

Independent manufacturer review found **TI TL431AIDBZR, DBZ/SOT-23** had E1 nets **1 VREF_2V5 / 2 GND / 3 VREF_2V5**. The original library symbol's pin names were already correct; its application connections were wrong. [TI SLVS543S, revised May 2024, Table 5-1/page 4](https://www.ti.com/lit/ds/symlink/tl431.pdf) requires **1 CATHODE, 2 REF, 3 ANODE**. E2 ties **1+2 to VREF_2V5, 3 to GND**. The new explicit local alias **TL431_TI_DBZ** preserves native TI numbering. The MPN, threshold intent and 2.495 V reference circuit remain the same. E1 cannot be assumed to establish the intended analog protection thresholds.

U311 remains at its original position and orientation. Four short old reference/ground segments were removed, local VREF branches were connected to pins 1/2, and pin 3 received a short ground stub and one 0.60/0.30 mm via at (108.9,72) mm. [Connection-by-connection record](../hardware/80m/review/M3B-E2/local-copper-changes.json) and [independent E1/E2 geometry comparison](../hardware/80m/review/M3B-E2/connectivity-change-audit.json) identify the changes. All other pre-existing track/via geometries are unchanged. Both ground zones were refilled.

## Other changes and preserved circuits

- D302 now specifies **Littelfuse SMBJ17A**, replacing an unspecified manufacturer field. Its electrical value/package and €0.35 unquoted allowance are unchanged. This selection does not make it an 18 V clamp.
- All five ignored PCB DRC categories were restored. Actual used symbol footprint filters were corrected to exact approved landings. No warning was hidden to obtain zero. Global mask expansion/web are now 0.025/0.075 mm; [full audit](M3B_E2_DRC_AUDIT.md) explains the manufacturing changes.
- Revision/date, symbol aliases, manufacturer/datasheet notes, population metadata and new exports consistently identify E2. Every hierarchical sheet's title revision changed; this is not a redesign of every sheet.
- No RF values, windings, PA supply settings, interlocks, pin-13 watchdog permission, pin-12 quiet holdoff, controller/VHF circuitry, PCB outline or layer count changed. No component was added or deleted. Gate/drain/source/filter routing remains E1 geometry.

The old E1 pin check repeated the incorrect expected BD140 mapping and did not independently assert the TL431 application nets. Its passing result was insufficient. E2's [manufacturer-specific test](../tools/m3be2_pinouts.py) checks symbols, physical pad nets, footprint identity, manufacturer identity, Q403 installed orientation and both exported/netlist representations. It rejects ten negative cases, including the actual archived E1 Q403/U311. **ERC/DRC cannot substitute for this test.** No physical result is claimed.
