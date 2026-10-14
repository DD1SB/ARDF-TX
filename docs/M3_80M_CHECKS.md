# M3A-R1 — electrical and documentation checks

Date: **2026-10-14**. **No physical RF measurement, analog RF simulation or hardware validation.** All prototype gates in the [test plan](M3_80M_TEST_PLAN.md) remain **NOT RUN**.

## KiCad artifacts

KiCad CLI **10.0.6** successfully opened the ordinary editable [root schematic](../hardware/80m/RF80.kicad_sch), exported its [14-page PDF](../hardware/80m/review/RF80.pdf) and [XML netlist](../hardware/80m/review/RF80.xml), and ran ERC with all enabled severities. The [JSON ERC report](../hardware/80m/review/ERC.json) records **zero violations** on all 14 pages. No ERC exclusions were added.

Four checks remain disabled by the installed KiCad default configuration: `single_global_label`, `four_way_junction`, `simulation_model_issue`, and `footprint_filter`. This is **not a claim that every possible ERC rule was enabled**. Explicit named-net/pin and footprint-pad checks below supplement ERC; the R1 passive driver-fault sensitivity uses ngspice, but no transistor/RF simulation or hardware validation exists. Package geometry, power ratings and component availability require engineering review regardless of ERC.

Reproduce from the repository root:

```sh
kicad-cli sch erc hardware/80m/RF80.kicad_sch --output hardware/80m/review/ERC.json --format json --severity-all --exit-code-violations
kicad-cli sch export netlist hardware/80m/RF80.kicad_sch --output hardware/80m/review/RF80.xml --format kicadxml
kicad-cli sch export pdf hardware/80m/RF80.kicad_sch --output hardware/80m/review/RF80.pdf
python3 tools/m3a_r1_logic.py
python3 tools/m3a_r1_driver_fault.py
python3 tools/m3a_r1_report.py
python3 tools/m3_80m_checks.py
python3 tools/m3a_r1_documentation.py
```

The initial CAD generator is [m3_80m_design.py](../tools/m3_80m_design.py). Its `--write` operation replaces generated schematics/libraries/workbooks; **reconcile manual CAD edits before regenerating**. The project needs its local symbol/footprint tables and installed standard KiCad footprints. Four custom footprints describe individual components, not board placement or routing.

## Independent design checks

[m3_80m_checks.py](../tools/m3_80m_checks.py) reads the **actual exported KiCad netlist**, compares it with the electrical manifest, checks selected critical physical pin maps independently, and resolves the gate logic from physical pins rather than an isolated block diagram.

| Check | Result / limit |
| --- | --- |
| Schematic pages / manifest rows | 14 pages /226 manifest references: full223 positions (193 purchased), Fox132 (115 purchased) |
| Exported connected pins | **597 pass**; no-connects remain explicit |
| Assigned physical footprint pad maps | **218 pass**; native HC21 omits package NC pins 3/11, explicitly documented exception |
| Permission combinations | **256 pass** over actual physical-pin gate/timer/FF networks; see R1 scenario coverage |
| Sequential and fault scenarios | **31 pass**, plus16 assumed timing corners; startup/stuck lease, both paths, individual trips, pending ARM, withdrawal, profile, KEY-high and deliberate rearm |
| Purchase arithmetic | **18 baskets /1,344 CSV rows pass**: per-MPN pooling, MOQ/multiples, price breaks and per-board totals |
| Key qualification / tail | Actual HC14/NAND gate mapping checks mute with no key-tail; separate path permissions required. Analog timing and startup transients remain unmeasured. |
| Stale-ARM behavior | HC74 asynchronous clear/clock connections checked; Pin-derived HC174 context/HC74 model preserves off until a fresh raw edge; both original HC123 polarity mutations rejected. Propagation-delay/race/brownout behavior requires E1. |
| Structural Fox separation | No watt RF/PA supply node connected to Fox circuitry; leakage, EMI and future layout isolation remain E6 gates |
| Analog arithmetic | Independent references, loaded thermal hub, comparator common-mode margin, TL431 bias, rails, pi pad and tolerant fault-power bound pass stated assumptions |
| CAD scope | No `.kicad_pcb` or Gerber in the new hardware directory; no production layout |

The [R1 verification](M3A_R1_VERIFICATION.md) adds actual timer/FF pin-derived checks,31state scenarios,16assumed timing corners, negative-polarity tests and a passive ngspice driver-fault sensitivity. Its imposed20 µs isolation/0.5 Ω ESR are OPEN physical bounds; all measurements remain NOT RUN.

The [calculation JSON](M3_80M_CALCULATIONS.json) records these results and the explicit endurance assumptions. It is checked for staleness. Nominal protected-input thresholds are 5.810/11.070 V, rail OV 8.973 V and OC 1.251 A. The maximum calculated comparator input is 0.940 V versus a conservative 1.135 V ceiling; worst calculated TL431 cathode current is 2.10 mA. These calculations do not include a measured offset/tolerance/temperature qualification.

The Fox fault budget is below 98.4 mW with −1% resistor tolerance and a **qualified minimum 1 dB available-power loss**. It is not a 10 mW output calibration, a short-circuit reliability result or a field-range measurement. The 4S1P modeled runtime likewise does not pass endurance qualification.

## Preserved baseline checks

Run the existing checks without rewriting historical calculations:

```sh
python3 tools/m1_analysis.py --check
python3 tools/m1_costs.py --check
python3 tools/m2_rf_analysis.py --check
python3 tools/m2_system_costs.py --check
python3 tools/m2_checks.py
python3 tools/foxoring_costs.py --check
python3 tools/m2_80m_analysis.py --check
python3 tools/m2_power_architecture.py --check
```

All eight preserved checks passed with no errors. The repository documentation check covered **76 baseline-scope Markdown files, 487 local links and 73 traced baseline requirements**. M3 independently checks **18 cost baskets and 1,344 CSV rows**; the exact row count is also stored in its calculation JSON. The R1 documentation/hash script independently passed77 Markdown files,505 local links and30 hardware hashes, plus current revision/population/cost consistency. [Artifact hashes](M3_80M_ARTIFACT_HASHES.json) identify the current delivered hardware files. Root, driver/shaper, filters, low branch, key-tail, protection and power sheets were visually inspected after PDF export; annotations were moved away from the title block.

Existing accepted ADRs, proposed ADR-0010/0011, old cost/endurance calculations and source evidence are preserved. [M3 source log](M3_80M_SOURCES.md) records failed retrievals and exact stock gaps; passing local links does not establish current external stock or legal/RF compliance.
