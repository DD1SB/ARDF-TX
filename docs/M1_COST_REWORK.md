# M1 cost optimization rework

Date: **2026-10-13**. Status: **M1 architecture conditionally accepted; this cost analysis is the preserved baseline before M2 RF proposal increments**. No circuit implementation, PCB design, orders or hardware validation is authorized by this report. The user's revised targets replace the original stretch targets. The [itemized workbook](M1_COSTED_BOM.md), [counts CSV](M1_COST_BOM.csv) and [dated part catalog](M1_COST_PARTS.json) are candidates, not an ordering BOM.

The [M2 preparation](M2_PREPARATION.md) records the accepted scope and new RF/thermal findings. MMIC drive is preferred; the stocked-EOL alternative below is historical and excluded from current selection. The new [all-in view](M2_SYSTEM_COST.md) includes required circuit/thermal increments and system material.

## Finding and budget feasibility

The three-board platform can plausibly approach the **upper combined budget at ten or twenty units**, with substantial unquoted material still exposed. All four targets are **not yet demonstrated together with repeatable sourcing**. The main remaining overrun is the complete VHF board, followed by quantity-six pricing. There is no evidence for the lower €33 combined target with these requirements.

| Complete candidate board; EUR/unit ex VAT | Target | Six identical boards | Ten | Twenty | Assessment |
| --- | --- | ---: | ---: | ---: | --- |
| Controller without LoRa | 8–15 | 15.01 | 12.88 | 12.82 | Plausible at ten/twenty; six misses by €0.01 before uncertainty. |
| 80 m RF, all required power modes | 10–20 | 20.13 | 17.88 | 17.80 | Plausible upper target; six misses by €0.13; PA/source/matching changes untested. |
| 2 m A2A RF with currently sourced MMIC driver | 15–30 | 36.38 | 31.80 | 31.73 | Misses upper target by 6.38 / 1.80 / 1.73. |
| 2 m with stocked EOL discrete-driver alternative | 15–30 | 33.90 | 29.32 | 29.18 | Ten/twenty fit numerically, with lifecycle and RF-performance gates. |
| Combined three-PCB basket, MMIC driver | 33–65 | **69.54** | **62.33** | **61.90** | Ten/twenty nominal combined fit; individual VHF target still missed. |
| Combined with stock-limited discrete driver | 33–65 | **67.07** | **59.86** | **59.36** | Six still misses; cannot claim repeatability from remaining stock alone. |

Each board row prices that board independently. Combined rows pool **only identical MPNs** across the three assemblies, so they differ slightly from sums of standalone board prices. The twenty-unit batch has no invented quantity-twenty discount. For example, two isolation FETs per board reach quantity ten already at six boards, but one MCU per board does not. Manufacturing, assembly/calibration labor, VAT, shipping and rejects are outside these material totals. With an illustrative 19% VAT, the nominal combined ten-unit PCB material is **€74.18 gross**, before shipping; budget tax basis must be agreed.

Scope is explicit: board components, hardware protection, local RF shields/heat spreaders and logic PCB sockets are included. The proposed RF connections are strain-relieved **soldered coax pigtails to dissimilar bulkhead sockets**, rather than PCB-mounted RF connectors. The required battery, detachable module-power and RF port sockets add **€5.20 estimated/unit**, making electronics plus those sockets **74.74 / 67.53 / 67.10**, before cable/crimps/strain relief (additional **€2–5 estimate**, no quote). These are wiring costs under the user's exclusion, not eliminated functions. Restoring PCB-mounted RF sockets adds the same estimated €1.10 to each RF board and reduces the scope benefit. The majority of the rework comes from simpler control and cheaper synthesis, not this relocation.

At ten, quoted/observed combined material is **€36.31** and unquoted estimates **€26.02**. Varying only estimates by −25% / +50% gives **€55.83 / €75.34**. The corresponding HF band is **€15.32–23.00** and VHF **€28.77–37.85**. These are sensitivity calculations, not confidence intervals, measured costs or safe maximums. Counts, RF component values, critical stock and prices still need closure; the nominal numbers must not be advertised as proven budgets.

