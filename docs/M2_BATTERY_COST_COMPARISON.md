# M2 battery and conversion material comparison

Date: **2026-10-14**. **Candidate costs, EUR net, no procurement.** Values combine dated supplier observations with explicitly unquoted estimates and unspent qualification reserves. They are not complete quotes or released ordering lists. [Sources](M2_POWER_ARCHITECTURE_SOURCES.md), [catalog](M2_POWER_ARCHITECTURE_INPUTS.json), [itemized CSV](M2_POWER_ARCHITECTURE_BOM.csv) and [results](M2_POWER_ARCHITECTURE_RESULTS.json) expose supplier codes, quantities, package, MOQ, price break, availability, date and missing positions. The [generator](../tools/m2_power_architecture.py) preserves earlier workbooks and aggregates identical MPNs within each alternative fleet only.

## Costed electrical choices

In the CSV, `needed`, `ordered` and `leftover` describe the **pooled identical-MPN purchase** and can repeat across functional rows. Use `qty_per_unit` for each row and sum `line_per_unit_eur` for allocated material; do not sum repeated pooled purchase quantities. JSON provides each purchase once. This preserves actual price breaks and allocates MOQ leftovers without double charging.

| Position | Count / applicable population | Net EUR supplier break or allowance | Evidence / purchase constraint |
| --- | --- | --- | --- |
| TPS54302DDCT, Mouser 595-TPS54302DDCT | Controller 1; HF 4S1; VHF 5V1; VHF 4S PA1 | 1.59 at 1, 1.18 at 10, 1.08 at 25, 0.955 at 100 | **Indexed observation**, stock cache conflicts; live basket OPEN. Cut tape MOQ1/multiple 1. Do not assume DDCR backorder or factory reel 250/3000 is required. |
| Controller buck inductor |1 |0.80 | ESTIMATE; upgraded from 0.45, saturation/DCR/MPN OPEN |
| HF PA buck inductor |1 |0.80 | ESTIMATE retained; actual 3 A switch ripple must qualify |
| VHF PA supply inductor |1 |0.80 | Retained in both boost and buck comparison; no false saving by removing the required buck inductor |
| VHF 5 V support, excluding IC |1 |1.27 | ESTIMATE: inductor 0.60, capacitors 0.32, bootstrap 0.025, resistors 0.05, quiet filtering 0.275 |
| Controller extra bootstrap/divider |1 capacitor +2 resistors |0.025 +0.05 | ESTIMATE; original bulk cap count retained |
| Controller 40 V isolation FETs, DMP4015SPS-13 |2 replacing old 20 V parts | Existing quote 1.38 single /0.646 at 10 /0.574 at 100 | Prior OBSERVED stock conflict, package/current/PCN qualification OPEN; identical devices pooled with RF boards |
| FET VGS clamps |2/controller;2/normal 4S RF |0.10 each | ESTIMATE; exact vendor/tolerance OPEN |
| Input TVS replacement |1/controller |0.35 | ESTIMATE SMBJ17A-class; replaces SMBJ8.5A, no double count; loaded clamp/charger tolerance gate |
| Input capacitor upgrade delta |1/controller;1/normal 4S RF |0.24 | ESTIMATE for 35 V input protection margin; original reservoir counts still present |
| Pack class/UV support | Extra dual comparator 1, reference 1, resistors 6, controller identity contact 1 | LM393B observed 0.140@10 /0.124@25; reference 0.35; R0.025 each; contact 0.25 | MPN/reference/contact thresholds and qualification OPEN. Hardware functions not released from these counts. |
| Bounded RF power selection |1/4S normal RF |0.35 | ESTIMATE discrete support, no DAC/MCU |
| HF additional 5 W thermal provision | Optional 1 |1.50 | ESTIMATE beyond existing 0.60 sink;3 W reduced thermal population can omit only after thermal validation |
| VHF 5 V alternative | Existing MCP1703A removed; buck/filter added | Board delta about 1.90@10 before pooling | Needed to avoid raw 4S16V limit and retain training with watt supply off. A cheaper LDO from bounded AM rail remains a thermal/independence comparator: roughly 0.9–1.3 W active heat at 13.5 V, depending measured driver/control current. It cannot power training when the watt converter is off without an independent supply. |
| VHF modulator/helper/thermal | D45H11+helper+completion, retained |1.08@10 +0.20 +3.00 support, plus old thermal material | Existing observed/estimated mix. Raw 4S comparator adds another 3.00 thermal allowance; no SOA pass implied. |

