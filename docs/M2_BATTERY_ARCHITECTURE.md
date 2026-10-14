# M2 battery architecture: 2S and 4S

Date: **2026-10-14**. **Engineering proposal; no hardware validation.** The user's new endurance requirement replaces the earlier blanket 24-hour maximum-power objective. It does not accept a new circuit, battery or ADR. Read [the proposed decision](M2_POWER_ARCHITECTURE_DECISION.md), [dated evidence](M2_POWER_ARCHITECTURE_SOURCES.md), [power modes](M2_POWER_MODE_COMPARISON.md), [calculations](M2_ENDURANCE_REWORK.md) and [costs](M2_BATTERY_COST_COMPARISON.md) together. Previous M1/M2 reports remain historical evidence; [ADR-0011](decisions/ADR-0011-dual-voltage-power-and-endurance.md) proposes the changes to ADR-0006/0007 and pending ADR-0010.

The preferred direction is **2S for Foxoring and an economy near-1 W configuration; 4S with a bounded buck supply for higher-power 80 m and a universal unit**. Retain the existing 2S boost alternative for 2 m until measurements resolve the 4S AM headroom problem. There is no justification yet for a universal buck-boost converter or unregulated 16.8 V PA feed.

## Pack domain and compatibility

| Pack | Cells | Nominal / charged / initial operating endpoint V | Usable Wh, 2.45 / 3.35 Ah assumptions | Intended capability |
| --- | ---: | --- | --- | --- |
| 2S1P | 2 | 7.2 / 8.4 / 6.0 | 11.43 / 15.42 | Compact Foxoring; Sprint; near-1 W Classic with limited endurance |
| 2S2P | 4 | 7.2 / 8.4 / 6.0 | 22.86 / 30.84 | Economy HF; boosted HF/VHF subject to current and runtime |
| 2S3P | 6 | 7.2 / 8.4 / 6.0 | 34.29 / 46.27 | Retained boosted VHF alternative |
| 2S4P | 8 | 7.2 / 8.4 / 6.0 | 45.72 / 61.69 | Maximum retained 2S configuration |
| 4S1P | 4 | 14.4 / 16.8 / 12.0 | 22.86 / 30.84 | Higher-power HF; VHF full-power headroom restricts usable energy |
| 4S2P | 8 | 14.4 / 16.8 / 12.0 | 45.72 / 61.69 | Universal maximum candidate, normally one active RF band |

Wh uses 0.80 aging × 0.90 discharge-window × 0.90 temperature provisions; M35A uses the manufacturer's 11.9 Wh minimum energy per cell, rather than the slightly larger nominal-voltage × Ah product. It is not a discharge-curve integration. A higher RF cutoff reduces these figures further. Both selected cell documents use a 2.5 V characterization endpoint; 3.0 V is our conservative operational assumption, with margin for load sag and imbalance still to establish. Pack voltage alone cannot guarantee that every series group remains above 3.0 V. Qualification requires individual-group logging and a suitable external BMS; do not claim cell-level operational cutoff from the sum-voltage comparator.

| Cell candidate | Verified source facts | Engineering boundary |
| --- | --- | --- |
| Samsung INR18650-25R | Manufacturer document: 2.50 Ah at 0.2C, at least 2.45 Ah at 10 A to 2.5 V; 20 A at 25 °C; initial AC impedance ≤18 mΩ at 1 kHz. Charge 0–60 °C, discharge −20–75 °C, with recovery-temperature restrictions. | AC impedance is not pack DC resistance. The published 250-cycle high-current condition permits only 60% capacity; our 80% aging allowance needs a maintenance/replacement policy. |
| Molicel INR18650-M35A | Manufacturer: typical 3.50 Ah, minimum 3.35 Ah, nominal 3.6 V, charge 4.2 V, discharge 2.5 V, discharge maximum 10 A. Standard/maximum charge 1.7 A; charge 0–60 °C, discharge −40–60 °C. Supplier currently shows stock. | One-page sheet does not establish DC resistance or an equivalent cycle-life guarantee. Its cold/current behavior cannot be substituted for 25R behavior. Use minimum capacity in selection, typical capacity only as sensitivity. |
| Samsung 35E / Sanyo NCR18650GA | 35E retained as an out-of-stock historical comparison. NKON GA Green shows stock, 3.45 Ah-class/10 A supplier description. | GA exact lot/manufacturer specification and batch quote not closed; M35A is the costed high-capacity candidate. No reclaimed/old-clearance cells selected. |

