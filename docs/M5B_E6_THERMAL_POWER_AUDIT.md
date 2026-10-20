# M5B-E6 power audit — analysis before CAD

Executed 21 October 2026 (Europe/Berlin), starting at `256c64888b680f5152e92f035e2ea0676a83630a`, branch `m5b-e6-unified-heatsink`. **Calculated planning loads, not measured device losses.** No native PCB, schematic, component value, safety threshold or RF layout was changed. The [decision is HOLD](M5B_E6_REVIEW_DECISION.md).

The source review includes [M2 power modes](M2_POWER_MODE_COMPARISON.md), [M2 endurance](M2_ENDURANCE_REWORK.md), [E4 correction](M5B_E4_THERMAL_CORRECTION.md), [E5 mechanics](M5B_E5_THERMAL_MECHANICAL.md), native electrical/netlist/PCB data and the frozen E5 thermal, pass-spacer and common-platform models. [Input hashes](../hardware/2m/review/M5B-E6/phase-A-source-inputs.json) identify those inputs. The new independently written [power calculator](../tools/m5b_e6_power.py) does not overwrite them.

## RF power and native supply

With the existing −1 dBd antenna/feed planning allowance, 1 W ERP needs 1.258925 W connector carrier. At 80% sinusoidal AM: mean tone RF is carrier ×1.32 = 1.661782 W, PEP is carrier ×3.24 = 4.078918 W, and clean PEP with 1 dB margin is 5.135 W. **This is not 5 W continuous carrier.** E5's 0.75 dB output-network allowance gives approximately 1.496 W internal carrier, 1.975 W full-tone mean and 6.10 W clean internal PEP capability. M2's 0.5 dB filter assumption is retained as historical context, not substituted silently.

The actual converter feedback gives full boost 9.02086 V, full buck 8.9996 V and reduced buck 7.5096 V. R511/R512 set gain 2.8. The modeled full-power drain centre is 4 V, with 0.8–7.2 V excursions at 80% AM. The reduced centre is 2.222 V; the intermediate 0.5 W calculation uses 2.828 V and requires native PWM calibration. No target firmware power profile is claimed implemented. M2's older 13.5 V rail is not the E5 circuit.

