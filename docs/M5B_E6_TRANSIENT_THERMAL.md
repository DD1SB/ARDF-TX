# M5B-E6 coupled transient thermal analysis

**HOLD before CAD.** This is a reproducible RC sensitivity analysis, not measured transient thermal impedance or physical thermal qualification. [Power assumptions](M5B_E6_THERMAL_POWER_AUDIT.md), [numerical results](../hardware/2m/review/M5B-E6/transient-results.json), [curves](../hardware/2m/review/M5B-E6/transient-responses.pdf), [fault sensitivity](../hardware/2m/review/M5B-E6/native-fault-envelope.json) and [closure calculation](../hardware/2m/review/M5B-E6/thermal-path-closure.json) are separate evidence.

## Network and numerical method

The [12-node source](../tools/m5b_e6_thermal.py) contains PA junction, package source, top PCB source copper, bottom PCB copper, aluminum bar, D45H11 junction/case, BD139 junction/case, shared plate, fins and pass-device NTC. Junction-to-case/source resistances are 3/2.5/10 K/W. Source solder/contact is 0.25–1.5 K/W; the conservative scenario adds the previous 1 K/W mesh/joint allowance. Pass case-to-plate is 0.6–2 K/W; helper 1.2–2 K/W. Bar-to-plate is 0.25–0.7 K/W. These interface values are engineering scenarios requiring actual pressure/flatness control.

The unchanged native 98-via source structure supplies the finite-volume DC source-to-bar resistance. That path is split around local top/bottom copper capacities; split fractions 0.2/0.6/0.9 are tested. This Cauer allocation is approximate, not a fitted manufacturer Zth curve. Manufacturer transient Zth curves were not established for these exact parts. Assumed PA die/source capacities are 0.001/0.025 J/K, D45H11 die/case 0.003/0.5, and BD139 0.001/0.2, swept ×0.1/×1/×3. These are deliberately bounded scenarios, not manufacturer facts or proven mathematical extremes for every possible package.

Known copper and via-barrel storage is calculated from the actual native 98-via array, drill diameters, 10–18 µm wall and 30–35 µm foil assumptions, using 8960 kg/m³ and 385 J/kgK. It is **never removed by the package-capacitance sweep**. Neighboring vias outside the canonical array receive no credit. Local FR4 storage remains an assumption. Aluminum uses 900 J/kgK: 214 g cooler and approximately 11.05 g source bar. A hypothetical 100/400 g mass sweep changes pulse accumulation; it cannot remove the local junction-to-plate resistance. No heat path through the plastic package top, solder-filled vias, premium laminate or a fan is credited.

The solver diagonalizes the passive conductance/capacitance system, propagates each constant-power interval exactly, and solves the periodic fixed point. Sampling includes submillisecond local edges and slower plate behavior; independent matrix-exponential, energy balance, periodic residual, time-grid and 128/256-phase AM checks are included. The 800 Hz ripple is calculated independently in the frequency domain and added conservatively to the cycle maximum. At 1 W ERP it adds approximately 0.387°C with nominal local capacities or 3.354°C with ×0.1 capacities. The zero-die-storage RθJC comparison gives approximately 6.6–6.7°C positive ripple. A sink-only 200 g lump cannot provide this information.

## Contest profiles

All five actual codes MOE/MOI/MOS/MOH/MO5 are modeled with PARIS timing. Classic uses 60/300 s, Sprint 12/60 s. Slow 12 WPM / fast 20 WPM are explicit analysis settings, not claims about completed target firmware or a mandatory event rule. Representative DD1SB identification is included in allocated slots. MO beacon repeats continuously. Gaps retain carrier. Clipping a final mark at a slot edge conservatively preserves the allocated slot duration.

The table shows BUCK4S, 40°C ambient, assumed 5.5 K/W sideways/restricted cooler, conservative TSP1600 interface, nominal package capacities. PA figures are cycle-averaged-AM maxima **before** the separately reported ripple. First/periodic means first cold-start slot / repeated periodic peak.

| ERP | Classic PA first / periodic | Classic pass case | Sprint slow PA first / periodic | Sprint pass case | Continuous MO PA / pass case |
| --- | --- | --- | --- | --- | --- |
| 0.25 W | 56.08 / 59.14°C | 46.77°C | 54.91 / 58.42°C | 46.35°C | 72.98 / 60.54°C |
| 0.30 W | 59.29 / 62.87°C | 48.02°C | 57.88 / 62.01°C | 47.52°C | 79.17 / 64.22°C |
| 0.50 W | 71.17 / 75.58°C | 49.59°C | 69.34 / 74.42°C | 48.97°C | 95.66 / 69.54°C |
| 1.00 W | 80.65 / 86.04°C | 51.63°C | 78.36 / 84.57°C | 50.87°C | 110.63 / 76.05°C |

