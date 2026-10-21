# M5B-E6R1 — carrier-keyed A2A feasibility

**HOLD for proceeding to native PCB implementation.** Hybrid C substantially reduces normal SPACE heat, but the Q501 source-joint→sensor threshold/delay bound remains unresolved. This package is analysis and a precise circuit proposal. It contains no implemented E6R1 PCB or fabrication data.

Starting commit `85186204619edec32ad1bb2a3044bb55ea399658`, branch `m5b-e6-unified-heatsink`; executed 21 October 2026. E6, E5 native CAD, historical reviews, M6-L2 and RF80 remain unchanged. No push, tag, order or powered hardware test occurred.

| Evidence | Entry points |
| --- | --- |
| Decision | [Gate dispositions](../../../../docs/M5B_E6R1_REVIEW_DECISION.md), [execution](EXECUTION.md) |
| Official requirements | [Independent regulatory interpretation](../../../../docs/M5B_E6R1_A2A_REGULATORY.md), [primary sources](REFERENCES.md) |
| Exact Morse | [Timing explanation](../../../../docs/M5B_E6R1_MORSE_DUTY.md), [integer duty CSV](morse-duty.csv), [JSON](morse-duty.json) |
| Electrical proposal | [Circuit/nets](../../../../docs/M5B_E6R1_CARRIER_KEYING.md), [exact package pins/components](circuit-proposal.json), [loop/spectrum cases](electrical-model.json), [ngspice tail](simulation/native-kill-tail.cir) |
| Energy | [Power explanation](../../../../docs/M5B_E6R1_POWER_BUDGET.md), [MARK/SPACE JSON](power-budget.json), [cycle integrals](energy-integrals.csv), [whole-system overhead sensitivities](system-power.json) |
| Transients | [Method/results](../../../../docs/M5B_E6R1_TRANSIENT_THERMAL.md), [612 normal +108 sensitivity cases](thermal-results.json), [operating/outdoor/CW-ID sensitivities](operating-sensitivities.json) |
| PA closure | [Fault/threshold analysis](../../../../docs/M5B_E6R1_PA_THERMAL_SAFETY.md), [288 fault +18 healthy sensor cases](sensor-fault-results.json), [candidate window](sensor-window.json), [fresh original 133.79°C failure](E6-failure-reproduction.json) |
| Common cooler / costs | [Three structures](../../../../docs/M5B_E6R1_COOLING_DECISION.md), [numerical comparison](cooling-comparison.json), [seven-unit costs](../../../../docs/M5B_E6R1_COST_IMPACT.md), [cost source](cost-impact.json) |
| Verification / preservation | [37 tests](test-results.json), [actual raw logs including failures](logs/), [2,831 frozen starting-file hashes](preserved-start.json), [commands](REPRODUCE.md), [inventory](SHA256SUMS.txt) |

All plots are calculated sensitivities, not measured results. PA trace plots show cycle-mean temperature; positive AM ripple is separately added in tabulated junction peaks. The thermal-fault plot uses an upper estimate including ripple and actuation storage.

| Figure | PDF | Preview |
| --- | --- | --- |
| A vs C RF envelope | [PDF](01-carrier-comparison.pdf) | [PNG](01-carrier-comparison.png) |
| Actual device-power waveforms | [PDF](02-device-power.pdf) | [PNG](02-device-power.png) |
| PA Classic/Sprint periodic response | [PDF](03-PA-junction.pdf) | [PNG](03-PA-junction.png) |
| Pass case Classic/Sprint response | [PDF](04-pass-case.pdf) | [PNG](04-pass-case.png) |
| Continuous full-profile MO | [PDF](05-continuous-MO.pdf) | [PNG](05-continuous-MO.png) |
| Local joint/sensor fault sensitivity | [PDF](06-local-fault-sensitivity.pdf) | [PNG](06-local-fault-sensitivity.png) |
| Three cooler mass/cost comparisons | [PDF](07-cooler-mass-cost.pdf) | [PNG](07-cooler-mass-cost.png) |
| Ideal-envelope spectral comparison | [PDF](08-ideal-keying-spectrum.pdf) | [PNG](08-ideal-keying-spectrum.png) |

The existing [E6 common-cooler concept](../M5B-E6/common-cooler-concept.pdf) remains a simplified mechanical reference. This milestone does not move transistors, route copper, add cutouts or issue a mechanical drawing. Future implementation requires review of the thermal closure and precise proposal first. Genuine RF, converter, AM-loop, thermal, sensor, isolation and outdoor qualification remain NOT_RUN.