## Architectural changes

1. **One processor for the product.** ESP32-S3 controls both frequency sources directly through separate module buses. Remove both STM32 configuration bridges and their support circuitry. A common external test fixture can configure each RF board independently. Manual RF calibration and passive module identity are essential; per-module EEPROM, detailed digital telemetry and remote calibration automation are optional population.
2. **Local inexpensive synthesis first.** Use Si5351 on HF. Evaluate Si5351 with a filtered, buffered VHF output before committing to a costly LMX2571. If the required frequencies fail spectral tests, compare an integer-N ADF4002 plus discrete VCO before a higher-cost integrated VCO/PLL. This changes the investigation priority, not the emissions acceptance criteria.
3. **Minimal discrete power stages.** Reconsider ON7YD's single IRF610 HF class-C stage instead of automatically selecting a three-BS170 class-E derivative. For VHF, retain the proven collector/drain-supply AM principle with an inexpensive series transistor; use a currently available discrete RF power transistor, not an oversized 25–55 W PA. Retain real sine AM and adequate PEP capability.
4. **Hardware safety stays local.** Replace specialized per-board watchdog ICs with a retriggerable monostable, persistent latch, POR and gates. Keep source/drive shutdown, actual PA supply disconnection, analog current/temperature/rail trips and retune muting. No safety function moves into an optional firmware feature.
5. **Calibrate on a shared bench.** Omit DACs, precision SWR/current-monitor ICs, displays and a USB-UART bridge. Filtered PWM supplies bounded setpoints and keyed sine envelopes; manual trimmers set limits. Basic sensing/fault reporting remains. Optional EEPROM, backup capacitor and USB socket are costed separately.

The accepted three primary PCBs and optional Silicontra LoRa module remain. Reducing the number of ICs does not make the RF layout or qualification easier; the RF stages and filters remain band-specific.

## Evidence for minimal RF topologies

Publisher descriptions, instrument measurements and our extrapolations are kept separate. New entries extend the [original evidence matrix](M1_FEASIBILITY.md); dated links and access failures are in [cost sources](M1_COST_SOURCES.md).

| Design / primary evidence | Demonstrated evidence | Missing or incompatible characteristic | Cost/performance implication |
| --- | --- | --- | --- |
| ON7YD ATX80; G3ZOI uses this family | Author reports URV3 power/efficiency and FSEA harmonics: 2.9 W/61% at 12 V; 4.8 W/65% at 15 V. Single IRF610 and simple driver/filter. | Fixed crystal, unsafe original oscillator/key order; no shaped programmable 2S derivative tested. | Strong minimal HF PA reference. Retain 5 W by boosting; do not replace the boost with an unproven raw-2S claim. |
| DL3BBX / Hoogeveen six-unit build | Builder reports six aligned 0.5 W, 70% AM units and a wet-forest field trial. Describes crystal multipliers, 2N4427 driver and BFQ43 final. | Original CQ-DL May 1992 pp. 289ff not obtained; no calibrated AM/spectrum dataset. Its reported frequencies are outside the 2025 championship range. | Evidence for economical discrete AM and actual fleet construction; no automatic transfer of old RF parts, frequency or PA capability. |
| ON7YD ATX2 | Published FSEA test attribution, simple ICS501/BLU86 amplitude-keyed transmitter. | Only about 0.4 W peak class reference; old components and crystal-multiplier frequency selection; envelope does not establish 70–80% sine AM. | Lower-power training precedent, insufficient default for maximum Classic ERP/PEP. |
| G3ZOI / PA0JBG Netherlands history | Built discrete AM and modified UV-3R supply-AM examples, as previously logged. | No complete modern-revision A2A measurements or UV-5R qualification. | Prefer its simple AM mechanism over a premium RF chain; legacy devices need sourced replacements. |
| SmartFOX / HG0HK / QCX / DF1FO | Prior M1 records include built/direct-clock HF, measured QCX PA examples and practical compact transmitters. | SmartFOX 2 m is FM; HG0HK does not establish nominal 10 mW/reference-load acceptance; compact legacy antennas differ. | Keep lessons on direct HF synthesis and small antennas; do not call these full-spec replacements. |
| Si5351 VHF / RA3APW | Published spectra include 144.490 MHz reference comparisons; one reported near-offset spur is −41 dBc. | No proof across 144–146 MHz, all fractional settings, PA power, retuning, regulator/LoRa interference or our applicable legal mask. | Source IC €1.388 at ten makes it the first cost experiment. An LPF cannot remove close-in spurs. Reject failing channels/topology; never weaken frequency selection silently. |
| ST PD55008 family | Manufacturer Active; datasheet RF power/gain measurements at 500 MHz/12.5 V; genuine small-quantity distributor stock. | No published 144 MHz, 70–80% supply-AM result found. | A concrete priced 8 W device closes the earlier **unsourced PA part** gap, while leaving RF gain/matching/AM suitability unverified. |

