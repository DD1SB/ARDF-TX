# M3A-R1 — final pre-layout review decision

Date: **2026-10-14**. **GO for review of the corrected electrical artifacts; conditional recommendation for a small evaluation-board layout after that review. No layout or procurement performed. Product/hardware release is NO-GO.**

The [editable project](../hardware/80m/RF80.kicad_pro), [root schematic](../hardware/80m/RF80.kicad_sch), [14-page PDF](../hardware/80m/review/RF80.pdf), [netlist](../hardware/80m/review/RF80.xml) and [ERC](../hardware/80m/review/ERC.json) now describe **M3A-R1**. R0 is preserved at Git tag `m3a-r0`/commit `dba9236`. [Logic audit](M3A_R1_LOGIC_AUDIT.md), [simplification](M3A_R1_SIMPLIFICATION.md), [cost delta](M3A_R1_COST_DELTA.md) and [verification](M3A_R1_VERIFICATION.md) provide the complete change record.

Critical U202 polarity is corrected using physical **Q1 pin 13** for LEASE_OK and **/Q2 pin 12** for bus holdoff, with POR/SCL/SDA qualification. A spare flip-flop blocks reset-release false progress. Additional defects corrected: pending delayed-ARM recovery, live-path transfer with retained key tail, weak unarmed tail discharge, low-current stack gate-voltage margin and direct driver-rail OV exposure. Raw ARM captures mode/path/key-low acceptance; any health loss clears that context. A held ARM cannot recover it. Current tests reproduce the old watchdog fault and reject both old output polarities.

KiCad ERC reports **zero violations**. Automated checks cover **597 connected pins, 218 footprint maps, 256 logic combinations, 31 state scenarios and 16 assumed timing corners**. A real ngspice passive sensitivity run bounds driver voltage only when **≤20 µs isolation and ≤0.5 Ω ESR are imposed**. These timing, voltage-domain and RF results have not been physically verified. No Boolean PASS is presented as analog safety proof.

The full fit has **193 purchased parts/18 ICs**, versus R0 185/20. Fox fit has **115 parts/13 ICs**, versus 128/15. Two redundant gate ICs and their bypasses were removed; PA trips share open collectors, and Fox omits watt-only comparator/reference/thermal infrastructure. New context/withdrawal and driver-fault protections increase individual parts. Required filters, RF paths and local UV remain. No new MCU, fourth board or repeated M1/M2 topology study.

| Scope, net EUR/unit | 6 | 10 | 20 |
| --- | ---: | ---: | ---: |
| Full RF80 components | 31.18 | 26.60 | 26.60 |
| Fox-only RF80 components | 12.01 | 10.80 | 10.46 |
| Complete Fox materials, retained scope | 66.38 | 59.43 | 59.15 |
| Fox including separate shared fleet allocation | 79.88 | 67.53 | 64.00 |

At ten, full components increase **€1.25** and Fox **€0.25** against R0. The nominal full-board cost target is still exceeded. Many passives, new latch, diodes and ancillary items remain estimates; no price-secured saving is claimed. The selected low-ESR driver capacitor costs more than an unqualified wet-electrolytic allowance. The historical €29.06/€55.24/€63.34 Fox audit is preserved, with connector halves counted once. Batteries/PCB/antenna/case/harness are outside board-component totals; labor, tooling and engineering stay separate. No assembly or fabrication quote was obtained.

The proven Si5351–LM5134B–IRF610 core, transformer and elliptic filter remain. Targets remain approximately **3 W full /1.2 W extended Classic, separately calibrated Sprint, independent 10 mW Fox**, normal protected 4S and compact Fox protected 2S. ESP32-S3/RTC/optional Silicontra and the three-PCB architecture remain. VHF is unchanged: **1 W carrier ERP true A2A with 70–80% sinusoidal AM and its existing PEP gates**.

Before authorizing the evaluation layout, the reviewer must accept the corrected pin/context/diode logic and resolve critical package/core/connectors and pending exact supply baskets. Include accessible waveforms, isolated normal/Fox loads and a power-only fault-injection arrangement. The next practical work should be that one small evaluation assembly, not another architecture study. First test bounded power and asynchronous logic; only then arm RF. Input-transient coordination (TPS22810≤18 V,20 V absolute;28 V passive case is outside system rating), driver interruption, feedback-reset pulse widths/races, BD140 hot SOA, AC00 supply ramps/backpower, calibrated RF/spectrum, physical port isolation, antenna field range and endurance remain **OPEN physical gates**. Failure of the driver bound or deliberate-rearm behavior is an immediate NO-GO for unrestricted 4S/RF integration.

[ADR-0012's R1 amendment](decisions/ADR-0012-m3a-hf-electrical-implementation.md) is **proposed**, not silently accepted. This milestone stops at corrected schematic/export/verification and pre-layout review; no PCB, Gerbers, orders, fabrication, assembly or production firmware.