The selected [ST PD54008L-E datasheet](https://www.st.com/resource/en/datasheet/pd54008l-e.pdf), Rev 2, identifies **PowerFLAT 5 × 5 mm**, not PowerSO-10RF. It specifies RθJC 3 K/W and an 8 W/500 MHz operating point at 7.5 V, IDQ 200 mA. It does not establish our 144 MHz/4 V-centre efficiency or load-mismatch behavior. [ST D45H11](https://www.st.com/resource/en/datasheet/d45h11.pdf) has RθJC 2.5 K/W; [ST BD139](https://www.st.com/resource/en/datasheet/bd139.pdf) has 10 K/W. The exact ST SOT-32 drawing labels pins 1=B, 2=C, 3=E, matching the native board. Other manufacturers' generic BD139 diagrams are not substitution authority.

## Consistent device ledger

For each AM phase, `V = V0(1 + m sin θ)` and `I_PA = I_bias + kV`. Carrier efficiency includes the selected 0.15 A bias: `I0 = P_RF_carrier/(η_carrier V0)`, `k = (I0−I_bias)/V0`. Bias is not added again. Nominal η is 50% at 1 W ERP and 40% at reduced profiles; η=35–60%, bias=50–200 mA and pass β=20–100 are separate sensitivity inputs. These are assumptions, not measured curves.

`P_PA = V I_PA + P_RF_drive − P_RF_out`. The 19 dBm driver input contribution is included, with equal subtraction from MMIC heat. `I_pass` includes PA current, feedback current and `C dV/dt`. `P_pass = (V_bus−V) I_pass + V_BE I_base`; helper current follows the pass base demand, base-return resistor, series resistance and helper emitter resistor. The extra base terminal power is explicit. β=60 is a nominal scenario, not a guaranteed hot minimum at every operating point.

At every phase, total DC input equals RF output plus all modeled semiconductor/resistor/converter losses plus envelope-capacitor energy storage `V C dV/dt`. RF battery and the controller-provided 3.3 V input are separate: the 0.10 W logic allowance and helper base drive are not drawn through the RF converter/current shunt. `DC_input_W` sums those two delivered supplies; controller conversion losses outside the RF board are not included. The reactive term averages to zero. Independent tests check the terminal and whole-system energy balances; no independent PA/pass/helper worst-case powers are combined as a normal operating point.

BUCK4S planning losses, W; entries are **80% tone mark / no-tone space**:

| ERP | PA | D45H11 | BD139 | Other PCB heat, mark |
| --- | --- | --- | --- | --- |
| 0.25 W | 0.713 / 0.640 | 2.038 / 2.231 | 0.048 / 0.048 | See full ledger |
| 0.30 W | 0.862 / 0.753 | 2.424 / 2.677 | 0.057 / 0.057 | See full ledger |
| 0.50 W | 1.425 / 1.202 | 2.641 / 3.104 | 0.073 / 0.074 | See full ledger |
| 1.00 W | 1.863 / 1.576 | 2.985 / 3.750 | 0.101 / 0.101 | Approximately 2.47 W |

[Full power-state CSV](../hardware/2m/review/M5B-E6/power-states.csv) includes both converter populations, mean DC/RF power, regulators, MMIC, base resistors, converter heat and peak currents. Driver planning current is 146.3 mA at 5 V; boost/buck efficiencies 87/91% and control overhead 0.10 W remain explicit assumptions. Their heat is not hidden in heatsink mass. The model couples 25% of other PCB heat to the common plate, with 100% sensitivity cases.

## Keying and off states

Native U402 is an AF/DC selector: pin 1 AF_DC, pin 3 LEVEL_DC, pin 4 AM_COMMAND, pin 6 KEY. **A Morse space retains a DC RF carrier.** It reduces PA heat but increases series-pass heat. CW-ID using keyed AF has the same behavior; an unmodulated carrier uses the space load continuously. Removing carrier in spaces would change the modulation/control architecture and has not been assumed.

Allocated-slot inactivity permits PA/pass/helper load zero only with native ARM/SLOT/PREPARE/PA_PREPARE inhibition and the documented source/driver/bias shutdown. A 0.04 W RF-board idle allowance remains, not a measured leakage result. PREPARE held high can leave converter/reservoir and analog overhead; indefinite prepared idle earns no assumed zero-power cooling credit. Startup/fault conditions are separate bounded cases. The service-carrier model uses 30 s maximum as a commissioning constraint, not proof of an implemented RF2M timer or permission to operate an unqualified assembly for 30 s.

The old 4 W PA / 4.24 W pass / 1.1 W helper allowances remain explicitly imposed stress cases. They are not the derived losses of one verified operating point. The separate M2 dynamic-efficiency-plus-added-bias family is retained; at its low-voltage E5 reinterpretation some AM crests exceed the nominal 1.797 A current trip. Those points are reported as invalid, not clipped and counted as achieved RF output.

## Open power envelope

Nominal full-power peak regulated current is 1.394 A. At 40% assumed carrier efficiency it is 1.736 A: below the nominal trip but without a guaranteed all-tolerance trip margin. A same-input-energy sensitivity assigns undelivered RF to PA heat. At 40% efficiency/full absorption the mean tone PA/pass/helper loads are approximately 4.825/3.683/0.125 W. This is a bounded sensitivity, **not a measured antenna-fault prediction**. The actual RF reflection, drain-current change and efficiency envelope remain unqualified. The existing netlist has no PA-temperature or reflected-power detector; valid application progress can continue its watchdog lease. [Thermal consequences and closure requirements](M5B_E6_TRANSIENT_THERMAL.md) prevent a premature E6 release.