Original source material remains attributed. Public schematics are not automatically licensed for redistribution. No third-party schematic/layout, firmware or Gerber has been copied into the repository.

## HF alternatives and separate antenna paths

**Proposed economy experiment:** Si5351, TTL-compatible RF gate driver, one IRF610, shaped keying, approximately 15–16 V boost, characterized output LPF, and a **separate bounded 10 mW branch**. ON7YD's 15 V observation is 4.8 W, not 5 W. Square-law scaling suggests about 15.3 V for 5 W, but this is our extrapolation and must be measured with losses/tolerances. The IRF610's higher voltage rating addresses the narrow drain-voltage margin of the BS170 reference; gate drive, mismatch survival, converter noise and clicks still require tests.

| HF choice | Quantified trade-off | Disposition |
| --- | --- | --- |
| Single IRF610 vs three BS170s | PA silicon at ten: €0.622 for stocked IRF610PBF-BE3 vs 3×€0.237 = €0.711; silicon saves €0.089, with circuit/support simplification and stress margin still more significant. Efficient class-C reference vs class-E reference. | Reconsider topology, not merely component count. Compare measured efficiency/clicks across all HF frequencies. |
| TPS611781RNWR cut tape vs RNWT | Observed ten €2.09 vs €3.73, saving **€1.64/unit**, same vendor RNW package/function; distributor customer MOQ 1. | Preferred cost candidate; external true isolation, inductor and capacitors still included. |
| MC34063 external-switch boost | IC observed €0.349 at ten vs €2.09; extra switch/driver/magnetics cost and switching noise reduce the difference. The 1.5 A figure is switch peak, not 15 V output current. | Secondary experiment only. A cheap internal-switch implementation cannot be assumed adequate. |
| Raw 2S instead of boost | Rough square-law model from 12 V/2.9 W gives 0.73–1.42 W over 6–8.4 V, before new losses. | Fails 5 W maximum; not a full-population solution. |
| Fixed crystal instead of Si5351 | Gross source saving about €1.39 plus reference/support, offset by crystal and oscillator. | Does not preserve programmed frequencies; only a separately identified reduced-function comparator. |

The cheap converter must preserve endurance. At HF PA efficiency 60%, the reference 4P pack requires roughly **≥70% boost efficiency** to reach 24 h with the rework overhead allowance; at 50% PA efficiency it requires roughly **≥84%**. These are energy-model thresholds, not efficiency measurements. A cheap converter which misses them has not solved the task.

The Classic/Sprint wire and the compact Foxoring installation remain physically different. The main PA connects only to the long-wire port. The bounded branch has its own filter/pad and a keyed compact socket. A compact-cartridge identity/contact inhibits the watt path in hardware; it must not rely on software setting the PA to 10 mW. The source port is calibrated at 50 Ω/10 mW separately from antenna reach.

