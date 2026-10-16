# M5B-E1 single-board commissioning

2026-10-16. **All stages NOT_RUN. This procedure is preparation, not authorization to buy, assemble, energize or radiate.** After independent review and explicit approvals, assemble one complete board progressively. No separate PA coupons are needed. Use a screened bench, current-limited supplies and dummy loads; never inject unqualified faults from a Li-ion pack.

Required equipment: adjustable isolated current-limited supplies, DMM,≥100 MHz oscilloscope for control/envelope and suitable RF probe/envelope detector, frequency counter or spectrum analyzer, RF power/PEP measurement,50 Ω≥10 W dummy load, analyzer-rated attenuators, temperature logging, and preferably a VNA for initial matching. RF instruments must be protected against DC and power overload. Do not attach a normal scope probe's long ground lead to the PA drain or RF matching line.

## 0. Unpowered inspection

Confirm native/package revision and the BOM variant before assembly. Inspect PD G-left/D-right/source-ground, PHA1/3 RF order and2/4 ground, RNW separated6/7/8 contacts, ST D45H11/BD139 pinout, TL431 K/REF/A, diode/FET orientation and polarized reservoir. Check finished holes and keyed harness pin1. Use controlled paste/hotplate or reflow-oven assembly for the hidden PowerFLAT/WSON/RNW contacts; a soldering iron alone does not qualify these joints. Inspect center-pad solder with suitable magnification/X-ray if available; ordinary visual inspection cannot establish hidden void percentage.

Fit exactly one converter population, matching J302 shunt, R101 ID and pack-divider values. Training-only omits all NORMAL and converter components and fits the TRAIN_ONLY links/pulls. Check that no removed normal branch backpowers the training source. Record resistance/diode readings rather than accepting an arbitrary universal resistance threshold. There must be no hard supply short, no interconnect between NORMAL_RF/TRAIN_RF and no conductive connection from live pass/helper tabs to grounded sinks. Mount thermal supports before soldering stressed power leads.

## 1. Logic and source

Use3.3 V, initially100 mA limit; ARM/SLOT/KEY/PREPARE/PA_PREPARE low, MUTE_N low, battery input absent. Increase only to the documented150 mA logic budget after inspecting excess current. Verify reset, actual application progress, watchdog timeout, I²C SCL-low inhibit, invalid ARM context, captured path/profile and deliberate rearming. A fault while ARM remains high must not rearm automatically. Check both physical output enables inactive after reset/timeout/mute.

Release mute and PREPARE with ARM/SLOT low. Configure/read back a legal source frequency with outputs initially disabled. Confirm source waveform/frequency and current. Use144.500–144.900 MHz for the championship profile; broader training frequencies require the future controller's country/band validation. No independent frequency counter or production firmware is implemented by this PCB. The future controller must refuse unsupported settings and sequence unpowered3.3 V inputs to prevent backpower.

## 2. Power only; MMIC disconnected

Leave U501 absent and R952 open. Fit the selected converter/protection, regulators, reservoir and dummy loads. Start2S at6.5 V/0.1 A or4S at12.5 V/0.1 A, with controls off. Increase current limit only as required by measured load; after inspection and low-energy checks, permit up to3.5 A at the2S raw input or2 A at4S for loaded tests. The≤2 A electronic-load ceiling applies at the regulated rail, not to2S input current. Never bypass the local≈1.80 A rail trip. Confirm pack-voltage windows, wrong-pack inhibit and correct exclusive supply routing.6.0/12.0 V are below nominal RF UV cutoffs and should inhibit rather than be forced to transmit.

At PREPARE/PA_PREPARE, measure converter output, U950 input/output,5 V rail and isolation output. Full upstream rail should agree with9.021 V within calculated component/reference tolerance; reduced4S approximately7.510 V. No unexpected pulse may enable the PA. Test at pack minimum above cutoff, nominal and maximum with short monitored leads.

Attach a0–180 mA dummy load at **VDRV_RF/TP401**, ahead of open R952. Require normal MMIC-feed equivalent4.8–5.2 V, clean startup, adequate regulator headroom and discharge. Probe each regulator output and U305 enable/output simultaneously. Repeat power cycling and controller disappearance. Resolve excessive overshoot or dropout before fitting the MMIC.

For the defined regulator-fault tests, isolate the failed-regulator input/output using temporary wiring and a current-limited source; maximum fault16.8 V **at the tested device pin**, not merely at the bench supply display. Test each regulator-short condition separately, MMIC absent. Start fault injection with≤100 µs pulses,≤0.25 A source limit and≤1 pulse/s;at16.8 V the source-energy bound is0.42 mJ/pulse. Use the180 mA dummy load only after lower-current traces are understood. A continuous16.8 V/180 mA LDO drop could dissipate about2.1 W, so do not hold this indefinitely. Increase duration only after voltage/shutdown traces and regulator thermal limits justify it. U950's16 V recommended input is exceeded during the defined16.8 V fault, although its18 V absolute limit is not; bound duration/current and inspect afterward. The other regulator must protect the MMIC node. Require node≤5.7 V, correct clock/bias inhibit, shutdown and no automatic restart. Record actual detection/isolation time; do not assume20 µs. Test input hotplug/disconnect with bounded source impedance before any unrestricted pack use. If this test cannot be bounded safely, do not fit R952 or enable RF.

