# M6-L1 optional radio, power and assembly contract

One PCB and one U70/J7 footprint support these independent radio options on any of the four existing base-controller populations:

| Assembly option | Trusted configuration | U70 | Antenna |
|---|---|---|---|
| NO_LORA | NONE | DNP | None; J7/R70/R71/C70/C71 DNP |
| LORA_433 | SX1262TR4_GC_433 | SX1262TR4-GC, C42381681 | Commissioned 433 MHz system |
| LORA_868 | SX1262TR8_GC_868 | SX1262TR8-GC, C42381682 | Commissioned 868 MHz system |

The native master retains an 868 MHz orderable MPN as its **DNP default**, with the 433 alternate selected in its own assembly BOM. All six optional positions must be fitted together for either radio option. Both options share identical copper; no GPIO, IDC connector, RTC, battery protection, USB or RF enable changes. [Twelve complete population BOMs and costs](../hardware/controller/review/M6-L1/LoRa-populations.json) cover the orthogonal choices; the old UNIVERSAL_LORA_OPEN name is superseded.

Do not infer the RF band from GetStatus or an SX1262 response. Establish it from the fitted-part/lot and trusted commissioning record; inspect supplier label and pin-1 geometry against the source register. An unknown, contradictory, uncommissioned or unresponsive radio leaves LoRa TX disabled. NONE is normal. A radio failure must not stop otherwise valid autonomous RTC-controlled ARDF operation. The host contract in `firmware/controller_hw/lora.py` requires a trusted exact population, matching antenna band, commissioning, stable power/main-pack validation, initialized response, approved frequency/power policy and an airtime authorization. It performs no RF probing. Its synthetic test policies are not legal country settings. Production firmware must independently enforce actual regional bands, EIRP/antenna gain and duty/airtime limits; the module's 22 dBm capability is not permission to use it.

Both modules are nominal 3.3 V / 120 mA at maximum stated RF power, with about 5 mA receive current. Common supply operation is within their 2.0–3.7 V / 1.8–3.7 V documented ranges. Reserve **150 mA** for radio TX as an engineering allowance; 120 mA is a published operating point, not a guaranteed all-corner transient maximum. Existing C70 100 nF and C71 10 µF remain near the module, on the common V3V3 domain. The native full-segment copper model gives roughly 0.149 Ω from regulator output to U70.13 at 80°C; a 150 mA radio contribution drops about 22 mV. The C70/C71 local paths add about 6.3/7.6 mΩ (roughly 1 mV at 150 mA). Shared rail load/ground effects still need oscilloscope tests. No new regulator or active switch is justified.

An effective local 4 µF capacitance scenario supporting a 150 mA step for 1 µs gives approximately 38 mV capacitive droop; 10 µs would give 375 mV if the regulator did not respond. This demonstrates the need for measurement, not a promised transient response. The previous 0.4 A steady-controller budget remains: 40 mA host + one 150 mA RF logic port + 150 mA LoRa allowance = 340 mA. Wi-Fi/BLE stays off. Do not convert the earlier 0.92 A short-burst allowance into a continuous rating. Initial LoRa TX is disabled on USB-only power and during ARDF RF slots; RX/diagnostics can be commissioned separately. NO_LORA has none of the six optional loads.

SPI is shared with the control shift registers. Keep NSS high except for a deliberate radio transaction, and SHIFT_LATCH low throughout it. Every control update must reload all 16 shift bits and latch atomically under a bus lock; radio data must never be latched as a control word. Direct key/slot/progress GPIO ownership is unchanged. Hold/reset/init the radio deliberately and validate BUSY/response before commands. DIO3 remains unused; do not select an external-TCXO mode based on another vendor's module. Selected module oscillator/RF-switch/SPI initialization is a commissioning/driver task; this milestone supplies no LoRa protocol stack. Remote commands retain all local pack, RTC, frequency, interlock and deliberate-rearm checks.

Use a short 50 Ω U.FL/MHF-I-compatible to normal-SMA bulkhead pigtail; **Taoglas CAB.011**, 95 mm, is a documented example. Separate antenna examples are **TE ANT-433-CW-HWR-SMA** (433 MHz quarter-wave; needs its specified counterpoise) and **ANT-868-CW-HWR-SMA** (868 MHz half-wave). These examples have manufacturer documentation; direct-store/distributor availability and prices remain unquoted, so band-correct equivalents may be used after their own data review. Never confuse SMA with RP-SMA. Cable loss and antenna gain enter regional EIRP limits. No generic whip is assumed dual-band. [Pigtail](https://www.taoglas.com/product/cab011-ipex-mhfiu-fl-to-95mm-1-13-cable-to-smafbkst/), [433 antenna](https://www.te.com/fr/product-ANT-433-CW-HWR-SMA.html), [868 antenna](https://www.te.com/en/product-ANT-868-CW-HWR-SMA.html).

Reserve the previous 15 mm top service envelope around J7; its roughly 2.4 mm mated height does not establish a final enclosure. Strain-relieve the coax to an independent support; do not pull the connector sideways or use it as a panel anchor. Keep the cable out of the ESP32 antenna keep-out and RF2M cooling envelope. U70 and J7 have no validated complete manufacturer 3D models in this project; the actual KiCad views show the default DNP lands, not proof of fitted module/cable height. There is no final enclosure acceptance.

Quantity-ten component estimates, net EUR, exclude freight/VAT/antenna/pigtail:

| Base | NO_LORA | LORA_433 | LORA_868 |
|---|---:|---:|---:|
| FOX_MIN | €18.99 | €24.30 | €24.36 |
| RF80_FULL | €19.26 | €24.57 | €24.63 |
| RF2M_FULL | €19.30 | €24.61 | €24.67 |
| UNIVERSAL | €22.34 | €27.65 | €27.71 |

LCSC observations are USD 5.5656/4.7161 (433, q1/q10) and USD 5.6375/4.7854 (868). The EUR model uses an explicit **0.90 EUR/USD planning factor**, not an exchange-rate observation or supplier EUR quote; no unobserved q20 discount. J7 uses an indexed EUR 1.11/0.946 observation; another regional listing differs. Significant base material remains unquoted. A PCB/stencil process change is unnecessary. See [sourcing](../hardware/controller/review/M6-L1/SOURCING.md), [cost JSON](../hardware/controller/review/M6-L1/LoRa-costs.json).