The historical 3.40 Ah calculations and a 3.50 Ah typical case are also retained in the [results](M2_POWER_ARCHITECTURE_RESULTS.json). No assumption of equal resistance, current rating, temperature capability or life is made between cell classes.

## What higher series voltage actually saves

For the same cells and same total input power, 4S1P and 2S2P have equal energy and equal per-cell current. If one cell has resistance `r`, pack cell resistance is `r` for 2S2P and `4r` for 4S1P; halving pack current gives the **same cell I²R loss**. The analogous eight-cell packs behave the same way. Wiring and BMS loss can fall to a quarter if their resistance is unchanged. This is conditional because 4S BMS hardware differs.

For illustration only, at 12 W input, 7.2/14.4 V gives 1.67/0.83 A. A 50 mΩ common wiring/BMS resistance dissipates 0.139/0.035 W, saving 0.104 W while transmitting, approximately 0.021 W at 20% duty. Neither resistance nor this loss is measured or separately added to the model's conversion allowance.

## 80 m: reuse the proven RF core, change its supply

The actual schematics and pinned revisions are preserved in [the reference comparison](M2_80M_REFERENCE_COMPARISON.md) and [annotated circuit extracts](M2_80M_RF_TOPOLOGY.md). The reference layouts are research material, not ARDF-TX layout proposals.

| Topology / supply | What can be reused | 4S assessment |
| --- | --- | --- |
| ON7YD ATX80B, IRF610 | Published measurements into 50 Ω: 2.9 W/61% at 12 V drain, 4.8 W/65% at 15 V; driver remained at 12 V. Combined output match/filter and oscillator/keying warning retained. | Raw drain feed may be feasible, **with separately bounded driver**, but no 16.8 V measurement or arbitrary-load qualification. Approximate interpolation between 15 V/4.8 W and 18 V/7.1 W gives 6.18 W at 16.8 V: not a safe championship maximum. Calibration or regulation required. |
| SignalSlinger/FlexFox80, LM5134B–IRF610 | Si5351, TTL driver, bifilar transformer, original elliptic filter. Author's SignalSlinger voltage table: approximately 1/2/3/5 W at 5/6.3/7.6/10.2 V. | **Best candidate for one 4S buck**, approximately 5.5–10.5 V before key shaping. Driver 4–12.6 V operating, 14 V absolute maximum: direct 16.8 V forbidden. LTC3600 is a 4–15 V input part and cannot simply replace its old boost input with 4S. |
| QCX three BS170 Class E | Proven 5 V drive, resonant drain stage, filter, analog key shaper. Manufacturer/project recommends 7–16 V operation. | Fully charged 4S exceeds that published recommendation; higher resonant drain peaks/mismatch and shaper stress require checks. A buck is still appropriate. No demonstrated cost advantage over one IRF610; do not rebuild the PA merely for native voltage. |
| DF1FO Midi Classic, SN75452 | Proven 6–9 V PA supply, regulated 5 V oscillator/logic, antenna-tuned match; about 1 W at 9 V and 0.5 W at 6 V author claims. | Needs a bounded 9 V buck plus 5 V logic. No raw 4S reuse. Lower-voltage alternative remains useful but does not eliminate conversion or supply a proven 5 W growth path. |
| DF1FO Sprint / HG0HK | DF1FO 5 V HC240 circuit is documented but native 50–80 mW is below current Sprint minimum. HG0HK author describes 1S operation. | Neither establishes an interchangeable 1–5 W/50 Ω 4S solution. HG0HK circuit evidence remains incomplete; no reconstruction or invented efficiency. |

Propose a TPS54302-class, 28 V input, 3 A buck with discrete bounded feedback selections. Reuse the RF core and key shaper; **converter, selection/OV circuitry, key-shaper bias and thermal adaptation are new work**. Start with 3 W normal target, 1.2 W extended target; keep a 5 W alternative with additional thermal provision. Driver and PA supply switch together, with INB hard mute and independent physical rail isolation. No source-active/driver-high startup sequence. Retune with source and PA muted, confirm the rail/frequency before arming.

A low setting around 5.5 V can serve depleted 2S; the same buck cannot supply 7.6–10.5 V from 6 V. Firmware capability validation and independent undervoltage inhibition must reject an unavailable higher setting. A 2S higher-power population retains the existing boost-plus-adjustable-buck proposal; it is not compulsory on Fox-only or 4S assemblies. Foxoring uses its own bounded low-power branch, filter, reference-load calibration and compact matching; **normal PA/driver/buck remain DNP in Fox-only population**.