A5V buck does not establish RF quietness; filter and receiver-immunity tests remain required. Its extra cost is shown on **both** comparable VHF supply variants; overhead savings from reduced LDO heat are not yet credited to endurance. Supply substitution cannot hide extra magnetics, cooling or PCB area. Proposed board variants remain the same three primary PCBs, with different populations.

| Board material only |6 /10 /20 units, EUR/unit | Scope |
| --- | --- | --- |
| Revised dual-voltage controller |16.70 /14.93 /14.83 | S3+RTC, LoRa DNP; input protection/ID included |
| Existing economy 2S HF |22.41 /19.76 /19.68 | Retained proven-core candidate,1.2 W maximum, independent Fox path |
| Existing higher-power 2S HF supply |35.48 /30.86 /30.79 | Boost+LTC3600 supply, same RF core,5 W thermal provision |
| Higher-power 4S HF single buck |24.39 /21.82 /21.75 | Same core,1–5 W evaluation envelope, additional thermal provision |
|4S HF 3 W thermal population |22.89 /20.32 /20.25 | Omits only the additional 1.50 allowance, not base sink/filter/guards |
| Reduced Fox-only RF |9.40 /8.50 /8.44 | Tentative TinyFox-derived branch; no watt PA/driver/converter |
| Revised VHF 2S boost |43.45 /38.04 /37.97 | Includes independent 5 V driver/control buck/filter |
| Revised VHF 4S buck |42.22 /37.92 /37.65 | Same RF/AM hardware, not a PEP qualification |
| VHF 4S raw-to-modulator comparator |43.30 /38.59 /38.52 | Greater thermal material offsets deleted PA converter |

The 4S HF board saves **EUR9.04 at ten** against the double-converter HF alternative, principally LTC3600/OPA171/boost/extra magnetics. Power-conversion group drops 11.91→2.43; new 4S protection adds 0.44. The 3 W population sits about 0.32 above the 20 EUR component target; the 5 W-capable budget adds 1.50. Quotes of the toroids, power magnetics, capacitors, interlocks, cooling and actual assembly remain unresolved. Do not call the ceiling achieved from an allowance table.

The 2 m board saving is only **EUR0.12 at ten**, after retaining the buck inductor, adding bounded selection/protection and pooling actualIC quantities. Deleting the boost alone is not a meaningful whole-system saving. Its component cost remains above the old 15–30 EUR objective because PD55008, preferred MMIC, filtering, genuine AM, thermal provision and independent training remain present.

## External battery bill

| Pack item | Count | Net unit price / allowance | Status |
| --- | --- | --- | --- |
| New 25R cell |2/4/6/8 |1.73≥10,1.64≥50,1.56≥100,1.48≥200 total cells | OBSERVED NKON; no invented 20-board discount |
| New M35A cell |2/4/6/8 |3.30 single,3.16≥30,3.00≥100 total cells | OBSERVED NKON;3.35 Ah minimum used for energy |
| Supplier welded tabs | One service/cell |0.62 | OBSERVED; avoids assuming free tooling/service |
|2S protection candidate |1 |1.29 | OBSERVED LA123112, historical stock 25; cell thresholds/balancing unqualified |
|2S protection reserve |1 |1.71 | RESERVE, not a purchased part; total protection budget 3.00 |
|4S protection candidate |1 |1.91 | OBSERVED LA123070; no verified balance function |
|4S balance provision |1 |2.00 | ESTIMATE; actual part/bleed behavior OPEN |
|4S protection reserve |1 |2.00 | RESERVE; not a firm safety cost ceiling |
| Fuse /barriers /shrink /restraint /leads | One set |0.22 /0.35 /0.25 /0.40 /0.28 | ESTIMATES retained from audit |
| Extra mechanics/sense leads | Per additional pair beyond 2 cells |0.60 | ESTIMATE; pack geometry/series-group wiring different, not free |
| Pack power connector half |1 |0.60 | ESTIMATE; transmitter mating half costed separately |
| Pack identity contact/resistor |1 each |0.25 +0.025 | ESTIMATE; charger protection independent of this resistor |
|4S charging keying delta |1 |0.35 | ESTIMATE, exact connector OPEN |