The complete long-wire accessory currently has a **€10.25 unquoted material estimate**, including separate match, RF capacitors/indicator/connector, support insulation, wire and symmetric radial allocation; pole/support is extra. The complete short-radiator accessory is **€8.38 estimated**: high-inductance loading/coupling coil, tuning/fixed capacitors, damping, low-capacitance protection, keyed plug/identity, insulation/strain relief, ~30 cm radiator and compact counterpoise. Unlike the prior broad allowances, every functional item is now in the workbook, but these accessory numbers are **not sourced quotes or a validated winding recipe**. Use +50% sensitivity and reopen if RF-voltage/Q/SRF or field tests require larger parts. A fixed long-wire match cannot substitute for this compact network.

Full HF RF board vs Fox-only population at ten is **€17.88 vs €7.92**. Controller plus reduced RF and the complete compact antenna is **€29.06**, plus transmitter-side battery socket €0.60, detachable module-power pair €1.20, compact-port socket €0.40 and actual wiring; pack, outer enclosure and assembly extra. A universal HF board plus compact antenna costs about €10 more and carries the unused boost/PA/thermal hardware. Reduced population retains the same HF PCB outline; it can reduce component height, heat and mass, but does not establish a smaller bare board. Omitting the VHF board and its horizontal antenna/heat sink matters more to size than chip integration. The short radiator, compact counterpoise and loading network still determine installed dimensions.

## VHF alternatives, modulation and headroom

Maintain full locally permitted band tuning and the independent 144.500–144.900 MHz championship restriction. The conservative sizing convention remains 1 W **carrier ERP**, net antenna gain −1 dBd, m=0.8: **1.259 W connector carrier, 1.662 W mark mean, 4.079 W PEP, ≥5.14 W clean capability including 1 dBmargin**. The rulebook ERP convention still needs referee agreement; this cost exercise does not redefine ERP as connector power.

| VHF topology | Cost evidence / quantified consequence | Recommendation or blocker |
| --- | --- | --- |
| Si5351 + filtered RF driver + PD55008 + BD140 series AM | Si5351 €1.388; PA €10.791; BD140 €0.264; GVA-84 €2.57 indexed small quantity. Whole board **€31.80 at ten** with isolated training/safety. | Preferred currently sourced research route. Carrier-source spurs, 144 MHz PA gain and AM transfer are unverified. Low-cost MMIC buffer is an availability comparator, not a requirement to use integrated RF throughout. |
| Same discrete final with two BFP650 driver devices | Two stocked devices total €0.644 at ≥ten; 5 V LDO omitted in favor of filtered 3.3 V. Whole board **€29.32 at ten**. | Lowest priced complete discrete-driver candidate; manufacturer discontinued, indexed remaining stock ~12,977, last-time-buy 2027-05-15. Consider only an explicitly accepted finite batch/spares policy, never call it a current-production drop-in. |
| Entire driver built from current general VHF BJTs e.g. MMBTH10 | Onsemi publishes 650 MHz fT minimum under stated conditions; low-power training use plausible. Driver price/stock/current gain at required output remain OPEN. | Investigate minimal two/three-stage class-C drive. fT alone does not prove sufficient 0.1–0.2 W clean drive or stability. Do not count hypothetical savings as achieved. |
| ADF4002 + discrete VCO | Observed PLL €3.875 at ten, external VCO/varactor/loop/lock/ref **€1.5–3 estimate**, replacing €1.388 Si plus existing crystal. Approx **€4–5.5 added/board**, not €11.58 LMX silicon. | Lower-cost spectral fallback. Example 25 MHz reference/1000 →25 kHz PFD, N5760–5840 spans 144–146 MHz; narrower competition guard still applies. Other step sizes possible, verify counter limits and channel needs. New VCO has no ARDF bench validation yet. |
| LMX2571 integrated source | Silicon €11.58 vs Si €1.388, **€10.19 difference**, plus reference/loop/support. | Higher-cost fallback only; manufacturer 480 MHz results do not certify 144 MHz. |
| Two active PD55003L-E 3 W devices | Observed €4.84 each at ten; two per six-board batch reach that break, **€9.68 vs €13.64** PA silicon. At ten, save only €1.11 vs PD55008. Combining/balancing/extra matching/14 V boost add estimated €1–2.5 and losses. | A batch-six alternative worth comparison, weaker at ten/twenty. 6 W total before combiner barely covers 5.14 W; 0.5 dBcombiner loss requires 5.77 W internally. No combined AM measurements found. |
| One 3 W final plus higher-gain antenna | To support 5.14 W sizing convention with a 3 W final, net antenna gain must be **≥+1.34 dBd**, before additional filter/combiner loss and device margin. | Not accepted as a cost shortcut: no such qualified horizontal omnidirectional 2–3 m forest antenna established. Antenna array/feed cost and sensitivity must be measured and costed. |
| Original DL3BBX/ON7YD crystal multipliers, legacy finals | Demonstrated simple AM, low historical component count. Modern non-reel RF replacements and programmable synthesis add real costs. | Study mechanisms; unchanged old designs do not meet the complete frequency/PEP/safety specification. |

