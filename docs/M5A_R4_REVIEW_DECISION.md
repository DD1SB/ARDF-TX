# M5A-R4 — review decision

Dated **2026-10-16**. **M5A-R4 electrical candidate — NOT RELEASED.**
All physical tests are **NOT_RUN**. No purchasing, fabrication, assembly or RF operation has occurred.
RF80, M4A and accepted ADRs are unchanged. R3 is preserved at tag `m5a-r3`
(`daf994c`); R0/R1 tags and the R1 native archive remain available.

**GO for independent electrical review. NO_GO for PCB commitment or manufacturing release.** The editable lower-cost schematic and reconciled material model exist. A fully sourced, buildable integrated PCB is not complete: the changed interstage and listed landings remain unresolved. No PCB, DRC result or Gerbers are invented.

The preferred candidate is direct 144 MHz Si5351, PHA-1+, active PD54008L-E, actual ST output matching/elliptic LPF, fixed gate bias and D45H11 drain sine modulation. **4S buck is the normal-power preference**; 2S boost is an alternate population. Independent µW training uses regulated 3.3 V with normal PA/converter omitted. MRF237, BF981, 2N4427, Neosid modules and RF trimmers are removed.

| Population | 6 units: EUR/board | 10 units | 20 units | Physical parts / ICs |
| --- | --- | --- | --- | --- |
| BOOST2S | 46.41 | 43.32 | 43.21 | 264 / 24 |
| BUCK4S | 44.77 | 42.03 | 41.92 | 260 / 24 |
| TRAIN_ONLY | 11.28 | 11.28 | 11.28 | 103 / 13 |

At ten, 2S saves **€49.84 versus R3** and **€9.32 versus R1**. The 4S savings are €49.20 and €8.68. RF core is €24.83; installed 4S module allowance is €68.53 before controller, battery, enclosure and labor. Most supporting prices remain estimates; [cost reconciliation](M5A_R4_COST_RECONCILIATION.md) quantifies the unquoted amount. These are not achieved purchase prices.

The original ST circuit/layout and final package drawings were recovered and inspected. Twenty-six network positions are checked in exported CAD. Their fixed-supply evidence does not prove our sine AM. At −1 dBd/1 W ERP/80%, the final needs 4.848 W PEP with the stated output loss and ≥18.86 dB gain for 19 dBm drive/1 dB input loss; at 0 dBd it needs ≥17.86 dB. These are unqualified targets. Optional extra 1 dB margin is not a championship rule.

Implemented changes remove obsolete RF stages, restore the actual elliptic filter, reduce low-drive inductor cost, replace a discrete driver switch, remove one permission IC, fix boost downregulation, precharge the driver reservoir and improve the conditional driver-OV bound. Slot shutdown uses pass/helper, gate bias, driver and clock controls while the upstream rail is precharged. That sequencing needs off-slot/pass-short testing. Full count is 264/24 ICs versus R3's 247/22; no false count saving is claimed.

## Checks and open gates

- **KiCad 10.0.6 ERC: zero errors, 7 visible footprint warnings.** Pin-to-pin/sheet-name errors were corrected, not waived. Default informational exclusions are recorded.
- Export/manifest parity covers **318 positions**. **4096 static combinations, 39 states, 19 deliberate mutations, 35 pin maps and 26 ST assertions pass.** These do not prove analog startup or timing.
- [Native schematic](../hardware/2m/RF2M.kicad_sch), [PDF](../hardware/2m/review/M5A-R4/RF2M.pdf), [netlist](../hardware/2m/review/M5A-R4/RF2M.net.xml), [BOM](../hardware/2m/review/M5A-R4/RF2M_BOM.csv), [pin audit](../hardware/2m/review/M5A-R4/pinout-audit.json), [reproducible checks](../hardware/2m/review/M5A-R4/final-checks.json).
- **Electrical hold:** the 50 Ω PHA-1+ cannot simply inherit the original PD84001 drain interstage. Establish the integrated input match and final gain/drive margin before routing. A small integrated alignment is acceptable; a fundamentally different PA is not silently substituted.
- **Physical holds:** the selected reservoir's C10 landing and temperature/stock confirmation, RF feed/air-coil landings and keyed connectors remain OPEN. Manufacturer-derived DF782 and RNW candidate landings now have dimensional checks; their stencil/thermal/assembly integration still needs review. Define final-source stencil/vias and actual stack-up. No unverified generic final pads.
- **Physical qualification:** drain-AM knee/linearity/stability, pass/helper hot SOA, sensor mounting, ≤20 µs isolation/≤5.9 V driver, input transients, RF/ERP/spectrum, off-slot silence, training isolation and 12 h/24 h endurance. All remain NOT_RUN. The consistent power model does not certify a small pack.

Close these specific input-network and physical landing definitions, then make **one integrated transmitter PCB**, review it and commission one complete unit using [one acceptance procedure](M5A_R4_BUILD_AND_TEST.md). No separate coupon program or broad architecture study is proposed. R1/R3 remain archived engineering fallbacks. Procurement/fabrication require explicit authorization; stop for review.