## 2 m: supply simplification does not close RF qualification

Retain Si5351 evaluation source, preferred MMIC driver, PD55008, feedback-controlled sinusoidal series AM, independent training branch and existing fail-off gates. The unresolved GVA-84+ compression margin remains unresolved. ST's 8 W/15–17 dB gain data is at 500 MHz, 12.5 V, 150 mA bias; its 40 V drain rating is not proof of clean 144 MHz operation or safe 16.8 V resonant peaks.

The retained full-power calculation uses 6.667 V carrier-center drain, 80% modulation, 1.333 V trough, 12 V crest and 13.5 V upstream supply. Thus even ideal raw 12 V cannot maintain the crest with a series modulator. With provisional 1.5 V pass headroom and 0.7 V buck/wire margin, **14.2 V pack cutoff** is the initial full-power 4S case. The extra accessible-energy fraction is unknown; 0.65 is a planning scenario, with 0.45–0.85 sensitivity, not a measured SOC mapping.

| Alternative | Consequence / disposition |
| --- | --- |
| 2S boost to 13.5 V | Retains headroom to 6 V pack endpoint subject to peaks/efficiency; TPS611781 supports 2.7–20 V input, 4.5–20 V output. Still conditional RF/AM hardware. |
| 4S buck to 13.5 V | Removes boost, retains bounded modulation rail; loses full-power capacity below headroom cutoff. Reduced preselected ERP profile can use a 9–10.5 V rail down to 12 V. |
| Raw 4S feeding series modulator | PA drain is still bounded, never directly raw. At 16.8 V full-tone pass loss rises to 5.29 W mean/6.35 W peak; no-tone loss 6.29 W. Additional cooling offsets silicon savings. Not preferred. |
| Lower crest: center 6.0 V / crest 10.8 V / rail 12.3 V | Needs about 13.0 V input with retained margins. Must establish clean PEP/gain at lower drain voltage; a 0.85 energy-window scenario still gives only 11.6 h on four M35A cells. Not booked as a 4S1P solution. |
| Still lower crest / altered match / economical lower-voltage PA | Potential full-range 4S1P solution if measured gain/PEP and modulation pass. Requires RF operating-point/matching qualification, not just voltage arithmetic. Keep preferred MMIC and existing PA first. |
| Universal buck-boost | Adds switches/magnetics/control solely to recover lower-SOC full-power operation. Not preferred until smaller-pack savings and measured necessity justify it. |

The pass transistor, helper, quiet 5 V supply, PA matching and driver must be tested together. D45H11 emitter sees bounded 13.5 V with buck, or raw 16.8 V in the rejected comparator. Helper base-current voltage/heat and capacitor current need reevaluation. Preserve ≥2× current margin against exact-vendor hot **DC** SOA, measured thermal limits and 70–80% modulation. A transistor's pulse/current/watt rating is not an SOA pass.

At 40°C ambient, the raw 4S no-tone pass loss of 6.29 W and a 110°C junction target permit total junction-to-ambient resistance of only 11.1°C/W. Subtracting the retained D45H11 2.5°C/W junction-to-case and an assumed 0.5°C/W interface leaves **about 8.1°C/W maximum dedicated sink resistance**. This is a static stress calculation, not a selected or measured heat sink. The previous 10°C/W starting sink is insufficient for that raw 4S case; shared PA/driver heat requires a larger thermal path. Carrier-only intervals and fault trajectories must be tested, not approximated by the modulation crest alone.

The base-current helper also gets hotter with raw 4S. At the retained 70 mA sink provision, approximate collector voltage `V_supply−0.7 V` and emitter 0.6 V give **about 1.09 W at 16.8 V versus 0.85 W at 13.5 V**. These are worst-current design calculations, not average measurements. A tiny unqualified helper is unsuitable; establish exact-vendor hot SOA, current-limit resistor dissipation and installed temperature alongside the pass transistor and PA.

## Controller and distribution contract

Retain the existing `VLOG3.3` interface feed from the controller for module safety, presence and gated local synthesis. The shared external fixture supplies this rail as well as raw battery power. Source current is an additional controller-converter load in the energy model, rather than a raw 4S-to-3.3 V linear-regulator assumption. Budget active-source conversion separately from controller idle and measure efficiency at the combined load. Local source gating and bus isolation still prevent backpower. The independent VHF 5 V buck supplies driver/control/training functions; the watt-supply converter can remain off during training.