Series PA modulation must produce **70–80% sine AM**, not a fixed FM sidetone or 100% square chopping. With a ~12 V peak PA rail, the center rail at m=0.8 is at most ~6.67 V before dropout. BD140/op-amp SOA, trough leakage, envelope feedback, AM-to-PM conversion, bias and continuous heat require characterization. The manufacturer's PD55008 500 MHz rating and 150 mA test bias are not our measured 144 MHz current, gain or AM efficiency. GVA's nearby-frequency typical data does not guarantee adequate drive: measured PA gain must establish whether the required drive is ~0.10 W at 17 dB or ~0.16 W at 15 dB. If the driver/PA combination misses this, recost; never derate maximum ERP silently.

Training uses a separate pre-PA buffer with its **own AM control, permanent pad, filter, bounded rail and keyed low-power connector**. The pre-PA carrier is unmodulated in the main drain-AM topology. No attenuator/switch is allowed to route watt output to the training network. With a 1 µW training setting and unwanted coupling budget 0.1 µW, a 5.14 W peak normal PA requires approximately **77 dB isolation**; at nominal 10 mW HF with 0.1 mW stray limit, 5 W requires **47 dB**. These are provisional engineering leakage budgets, not IARU mask numbers. Cheap shields/returns must pass the isolation tests or be recosted.

## Synthesis placement reconsidered

| Placement | Cost scope and RF consequences | Rework proposal |
| --- | --- | --- |
| Si5351 on each RF board | ~€1.79 source/crystal per board at ten; independent source/filter/quiet return, direct separate control buses, shared external test fixture. No 144 MHz cable between primary PCBs. | Preferred research base; duplicated source material is small once bridges/LMX removed. |
| One controller Si5351, HF logic feed +144 MHz coax | Gross saving one source/crystal ~€1.79; add launches/receiver buffer/filter/strain relief/shield. Added board hardware **€0.8–2 estimate**, coax harness **€0.5–2 estimate**, putting the source on the controller leaves about €0.33 of its ten-unit €15 ceiling before extra launch hardware. | Approximately −€0.49 to +€2.21 whole-system difference; no evidence of a large saving. Do not count excluded coax wiring as free. Test broken return/harness radiation, carrier leakage and simultaneous LoRa. |
| Controller HF source + local VHF PLL | Saves only HF Si/reference; controller remains mandatory for source test and variants; VHF cost blocker unchanged. | No demonstrated total saving compelling enough to select. |
| Shared low-frequency reference | Could remove one crystal but adds distribution/buffering/returns and continuous digital emissions. | OPEN; not presumed cheaper or quieter. |

The original estimated €4–10 shared-coax penalty was not price-closed and is withdrawn as a decisive argument. Source placement remains a proposed decision based on the revised full-system comparison, RF isolation and tests rather than schematic simplicity.

## Essential and optional population

