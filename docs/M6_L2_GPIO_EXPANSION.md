# M6-L2 GPIO expansion and service access

U80 is the exact **Texas Instruments TCA9534APWR**, TSSOP-16, operated from a protected nominal 3.3 V rail. [TI's datasheet](https://www.ti.com/lit/ds/symlink/tca9534a.pdf) specifies 1.65–5.5 V operation and inputs on all eight ports after power-on reset. A2,A1,A0 are all grounded, selecting **7-bit address 0x38**. This is the A variant; the non-A device has a different address range and is not an automatic substitution. The RV3032 remains at 0x51, as specified in section 6.6 of the [manufacturer application manual](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3032-C7_App-Manual.pdf). The older RF-interface prose lists 0x52; that historical description does not override the installed RV-3032 device documentation. Existing RF I²C branches and their switched buffers are unchanged.

The option connects to RTC80_SCL/SDA through its own TCA9517DR buffer. The original RTC-side 4.7 kΩ pull-ups remain; the option adds no parallel upstream pull-ups. Its downstream pull-ups are 4.7 kΩ to EXP_VDD. EN is tied to its protected B-side supply. Internal undervoltage isolation disables the buffer when either supply is absent; this avoids an EN pull-up leakage path into MCU_EN. The expander cannot originate I²C transactions. Its supply-off high-impedance behavior separates a partially powered accessory branch from the RTC bus. Run the shared bus at 100 kHz with bounded transactions and the existing fault handling. Include device and actual copper capacitance in the recorded rise-time budget. A downstream stuck I²C device is a fault that must withdraw valid RTC/configuration evidence and force fail-off; the expander does not become an alternate clock or protection controller.

U82 is **LM66100DCKR**, SC70-6, with VIN=V3V3 and CE=VOUT=EXP_VDD. It blocks reverse current while preserving the TCA9517 B-side minimum 2.7 V supply margin. R33110k on V3V3 provides a defined leakage termination; the reverse blocker plus a20µA aggregate buffer off-leakage envelope for both lines predicts less than0.221V on an otherwise unpowered rail. ST is grounded as TI permits for an unused status output; NC is unconnected. [TI's specified reverse leakage](https://www.ti.com/lit/ds/symlink/lm66100.pdf) is included in the unpowered calculation, not assumed zero. A simple Schottky drop is not used for this buffered supply. Header power is separately current-limited by R330, 22 Ω/1 W.

J9 is a normally unpopulated **2×5, 2.54 mm** header on the underside. The square pad is pin 1. With board north up, its underside component/mating view matches the mirrored `PCB-bottom.svg` export:

```text
   2 P1       4 P3       6 P5       8 P7      10 GND
   1 P0       3 P2       5 P4       7 P6       9 3V3
   ^ square pad
```

Native pad 1 is at (36,25.5) mm, pad 2 at (36,22.96) mm; subsequent pairs advance 2.54 mm toward decreasing native X. The placement and native mechanical files record every contact. Rotate this drawing to match the assembly; do not mirror the cable numbering.

Every signal has an individual 1 kΩ series resistor. Header supply is nominal 3.3 V **before** its 22 Ω limiter: at 10 mA load the limiter drops 0.22 V. Use the contact for small LEDs/buttons/low-current logic that tolerate that drop and the calculated copper loss; an accessory requiring a tightly regulated 3.3 V supply must use a separately reviewed power interface. The 10 mA budget is a maximum operating allocation, not a 3.3 V/10 mA regulation claim. A short is bounded to at most 3.6 V/(22 Ω×0.983) = 166.5 mA and 0.600 W at the limiter, below its 1 W rating and temperature derating allowance.

Keep all external signals in the 0–3.3 V range, share GND, and do not externally power the header or drive an unpowered controller. The reverse blocker and I²C buffer bound accidental 3.3 V accessory backfeed, but they are not permission to connect arbitrary 5 V/pack-voltage equipment. A GPIO short to GND or 3.3 V is limited to at most about 3.67 mA through a 1 kΩ resistor including1.7% tolerance/temperature envelope resistor; eight simultaneous shorts remain below the expander's aggregate-current ratings and the power-budget allowance. Limit normal per-pin current to 1 mA and total programmed output current to 8 mA. The device's absolute maximum currents are not operating recommendations. GPIO voltage drop across the series resistor must be included in accessory logic/LED calculations.

At the expander's power-on reset all ports are inputs without internal pull-ups. The TCA9534A has no reset pin: an ESP32 warm reset alone does not power-cycle it. Early optional-peripheral initialization writes all ports to inputs; retained UI output states have no RF or protection connection. The accessory must provide suitable local pull-ups/pull-downs for buttons or open contacts; software initializes the output latch to its safe value **before** changing any direction bits. Disconnection is an ordinary open input, not an RF action. No port connects to ARM, INIT_OK, KEY, SAFE_OE_N, PROGRESS, either RF connector, an RF power switch or a PA interlock. Firmware treats unavailable expansion as optional and continues native autonomous operation if its core configuration and protection evidence are valid.

Use external driver circuitry for high-power LEDs, relays, motors or inductive loads. Debounced buttons, low-current indicators and modest-speed encoders are suitable. Timing-critical waveform generation, FoxPro serial timing, CW/slot edges and protection signals cannot be moved to this I²C expander merely because it has spare bits.

The only genuinely unused module GPIOs are 3,45,46, all reserved straps. UART43/44 are occupied, GPIO35–37 remain essential, and flash/USB/RTC/LoRa/RF-control pins are not spare.

| MCU GPIO | Module pad | Normally open service link | Isolated access pad | Limitation |
|---|---|---|---|---|
| 3 | 15 | JP1 | TP81 | JTAG strapping; service only |
| 45 | 26 | None | None | Flash-voltage strap retained NC; no accessory access |
| 46 | 16 | JP3 | TP83 | Boot strap and input-only |

GPIO45 has no breakout: a local service escape could not be accommodated around the reviewed SPI/core routing with ordinary via and service clearances. M6-L2 uses the allowed access limitation rather than changing the flash-voltage strap or safety routing. The actual module pad remains unconnected.

The two service links remain physically open in every standard population, including both optional interfaces. Accessories attach only after the open link, so they cannot load a strap in the default build. Closing a link is a controlled service modification: remove accessory power/connections before reset, inspect strap conditions and restore the link open afterward. These are individually identified service pads, not ordinary unrestricted digital outputs. The default module pull/strap configuration is retained; no safety signal is moved to recover pins. Physical accessory, reset, short, sequencing and strap tests remain **NOT_RUN**.
