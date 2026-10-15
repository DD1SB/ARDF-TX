# M5A-R2 input-AM implementation review

2026-10-15. **Calculated/pre-CAD candidate; sourcing gate OPEN. No implemented R2 circuit or measured AM performance.** The R1 drain-modulated circuit remains unchanged as fallback.

## RF envelope and capability

For net antenna/feed gain −1 dBd, `Pconnector_carrier = ERP × 10^0.1`. For sine AM, `Paverage = Pcarrier × (1+m²/2)` and `PEP = Pcarrier × (1+m)²`. At 1 W carrier ERP and m=0.80 these are 1.258925 W carrier, 1.661782 W average and 4.078918 W PEP at the connector. A 1 dB capability allowance requires 5.135054 W connector PEP.

| Output filter loss, assumed | Module PEP for actual envelope | Module capability including 1 dB | Distance below RA07 6.5 W nonlinear rating |
| ---: | ---: | ---: | ---: |
| 0.35 dB | 4.421 W | 5.566 W | 0.674 dB |
| 0.75 dB | 4.848 W | 6.103 W | 0.274 dB |
| 1.00 dB | 5.135 W | 6.465 W | 0.024 dB |

These distances are **not linear compression margin**. At a different VGG/idle current, clean crest capability can be lower. Filter loss, temperature and unit variation can reject RA07. An 8 W alternative adds approximately 0.90 dB nonlinear-rating distance, without proving AM. Reproducible [RF calculations](../hardware/2m/review/M5A-R2/rf-budget.csv) include 75/80% and 1/0.90/0.30 ERP cases.

Nominal 0.90/0.30 W ERP settings with an illustrative ±0.4 dB total uncertainty span 0.821–0.987/0.274–0.329 W ERP. Real antenna and calibration uncertainty must fit those bounds. The hardware capability investigation remains based on 1 W; no requested capability is removed.

## One concrete input-amplitude route, not yet selected into CAD

The bounded shortlist identified **MACOM MAAV-011017-TR0500**, a 50 Ω analog attenuator covering 144 MHz. [Manufacturer Rev. V4](https://cdn.macom.com/datasheets/MAAV-011017.pdf) provides a complete pin table and application circuit. This is a practical input-AM route, but current cut-tape delivery is unresolved: the recent EU listing has zero stock and incoming dates in December/January. It is not booked as available.

The contemplated connection is:

```text
Si5351 CLK0 -> two series 47 ohm limit resistors -> DC block
 -> existing 50 ohm fundamental LPF -> MAAV RF input pin3
MAAV RF output pin10 -> DC block -> Mitsubishi RF input pin1
MAAV VDD15 = sequenced regulated 3.3V, bypass1nF +100nF
MAAV VMODE16 = GND (negative attenuation slope)
MAAV VC14 = reconstructed, bounded analog envelope control
MAAV ground pins1/5/6/7/8/12/13 and paddle17 = RF ground
NC2/4/9/11 may be grounded per manufacturer instructions
```

The module's high typical small-signal gain makes a direct filtered clock plausible; **actual Si5351 fundamental power and required linear module input remain OPEN**. No expensive driver is automatically carried over. If that direct path cannot supply the required crest with margin, this candidate must be revised before calling the full design complete. A cheap amplifier cannot be assumed to fix it without revisiting the input-power limit.

Two series 47 Ω/1% resistors, a 0–3.465 V bounded clock, DC blocking and a purely passive downstream RF path bound total available AC power to 8.064 mW; one resistor short gives 16.127 mW. This uses `variance(V)≤Vpp²/4`, followed by maximum-power transfer, not a typical Si5351 output estimate. Both are below 30 mW. This bound **does not apply if downstream RF gain is added, the logic rail becomes unbounded, an external RF source is connected, or a damaged attenuator injects supply energy downstream of the limiting resistors**. It proves neither sufficient crest drive nor complete single-fault input protection; downstream fault energy still needs a real circuit disposition. See [source bound](../hardware/2m/review/M5A-R2/source-power-bound.csv).

## Audio/control and bias

Retain ESP32-S3 filtered PWM; there is no assumed internal S3 DAC. The existing LEVEL/AF reconstruction can supply the new control after adaptation. Required voltage-envelope dynamic range is 15.07/16.90/19.08 dB at m=0.70/0.75/0.80. A sine in **control voltage** is generally not a sine in RF voltage: use the inverse attenuator transfer, then a single end-to-end RF calibration. A 32 dB range is mathematically adequate for the modulation span plus the 5.23 dB carrier-profile difference. Device control settling, reconstruction phase/ripple, temperature drift and AM-to-PM remain physical acceptance items.

MACOM requires VC/VMODE zero during supply transitions and a limited supply ramp. **VMODE=VC=0 selects minimum attenuation, so this state is not an RF mute.** Independent source inhibit, zero module bias and drain isolation must cover it. A divider must bound normal VC to ≤2.5 V including logic/reference tolerance; clamping/default logic must also cover power sequencing. Raw PWM into VC is unacceptable. No completed clamp/filter/enable network is claimed here; the sourcing gate stopped circuit implementation before these could be represented honestly as a finished schematic.

VGG establishes a **fixed** quiescent operating point during a slot; it is not the sine modulator. Start at zero, adjust using current-limited bias commissioning, bound VGG below its conditional maximum, and independently pull it to zero on inhibit. The 0.30 A idle bias used in the energy model is an assumption, not a Mitsubishi recommendation. Gate-off alone has finite RF feedthrough; source inhibit and drain disconnect are still needed for off-slot silence.

Inside an allowed slot the design intent is continuous carrier with Morse-keyed sine tone; outside the slot all RF permissions are withdrawn. Tone frequency 800 Hz and THD ≤5% are engineering test choices, not rulebook mandates. No 70–80% claim can be inferred from a correct control waveform or ideal simulation.

The older [SMP1307 PIN attenuator application circuit](https://www.skyworksinc.com/-/media/SkyWorks/Documents/Products/1-100/200327B.pdf) is documented but its quad diode is now EOL; Mini-Circuits [PCN24-012](https://www.minicircuits.com/pcn/PCN24-012.pdf) likewise rejects RVA-33+/RVA-2000V35+ as current production choices. No undocumented diode substitution was made to force a low price.