| Function | Essential base | Optional / reduced population and consequence |
| --- | --- | --- |
| ESP32, compensated RTC, quiet buck | Retained. S3 €3.88, RV3032 €2.032 and TPS62160 €1.408 at ten total €7.32 before support. | C3 saves about €1.47 MCU silicon but needs a verified GPIO/lifecycle solution; I/O expansion can erase savings. Bare SoC adds flash/crystal/RF/assembly work; no proved net saving at 6–20. |
| Timing holdover | RTC while pack supplies unit; wired synchronization/time-valid guard. | Backup capacitor ~€0.30 estimated; without it a cold pack swap requires resync before arming. No relaxation of 24 h timing accuracy. |
| RF safety / low-power protection | Monostable+latch+POR+gates, current/thermal/rail cutoffs, source and PA gates, bounded branches and interlocks. | Never omitted to hit cost. Passive RC-only reset or firmware-only watchdog is not equivalent. |
| Power/modulation control | Filtered PWM, local trimmers, hardware upper bounds, external conducted calibration. | DAC, detailed SWR logger/digital current monitors/EEPROM automation optional; basic analog sensing and fault reporting remain. |
| Provisioning / local status | Pads, shared wired fixture, button/LED; validated autonomous stored profiles. | Board USB socket ~€0.35; no UART-USB bridge required with S3 native USB. Fixture **€3–6 estimate once/fleet**, not per unit. |
| LoRa | Unpopulated fully supported. Reserve protected footprint/interface; robust presence/BUSY/status tests. | Exact Silicontra MPN/price remains OPEN; prior €10–20 module allowance is not a quote. No LoRa-derived contest timing dependency. |
| HF watt path | Present on universal 80 m PCB. | Fox-only population omits watt PA/boost/driver/watt LPF/heat sink, retains short-antenna branch and complete external cartridge. |
| 2 m training | Present in full board cost and independent of normal final. | Classic-only or training-only populations may omit unused branch, clearly labeled reduced-function configurations; neither is the full 2 m board budget result. |

The full enhanced electronics population adds **€1.65 estimated/unit** for the six optional rows. Display/GNSS/precision RF meters/local MCU/DAC are not automatically part of any population.

## Cost drivers and sourcing closure

The [pre-rework ledger](M1_BOM_PRE_REWORK.md) was a broad functional allowance: controller 22–32, HF 26–42, VHF 44–72, combined 92–146. It lacked a sourced fleet PA and over-reserved duplicated functions. Those ranges are historical, not current recommendations. Savings are not the mathematical subtraction of every allowance below; the original allowances overlapped supporting passives, while the new workbook uses individual rows.

| Driver | Lower-cost response | Quantified evidence / remaining barrier |
| --- | --- | --- |
| €14–20 VHF source block | First evaluate local Si, then discrete VCO+integer PLL | LMX silicon saving €10.19 at ten; VHF spectra determine whether available. |
| RF microcontrollers/private bridges | Direct source control with host fixture | Remove 2×STM32C011, silicon €1.858 at ten plus support; no local firmware to maintain. |
| Specialized watchdogs | HC123 + HC74 + HC08 + MCP100 | Per RF unit silicon about €0.817 vs TPS3431 €1.313 **before its required latch/POR/gates**. RC/tolerance/failure qualification still mandatory. |
| DACs and precision telemetry | Filtered PWM, analog trips, calibration fixture | MCP4725 ceiling €1.09 each removed; digital meters/muxes not required in base. Ripple/modulation tests decide filter cost. |
| HF converter packaging | RNWR customer cut tape | Saves €1.64/board at ten without factory-reel purchase. MC34063 remains a separate efficiency-risk alternative. |
| VHF PA / driver | Real priced PD55008; available MMIC buffer or explicit EOL discrete comparator | PA alone €10.791 at ten, about 36% of €30 ceiling; including Si/boost/MMIC roughly €16.51 before modulator/safety/filters. Existing stocked small parts can meet 10/20 driver demand, future substitute unqualified. |
| RF filters, shielding, heat and protection | Hand-wound standardized coils, simple analog limits, local heat spreaders | VHF nonquoted functions still €12.11/board at ten. Removing them blindly would compromise performance/safety; exact part quotes/winding labor may reverse expected saving. |
| Connectors/wiring | Shared fixture, keyed bulkhead pigtails; board logic sockets only | €5.20 for mandatory power/RF connector material is costed in wiring; add €2–5 actual harness estimate. Modularity and safe port distinctions preserved. |
| Availability/MOQ | Genuine distributor cut tape/tube, same-MPN pool | No reel requirement for selected Si/boost/PA. Some cheap offers have zero stock or MOQ 400/3000 and are excluded. New PD55008TR stock observations24 vs151 and HC123zero vs1037 must be reconciled before order. |

