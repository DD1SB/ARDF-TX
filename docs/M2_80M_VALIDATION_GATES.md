# Acceptance gates for the derived 80 m module

Date: **2026-10-13**. **All hardware gates NOT RUN.** This plan specializes [M2 evaluation](M2_RF_EVALUATION.md) for the proposed HF core. VHF gates and architecture remain unchanged. [ADR-0010](decisions/ADR-0010-proven-80m-core-and-power-target.md) proposes revising the old mandatory 5 W and seven-pole implementation assumptions, subject to review.

## Minimum shared evaluation hardware

Use one shared current-limited 6.0–8.4 V supply/control/safety fixture, one programmable Si5351 source and **one reproduced LM5134B/IRF610/transformer/reference-filter coupon** with replaceable supply connections. Start at publisher settings using laboratory rails, then attach the economy buck and QCX-derived shaper. A temporary coupon is not a fourth product PCB; no coupon layout, fabrication or order is supplied here.

Add a separate TinyFox-style buffer/filter/pad coupon with its bounded rail, starting with the watt PA absent. Compare the existing BJT buffer if the logic path fails. Two passive accessories evaluate the long wire and compact radiator with representative enclosure/pack geometry. A shared external host supplies I²C/GPIO stimulus through hardware ARM, lease and trips. No duplicate MCU/RTC, onboard precision meter, DAC or display is needed.

First-sample material allowances: safety/control/power fixture €8–15; source €3–6; watt coupon €12–20; Fox coupon €3–8; antenna fixtures €19–30. **Total €45–79 estimated**, excluding cables/loads, instruments, calibration and labor. Repeat critical results on **three independent RF builds** after the first sample passes. Do not build a fleet to discover a basic circuit failure.

Instruments: calibrated HF wattmeter and ≥10 W 50 Ω load; calibrated low-level sensor/RF voltmeter for 10 mW; ≥100 MHz oscilloscope with suitable drain-rated, low-capacitance probes/current shunt; spectrum analyzer through ≥1 GHz with attenuators; calibrated VNA/impedance bridge; stable reference/counter and logic analyzer; current/Wh logger; thermocouples/hot environment; mismatch fixtures; representative ARDF receivers and surveyed field paths. SDRs/simulators supplement these tests. Instrument access and cost remain open.

## Go/no-go criteria

Limits are **project targets** unless traced to IARU. Country emissions requirements, referee interpretation and uncertainty must also be resolved. No gate currently passes.

