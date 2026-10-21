# M5B-E6R1 — consistent electrical-power ledger

All numbers are calculated planning cases. The [power source](../tools/m5b_e6r1_power.py) imports actual E5 component values, retains E6 PA assumptions and checks energy at each sampled AM phase. [Power JSON](../hardware/2m/review/M5B-E6R1/power-budget.json), [integrated CSV](../hardware/2m/review/M5B-E6R1/energy-integrals.csv) and [whole-system sensitivities](../hardware/2m/review/M5B-E6R1/system-power.json) are fresh outputs.

The unchanged full profile has approximately 1.259 W connector carrier, 1.662 W full-tone mean RF, 4.079 W connector PEP and 5.135 W required clean PEP capability with reserve. Internal carrier RF is ERP × 10^0.175, including antenna/feed and 0.75 dB filter allowance. VPA centres are 2.222/2.828/4.000 V for 0.25/0.5/1 W ERP. `VPA(t)=V0[1+0.8 sin(2π800t)]`; `I_PA=k VPA + 0.15 A` at normal MARK voltages, with k chosen consistently for 40% reduced-profile or 50% full-profile carrier efficiency. These efficiencies at 144 MHz and the chosen voltages are assumptions, not manufacturer guarantees. Low shaped tails roll bias current toward zero below 0.2 V; that new behavior is explicitly unmeasured.

The pass calculation includes PA current, feedback current, native R513 1 kΩ bleeder, envelope capacitor current and BJT base current. Helper beta is 40, nominal pass beta 60, with beta 20 sensitivity. VPA and MOD_SINK remain isolated from the common metal. R606/RV501's 11 kΩ bias-divider load and prepared-converter idle allowance are added to the old E6 accounting. They slightly increase R1 A losses; the old numbers and their 133.79°C failure are independently reproduced, not replaced.

| Supply / ERP | MARK PA / pass / helper W | Existing A SPACE PA / pass / helper W | A module DC MARK/SPACE W |
| --- | --- | --- | ---: |
| BUCK4S / 0.25 | 0.713 / 2.048 / 0.048 | 0.640 / 2.242 / 0.048 | 4.873 |
| BUCK4S / 0.5 | 1.425 / 2.652 / 0.073 | 1.202 / 3.117 / 0.074 | 6.896 |
| BUCK4S / 1 | 1.863 / 3.000 / 0.101 | 1.576 / 3.770 / 0.102 | 9.129 |
| BOOST2S / 0.25 | 0.713 / 2.688 / 0.059 | 0.640 / 2.882 / 0.059 | 6.108 |
| BOOST2S / 0.5 | 1.425 / 3.656 / 0.090 | 1.202 / 4.121 / 0.091 | 8.650 |
| BOOST2S / 1 | 1.863 / 3.015 / 0.102 | 1.576 / 3.786 / 0.102 | 9.578 |

C preserves these flat-MARK device losses and adds a 20 mW key/protection logic allowance. C SPACE budgets PA/pass/helper at **1/2/1 mW** with driver off and drain clamped, not just output muted. These are design budgets requiring leakage measurements. Total SPACE DC is approximately 0.138/0.138/0.141 W BUCK and 0.153 W BOOST. Synthesizer/control, bias divider and prepared converter remain included. B SPACE is an ideal cold-domain lower bound, not a working converter design.

BUCK rail is approximately 7.510 V reduced /9.000 V full, efficiency 91%, idle 8 mW. BOOST holds approximately 9.021 V even at reduced ERP, efficiency 87%, idle 20 mW. Thus BOOST pass loss at low ERP cannot be copied from BUCK. At full MARK the modeled driver-domain heat is 1.237/1.240 W and converter loss 0.820/1.249 W BUCK/BOOST. Driver heat includes MMIC, series resistor and LDO; RF drive input is credited to the PA ledger. Converter current/efficiency variation across battery voltage, especially light-load PFM behavior, remains a measurement uncertainty. +3% regulated-rail sensitivity is included; it is not a claim of complete converter corner coverage.

At every phase and integrated cycle:

`RF battery input + RF-board 3.3 V input = connector RF + PA heat + pass heat + helper heat + other PCB heat + stored-energy change`.

Other PCB heat includes converter, driver, bias/feedback/bleeder, logic and RF-filter losses. Capacitor power is signed. Rise/fall packets explicitly charge, store and release energy; C's full-profile packet is about 2.904 mJ BUCK /3.044 mJ BOOST, dominated by the conservative 2 ms MMIC warm-up. The VPA capacitor itself stores only 2.601 µJ at 7.2 V. B additionally cold-charges the converter/driver reservoirs. Neither a large imaginary VPA capacitor nor an omitted driver is used to obtain savings.

For 1 W ERP BUCK at 12 WPM, MO5 slots and continuous MO:

| Mode / architecture | PA J | Pass J | Helper J | Other heat J | Connector RF J | Total DC J |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Classic A, 300 s | 103.144 | 203.098 | 6.103 | 157.385 | 87.621 | 557.351 |
| Classic C, 300 s | 55.606 | 92.222 | 3.092 | 96.331 | 49.348 | 296.599 |
| Sprint A, 60 s | 20.629 | 40.620 | 1.221 | 31.477 | 17.524 | 111.470 |
| Sprint C, 60 s | 11.115 | 18.435 | 0.618 | 19.259 | 9.864 | 59.291 |
| Continuous MO A, 2.8 s | 4.842 | 9.401 | 0.285 | 6.905 | 4.129 | 25.562 |
| Continuous MO C, 2.8 s | 2.785 | 4.575 | 0.154 | 4.034 | 2.476 | 14.025 |

C removes carrier energy during gaps; the lower cycle-average RF is intentional and does not lower the specified on-MARK ERP or clean PEP capability. Continuous MO module input falls from 9.129 to approximately 5.009 W. Classic averages 0.989 W before whole-controller consumption and common slot-preparation overhead.

The system file separately sweeps controller delivered load 0.2/0.5/1.5 W and controller conversion efficiency 85/90/95%; none is presented as measured ESP32 consumption. It adds RF-battery input and converts the separate 3.3 V domain once. A conservative common cold-bank charge plus 250 ms ×0.15 W preparation is included once per allocated cycle, outside the RF waveform. The controller's local heat is outside the RF cooler. No endurance claim follows from these allowances.

At the same full-profile DC point, assigning all undelivered RF to PA heat conserves energy: eta 40% gives 4.825 W PA mean MARK, rather than independently adding arbitrary worst-case losses. Native current may remain below nominal trip. Historical independent 4 W PA /4.24 W pass /1.1 W helper stress allowances remain preserved E6 stress cases, not simultaneous normal-operation inputs. [Thermal sweeps](M5B_E6R1_TRANSIENT_THERMAL.md) retain efficiency, supply and thermal uncertainty.