Final source check replaces the original zero-stock Mouser IRF610 offer with Farnell's indexed IRF610PBF-BE3 offer (code 4853567, 614 stock, €1.11/€0.622 at 1/10, MOQ1). The BE3 suffix and PCNs still require review; distributor form/fit/function statements do not validate the RF derivative.

Supplier order codes, observation dates, stock conflicts, package names, quantities and each 6/10/20 unit/extended price are in the workbook/catalog. **OPEN** means the supplier number, quote, stock or selected value was not established; no guessed SKU is an order authorization. Supporting RF values/counts are architecture estimates because no schematic has been designed. This is a full functional candidate BOM with an explicit unresolved sourcing list, not a falsely exact production BOM.

## Modified handheld comparator

Current retail UV-5R examples were previously observed at **€29–29.95 including retailer tax**, not distributor volume quotes. Replacing the earlier premium-controller allowance yields approximately **€51–64 conversion material**: revised controller €12.88; radio29–29.95; AM/supply-access/thermal/filters/safety interface **€6–12 estimate**; independently bounded AM training path **€3–6 estimate**; wiring allowance handled separately. Six/ten/twenty discounts for radios have not been observed; use flat retail prices. Do not add the standalone custom VHF board again.

This is a mixed retail-tax/ex-VAT comparator, excluding external pack/charger/antenna/assembly. The radio purchase includes inseparable retail accessories; no fictitious battery-credit deduction. UV-3R supplies precedent, not measured UV-5R equivalence. PA rail access, FM gain-control interactions, exact radio revision, genuine RF behavior, A2A envelope/PEP/spurs and repeatability remain unverified. The Arducon external-attenuator approach is another AM concept, but a 500 mW input-limited attenuator cannot be assumed to provide maximum ERP/PEP through loss. Handheld modification may save development time; it is not clearly cheaper than the optimized controller+VHF nominal €44.53 electronics, and cannot replace the accepted three PCB family silently.

## Review gates and preserved acceptance

The existing [rule trace](M1_REQUIREMENTS_TRACE.md), [country review](M1_REGULATORY.md) and [validation plan](M1_VALIDATION_PLAN.md) remain binding. IARU competition rules are not legal authorization. The rework preserves 1–5 W Classic, 0.3–1 W Sprint, nominal 10 mW continuous Foxoring, actual A2A 0.25–1 W ERP/70–80%, flexible frequencies, concurrent Sprint groups/beacons, accurate autonomous clocks, optional LoRa, 2S1P–4P and hardware fail-off.

After architecture review and separate authorization for experiments, qualification must resolve: source spectra on every planned channel/full local band; HF 5 W efficiency/drain stress/CW clicks; current VHF PA gain/drive/PEP/AM/thermal behavior; source-backfeed and retune latch sequencing; isolated low-power-port leakage; distinct long and compact antenna matching, 10 mW reference-load measurement and reproducible 30 m audible/250 m inaudible field tests; timing/LoRa coexistence; actual standby currents and 24 h discharge. Repeat a representative build/calibration on multiple units and obtain live comparable distributor baskets. All are **pending**, not optional acceptance features. These physical tests precede hardware validation/release; they were not performed during M1 and do not require pretending that research has already passed them.

Previous M1 review questions (architecture and current-production driver policy now settled): accept/revise [ADR-0007 minimal control and RF topology](decisions/ADR-0007-cost-optimized-m1.md); choose whether a finite stocked-EOL-driver batch is acceptable or require future current-production sourcing; agree ex-VAT/gross target basis and allowed board-vs-wiring scope; decide whether the approximate €1.8 VHF-board overrun at ten is acceptable or keep the sourcing/topology gate open. **Conditional acceptance permits RF circuit/evaluation preparation; complete layout/procurement remains gated by measured RF evidence.** No procurement, PCB design or firmware implementation follows automatically.
