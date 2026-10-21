# M5B-E6R1 — transient thermal comparison

**Keying improves nominal operation; the adverse/protection envelope remains HOLD.** [Calculation source](../tools/m5b_e6r1_thermal.py), [all normal and sensitivity results](../hardware/2m/review/M5B-E6R1/thermal-results.json), [operating sensitivities](../hardware/2m/review/M5B-E6R1/operating-sensitivities.json) and [plots](../hardware/2m/review/M5B-E6R1/README.md) are reproducible. No thermal measurement was performed.

All A/B/C comparisons use the same immutable E6 12-node passive thermal network: PA junction/source, source copper, bottom copper, source bar, pass junction/case, helper junction/case, common plate/fins and existing Q401 NTC. The actual 98 ordinary open source vias and copper thermal storage remain included. No filled vias, top-of-package heat path or thermal-mass bypass is credited. Manufacturer steady RθJC is 3/2.5/10 K/W for PA/pass/helper. E6 source-to-bar finite-volume paths and their contact/pressure uncertainty are retained, including approximately 15.896 K/W conservative and 18.402 K/W poor-contact cases. The better 11.847 K/W path is examined separately for the original fault and sensor study.

E6 package/FR4 heat capacities are assumed bounds, swept ×0.1/1/3; known copper/via storage is not scaled away. Source-path split is an approximate Cauer representation, not a fitted manufacturer Zth. Aluminum remains 214 g ×900 J/kgK plus the existing bar. Same cooler boundary is used across keying methods: 5.5 K/W restricted/sideways comparator, not a measured catalogue orientation rating. Independent source-joint fault resistance is varied in the sensor study. Grease thickness, pressure, wet source area, copper plating and sensor attachment remain first-article controls.

Each constant-power interval is propagated exactly by the conductance/capacitance matrix. A periodic fixed point is solved, with millisecond/local and slower plate sampling. Edge intervals use eight subdivisions; 32-step comparison changes integrated input by less than 0.1%. The PA's positive 800 Hz temperature ripple is calculated separately and conservatively added to peak cycle-mean temperature. The nominal 1 W addition is approximately 0.387°C; faster assumed local capacities increase it. No claimed precision of physical temperature is implied by solver decimals.

The table uses BUCK4S, 40°C, conservative E6 local network, 12 WPM, MO5 for allocated slots. PA entries include the positive AM addition; Q401 is case temperature.

| ERP | Classic C: first / periodic PA; Q401 case | Sprint C: first / periodic PA; Q401 case | Continuous MO C: PA / Q401 case |
| --- | --- | --- | --- |
| 0.25 W | 52.29 / 53.88; 44.04°C | 51.75 / 53.58; 43.82°C | 61.59 / 51.60°C |
| 0.5 W | 64.24 / 66.49; 45.49°C | 63.43 / 66.01; 45.16°C | 77.60 / 56.31°C |
| 1 W | 71.61 / 74.31; 46.43°C | 70.62 / 73.72; 46.03°C | 87.76 / 59.51°C |

At 1 W, the same-boundary reference A predicts Classic 80.87/86.30°C PA, Q401 51.79°C; Sprint 78.85/85.09°C, Q401 51.00°C; continuous MO 111.07°C PA and 76.23°C Q401. Ideal B is nearly identical thermally to C: periodic PA 74.32/73.72/87.77°C and Q401 46.43/46.04/59.52°C. Its converter start behavior is unqualified, so this small difference does not justify cold-keying the converter.

For C at 1 W, PA periodic minima are approximately 42.86/43.14/67.11°C for Classic/Sprint/MO. Source-case peaks are 68.41/67.81/81.85°C, helper cases 43.84/43.44/56.91°C and common-plate peaks 43.69/43.31/56.74°C. All node maxima/minima are retained in JSON. Classic/Sprint include cold first slot and accumulation through periodic equilibrium. The cold result for MO is only its first word, not a one-minute pulse; continuous-beacon acceptance uses the true periodic word equilibrium. Shutdown recovery is visible through the 240/48-second intervals; no carrier is scheduled there. In this linear model 25°C ambient subtracts 15°C from 40°C results; ambient-dependent electrical/material properties remain unvalidated.

The original E6 failure is replayed without corrected R1 loads or timing changes: **133.788836°C**, pass case 56.902°C, old NTC 56.440°C, rail peak 1.736013 A. The [fresh reproduction](../hardware/2m/review/M5B-E6R1/E6-failure-reproduction.json) differs from historical E6 by 0°C numerically. R1 A differs slightly from historical nominal tables because native bleeder/bias and prepared idle loads were made explicit and continuous MO now uses its actual repetition period. No historical file was regenerated.

Important adverse full-profile findings, at 8 WPM/40°C and the same 5.5 K/W boundary:

| C case | PA junction estimate | Q401 case | Result |
| --- | ---: | ---: | --- |
| Nominal losses, conservative network/capacity ×1 | 89.46°C including AM | 59.64°C | Narrow conditional nominal margin |
| Same network, capacity ×0.1 | 96.95°C including AM | 60.30°C | Q401 criterion exceeded |
| Poor source/contact network, capacity ×1 | 93.15°C including AM | 61.21°C | Q401 criterion exceeded |
| eta 50%, beta 60, +3% BUCK rail | 89.74°C cycle-mean | 60.49°C | Q401 criterion exceeded |
| eta 40%, beta 60, nominal BUCK rail | 111.39°C cycle-mean | 65.48°C | PA target and Q401 criterion exceeded |
| eta 40%, beta 20, +3% BUCK rail | 112.99°C cycle-mean | 67.35°C | Same failures; add positive AM for junction peak |

BOOST is analyzed independently. At 8 WPM nominal full profile its pass case is approximately 60.03°C; eta 40%/beta20/+3% gives 67.85°C. The intact full-profile capability is not made acceptable by silently choosing a lower beacon ERP. A reproducible heat/efficiency and installation boundary is still required. Nominal 1 W BOOST/BUCK and reduced profiles are all in the results, including all codes and CW-ID cases.

Continuous no-tone carrier remains a separate bounded service mode: maximum 30 s comparator followed by shutdown, not indefinite CW at a Morse average. C's conservative network predicts about 78.17°C PA including the deliberately conservative AM addition and 48.56°C Q401 for repeated 30/270 s. This is not permission to run unsafe full-power tests or a target-firmware implementation. Startup packet heat, actual keying edges and capacitor release are included. A stuck-high transaction and same-input RF-absorption fault are separately evaluated by the [PA sensor model](M5B_E6R1_PA_THERMAL_SAFETY.md).

Restricted cooling at 8 or 12 K/W makes nominal MO pass case about 67.22/79.36°C. Adding 10 W solar heat to the plate at 5.5 K/W gives an unprotected equilibrium near 114.64°C pass case. These are deliberate failure sensitivities; existing shutdown is expected to interrupt, not permit such equilibrium. The Q401 NTC lags the case (1/5/15 s sweep); it cannot bound local Q501 junction temperature. A raised shaded ventilated guard and measured installation envelope are required. Neither simulation nor an assumed leaf ignition point establishes fire safety.

The limits remain PA target 110°C/ceiling 125°C, pass case 60°C, helper case 80°C. Model-level test PASS means calculations and detection of failures are reproducible; it does not mean these operating gates all pass.
