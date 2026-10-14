# M2 power architecture review recommendation

Date: **2026-10-14**. **Proposed direction; physical measurements NOT RUN.** No PCB layout, Gerber, fabrication, procurement or production firmware was performed. Completed M1/M2/Foxoring research and accepted decisions are preserved. [ADR-0011](decisions/ADR-0011-dual-voltage-power-and-endurance.md) requests review of the battery/supply changes; it does not silently accept them.

Recommend a **dual-voltage controller**, compact 2S Foxoring, and **4S plus one bounded buck for higher-power 80 m**. Keep an economy 2S near-1 W population. Prefer **3 W full /1.2 W extended Classic** with the proven SignalSlinger/FlexFox80 Si5351–LM5134B–IRF610 RF core; retain a separately qualified 5 W option. Keep the existing 2 m MMIC/PD55008/true-AM topology: 4S does not yet justify eliminating its boost alternative across the full discharge range.

The strongest result is electrical and economic: 4S permits the HF supply to replace boost+LTC3600+support with a single wide-input buck, keeping the driver below 12.6 V. At equal-cell count, modeled 3/5 W input falls 12.6%/13.4%, and complete higher-power HF material falls **5.78 EUR per unit at ten** after the more expensive 4S pack is included. The 5 W-capable HF board is 21.82 EUR components; a 3 W thermal population is 20.32 EUR, both candidates with substantial unquoted material. Direct 16.8 V feed is not recommended.

For 2 m, the retained 12 V modulation crest needs 13.5 V upstream; a 4S buck cannot maintain that rail to a 12 V battery endpoint. The preliminary 14.2 V full-power cutoff may strand significant energy. Raw 4S feeding the series modulator raises pass dissipation to 6.29 W during carrier-only intervals at 16.8 V and does not solve depleted-pack headroom. More cooling cancels converter savings. A lower-crest PA operating point is worth measuring, but cannot be accepted from the manufacturer's 500 MHz gain/rating or our energy model.

| Use | Preferred evaluation pack/profile | Modeled 12 h full /24 h extended result | Material at ten, excluding shared fleet equipment/freight |
| --- | --- | --- | ---: |
| Fox field |2S1P 25R,10 mW continuous |32.7 h at same specified output |57.83 EUR complete candidate; old audit 55.24 EUR preserved |
| Sprint only |2S1P 25R,0.85 W /0.5 W |19.5 /26.6 h; cold/idle margin limited | Pack 10.08 EUR; HF economy board 19.76 EUR, other material follows full HF scope |
| Economy Classic |2S2P 25R,1.2 W /1.2 W |33.0 h; no reduction needed in nominal model |92.92 EUR with both long/compact antennas;84.54 EUR without compact accessory |
| Higher-power Classic |4S1P 25R,3 W /1.2 W |17.0 /32.7 h; poor efficiency fails 12 h |98.24 EUR with 5 W thermal provision/both antennas;96.74 EUR tentative 3 W thermal population |
|5 W HF option |4S1P M35A,5 W /1.2 W |14.6 /44.1 h; poor efficiency fails 12 h |103.96 EUR with both antennas |
| Standalone VHF, smallest modeled |2S3P 25R,1 ERP /0.30 ERP |14.6 /24.9 h; little margin, no qualification claim |120.33 EUR |
| Standalone VHF with reserve |2S4P 25R, same settings |19.4 /33.2 h nominal |125.45 EUR; currently cheaper than 4S2P counterpart |
| VHF on 4S /universal supply |4S2P 25R, same settings |13.0 /34.1 h with assumed 0.65 full-power energy window; poor PA fails 12 h |128.29 EUR standalone VHF;177.12 EUR universal all antennas |

All runtimes are **calculated**, include no LoRa and conservative capacity/aging/temperature provisions, and require measured RF output throughout. Higher-capacity M35A offers margin/less cell count in some 2S cases at additional cost. Neither 4S1P nor 2S2P is currently a comfortably qualified VHF pack satisfying both targets; six/eight-cell choices depend on measured idle, efficiency and cutoff energy. 4S2P is a maximum universal candidate, not mandatory for Foxoring or HF.

