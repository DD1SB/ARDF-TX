# M80-E1 first-article procedure and release gates

All physical tests below are **NOT RUN**. Five bare boards are justified for these measurements; the work does not assume impossible pre-manufacture RF results. The native CAD/firmware and supplied calculations are engineering inputs, not a certificate for populated equipment. Record serial number, physical resistor population, firmware/hash, configuration, instruments, calibration dates, cell voltage, temperature, antenna fixture and measurement uncertainty for every result.

Use one current-limited bench article first, preferably FOX10's 560 Ω ballasts. Do not initially assemble twelve transmitters. Use a shielded bench setup, no antenna, a noninductive 50 Ω load, an appropriate attenuator/coupler, oscilloscope, calibrated RF power measurement/spectrum analyzer and frequency counter. A DC voltmeter alone cannot establish RF power, output skew or harmonic suppression. Protected cells, external charging and verified harness polarity are required for eventual battery tests.

## 1. Assemble, program and verify the AVR

Inspect the bare outline/drills, verify pin-1 positions against the assembly PDF, inspect QFN/MSOP joints and grounded exposed pads. Confirm no shorts on BAT/V3/V5/VPA. Keep the RF stage unpopulated or physically inhibited for initial logic tests. Verify UPDI signature, target 3 V level, 20 MHz oscillator selection, retained UPDI and 2.9 V BOD settings before writing the universal HEX. Read back/verify flash. Blank or corrupt EEPROM must reject ARM; writing a valid settings record and reading it back must succeed. Reset/power cycle must leave RF, clock and boost off even with valid stored settings. Test incomplete writes and bad CRC without transmitting. Do not substitute a raw fuse byte from another AVR family.

## 2. Verify the battery and low-voltage circuitry

With current limiting, sweep the correct-polarity input from 4.2 down to 3.0 V. Confirm 3.0 V logic regulation in the useful 3.2–4.2 V range, battery ADC calibration, boost off/disconnect, no reverse-polarity conduction and safe control pull states while reset is asserted. Use a limited source for reverse-polarity testing, not an unprotected cell. Confirm below-3.2 V shutdown within approximately one second, no spontaneous re-arm on recovery, and at least 3.4 V required to ARM. Verify BOD and stalled-RTC watchdog reset both inhibit RF.

Command scheduled preparation with RF still inhibited. Measure 5 V rail setpoint/ripple, boost settling and startup overshoot at 3.2/3.7/4.2 V and with realistic cell resistance. Firmware expects 4.6–5.35 V after 12 ms. Confirm effective C4 capacitance/loop stability at bias and temperature, L1 current margin and true-disconnect behavior. Reject oscillation, excess overshoot or unintended battery-through conduction. Observe VCLK discharge and all unpowered-domain input voltages/clamp current.

## 3. Verify carrier and timebase

Check Si5351 crystal startup, PLL lock, I²C success/failure timeout and source frequency at every configured channel. Measure correction over the intended temperature range, store carrier_ppb and confirm total frequency error better than 50 ppm; verify the upper channel setting against the specified 3.600 MHz limit. Record spurs, duty cycle and rise/fall at CLK0 **and at the shared HCT input after R16**. Check that disabling outputs commands low, that retuning always holds OE inhibited/VPA off, and that loss of I²C/PLL/startup never keys the PA. Confirm the ±10 ppm initial / ±20 ppm temperature reference specification is adequate with load/aging error included; do not infer this from divider arithmetic.

Measure the RTC rate independently, trim the 18 pF load values if needed and store timing_ppm. For a twelve-hour session, demonstrate total residual ≤20 ppm over the expected operating range or specify a shorter resynchronization interval. Initial ±20 ppm alone excludes temperature/load error. Verify common-SYNC skew with all twelve fixture loads, deployment delay and run end. The 128 Hz sampling granularity is 7.8125 ms.

## 4. Verify output into the dummy load

Fit the bench network: L30–34/C30 DNP, R50–54 zero-ohm. Connect exactly one 50 Ω load at ANT/CP or a de-embedded TP7 fixture. Start with the FOX10 ballasts and reduced/current-limited conditions. Measure carrier power and RF waveform, individual ballast voltage/current, VPA and HCT case temperature. Check that all eight outputs switch with acceptable phase/duty behavior and no sustained opposing drive. Account for local bypass-capacitor pulse current; a slow supply-current average misses output contention.

Only move toward the MINI50 population after reviewing pulse/package-current evidence and the manufacturer's limits. The calculated four-against-four bound with 100 Ω is 105 mA versus a 70 mA DC package rating; pulse behavior is unspecified. Manufacturer clarification or a conservative circuit/population revision may be necessary. Reject a population that depends on unqualified current stress. No five-board GO grants a populated fleet release.

Select the eight ballast values consistently to obtain approximately 50 mW MINI50 or calibrated 10 mW FOX10 at the reference plane. Record uncertainty; for FOX10 use a suitable margin so calibration uncertainty cannot conceal excess conducted power. Profile settings must match the physical population label. No official Sprint-power assertion is allowed for MINI50.