Rows use MO5 for allocated slots; all code results, BOOST2S, case temperatures, minima, plate/fin/sensor temperatures and recovery are in the JSON/CSV. At 1 W Classic the PA source case peaks around 80.45°C, helper case 47.60°C and plate 47.41°C. Sprint fast PA peaks 84.51°C. These are plausible nominal planning results, not a qualified operating envelope. The repeated-cycle PA minimum and all other minima are retained numerically. After shutdown at Classic's hottest PA sample, PA estimates are 57.66°C at 1 s, 48.23°C at 5 s, 46.76°C at 60 s and 45.69°C at 240 s; slow plate recovery remains visible.

## Continuous beacon and outdoor limits

At 40°C, the catalogue-upright 2.2 K/W comparator predicts pass cases 49.79/53.97/56.99°C for 0.25/0.5/1 W ERP. At assumed 4 K/W horizontal cooling they become 55.66/62.46/67.38°C. At 5.5 K/W even 0.25 W slightly exceeds the unchanged 60°C case criterion. Low-power finish use is a legitimate option, but neither field coverage nor start-area audibility is established. No silent reduction of the required 1 W capability is made.

The model includes 25/40°C plus 45/55°C adverse ambient sensitivity, 2.2/4/5.5/8/12 K/W orientation/obstruction scenarios, 100% PCB-heat coupling and supply +3%. Apart from the catalogue comparator these convection resistances are assumptions, not measured deratings. Black-surface solar absorption at 800 W/m², 0.0165 m² projected area and absorptivity 0.8 is 10.56 W. A 10 W added-plate sensitivity plus continuous carrier violates the pass operating criterion before the lagged sensor trips. Shade and a ventilated raised guard are required concepts; they earn no invented thermal credit.

Accessible guard target ≤50°C, stop boundary 55°C, is a conservative proposed field-use criterion below the existing semiconductor case restrictions. It must be measured independently, including sunlight. It is not an ignition threshold or a fire-safe claim. Fin/leaf contact is prohibited; provide ≥15 mm clearance from vegetation/soil and unobstructed paths in any permitted orientation. A vertical-only catalogue rating is insufficient for ordinary field release. Beacon operation requires a separately established power/installation envelope; severe obstruction and solar-heated confinement are not accepted.

## Local PA fault closure

The native TPS3431SDRBR/CWD 10 kΩ selection gives a 170–230 ms watchdog interval. Loss of progress withdraws permission; a healthy application can continue progress during an undetected RF mismatch. The NTC is on Q401, not the PA. Sensor time constants 1/5/15 s and AF held-crest interruption are evaluated. Timing and trip propagation remain physically NOT_RUN. The old independent 4/4.24/1.1 W stresses are retained separately and do not decide the normal power ledger.

At 40% assumed carrier efficiency, 1 W ERP calibration, full RF absorption, 40°C and Classic MO5, the energy-consistent load has 1.736 A peak regulated current, PA 4.825 W and pass 3.683 W mean tone heat. With a better source-sheet contact allowance giving 11.847 K/W source-to-bar, the calculated PA peak including AM is **133.79°C**, pass case **56.90°C**, NTC **56.44°C**. Changing local capacity ×0.1..3 and DC-path allocation 0.2..0.9 gives approximately 130.63–144.64°C; none establishes the 125°C ceiling. The all-tolerance current trip may interrupt some units; it cannot be assumed to protect every one of these points.

This sensitivity is not proof that an actual antenna fault retains exactly that current or deposits all RF in the die. It establishes an unresolved loss/protection bound. At the nominal 50% efficiency the better interface gives approximately 114.86°C in the same full-absorption scenario; this difference must not be hidden. The former E5 grease path at its conservative boundary still gives approximately 128.98°C at 40% efficiency. The initial TSP1600 sheet is worse. A favorable 6 K/W source path passes this ceiling sensitivity, but that is not the qualified conservative standard-process assembly path.

For this specific sensitivity, required source-to-bar resistance is ≤9.888 K/W at nominal capacities or ≤7.698 K/W for fast capacities to meet 125°C; the 110°C target needs ≤6.571/4.507 K/W respectively. Those are conditional model requirements, not manufacturer specifications. Larger sink mass cannot remove this source bottleneck. A credible RF-loss/current bound, reproducible local thermal path/transient bound, or separately justified fast PA-fault interruption is needed before CAD release. **The HOLD is this pre-manufacturing analytical closure gap, not the mere absence of Gate H measurements.**