Use a dummy upstream load to verify the corrected approximately1.80 A current trip and latch, with electronic-load ceiling≤2 A at the regulated rail and appropriate raw-input limit (up to3.5 A for2S,2 A for4S after preceding checks). Check INA output near2.443 V at nominal trip. Verify UV/OV, open/short NTC and loss of3.3 V. A fuse is not the test's fast current limiter.

## 3. AM and thermal circuit without RF

Fit modulator and its insulated pass sink. Use a5.6 Ω≥25 W load at VPA, appropriately heatsunk. Configure PWM carrier/sine with bounded commands, initially low amplitude. Verify feedback sign, stable gain, no unexpected oscillation and no substantial PWM ripple (initial engineering target≤1% of carrier envelope). Initial full voltage envelope0.8/4.0/7.2 V and reduced0.444/2.222/4.0 V are starting points, not RF AM calibration.

Check no-tone carrier dissipation, helper current, crest dropout, inhibit and controlled fall. Grounding a failed-pass simulation must use a bounded fixture and reduced energy, not a raw pack. Verify hardware still withdraws clock, bias and driver permission. Require normal pass case≤60°C at defined worst ambient, NTC trip near its calculated65.85°C with measured tolerance/lag, and deliberate rearm after cooldown. Verify the bonded sensor and strain relief; an intact-wire detached sensor is not detected electrically.

## 4. Driver and one integrated RF alignment

Fit the source/driver only after Stage2 passes. Initially retain the10 dB π pad. Lift R650, temporarily fit R65149.9 Ω, and measure the DC-blocked MMIC output into a correctly rated50 Ω reference. Verify physical feed≥4.8 V and ≤5.2 V, stability and spectrum. Select6/8/10 dB pad from measured source/filter/MMIC gain, aiming approximately19 dBm maximum without unexplained compression. Require approximately3 dB P1dB backoff unless measured operation justifies another value. If the source cannot supply the required drive, record the deficit and stop normal-PA calibration; do not hide it by lowering the required ERP.

Remove R651 and refit R650. Fit the final, exact ST output network/filter and grounded thermal assembly. Connect normal SMA to50 Ω≥10 W load with protected measurement coupler/attenuator. Set gate bias and drain voltage to the conservative documented starting state; start at low drain voltage/current and low drive. Observe bias-only current and search for unwanted oscillations before increasing RF.

Align only the specified bounded input options: L63424/33/47 nH, C633DNP/22/27/33/39/47 pF and C631DNP/22/33/47/56 pF. Record the chosen values as the new assembly calibration. Do not change the ST output topology or silently replace the driver. Verify144.500/144.700/144.900 MHz and any permitted training-frequency limits claimed. Check load variation only at bounded reduced energy; no unconditional open/short survival claim exists.

## 5. Complete true-AM acceptance

Measure at the output connector, not just the PA supply. Record carrier, average RF, crest/trough, PEP, depth `(Vmax−Vmin)/(Vmax+Vmin)`, envelope distortion and sideband symmetry. Require70–80% RF depth, nominal75%, engineering RF-envelope THD≤5% (not an IARU rule), no clipping at crest/trough and no parasitic oscillation over the envelope. Tone frequency starts800 Hz and remains configurable; it is not a rulebook-mandated value.

Demonstrate the requested near1 W ERP capability using actual measured feed loss/antenna gain assumptions. At−1 dBd,1 W ERP/80% requires1.259 W connector carrier and4.079 W PEP. Calibrate a nominal≈0.9 W ERP setting only if the uncertainty budget establishes the upper bound≤1 W; independently calibrate≈0.30 W ERP with lower bound≥0.25 W. Record the actual gain/feeder uncertainty. A dummy-load power measurement alone does not establish ERP.

Check carrier stability better than50 ppm, scheduling/8–15 WPM behavior, carrier/tone edges, full/reduced profiles, all fitted supply ranges, current and temperature. Require the applicable national unwanted-emission limits; initial engineering screening is harmonics≥60 dBc suppression, but it does not supersede stricter local masks. Record analyzer noise floor and measurement bandwidth. Off-slot initial screen is≤−70 dBm at the connector or the documented instrument floor, whichever is measurable; this is a test threshold, not proof of literally zero radiated energy. Verify actual scheduling and source shutdown.

## 6. Training, faults and endurance

With normal PA/converter off, align the nominal1 µW carrier (−30 dBm),70–80%AM training branch at its separate MMCX into50 Ω; record output, AM depth and spurs; initial inhibited-output goal≤−90 dBm or documented analyzer floor. Measure compact-port leakage with normal output active, including controlled mute/reset/fault cases, and verify that the watt-level signal has no direct circuit path to it. Check training-only operation with normal components absent. Any excessive coupled power is a qualification failure requiring correction before antenna connection.

Repeat watchdog loss, I²C activity, controller reset, wrong path/profile, power fault, sensor fault and deliberate-rearm checks with RF monitored. Record PA/pass/helper temperatures and input power through a full worst-case duty cycle and continuous-beacon case. Conduct12 h full and24 h reduced battery tests at defined temperature/aging/cutoff and LoRa state. Model estimates are not substitutes. Record all instrument settings, component tuning populations, supply limits, uncertainty, temperatures and outcomes in a per-board acceptance sheet. Only then reproduce the qualified assembly for the fleet.
