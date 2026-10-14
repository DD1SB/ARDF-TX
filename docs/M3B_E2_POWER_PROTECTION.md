# M3B-E2 — bounded power protection review

Date: **2026-10-15**. **Design calculations and passive surrogate simulations only. Every physical safety/RF/thermal test is NOT_RUN.** E2 corrects U311 so the analog threshold circuit has its intended reference; it does not prove reference startup or fault timing. [Machine results](M3B_E2_POWER_RESULTS.json), [input deck](../hardware/80m/review/M3B-E2/input-surrogate.cir), [driver deck](../hardware/80m/review/M3B-E2/driver-surrogate.cir). Reproduce with `python3 tools/m3be2_power.py --write`. No electrical power-component values were changed from E1.

## Actual input chain and limits

J301/F301 → **D301 SS34** reverse barrier → `VIN_PACK` (sense/C314100nF50V) → **R3501.5Ω1W** → `VIN_PA` (**C350100µF35V**, D302SMBJ17A) → TPS54302 buck → `VPA` → TPS22810 → `VPA_ISO`/R330 → `VPA_LOAD` → R410 → `VDRV`. TPS22810 is on the regulated PA rail; a failed buck can expose it to the input. It is not a28 V input protector. Local3.3 V comes independently from the controller/fixture and may not be confused with raw pack voltage.

With corrected U311 wiring, nominal reference-feed current is `(3.3−2.495)/180`=4.472mA. The five resistor-divider loads draw≈1.110mA total, leaving≈3.362mA cathode current before bias/leakage. This is a nominal DC calculation, not proof of TL431 startup/stability over tolerance and temperature. Stage1 must measure VREF near2.495V and each actual comparator trip before relying on the protection logic; failure blocks power-stage tests.