Cheap candidate BMS claims of 4.25±0.05 V OV and 2.5-class UV do not release a pack. Worst OV can reach 4.30 V, beyond the intended 4.20 V charge setting/selected cell limits; actual lot/device thresholds and qualified CC-CV charger must be verified or replaced. A35A label does not set the transmitter fault cutoff. Balancing, series-group monitoring, cold behavior, assembly barriers and fuse coordination are necessary, not omitted for cost.

| Complete external pack including reserves |6 /10 /20 fleet units, EUR/pack |
| --- | --- |
|2S1P 25R |10.08 /10.08 /10.08 |
|2S2P 25R |15.38 /15.38 /15.02 |
|2S3P 25R |20.68 /20.14 /19.66 |
|2S4P 25R |25.98 /25.26 /24.62 |
|4S1P 25R |18.64 /18.64 /18.28 |
|4S2P 25R |29.24 /28.52 /27.88 |
|2S1P M35A |13.22 /13.22 /12.94 |
|2S2P M35A |21.66 /21.10 /21.10 |
|2S3P M35A |29.26 /29.26 /28.30 |
|2S4P M35A |37.42 /37.42 /36.14 |
|4S1P M35A |24.92 /24.36 /24.36 |
|4S2P M35A |40.68 /40.68 /39.40 |

Equal-cell-count 4S packs cost **EUR3.26 more** in this provision because balance/protection/keying differs. Cell/tab expenditure is equal at the same batch break. That increase must be included when claiming an RF-board saving. Supplier observations are alternatives, not a purchase plan simultaneously consuming stock for every table row.

## Shared charging, fabrication and complete material

Retain one qualified charger per ten packs, rounded up: fleets of 6/10/20 need 1/1/2 chargers. The 2S 8.4 V, 1 A charger allowance is 15 EUR; the 4S 16.8 V, 1 A allowance is 20 EUR. Keyed adapter 1 EUR/charger, shared provisioning 5 EUR/fleet and freight 60 EUR/fleet are separate. 4S 2 A charger comparator is 8.07 EUR net but stock 1 and too much charge current for M35A 1P;4 A comparator 19.96 EUR is not a cell-safe universal charger. Neither unqualified low price is the preferred budget.

Shared/freight allocation for 2S is **13.50 /8.10 /4.85 EUR per unit** at 6/10/20;4S is 14.33 /8.60 /5.35. Charging packs sequentially at 1 A may take several days for a fleet; if event turnaround requires additional chargers, change the shared line rather than concealing one charger/unit in transmitter material. No parallel charging of packs proposed.

Bare fabrication remains **ESTIMATE3 EUR/design/board**, assumed MOQ/multiple 5 **per independent artwork**. For 6 units buy 10 of each design: two/three-board fabrication allowances 10/15 EUR per unit. At 10/20 they are 6/9 EUR. Add 0.25 EUR per board as an explicitly unquoted power-area provision; it might fit the old outline and disappear after review. A reduced Fox population does not shrink the existing HF board. No panelization saving has been booked without a quote/design review.

Normal-case/wiring allowances are 8/3.50 EUR; normal RF socket 0.70, low RF socket 0.40, each power connector half 0.60. Both ends of each module power connection and pack connection are counted. The existing 8.38 EUR compact antenna and 10.25 EUR long-wire/match are both included in full HF/universal material, with 3 EUR HF support; VHF includes 15 EUR antenna/feed,8 EUR support and 3 EUR training antenna. A normal HF-only deployment without the optional compact assembly subtracts 8.38; do not compare that smaller scope to a both-antennas total. Antenna accessories are not a fourth primary PCB.

