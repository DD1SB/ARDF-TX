# M5A review decision — RF2M electrical candidate

Date: **2026-10-15**. Revision **M5A-R0 — NOT RELEASED**. **GO for independent schematic review; NO-GO for an integrated evaluation-PCB layout or procurement until the listed package/component and stability-review blockers close.** Then the next bounded step is a small, separately measurable RF/source/AM evaluation assembly, not a transmitter fleet.

## Delivered

- [Editable KiCad project](../hardware/2m/RF2M.kicad_pro), [schematic](../hardware/2m/RF2M.kicad_sch), [complete PDF](../hardware/2m/review/M5A-R0/RF2M.pdf), local symbol library, pin-explicit manifest, XML netlist and actual ERC report.
- [PA/driver decision](M5_2M_PA_SELECTION.md), [true-AM circuit](M5_2M_AM_DESIGN.md), [supply/endurance comparison](M5_2M_POWER_ARCHITECTURE.md), [controller interface](M5_2M_CONTROLLER_INTERFACE.md), [itemized BOM/cost](M5_2M_BOM.md), [schematic review](M5_2M_SCHEMATIC_REVIEW.md), [physical test plan](M5_2M_TEST_PLAN.md), [primary source log](M5_2M_SOURCES.md) and [requirements trace](M5_2M_TRACEABILITY.md).
- Reproducible netlist-derived digital checks: **4096 combinations, 36 state scenarios, 8 rejected mutations**; **34 critical pin assertions**. These include explicitly OPEN physical-package statuses. KiCad10.0.6 ERC: **zero errors, two OPEN-connector footprint warnings**. No PCB/DRC result exists or is claimed.

## Selected implementation and capability target

One local Si5351, fundamental filtering/pad, **PHA-13HLN+ single driver and formed-lead ST PD55008-E final**, replaceable144 MHz matching and harmonic filtering. Main supply modulation uses **ST D45H11 with ST BD139 helper**, filtered PWM references and a low-cost RRIO feedback amplifier. This is real series AM with keyed sine tone inside a continuous in-slot carrier. It is not FM or RF on/off chopping presented as75% AM.

At assumed−1 dBd antenna/feed gain,1 W carrier ERP means **1.259 W connector carrier /4.079 W PEP at80% AM**, with **5.135 W connector capability** investigated for1 dB reserve. The revised0.75 dB output-loss budget requires6.103 W device-plane capability. The15 dB PA-gain floor and1.25 dB input loss require driver24.11 dBm output and measured P1dB≥27.11 dBm for3 dB margin. No144 MHz gain, AM or PEP measurement currently exists.

Do not set a nominal1.000 W ERP without uncertainty margin. For example0.90 W full and0.30 W reduced only fit their respective upper/lower limits if total antenna/feeder/power uncertainty is sufficiently bounded;±0.4 dB gives approximately0.821–0.987 W and0.274–0.329 W. If uncertainty is larger, choose new guarded settings and recalculate endurance. The antenna system is still an assumption, not a measured−1 dBd result.

Prefer **2S boost13.5 V full/10 V reduced**, with a separately populated4S buck alternative and an explicitly higher full-power cutoff around14.5 V. The shared driver rail is approximately8 V, with conditional RC/OV shutdown. **2S3P/M35A is the initial two-target budget candidate**, not a qualified minimum.2S2P has inadequate extended runtime;2S3P/25R fails24 h reduced;4S1P strands too much energy at full power. The4S2P/25R full result is marginal/failing at the revised assumptions. Use actual pack curves and temperature/current logs before selecting a released minimum.

Training has its own inhibited3.3 V clock buffer, current-modulated small BJT, filter, fixed pad and incompatible connector. It targets nominal1 µW/optional1–10 µW calibrated carrier without the normal PA or converter. Conductive topology separation is established; actual off leakage, RF coupling and fault isolation are not.

## Cost and complexity

Full2S/4S component allowances at10 are **€74.61 /€72.77 net**, training-only **€16.37**. The6/10/20 tables intentionally use no unsupported batch discounts. These are mixed observations/converted displays/estimates, not completed procurement quotes. Full2S fits267 physical parts/23 ICs; training-only104/14. Non-physical flags and test pads are excluded.

**The former approximately€36 VHF target has not been achieved.** The selected RF silicon is about€29.66 before matching/chokes/filtering, AM, conversion and protection. The strongest concrete saving would be a cheaper driver after measured high PA gain, not removal of distinct fail-off functions. Current sourcing and35 unquoted-MPN positions prevent a proven series cost. No premium feature claim conceals this overrun; review the actual costed topology before investing in full-board prototypes.

## Required next evidence and decisions

1. Close exact PowerSO10RF formed-lead/DF782/RNW landings, thermal orientation, capacitor voltage/package selection, power-magnetic saturation/effective capacitance, fuse/shunt pulse ratings and mating connectors. Do not invent generic footprints to pass a check.
2. Review the144 MHz matching/stability starting networks and authorize only the minimum staged RF fixture/evaluation layout. Gain/compression and voltage-to-RF-envelope transfer must decide the final driver/bias/calibration settings.
3. Qualify the AF/pass loop and exact hot SOA/thermal arrangement; demonstrate70–80% RF sine AM and the required PEP. The ideal behavioral simulation does not close this gate.
4. Demonstrate bounded input/driver fault response, including≤20 µs isolation and driver voltage≤9.5 V, plus real asynchronous reset/ARM races. No unrestricted pack connection before these tests.
5. Review the20-pin/dedicated-I²C/PWM contract and controller GPIO allocation. Production firmware must refuse unset country/unsupported frequency and demonstrate legal/event profiles, timing and off-slot source control.
6. Measure port isolation, antenna ERP/pattern, spectrum/national mask, optional Silicontra coexistence and actual12 h/24 h endurance. No model or ERC report substitutes for them.

The still-proposed ADR0011 can receive the VHF supply/cutoff clarification in the power document after review. No accepted architecture,80m circuit, RTC/controller decision or2m power objective is silently changed. All physical qualification entries remain **NOT_RUN**. No PCB layout, Gerbers, purchasing, fabrication, assembly, RF transmission or production firmware occurred in M5A. Stop here for engineering review.