Protected normal4S is **12.0–16.8 V**; TPS22810 recommended VIN≤**18 V**, absolute20 V. Its typical turn-off **3.3µs** is under specified TI test conditions (RL10Ω,CIN1µF,CL0.1µF,CT2.2nF); the board CT is4.7nF. This is not a maximum complete comparator/logic/switch isolation delay. [TI SLVSDH0C, Jan2018](https://www.ti.com/lit/ds/symlink/tps22810.pdf).

E2 names the TVS manufacturer: [Littelfuse SMBJ17A](https://www.littelfuse.com/assetdocs/littelfuse_tvs_diode_smbj_datasheet.pdf?assetguid=09a6ae9a-73cb-4ac4-acac-e6dab92ab953). Stand-off **17 V**, breakdown **18.9–20.9 V at1mA**, pulse clamp **27.6 V at21.8 A**. None guarantees18/20 V protection. Its presence is not credited as such a clamp. A different nominal17 V vendor is not silently substituted.

| Mechanism / calculation | Result and limitation |
| --- | --- |
| Insertion series-RLC corners | 32 analytic corners,16.8/17.0 V steps, L0.1/1/10/100µH, sourceR0.02–1Ω, damper minimum1.4775Ω, C80–145µF. At assumed **L≤10µH**, analytic peak≤17.0 V. 17.0 is a sensitivity step, not an allowed charging voltage |
| Detailed passive surrogate | 24 actual ngspice cases, generic diode/upstream10pF/40/110nF, cable/source corners. At L≤10µH post-damper peak16.972 V; upstream undamped node can reach21.738 V. C31450V retained;309k/10k sensing gives≈0.682 V at that peak |
| Outside-envelope100µH | Analytic17.0 V step reaches**18.00013 V**; passive surrogate downstream17.633 V. Neither licenses that harness; difference exposes model sensitivity |
| C tolerance / ESR | C350−20% and conservative high-C corner used; surrogate ESR0.03Ω is an assumption, not all-temperature proof. C404/ceramic derating, PCB ESL and actual wiring must be measured |
| Inrush/fuse | Conservative I²t=CmaxV²/(2Rmin)=**0.01399 A²s**,18.3% of fuse nominal0.0766 A²s. No guaranteed minimum-melting/repetitive life margin. Littelfuse4671.5A32V has35A interrupt capability; external BMS fault-current coordination remains essential |
| R350 heating | At0.6 A,0.54 W active/0.108 W at20%;1.296 Wh/12h. At0.8 A,0.96 W active before hot derating. Neither a1 W label nor a fuse authorizes sustained hot overload |
| Disconnect | 10µH at0.8 A stores3.2µJ; connector arcing, source energy, buck energy and ground bounce are additional unmodeled mechanisms. Input+rail discharge/reconnect must be scoped |
| Wrong positive24 V supply | Excluded. Illustrative assumed20.9 V TVS node implies≈2.07 A, **6.41 W in R350 /43.19 W TVS**; not a nonlinear DC TVS model. Fuse timing cannot guarantee semiconductor survival. A supply may reach unsafe voltage before it opens |
| Reverse supply | SS34 blocks static reversed input; a charged16.8 V capacitor with−16.8 V source can place33.6 V across a40 V diode. Only6.4 V static headroom; ringing, hot leakage, diode short and incorrect grounding remain unqualified |

The modest E1 damping network is retained for **bounded evaluation**. It is not comprehensive surge/wrong-supply protection. A higher-voltage switch alone would not protect LM5134B and the other downstream parts. No broad power redesign is justified for an unpowered evaluation PCB. **Unrestricted pack connection remains NO-GO.** Before permitting it, qualify measured wiring/source limits, pulse/temperature margins, pack/BMS/fuse interrupt coordination and keyed polarity. If any fail, make a focused protection correction before using that configuration.

## Driver fault, discharge and local layout

[LM5134B SNVS808C](https://www.ti.com/lit/ds/symlink/lm5134.pdf): **4–12.6 V operation,14 V absolute**. R4104.7Ω/C40447µF25V polymer isolate/delay the rail. Panasonic25SVPF47M's nominal30mΩ at100kHz/20°C is not an all-temperature fault-ESR guarantee. The model imposes interruption and does not simulate the comparator/switch/actual buck failure.

| Fault step / imposed opening | Assumed ESR / parasitic L | Simulated peak VDRV |
| --- | --- | ---: |
|16.8V /20µs|0.03Ω /10nH|9.558V|
|18V /20µs|0.5Ω /100nH|10.298V|
|18V /100µs|0.5Ω /100nH|**12.864V — fails12.6V operating gate**|
|18V /20µs|1.5Ω /100nH|11.417V; does not qualify selected capacitor|
|18V /20µs, useful ceramic omitted|0.5Ω /100nH|10.989V|

These are conditional results. Actual VDRV routing totals34.704 mm across branches on F.Cu; the gate traces and returns retain E1 geometry. C404 and local ceramics remain accessible near U401, with nearby ground pads. **10/100nH are sensitivity inputs, not extracted parasitics.** Ground bounce/loop ringing must be measured at the IC pins with a low-inductance probe; a remote rail TP alone is insufficient.

Power disconnect does not imply immediate driver-rail discharge. TPS22810 QOD resistance is265Ω typical/350Ω maximum **at12V**, not a guaranteed low-voltage8V discharge bound. With Cmax≈57.71µF and series/QOD resistance, illustrative8.6→4V times are about**16.4/20.1ms** at265/350Ω (an assumed1kΩ example is longer). Coupled shaper capacitance/backfeed may change this. **INB must inhibit before/while isolation opens; no RF permission may return during the slow decay.** A stopped clock/inhibited driver and the deliberate-rearm latch remain necessary. Scope PA_INB, PA_PERMIT, VPA/VPA_ISO/VDRV together, including brownout.

A simple unqualified zener is not a demonstrated replacement. A nominal10 V clamp under a stuck18 V rail through4.653Ω would draw≈1.72 A and dissipate≈17.2 W while R410 dissipates≈13.8 W, far beyond a small500mW part's sustained capacity. A nominal12 V device's tolerance/dynamic voltage can also exceed12.6/14 V. No such part is installed or credited. If real isolation fails the gate, a properly rated clamp/independent cutoff or rail correction must be reviewed before fitting U401.

## Mandatory bounded bring-up amendments

Use the retained [staged procedure](M3B_BRINGUP_PLAN.md) only with the E2 corrections below; never its old BD140E-C-B instruction or E1 drawings. The review/procedure does not authorize assembly or energizing.

1. **Stage0:** Use E2 netlist/assembly/population map. Continuity-check Q403 **1B→SHAPE_BASE,2C→VPA_SHAPED,3E→VPA_LOAD**, ST illustrated face→PCB+Y. Check U3111K+2REF→VREF and3A→GND. Gauge finished holes, wiring keys, insulated tabs/NTC/sink. No soldering until these pass.
2. **Stage1:** Isolated3.30 V supply, initially100mA limit; raw pack disconnected. Qualify real reset/ARM pulse widths, U202 heartbeat witness/quiet timing, held-ARM non-rearming and fault withdrawal. Use ≤1pF probes/local ground and record probe-loading sensitivity. No PA fitted.
3. **Stage2/Input Gate I:** U401/Q402 absent; external laboratory supply with independently checked **OVP≤16.8 V**, initially50mA current limit, no long leads. Begin at6 V/disabled output, inspect; then12 V with dummy load, advance only after records pass. Input transient measurements at12/14.4/16.8 V must establish VIN_PA≤18.0 V including uncertainty, no dangerous upstream stress, inrush/pulse/hot margin. Do not directly inject24/28 V into the board or use a Li-ion pack to test shorts. The **assumed≤10µH harness** must be measured before pack use.
4. **Driver Gate D:** Keep U401/Q402 absent. Remove L301/disconnect the buck output to avoid back-driving it. Supply safety logic normally. Use a bounded external pulse source, rated fast switch, representative loads and reconstructed C404/local ceramics to apply an upstream-failure surrogate, **maximum18 V**, starting≤20µs, then extending to100µs only after confirming safe pulse limits. Bound peak current≤3A and injected energy≤5.4mJ with an independent timeout; confirm the resistor/capacitor pulse ratings first. The applied fault must persist after the board opens so that the fixture's pulse ending cannot be mistaken for successful board isolation. A continuous source must not depend on this unqualified board for its own shutdown. Record OV input→INB and complete TPS22810 isolation, VDRV peak and decay at cold/hot/low-load corners. Require isolation **≤20µs**, VDRV **≤12.6 V including measurement uncertainty**, no re-enable with ARM held. Exceeding either blocks driver population; repeat with appropriate energy limits, never by sacrificing a driver.
5. **Driver/PA stages:** Only after Gates I/D/L pass may U401 be fitted. Q402 stays absent for dummy-gate/shaper tests; isolate R403 as described in the retained procedure. Then limited PA tests start at12 V input/lowest rail,≤200mA,≤1% marks; stepwise maximum0.8A only after thermal/pulse assessment. Use rated50Ω load, low-capacitance drain probe and insulated thermal sensors. No direct pack or continuous beacon until separately qualified.

Timing gate L still requires physical clear/recovery widths at device pins, ≥2× manufacturer minimum margin (100ns conservative initial target pending exact3.3V/temperature bound), swept ARM/reset/health/SCL edges, no false permit and deliberate rearm. All RF output, harmonic/CW,3W/1.2W/Sprint calibration, Fox10mW/backpower/isolation, BD140 hot SOA, NTC bond, temperature and endurance gates remain OPEN. Separate Fox reference-load and compact30cm radiator/return/loading/30m-audible/250m-not-audible field evaluation remain unchanged.
