# M5B-E6R1 — Q501 protection closure

**HOLD: no defensible installed junction-to-sensor threshold/delay window is established.** Carrier keying lowers nominal average heat but does not remove a local source-joint fault, unexpected PA loss or a stuck MARK. A larger sink does not resolve this constraint.

The [ST PD54008L-E datasheet](https://www.st.com/resource/en/datasheet/pd54008l-e.pdf) gives the actual PowerFLAT 5 ×5 package and steady junction/source thermal data. The source solder and native copper/98 ordinary plated vias carry heat to the bar. No manufacturer transient Zth or installed sensor transfer function was established for this assembly. Its 500 MHz/7.5 V example does not guarantee efficiency at our 144 MHz, AM envelope and lower centre drain voltage. The package, local copper, solder and interface remain separate thermal elements.

| Cause | Treatment / consequence |
| --- | --- |
| Higher PA dissipation | eta 40% and same-DC full RF absorption are separate energy-conserving sensitivities |
| Source solder degradation | Vary package-source→PCB joint 1/5/10 K/W without removing known copper capacity |
| Via/copper path | Retain E6 finite-volume resistance and ordinary plating; no solder-fill credit |
| Poor bar/TIM pressure | Compare conservative and poor-contact paths, independently of solder fault |
| Shared cooler hot | Warm continuous-MO initial state and restricted convection retained |
| Sensor location/coupling | Measurement-only observer on source copper, with independently assumed lag; no fictitious cooling path |
| Delay/threshold | Sweep 10 ms–1 s installed lag, 80/87°C trip budgets, 1 ms actuation budget |
| Native monitored signals | Q401 NTC/current/watchdog remain necessary but do not measure Q501 junction |

The original 133.79°C counterexample is freshly [reproduced](../hardware/2m/review/M5B-E6R1/E6-failure-reproduction.json). Current 1.736 A and pass NTC 56.44°C remain below nominal thresholds. An application can keep WDI progressing during an unobserved PA fault. The 170–230 ms watchdog is therefore not credited as a universal PA thermal interrupt.

The exact candidate is RT970 **Murata NCP15XH103F03RC**, 0402, 10 kΩ ±1%, B25/50 3380 K ±1%, B25/85 typically 3434 K. A possible source-ground-wing target is F.Cu (92.0,51.4) mm near Q501. This is a location proposal, not approved routed geometry. A short electrically isolated sense pad and thermally controlled bond are required. It is a source-region sensor, never a junction-temperature measurement. [Murata's primary NCP15 table](https://www.murata.com/-/media/webrenewal/products/thermistor/ntc/ncp/ncp15.ashx?la=en) specifies typical dissipation constants of 1.0 mW/K free-air and 2.5 mW/K on its test board. **Those numbers are not time constants.** They establish no 10/50/100 ms installed response guarantee.

Candidate analog interface: 33 kΩ pull-up to 3.3 V, NTC to GND, TLV7034PWR hot/window comparisons. Hot reference is 191 kΩ/10 kΩ (0.16418 V), nominal beta-model trip **78.62°C**; cold/open reference 22.1 kΩ/191 kΩ (2.95777 V). Comparator offset ±8 mV and maximum 25 mV hysteresis are included in the explicit temperature scenarios, along with sensor resistance/beta. Calculated hot corners are 73.30–85.24°C, but beta-curve and reference tolerances do not establish a guaranteed assembly bound. **87°C is a sensitivity budget, not a qualified threshold.** No existing safety threshold is raised.

Healthy-operation checks are also necessary. At 8 WPM/40°C, conservative network, a 50 ms source-region observer reaches about **81.56°C** during valid full-power MO, above the candidate nominal threshold. Fast protection therefore risks nuisance inhibition; a slow sensor reduces that reading but weakens fault response. The proposal does not yet meet simultaneous availability and safety requirements. [Healthy headroom and all 288 fault cases](../hardware/2m/review/M5B-E6R1/sensor-fault-results.json) preserve that conflict.

Representative warm-start stuck-MARK results, source-to-bar 11.847 K/W, fast local-capacity scenario ×0.1, 87°C sensor threshold, 1 ms actuation budget:

| Source joint K/W | Observer lag | Trip / completed interruption | Estimated upper PA junction |
| --- | --- | --- | ---: |
| 1 | 10 ms | 42.29 /43.29 ms | 117.75°C |
| 1 | 50 ms | 73.64 /74.64 ms | 122.88°C |
| 1 | 100 ms | 103.63 /104.63 ms | 126.70°C |
| 1 | 600 ms | 333.56 /334.56 ms | 141.05°C |
| 5 | 10 ms | 50.97 /51.97 ms | 134.72°C |
| 10 | 10 ms | 60.74 /61.74 ms | 154.64°C |

The upper estimate adds positive AM ripple and the residual VPA capacitor energy to the smallest die capacity. Passing rows are conditional examples, not proven worst-case bounds. Even the very fast 10 ms sensor cannot protect the modeled degraded joint at the candidate threshold. A 30-second service timer cannot prevent a subsecond local excursion.

The 5/10 K/W joint cases are faults, not acceptable factory joints. They cannot currently be excluded by an established source-joint inspection/void acceptance bound. For scale only, a 50 µm solder layer, thermal conductivity 50 W/mK and effective wet area 0.2 mm² give 5 K/W; assumed resistivity 1.3×10^-7 Ωm gives only 32.5 µΩ. Such a path can conduct electrically while transferring heat poorly. These material examples are assumptions, not ST package specifications or proof of a particular void morphology. X-ray/source-joint qualification remains required.

Open, shorted and disconnected sensor wires leave the analog window and force HARD_OK_N low through Q970 without firmware polling. Unpowered/missing U970 outputs are pulled low; TEMP_BAD's gate pull-up also inhibits if its NAND driver is missing. A detached but electrically intact sensor or plausible stuck resistance can still look normal. A window alone cannot detect those failures. Bond retention, production test, transfer-function acceptance and an independent bounded PA power/energy mechanism are needed if thermal coupling cannot be guaranteed. The existing current limit does not establish die heat under reflection; a timed pulse limit alone does not establish safety without initial-temperature and minimum-capacity bounds. No unverified firmware latency is credited.

The minimum next experiment is a **bounded thermal-step characterization of the unchanged Q501 source-region stack**, with a calibrated junction-related proxy, source-copper sensor and case/bar measurements. Establish normal and deliberately degraded contact/known-joint bounds, sensor lag, initial temperature and hardware interruption latency using current/energy-limited steps; do not use an extended unsafe RF run to find equilibrium. This experiment is proposed, not authorized or performed here. If no threshold/delay window survives, the next required circuit change is an independently justified hardware PA power/energy interruption rather than more aluminum or higher limits. Review that closure before native E6R1 PCB implementation.
