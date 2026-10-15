# M5A-R1 — low-voltage true-AM feasibility

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

**Plausible but unqualified evaluation candidate.** There is no retrieved manufacturer result demonstrating 70–80% sinusoidal RF AM from the changed chain. The integrated schematic implements supply feedback and tone reconstruction; only a measured RF-envelope transfer can show that it produces the required emission.

Use continuous carrier within SLOT and keyed sine audio; outside SLOT both branches are inhibited. Preserve the [R0 PWM/controller contract](M5_2M_CONTROLLER_INTERFACE.md): ESP32-S3 supplies coherent LEVEL_PWM and AF_PWM, initially 800Hz tone,312.5 kHz PWM and appropriately scheduled samples. Two 10 kΩ/4.7nF unity-gain Sallen-Key stages reconstruct the waveform; no S3 internal DAC is assumed. KEY switches carrier-only reference versus sine at matching phase, with approximately 3ms amplitude ramp. No IARU-mandated tone frequency is invented.

R1 changes normal feedback to 18 kΩ/10 kΩ, gain 2.8, improving low-voltage PWM resolution. U401C drives ST BD139/Q402 and D45H11/Q401; R506 falls 100 Ω→10 Ω. The previous 100 Ω lost 3.4 V at 34 mA base current, enough to prevent the intended low-voltage crest. R507 = 8.2 Ω/helper clamp remains an approximate 73 mA limit, not a precision RF current regulator. Retain separate 1.8 A upstream-current trip, default base pull-up, command/helper clamps, driver switch and gate-bias inhibit. Feedback compensation 4.7nF and 101nF drain decoupling are starting values; no large electrolytic belongs on the modulated drain.

## Explicit transfer hypothesis

Illustrate, do not assert, `A_RF ∝ max(Vdrain−0.6 V,0)`, anchored to the original 5 W/7.2 V connector point. With this hypothetical knee, the required supply waveform is `Vcenter + m_RF(Vcenter−0.6)sin(ωt)`; supply fractional modulation is smaller than RF depth. A naïve4V center/0.8 V trough is not evidence of usable RF behavior.

| ERP carrier | Assumed center V | Crest/trough V at RF m=0.8 | Upstream V |
| --- | --- | --- | --- |
| 1 | 3.912 | 6.561 / 1.262 | 10 |
| 0.9 | 3.742 | 6.255 / 1.228 | 10 |
| 0.3 | 2.414 | 3.865 / 0.963 | 7.5 |


The 1 dB capability investigation corresponds to roughly 7.288 V drain under this same hypothesis. This is independent of normal operating crest and must include actual output losses. If the PA acts as a voltage-independent linear amplifier, supply modulation will be too shallow. If it enters the knee, changes bias, oscillates, or has a nonlinear transfer, a sine supply can give clipped or distorted RF. A monotonic inverse calibration is permissible only after measured amplitude/phase maps show an acceptable waveform; it must not mask missing crest capability or unsafe trough bias.

Only the final drain is modulated. PHA-1+ runs from fixed 5 V, its output drive calibrated; gate bias has its own filtered fixed setting. Do not modulate APC, driver rail or gate threshold to hide an unusable drain transfer. The provisional R0 bias network needs temperature and low-drain review against the actual ST arrangement before RF layout.

## Headroom and low-voltage base drive

At full modeled crest, PA current is about 1.36 A and β40 implies 34 mA D45 base drive. With 1 V pass VBE,10 Ω base resistor,8.2 Ω emitter resistor,0.3 V helper VCE and 0.2 V path allowance, required headroom is approximately 2.12 V. A 10 V rail−3% leaves about 2.21 V above the 7.288 V capability illustration: approximately 0.29 V remains under that particular crest-current bound. At the reserve-capability current it is smaller; margin is conditional. β20 can consume the margin or helper-current ceiling; it is not accepted automatically. Measure hot beta, op-amp drive, crest droop and loop recovery. R506's dissipation at 73 mA is 0.053 W; its 1 W/pulse allowance is retained pending exact part selection.

Use `m=(Amax−Amin)/(Amax+Amin)` from RF voltage envelope. Gates:70–80% depth at every supported channel/profile, nominal 75%, no trough clipping or RF bursts, envelope THD≤5% and sideband imbalance≤1 dB as initial engineering targets. These last two are project criteria, not IARU rules. Measure crest 4.079 W connector and test 5.135 W capability with the stated uncertainty/loss budgets. Neither supply oscilloscope shape nor an ideal op-amp simulation proves this.

D45 tab is collector/VPA; BD139 collector/tab is MOD_SINK. Neither may share an uninsulated grounded PA spreader. The [power/thermal review](M5A_R1_POWER_THERMAL.md) retains the 66 °C sensor trip and specifies a cooler assembly. Training still uses the independent current-modulated BJT; its 104 fitted physical positions are electrically unchanged after effective variant values are applied.

The previous R0 ideal behavioral simulation is archived. R1 provides analytical envelope trajectories and passive transient calculations; no new transistor/RF AM simulation or physical distortion pass is claimed. Vendor RF/nonlinear models, feedback phase margin and real component beta/storage remain OPEN.
