# M4A — qualification and small-fleet production test

Date: **2026-10-15**. **Plan only: every physical result NOT_RUN.** No assembly, power-up, RF operation or release is authorized. The initial practical experiment is one staged E2 population; compact V1 remains a production-intent candidate until reference and compact hardware have passed separately.

## Shared fixture and instruments

Use one reusable controller/pulse/I²C fixture connected through J101, current-limited isolated3.3V and0–18V laboratory supplies with independent limits, calibrated DMM/current measurement, rated normal≥10W50Ω dummy load, low-power50Ω Fox load/adapter, RF power meter resolving10mW, counter/reference, spectrum analyzer with calibrated attenuation/DC block and verified dynamic range, oscilloscope/appropriate differential or≤1pF active probes, LCR/VNA and insulated thermocouples. Asynchronous reset evidence needs the retained≥500MHz/low-capacitance method. No extra processor, RF detector or expensive measurement connector is fitted to every module to replace shared equipment.

The source has no module firmware/programming processor. Configuration/provisioning uses the common ESP32 controller and I²C; record source calibration, allowed profile/frequency/PA power settings per module serial number. RF-module ID/calibration storage policy on the controller remains a system integration item, not a new RF EEPROM/DAC.

Retained14pads provide rails/clocks and essential status; RF measurements use J401/J502. Detailed qualification accesses SOIC leads, resistor/capacitor pads and the IRF610 drain with suitable probes, rather than restoring74laboratory pads. Record probe loading. Normal test-contact fixtures must not short an exposed drain/tab or mate the compact antenna to the watt port.

## First-article gates

1. **Reference E2 inspection/bring-up:** receive five bare boards only after A1 approval; inspect holes/annular rings/pin1/package orientations before any assembly. Separately authorize Stage1 procurement, then bounded Stage1 power. Use exact E2 Q403/U311 corrections and source archive. Every later population/power/RF permission remains separate.
2. **Power/logic before RF:** establish reference startup/thresholds, heartbeat edge witness, watchdog≤250ms, quiet holdoff≥1.5ms, real clear/recovery widths and no false permission/rearm. Apply defined bounded input/fault surrogates with driver/final absent; require TPS22810 limits, **≤20µs isolation** and **VDRV≤12.6V including uncertainty**. Do not call the20µs simulation a result.
3. **Driver/shaper before PA:** only after passing faults, fit driver and dummy gate/shaper loads. Verify inhibit, gate voltage/ringing,3–8ms edge candidate, key-tail/fault priority and BD140 hot SOA. Then separately authorize normalRF activation at reduced energy and rated dummy load.
4. **Reference normal/Fox qualification:** low/mid/high3.510–3.600MHz,12/14.4/16.8V, selected thermal corners;3.0–3.3W full target,1.10–1.30W extended with uncertainty≥1W, separately calibrated0.75–0.95W Sprint within0.3–1W. Fox9–11mW into reference50Ω. Targets are not measured achievements or new IARU minima.
5. **Compact first article:** repeat **all layout-dependent power/reset/driver gates before its driver/PA population**, not only a quick RF comparison. Measure compact-vs-E2 gate/drain/supply waveforms, CW/click spectrum, efficiency, hot SOA, current-trip behavior, near-field/common-ground coupling and normal→Fox leakage. Matching netlists never waive these tests.
6. **Release sample/endurance/antenna:** retained independent-build sample requirement, not one lucky transmitter; normal and Fox accessory tuning/field checks; defined12h full/24h reduced profiles on selected protected packs; continuous beacons separate. Source/no-LoRa operation and simultaneous LoRa/RF immunity require system-level qualification with the unchanged controller later.

Normal RF initial tests begin at12V lab input/lowest rail,≤200mA and≤1%marks; step current only after recorded passes, up to0.8A for bounded short tests subject to R350/pulse/thermal limits. Input transient envelope and failed-buck injection follow [E2 power restrictions](M3B_E2_POWER_PROTECTION.md). No unrestricted4S pack, destructive battery fault,24/28V whole-board test or unqualified radiation.

## Objective RF/safety records

Retain project harmonics/spurs≤−50dBc with adequate analyzer floor;3–8ms RF rise/fall,≤10%overshoot and retained±20kHz click method; measured off-slot search aim≤−70dBm at stated instrument settings. Record actual national requirements separately from IARU competition rules. Initial VDS gate≤100V and VGS target≤12V are conservative project limits, not proof from200V/±20V transistor absolute ratings. Initial full/extended stage efficiency targets≥50%/≥40% require reassessment if unmet, never a fabricated endurance pass.

Thermal records include IRF610/BD140/buck/driver/inductor/R350 and junction/SOA estimation with real cooling path. Retained initial25°C-ambient case≤70°C/junction estimate≤110°C and50°C hot testing remain. Electrical NTC open/short and physical detached-sensor/bond tests are distinct. Test initial2:1 then retained3:1VSWR phase sweeps at bounded power; open/short only if reviewed SOA/current/voltage evidence permits it.

Both paths must fail off at startup/reset, heartbeat loss, bus activity/stuck-low, invalid path/profile, UV/OV/OC/hot/sensor faults and controller disappearance. Clearing a fault with ARM high must not rearm; KEY high at ARM rejected; path/profile transfer requires deliberate disarm/rearm. Physical rail and RF behavior must match, not merely a FAULT_N indication.

At maximum normal setting require compact-port leakage **≤66µW**, roughly47dB isolation at3.3W, including key/fault/retune transients. No watt-PA injection into the compact accessory. Test its retained100mW fault-withstand with a bounded independent source. Nominal10mW reference-load calibration is independent of the compact≈30cm radiator/return/loading and reproducible30m-audible/250m-not-audible field evaluation; record receivers/sensitivity, ground, weather, orientation and repeated placements.

## Every-unit routine after qualification

Inspect assembly/lead forming/identity/continuity and full/Fox variant links. Use shared fixture to check idle current, source frequency/error, each permitted profile/output calibration and spectrum/edge sample, heartbeat/mute/bus/reset/guard withdrawal, held-ARM recovery prohibition and compact-port leakage. Verify current/thermal sensor operation with bounded surrogates; do not damage each unit by repeating destructive-fault experiments. Full boards additionally verify normal supply/calibration/thermal soak; Fox boards demonstrate no watt dependency on protected2S/controller3.3V.

Use a common fixture and test script later, not production firmware implementation in M4A. Record board revision/serial, actual MPN/lot/values/windings/photos, fixture/software versions, calibration uncertainty, supply/current/duty, ambient/cases and raw traces. Store **PASS/FAIL/NOT_RUN** with objective bounds and failure notes. Small-fleet calibration labor estimates are unmeasured; initial field/thermal/endurance engineering is separate. No final production release until all ten user-specified physical/sourcing/review/release gates and explicit user approval are complete.