## 5. Sweep supply and loading

At 3.2/3.7/4.2 V, each operating frequency and realistic temperature, record output power, rail regulation, efficiency and gate/coil temperatures. Repeat with 25, 50, 100, 150 and 200 Ω reference loads and controlled reactive/open-load tests under current limiting. Include cold start, warm start, reset and battery sag. A matched load is not proof of acceptable operation into every antenna. Compare measured filter/input impedances with the model and update the manifest/analysis for any selected component changes before release.

## 6. Measure currents and endurance

Measure true off/reset, invalid-config, fixture-idle, synchronized standby, prepared/unkeyed, mark, space and complete-cycle currents. Capture boost quiescent leakage, synthesizer current and startup charge. Integrate complete slow/fast, S, MO and FOX10 sessions, rather than multiplying a peak-current reading. Recalculate runtime from measured energy and usable cell capacity to the 3.2 V cutoff, including temperature, protection cutoff and cell resistance. Demonstrate at least twelve useful hours for each training role with its selected battery; investigate twenty-four hours for FOX10 with 1,200–1,500 mAh. Leave calculated runtimes labeled as such until the discharge runs finish.

## 7. Measure harmonics and key clicks

With a calibrated attenuator and checked analyzer overload floor, record carrier, second/third and higher harmonics, synthesizer spurs, converter components and wideband noise. Repeat at all carrier/supply/load cases. Use at least 40 dB harmonic suppression as an engineering prototype screening goal, then assess the applicable final emission limits separately. This screening figure is not a regulatory certification. Compare near-field/conducted coupling against the ideal LPF model; strong suppression in the model can be defeated by PCB coupling.

Measure RF amplitude rise/fall, overshoot and residual carrier in spaces, slot boundaries, startup, reset, retuning and forced faults. The nominal gate RC is not an RF rise-time measurement. Verify smooth millisecond transitions with no objectionable key clicks and no HCT instability while the rail passes through its unqualified low-voltage region. Adjust R/C values or revise envelope topology if needed. Confirm the 15.625 ms firmware tail is adequate under worst-case loading and safe fault shutdown remains prompt.

## 8. Tune antenna fixtures

First characterize the original-style external 100 Ω + series 33 pF artificial antenna with a suitably rated capacitor (at least 100 V C0G) and known parasitics. Measure impedance, coil Q/ESR, loading voltage and delivered resistance power; compare available loading combinations and choose values, not merely the highest field reading. Repeat with defined 6–9 m wire/counterpoise installations. Record the exact lengths/heights/soil and transformer/loading population. Check optional coil voltage suitability; manufacturer current ratings do not define winding voltage limits. Keep bypass/coil mutual exclusivity and C30/L30 pairing correct.

Use a **separate** short-antenna Foxoring population, initially around 30 cm, with loading bypassed and optional R54 coupling capacitor selected experimentally. Finalize its exact BOM only after field tuning. Do not claim the long-wire loading bank is an optimal short-antenna match. A mismatch is part of the Foxoring installation, not a conducted-power calibration load.

## 9. Verify the twelve-transmitter schedule

Use ten field units plus S and MO training beacons, one common SYNC and independent stored roles/frequencies. Log RF envelopes/frequency identifiers simultaneously at cycle start, after deployment, and near the end of a twelve-hour run. Verify slow/fast MOE/MOI/MOS/MOH/MO5 order, exact nominal 12-second windows, one-second guards, complete IDs, 10/15 WPM, continuous repeated S/MO IDs, configured delays and scheduled shutdown. Check both group frequencies and independent beacon frequencies, minimum spacing and no same-group keyed overlap within the qualified drift budget. Repeat resets, invalid data, low battery and failed clock preparation. A reset unit must stay off, not rejoin by guessing epoch.

## 10. Conduct Foxoring range measurements

After conducted calibration and safe bench acceptance, test each final short-antenna unit using the intended receiver and a documented repeatable detection criterion. Record receiver gain/bandwidth/antenna, background noise, geography, weather, antenna mounting, battery state and orientations. Check audibility at the nominal position and at 30 m; verify absence of audibility at 250 m around the installation, including stronger propagation directions. Repeat at representative fresh/end-of-run states and relevant site conditions. Adjust antenna/coupling and repeat both distances; changing output alone does not prove the required range. Use a separate normal-power finish beacon with proper frequency separation. Preserve logs for each unit and installation; no field result is assumed transferable to another antenna/site.

## Release record

`review/physical-results.csv` deliberately contains NOT_RUN results. Complete it with raw measurements and uncertainty, revise cost/power/runtime models from evidence and obtain independent engineering review before a populated fleet release. Any design change requires rerunning ERC/DRC/parity/DFM, updating native CAD/BOM/firmware and regenerating outputs. The current decision is **GO five bare boards / HOLD populated fleet and compliance claims**. There has been no hardware order or activation in this task.
