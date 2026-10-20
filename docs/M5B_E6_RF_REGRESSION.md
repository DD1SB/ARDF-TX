# M5B-E6 regression of unchanged E5 sources

Executed 21 October 2026 with KiCad/pcbnew 10.0.6. **These are fresh E5 baseline replays; there is no revised E6 PCB.** All controller M6-L2, RF80, active RF2M native files and historical review data remain byte-identical to `256c64888b680f5152e92f035e2ea0676a83630a`. [Preservation inventory](../hardware/2m/review/M5B-E6/preserved-baseline.json), [replay data/logs](../hardware/2m/review/M5B-E6/).

The [replay wrapper](../tools/m5b_e6_baseline_replay.py) only runs in a disposable `/tmp` clone at that starting commit. It redirects output away from frozen E5 reviews and starts the preservation guard at the current public baseline, rather than the old pre-publication RF80 commit. Package/electrical/RF/DFM tests and thresholds are unchanged. Tracked native input hashes are checked after every replay. KiCad creates an ignored `.kicad_prl`; the first harness attempt incorrectly included that generated preference file in its input set. The correction restricts the hash set to tracked authoritative inputs, retaining the complete original failure log. No native geometry was changed.

| Fresh execution | Result |
| --- | --- |
| Native hierarchy/ERC | 0 errors, 0 warnings |
| Native DRC with refill/parity | 0 errors, **11 existing missing-courtyard warnings**, 0 unrouted, 0 parity |
| DRC exclusions | None; project configuration unchanged |
| Electrical logic | All 4,096 combinations and 39 state scenarios PASS |
| Native package/pad checks | 320 PASS |
| Existing electrical mutations | 19 historical +18 M5B additional rejected |
| Compact/source-joint mutations | 18 compact +16 source geometry +4 source thermal negatives |
| Controller connector | All 20 pins compared with native M6-L2 J5 and original netlist |
| RF geometry | Native matching parts/lines/source/ports unchanged; rigid E4R1 baseline comparison PASS |
| Ground connectivity | One anchored native filled-ground component |
| DC paths | Refined contact graph and conservative copper/via sensitivity PASS existing 0.35 V path budget |
| Standard JLCPCB geometry | PASS; 50,384 independent copper-pair tests; 11 DFM mutations rejected |
| E6 numerical host checks | 25 tests PASS; energy/periodicity/AM/convergence/native storage/fault-envelope tests |

The 11 courtyard warnings belong to inline RF copper/probes, as individually recorded in the baseline warning-disposition report. They were neither hidden nor changed to exclusions. Consequently **the requested E6 zero-warning gate has not passed**. This is a preserved baseline condition, not a newly introduced E6 CAD defect.

DFM minimum track 0.15 mm, via annulus 0.15 mm, component PTH annulus 0.275 mm, 724 holes. The existing 518 via preferred-margin exceptions remain listed: they satisfy the 0.15 mm design minimum but fall below the preferred 0.25 mm annulus. These are explicit local margins, not premium fabrication or DRC exclusions. Source vias remain open as specified; no filled/capped-via assumption is added.

The first source-assembly replay ran before its required freshly generated thermal-model dependency existed and failed with FileNotFoundError. It was rerun after the full thermal replay, without changing the test. The initial analytical reflection-energy test omitted instantaneous capacitor storage; the model already conserved it, and the test was corrected to include `V C dV/dt`. The supply ledger was also corrected to separate controller-provided 3.3 V/base-drive power from RF converter and shunt current; all affected thermal/fault calculations were rerun. Early development numerical failures and the final passing run are retained separately. Nonfatal pcbnew enum-property assertions and duplicate-image-handler diagnostics are visible in raw logs; the CLI CAD reports and Python assertions determine the recorded results.

NORMAL and TRAIN_ONLY population logic, branch isolation, controller pin mapping, package potentials Q501=S/GND, Q401=C/VPA and Q402=C/MOD_SINK remain unchanged. No new RF-sensitive length/width/placement changed: there is no E6 RF copper equivalence claim requiring extrapolation from ERC/DRC. Actual power, harmonic/spur spectrum, matching, AM quality, off-slot leakage, thermal behavior and field performance remain **NOT_RUN**. Mechanical/cutout/collision checks for the proposed E6 arrangement are **NOT_IMPLEMENTED**, not counted as regression PASS.