The proposed controller accepts **6.0–16.8 V operating**, with tolerance/transient bounds to qualify. Replace TPS62160 (17 V maximum input), PMPB20XPE (20 V drain rating) and SMBJ8.5A. The 8.5 V TVS must **not** remain on a 4S input. Costed candidates use TPS54302DDCT, existing 40 V DMP4015SPS pair with VGS clamps, and an independently selected TVS. MCP1703A's 16 V maximum also excludes raw 4S: supply VHF driver/control from a gated buck-to 5 V plus quiet filtering.

The TPS54302 is active, 4.5–28 V/3 A,400 kHz with internal compensation, soft start and pulse skip. It is not footprint-compatible with TPS62160 or AP63200. EN can float enabled and is rated only 7 V: **external pulldown/bounded drive required for RF converters; never tie EN directly to 4S**. Bootstrap refresh/near-dropout regulation must be measured. Cheap AP63200/03 alternatives offer 32 V ratings, but current indexed availability conflicts/out-of-stock prevent selecting their cheaper price as a buildable baseline. Neither spread spectrum nor high headline efficiency demonstrates acceptable receiver noise.

Keep controller 3.3 V independent of switched RF power. Each RF board has its own PA conversion/filtering and hard isolation; quiet synth/control rails and high-current PA loops return separately to the pack distribution point. Do not send 144 MHz through the controller harness or use an antenna return as a DC power path. Reuse existing fuse/monostable/POR/latch/overcurrent functions; measure the effective rail-off state and discharge time, not only EN logic.

Proposed battery connector functions: power+, power return and passive PACK_ID. No connector footprint locked. Use distinguishable resistor windows for 2S and 4S, with open/short/invalid windows rejected; measure battery voltage independently. IDs are capability evidence, not energy gauges. Never infer cell count solely from a stored software field. Normal RF arms only after identity, voltage and module capability agree. Hardware must default to source mute and rail off when control supply or ID disappears. Physical charger keying provides a separate barrier against misidentification; a wrong resistor must not expose a low-voltage device to raw 4S. All redesigned raw-input paths must tolerate 4S even when unarmed. Unrevised 2S-only circuit proposals are not automatically plug-compatible with 4S.

One reviewable ID starting point is a 100 kΩ pullup to 3.3 V with a 10 kΩ 2S pack resistor or 47 kΩ 4S resistor: nominal 0.300/1.055 V, proposed acceptance windows 0.20–0.40/0.90–1.20 V. Short gives 0 V, open 3.3 V, both invalid. RC acquisition, resistor tolerance, leakage, ESD and ADC accuracy require qualification; voltage validation independently rejects a 4S voltage with a 2S ID. For a 2S-only boost/LTC population, an immutable hardware input-overvoltage inhibit must keep the downstream LTC/driver isolated before 4S can reach it, even with a wrong ID or MCU fault. An off boost can pass input through a body-diode/precharge path; EN alone is insufficient. Gate placement and these comparator/support counts are proposals, not a demonstrated one-fault safety circuit.

Provisional operating inhibition: 2S below 6.0 V,4S below 12.0 V; additional full-VHF cutoff near 14.2 V. Actual comparator tolerances, voltage sag, hysteresis and weakest-cell behavior determine final thresholds. After an undervoltage trip, latch off; no repetitive RF bursts or automatic in-contest power reduction. Existing module PRESENT/capability and power-mode functions carry module restrictions; no added RF MCU/RTC/DAC. A shared external fixture exercises every module independently.

RV-3032 retains time through its documented backup switchover using a separately qualified hold-up capacitor/coin-cell option; the existing EUR0.30 capacitor is an **unqualified allowance**, not guaranteed retention. Do not charge a primary backup cell. Verify RTC flag/clock continuity at pack removal. Without validated backup/time, reboot leaves RF unarmed until synchronization. LoRa absent is fully supported; RTC timing never depends on reception.

Charging/protection stay inside external pack/accessories. 2S CC-CV 8.4 V and 4S CC-CV 16.8 V chargers require physically incompatible pack charge interfaces, labels and qualified voltage/current/termination behavior. No passive universal barrel adapter or parallel-pack charging. LaskaKit 4S protection comparator does not establish balancing; the budget includes separate balancing and replacement reserves. Cell/group fuse, per-cell thresholds, imbalance detection, cold charge prohibition and recovery tests remain release gates. These are external battery-pack circuits, **not a fourth primary transmitter PCB**.
