# M3A — electrical review decision

Date: **2026-10-14**. **GO for engineering review of the delivered schematic. NO-GO for layout, ordering, fabrication, assembly or a fleet.** All physical gates remain NOT RUN.

The [editable KiCad schematic](../hardware/80m/RF80.kicad_sch) implements one **SignalSlinger/FlexFox80 Si5351–LM5134B–IRF610** stage, its bifilar transformer and original elliptic filter, one 4S buck and a QCX-derived BD140 drain shaper. Targets are approximately 3 W full /1.2 W extended Classic and independently calibrated Sprint. Its independent Fox path uses TinyFox's three-NAND buffer mechanism, adapted to a stronger **SN74AC00DR**, shaped supply and separate filter/pad/compact port. The watt converter, driver, final and normal magnetics are DNP in Fox-only assemblies.

The common ESP32-S3/RTC/optional Silicontra and three primary PCBs remain. The 2 m target is unchanged: **1 W carrier ERP, genuine 70–80% sinusoidal A2A**, with existing PEP, driver and thermal gates.

Review artifacts: [PDF](../hardware/80m/review/RF80.pdf), [circuit explanation](M3_80M_SCHEMATIC_REVIEW.md), [PA selection](M3_80M_PA_SELECTION.md), [BOM](M3_80M_BOM.md), [test plan](M3_80M_TEST_PLAN.md), [check report](M3_80M_CHECKS.md). Components have actual pin maps, named nets, footprints, population fields and probe pads. Four custom footprints describe individual packages/wound parts; **there is no PCB file or layout**. [ADR-0012](decisions/ADR-0012-m3a-hf-electrical-implementation.md) proposes these implementation choices; accepted ADRs and proposed ADR-0010/0011 statuses are preserved.

At 6/10/20, full board components budget **€28.54/€25.35/€25.14**; Fox-only **€11.61/€10.55/€10.53**, net. The full board misses the €20 target; supply, filters, independent protection and unquoted supporting components explain the overrun. The normal stage with drive/shaping/filter/supply/input/output hardware is about **€14.16 at ten**, before shared source/safety/Fox circuitry. Current baskets and ancillary material remain open.

The Fox complete-unit replacement budget is **about €59.18 in materials at ten**, including the compact antenna/matching, protected 2S1P pack, S3/RTC, case, wiring and two bare PCBs; **€67.28** with shared charging/provisioning/freight. Historical €55.24/€63.34 audit totals remain intact. The [BOM bridge](M3_80M_BOM.md) explicitly removes connector allowances now included on the RF board. Labor, instruments, engineering and spares remain separate.

The M3 model includes an always-powered source and explicit shaper base-drive, diode and standby losses. On 4S1P 25R, **13.2 h at 3.15 W /25.2 h at 1.2 W** is calculated before LoRa or poorer efficiency. At 40% PA/85% buck efficiency, these fall to **9.2/19.7 h**. Adding 0.18 W idle overhead gives **12.0/21.0 h**, missing the respective targets before rounding. The small pack therefore remains a measurement-dependent candidate; 4S1P M35A provides more margin at additional cost. Fox retains the 0.350 W planning load/2S1P 25R 32.7 h assumption. **No modeled runtime is a qualification result.**

Before producing the first evaluation PCB, review must approve:

1. Exact component stock, critical pin maps/footprints/core identity/winding polarity, effective capacitors, buck stability and driver protection during an OV fault.
2. Fixed rail calibration, BD140 hot repetitive SOA and initial shaping values, the 80°C case interlock and qualified heat path.
3. AC00 current/10 mW feasibility, operation through the supply ramp, independent mute and minimum 1 dB pad/fault bound. Keep the existing BJT-buffer fallback if the logic branch fails.
4. Connector/harness keying, the bounded 3.3 V interface, current-return arrangement, pack backstops and stale-ARM/lease/retune behavior. The controller's dual-voltage implementation still requires its own review.
5. A **small evaluation PCB scope and explicit layout authorization**, suitable instruments and the physical test plan. No fleet or procurement authorization is implied.

After that review, only the selected RF stage and separate Fox section should enter an evaluation layout. Power-only and interlock tests precede armed RF; power/spectrum/shaping/fault/thermal results precede final system layout. Antenna, field, endurance and repeatability tests remain release gates.
