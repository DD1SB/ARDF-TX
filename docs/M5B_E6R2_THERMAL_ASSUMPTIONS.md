# E6R2 thermal basis and remaining qualification

Use the unchanged [E6R1 transient study](M5B_E6R1_TRANSIENT_THERMAL.md), exact
[Morse fractions](M5B_E6R1_MORSE_DUTY.md) and [power ledger](M5B_E6R1_POWER_BUDGET.md).
Those are analytical evidence. This milestone adds native hardware and circuit
simulation; it does not relabel thermal calculations as measurements.

| 1W ERP,40°C ambient,restricted cooling,ArchitectureC | Q501 peak Tj | Q401 peak case |
|---|---:|---:|
| Classic60/240s |74.31°C|46.43°C|
| Sprint12/48s |73.72°C|46.03°C|
| Continuous MO |87.76°C|59.51°C|

Retain Q501110°C target/125°C engineering ceiling, Q40160°C case and Q40280°C
case. Continuous1W MO has only0.49°C Q401 modeled margin. It is an explicit
first-article priority, with progressive duty/power and controlled shaded
installation. Lower-power beacons are optional, not the sole thermal solution.

One SK81100SA100×100×15mm is retained. Q401/Q402 now use direct mica attachment
to the same flat base. No old independent SK100/FK213 remains. The source bar
is ordinary15×44×6mm stock, shortened from10mm; a full15×44×0.25mm KERATHERM86/82
sheet isolates underside foreign copper. For6.5W/mK, the full-area sheet-only
resistance is0.058K/W; actual local contact/pressure/spreading adds resistance.
No claim that this removes junction/source/solder/via bottlenecks is made.
The 98 ordinary open thermal vias, source mask and five paste windows totaling 6.765mm²
are unchanged. No required solder fill, via cap, premium copper or RF laminate.
The idealized spacer improvement is not booked as a validated temperature gain.

The134.72°C degraded-contact scenario remains in E6R1 evidence. It is an
assembly/measurement risk, not the nominal prediction or a reason to prohibit
unpopulated boards. A seriously defective source joint can evade the existing
pass-case sensor. Source-region thermocouple readings are not Tj measurements.
Correlate voltage/current/RF heat and transient thermal proxies before extending
power/duration. Existing hardware protection is necessary but is not claimed
to bound every hidden solder defect.

CategoryA blockers: electrical shorts, inadequate insulation, invalid routing,
impossible mounting or nominal thermal inadequacy. They must be corrected.
CategoryB risks: source coverage, pressure/flatness, gain, actual thermal paths,
sensor delay, convection and converter light-load behavior. Resolve by controlled
assembly/measurement. CategoryC: arbitrary contact loss or simultaneous severe
assembly defects/out-of-envelope solar obstruction; record limitations without
claiming qualification or designing to unlimited faults.

Protect the finned underside above an insulating carrier with≥15mm external
feet and10.7mm nominal internal air gap. Mounting supports the sink independently.
Use free fin channels; upright/horizontal deployment must be compared physically.
Keep dry vegetation out of channels. Full-power continuous beacon requires a
shaded ventilated support, not a buried/fully enclosed or leaf-obstructed cooler.
Solar-heated/restricted installations are sensitivities, not qualified conditions.
Accessible surfaces should target≤55°C in intended deployment; this is a field
acceptance target, not proof of fire safety or a new shutdown threshold.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.
