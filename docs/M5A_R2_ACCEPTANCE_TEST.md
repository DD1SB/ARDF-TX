# M5A-R2 single integrated-board acceptance procedure

2026-10-15. **Procedure only; every physical result NOT_RUN. The integrated R2 board does not yet exist.** This is the intended end-of-build process after the sourcing gate, electrical design and independent PCB review are complete. It does not authorize buying, assembly, power-up or RF transmission. No separate PA coupon or repeated transistor-development program is proposed.

An experienced amateur-radio technician can commission the first complete board using a shielded50 Ω bench setup. Subsequent units use the same recorded settings, fixtures and shortened acceptance record; they still need individual bias/power/modulation checks. Do not substitute a handful of waveform screenshots for complete acceptance, or price fictitious time savings before a timed build exists.

## Required shared equipment

- Adjustable, current-limited laboratory supply with overvoltage protection and independent rail disconnect; no unrestricted Li-ion pack for initial power-up.
- Calibrated50 Ω dummy load≥20 W at144 MHz, suitable attenuator/coupler with a known frequency response, and protection for the analyzer/power sensor.
- RF power sensor/meter capable of carrier, mean and PEP measurements, or calibrated equivalent using a sampler/envelope measurement.
- Spectrum analyzer covering the fundamental and relevant harmonics; frequency/reference uncertainty sufficient for the50 ppm check.
- Oscilloscope with a calibrated RF envelope sampler/detector and audio/control access; current logging and case-temperature contact probe. A VNA is useful for first-board LPF/antenna checks, not for retuning an internally matched PA on each unit.

Record instrument model, calibration, attenuator/cable loss, dummy-load VSWR, ambient temperature, module marking/lot, firmware/configuration identifier and uncertainty. Power values are connector-plane unless explicitly stated otherwise. Never connect the transmitter directly to an unprotected analyzer.

## One staged commissioning record

| Step | Action | Objective gate |
| --- | --- | --- |
| 1 | Unpowered identity, footprint/pin/flange, polarity, shorts and DNP inspection | Exact selected suffix matches approved drawing; no reversed leads; normal/training ports have no conductive RF bridge; heatsink/flange installed before leads soldered |
| 2 |3.3 V-only supply, bounded initially100 mA; adjust to the finalized design budget if required | No abnormal current/backpower; all controls/default rails off; reset/watchdog/source inhibit work; no RF permission without fresh valid ARM |
| 3 | Main converter, module gate grounded, current-limited dummy rail load | Rail min/max/ripple/startup and deliberate shutdown within final component ratings at battery min/nominal/max; OV/UV/inrush response passes approved limits |
| 4 | Module gate zero, RF disabled, initially≤50 mA laboratory current limit | No excessive leakage/heating; no unexpected RF; increase limit only after the preceding check passes |
| 5 | Adjust VGG from zero with RF still absent | Set approved quiescent current, bounded VGG and stable current/temperature; if necessary Iq invalidates the endurance/cooling budget, reject rather than continue at an arbitrary high bias |
| 6 | Enable source/AM at low RF level into dummy load; increase bounded current limit gradually | Correct frequency, stable carrier, source drive below the approved operating ceiling and always below absolute input limit; no out-of-band oscillation |
| 7 | Calibrate normal/reduced carrier levels | Use actual feeder/antenna gain and uncertainty; actual ERP intervals remain within0.25–1 W. Initial examples0.90/0.30 ERP are not automatic compliance values |
| 8 | Apply nominal75% sine and check80% boundary | `m=(Vmax−Vmin)/(Vmax+Vmin)` at actual RF output is70–80%, with uncertainty included; no trough clipping/flat crest; engineering envelope THD≤5%; record sideband symmetry and AM-to-PM observations |
| 9 | Measure carrier/mean/PEP and capability reserve | At1 ERP capability basis/−1 dBd assumption:1.258925 W carrier,4.078918 W PEP at80%; demonstrate5.135054 W connector crest capability with acceptable envelope linearity as engineering reserve. Do not operate above legal ERP to radiate this test; use the terminated bench setup only |
| 10 | Frequency/temperature/supply sweep | Championship144.500–144.900 MHz; better than50 ppm including uncertainty over approved conditions; output and70–80% modulation maintained at every approved supply/profile endpoint |
| 11 | Spectrum and keyed-tone transitions | Measure harmonics, spurs, PWM products and occupied envelope; pass the selected country's limits, plus the approved engineering mask. No universal national mask is invented here. Any unconfigured legal mask blocks radiated release |
| 12 | Schedule/inhibit/reset/fault/rearm test | No identifiable RF outside SLOT above documented instrument floor; measure floor and residual power. Reset, missing progress, bus activity, mute, faults and conflicting/path changes cannot leave either output active; held ARM must not automatically rearm |
| 13 | Training path, main module off | Calibrated nominal1 µW carrier (approved range initially1–10 µW), correct AM/timing, own filtered connector; no main converter/bias needed; normal activation cannot exceed the training port's approved fault/measurement limit |
| 14 | Hot run: full/reduced and separately continuous beacon | Case target≤60°C under the approved ambient/cooling conditions; local trip safely precedes unsafe case/junction current/temperature; sensor-open/short causes inhibit. Log source/buck/module power and hot RF/AM drift |
| 15 | Bounded fault injection | Independently exercise voltage/current/thermal shutdown and controller loss using current-limited fixtures; no uncontrolled4S applied to module. Record actual delay and stored-energy overshoot, not just logic level |
| 16 | Battery/endurance acceptance | Selected pack keeps calibrated RF, AM, frequency and timing valid for≥12 h full/≥24 h reduced, with stated cells/age/temp/LoRa. Controller survival after RF sag is a failure. Test continuous beacons separately |

The manufacturer's mismatch/stability results apply to its specified nonlinear conditions. They do not authorize arbitrary full-power open/short tests. First approve a bounded mismatch procedure/current/thermal limit; preserve stability and safe shutdown in the actual antenna/load envelope.

The [IARU2025 Part B](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), Appendix1 T2.4/T2.8, remains the championship reference: A2A,70–80%,144.500–144.900 MHz, better-than50 ppm, simultaneous-transmitter separation>200 kHz,0.25–1 W ERP,8–15 WPM, horizontal antenna2–3 m. Configure frequency permissions independently for training and local law. This is not transmitter authorization.

Installed antenna gain/loss/pattern and actual ERP require a separate recorded installation measurement within this acceptance process. A50 Ω load alone proves neither horizontal omnidirectionality nor ERP. No RF/thermal/safety/endurance result is presently a PASS.