| Complete candidate material, including pack/reserves |6 /10 /20 EUR/unit | Fleet cash at 10, including separately shared equipment/freight |
| --- | --- | ---: |
| Fox 2S1P 25R |64.47 /57.83 /57.83 |65.93 |
| HF economy 2S2P 25R, both antennas |101.36 /92.92 /92.56 |101.02 |
| HF higher-power 2S2P 25R, both antennas |114.43 /104.02 /103.66 |112.12 |
| HF higher-power 4S1P 25R, both antennas |105.78 /98.24 /97.68 |106.84 |
| HF 5 W 2S2P M35A |120.71 /109.74 /109.74 |117.84 |
| HF 5 W 4S1P M35A |112.06 /103.96 /103.76 |112.56 |
| VHF 2S3P 25R |131.24 /120.33 /119.65 |128.43 |
| VHF 2S4P 25R |136.54 /125.45 /124.61 |133.55 |
| VHF 4S2P 25R |138.98 /128.29 /127.65 |136.89 |
| Universal 2S4P 25R |198.15 /183.42 /181.39 |191.52 |
| Universal 4S2P 25R |190.49 /177.12 /175.63 |185.72 |

The 3 W thermal population subtracts 1.50 EUR from the higher-power HF total **conditionally**, keeping all antennas and safety functions. At ten,4S saves **5.78 EUR unit material /5.28 EUR fleet cash** against matched four-cell boosted HF, and 6.30/5.80 EUR for matched eight-cell universal hardware. For VHF, matched eight-cell 4S is **2.84 EUR more material /3.34 EUR more fleet cash**. Smaller 6-cell 2S VHF is cheaper still, with little endurance margin. These results favor 4S for higher-power HF, not every mode.

## Preserved Foxoring audit and new-cost bridge

The accepted accounting remains **29.06 EUR controller+reduced RF+compact antenna;55.24 EUR complete materials;63.34 EUR allocated fleet cash at ten**. The earlier 77.11 EUR included different charger/freight/tooling allocations; it is not restored as a baseline.

New conditional ten-unit material is 57.83 EUR, a **2.59 EUR increase**, reconciled as:

| Change from 55.24 EUR audit | EUR/unit |
| --- | ---: |
| Tentative TinyFox-derived RF component simplification |−0.17 |
| Wide-input controller protection/regulator/ID and pooled price breaks |+1.98 |
| External pack identity resistor/contact |+0.28 |
| Unquoted fabrication-area provision, two boards |+0.50 |
| Result |57.83 |

The shared 2S allocation stays 8.10 EUR at ten, giving 65.93 EUR. This is an engineering change, not the old 48 EUR accounting discrepancy. At 20 the original audit 55.20/60.05 remains history; the new candidate 57.83/62.68 is separate. Proposed small RF savings require hardware acceptance; if the new low-power branch fails, retain the prior branch and add back approximately 0.17 EUR. No antenna field/matching or controller/RTC/LoRa-footprint requirement has been removed.

Labor, pack assembly, winding, calibration/field testing, tools/instruments, capital, spares/yield and engineering are **OPEN and excluded**, not priced at zero. Observed material at ten is only 21.11 EUR for Fox,28.81 EUR for the higher-power 4S HF unit and 58.12 EUR for universal 4S; the rest is estimates/reserves. Increasing estimates by 50% takes their material totals to 76.19/132.95/236.62 EUR respectively. These are uncertainty scenarios, not quotations or guaranteed upper limits.

Net EUR is used throughout. Illustrative German 19% VAT on 57.83 EUR material is 10.99 EUR, gross 68.82 EUR; on 65.93 EUR fleet allocation it is 12.53 EUR, gross 78.46 EUR. Actual supplier jurisdiction, freight VAT and recoverability must be determined at checkout; do not combine source gross prices with net totals.