| Gate / trace | GO evidence | NO-GO response |
| --- | --- | --- |
| **H0 fail-off**; RF80-006/007, VSAFE | Boot, brownout, unplugged control, stuck key/clock, missing lease, stale ARM and forced analog faults default RF off. Persistent latch requires fresh rearm. Direct inhibit ≤1 ms; lease ≤250 ms; overcurrent initially ≤100 µs or faster as exact SOA requires. Measure supply disconnect, discharge and I²C backpower. | Any burst, excessive current or automatic restart blocks powered testing. Stuck-high drive must survive analog trip; software order is insufficient. |
| **H1 source**; RF80-007, RULE-001/002 | Every intended channel in 3.510–3.600 MHz, endpoints/divider stress: stability **better than 50 ppm** across supply/temperature, project aim ≤10 ppm; close-in/wide spur records and off-slot/retune silence. | Revise source/reference/returns if a required channel fails. Do not silently remove channels. Internal clocks can radiate despite output gating. |
| **H2 normal power**; RF80-001/002 | Reproduce reference 50 Ω points first. Classic target 1.2 W has its entire uncertainty interval within 1–5 W; Sprint 0.85 W within 0.3–1 W, all channels and 6–8.4 V. Record post-filter mark power, PEP and duty average separately. | Low-battery/drive failure requires supply/match/target revision and recosting. Optional 2–3/5 W needs separate measured capability, stress and thermal evidence. |
| **H3 Fox power/protection**; RF80-004/006, ADR-0004 | Own reference gives nominal 10 mW, provisional ±10% including uncertainty pending referee agreement. Measure pre-pad maximum, drive/backfeed input energy, rail/current limits, stored energy and guard shutdown. Normal PA/boost are DNP in Fox-only builds. | Change buffer/pad/guard if drive is insufficient or power unbounded. Neither 72 mW DC input nor matched-pad arithmetic proves nominal RF power. No watt-to-Fox routing. |
| **H4 shaping/retune**; RF80-006/007, VSPEC | Both branches: **3–8 ms 10–90% edges**, ≤10% overshoot, no DUT-related clicks at adjacent ±20 kHz in receiver/spectrum tests. Inhibit PA before divider/level changes; no unwanted carrier. Maintain drive during graceful decay, then disconnect. | Hard-keyed reference claims do not pass. Repair ramp backpower/ringing/clicks. Emergency shutdown bypasses shaping and still passes SOA/transient tests. |
| **H5 spectrum/stress**; VSPEC, VTHERM | Country mask and project HF aim **−50 dBc** where applicable, absolute floors recorded. Measure filter loss, core variation, polarity and power. At provisional 50°C ambient: TJ ≤125°C, ≥20% normal gate/drain stress margin and exact hot SOA respected. VSWR ≥3:1 phase sweep and controlled open/short tests cause safe operation/trip without damage. | Ratings, filter labels and ideal SPICE are insufficient. Change magnetics/filter/shaper/thermal protection as needed. Indefinite open/short survival is not presumed. |
| **H6 antennas/field**; RF80-005/008/009, RULE-003 | Long-wire complex-load tests, qualified source VSWR ≤2:1, loss/current/reactive voltage, symmetric Sprint return and horizontal omnidirectionality. Separate compact Q/SRF/coupling tests with approximately 30 cm radiator, defined return and actual case/pack; field method below. | Native longer wires/reach claims do not establish this compact installation. Change matching/installation while preserving nominal power. |
| **H7 energy**; PWR-001/002/003 | Measure active/idle/retune/LoRa currents, Wh and efficiencies. Selected protected pack lasts ≥24 h at normal specified maximum/profile; characterize cold/aging/ESR/cutoff and peaks. Continuous beacons have a separate service criterion. | Calculations are not a pass. Modeled 5 W/25R4P failure needs measured improvement or qualified higher-capacity cells; no pack above 4P. |
| **H8 system**; CTRL-003, RULE-004/005 | Common RTC/controller handles Classic minute slots, concurrent Sprint groups with 12 s slots/different speeds, beacons and frequency separation. Rule period deviation/overlap ≤5 s; Sprint project aim ≤0.1 s/no intentional overlap. Test no-LoRa operation and RF/LoRa immunity, including an inactive 2 m board. | Timing error, brownout or audible interference blocks release. Another MCU/RTC is not a substitute for tests. |
| **H9 repeatability/cost**; COST-001/002/003 | Three builds reproduce power, spectra, shaping and fault behavior using documented windings/exact active parts. Close 6/10/20 baskets, MOQ/leftovers, PCB stackup, antennas, packs, freight and labor separately. | Recost necessary replacements, heat/shields/matching. Do not book conditional Fox deletions or claim €20 from allowances alone. |

Off-slot searches retain the bench aim ≤−70 dBm with declared RBW, detector, reference plane and time capture, plus on/off receiver comparisons and near-field probing. This finite floor does not rewrite IARU's silence requirement. Close-in interference may fail even when harmonics pass.

## Reproducible compact field method

Calibrate 10 mW at the reference load before and after field testing. Record channel/code/speed, radiator length, return, coil/tap/trimmer, mounting height, case/pack orientation, soil/weather and receiver settings. Keep applicable installations uniform; no changes during an event.

Survey actual/nominal map positions, then 30 m and 250 m points in several azimuths, including the strongest direction and a favorable open/dry path. Use a sensitive competition receiver and a beginner receiver. Fix gain/bandwidth/headphones, record audio/noise, and alternate blinded transmitter-on/off trials. Provisional criterion: correct code in ≥9/10 trials at the nominal point and 30 m; no above-chance detection at 250 m. Referee agreement remains open; a quick subjective walk is insufficient.

Repeat wet/dry conditions and representative grounds/pack placements. Demonstrate horizontal coverage and no map-point blind spot. Conducted power and good matching do not predict reach. If 250 m is audible, adjust compact coupling/loss/return; if 30 m is inaudible, improve efficiency/coupling. Preserve nominal 10 mW and the protected port. A Classic wire cannot substitute.

## Measurements simulation cannot replace

1. Source spurs, drift and off-slot radiation.
2. Loaded PA power/efficiency and gate/drain/current waveforms at low battery/mismatch.
3. CW envelopes/clicks, startup/retuning and stuck-drive faults.
4. Fox RF/transient/backfeed ceilings and ≥47 dB main-to-Fox isolation for the 5 W option.
5. Real core/filter losses, shaper hot SOA and beacon heat.
6. Compact loading and blinded 30/250 m audibility.
7. Pack energy/peaks, autonomous timing and optional-LoRa immunity.

**GO** for architectural review/shared-coupon specification. **NO-GO** for complete layout, procurement/manufacture or hardware acceptance. Physical evaluation needs a subsequently reviewed scope. H0–H5 bench evidence precedes full layout; H6–H9 field/pack/integration checks remain mandatory for release.