At 6/10/20, revised controller component budgets are 16.70/14.93/14.83 EUR. Complete universal 4S2P 25R material is 190.49/177.12/175.63 EUR, versus 198.15/183.42/181.39 EUR for equal-cell 2S4P. Shared equipment/freight is separate: universal 4S fleet allocation 204.82/185.72/180.98 EUR. Fox revised complete material 64.47/57.83/57.83 EUR, fleet 77.97/65.93/62.68 EUR. Net EUR throughout; VAT/labor/instruments are separate. No economic conclusion is a supplier quote.

## Architecture disposition

**Propose go for the power direction only:** controller 6.0–16.8 V, externally protected/balanced keyed 2S/4S packs, bounded local supplies, calibrated fixed power profiles, independent normal/low-power rails and hardware source/rail fail-off. Keep S3/RTC/optional Silicontra, local synths and three primary PCBs. Upgrade controller regulator, raw FETs, TVS/caps and battery identity/UV support. Do not feed raw 4S into LM5134B, LTC3600, MCP1703A or the old controller input network.

**No-go for committing a 4S-only VHF supply or claiming endurance today.** Retain 2S boost as fallback. Prefer 4S higher-power HF and conditional universal 4S, but do not require 4S merely for economy HF. Full/reduced profiles are configured before the contest; undervoltage latches RF off, with no unreviewed automatic coverage change. Universal defaults to one active band: simultaneous 5 W HF+1 ERP fails 12 h on 4S2P in the early-cutoff model, while its 2S boost counterpart can pass nominally on eight M35A cells. Continuous maximum beacons need a separate duration/supply/service plan.

## Measurements that decide the next step

| Gate | Required physical result / go criterion |
| --- | --- |
| P1: HF supply/RF map | At 12.0–16.8 V and 2S allowed low settings, meet selected conducted power across 3.510–3.600 MHz including uncertainty; driver≤12.6 V, no converter/retune overshoot, CW/spectrum/mismatch limits fromH0–H9. Characterize driver/base currents, efficiency and key-shaper heat. |
| P2: VHF gain/envelope/headroom | Clean connector PEP≥4.079 W at 1 ERP assumption, reserve≥1dB and driver≥3dB below measured compression; true 70–80% sine AM, target 75%, proposed THD≤5%; stable matching/gain at 144 MHz, measured trough/crest/no-tone/retuning and full-range frequency capability. Establish minimum pack voltage while still meeting all limits. |
| P3: thermal/SOA | Exact-vendor hot DC SOA≥2× current trajectory margin, junction design target≤110 °C at stated ambient, limits/latches tested under mismatch and fault. Measure D45H11/helper/PA/converters together, including 16.8 V/no-tone comparator. No bareBD140 fallback. |
| P4: identity/fail-off | Wrong/open/short packID, incompatible module, reverse plug, UV, reboot, disconnected control supply, stopped lease and converter fault never arm unsafe RF; no measurable off-slot signal to the existing receiver/analyzer protocol. Prove actual disconnected rails and low-port isolation, not just logic levels. |
| P5: battery/charging | Qualify cell lot, weakest series group, BMS thresholds/balance/current, charger CC-CV/termination/current and distinct charger keying; full RF maintained 12 h and selected reduced profile 24 h under defined aging/temperature/LoRa cases. Measure accessible energy above full-VHF cutoff instead of adopting 0.65. |
| P6: compact antenna /immunity |10 mW at defined reference load plus separate loading/compact-counterpoise matching and reproducible 30 m audible /250 m inaudible field evaluation; normal output cannot reach compact port. Check RTC timing and optional simultaneous RF/LoRa immunity. |

Use the shared current-limited programmable supply, calibrated RF power/PEP and spectrum measurements, oscilloscope/envelope detector, VNA, cell/group logger and temperature sensors specified in [RF evaluation](M2_RF_EVALUATION.md) and [HF gates](M2_80M_VALIDATION_GATES.md). No voltage scaling, ideal filter simulation or energy arithmetic can replace these measurements. Record converter switching current separately from pack/PA current. Calibrate actual antenna/feed gain before claiming ERP.

Review needs acceptance of the dual-voltage controller/pack restrictions and 3 W full /1.2 W extended HF direction; whether 5 W must be the normal maximum; the allowed ambient/capacity-maintenance/LoRa profile; whether simultaneous full dual-band or a particular continuous beacon duration is required; and the smallest-pack experiment priority for VHF. **This milestone stops at architectural review.** It does not authorize test-hardware ordering, complete layout or manufacturing.
