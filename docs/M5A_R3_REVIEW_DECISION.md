# M5A-R3 — review decision

Dated 2026-10-15. **PRIVATE CONSTRUCTION DERIVATIVE / NOT RELEASED. All ARDF-TX hardware tests NOT_RUN.** No orders, PCB fabrication, assembly or transmission. M5A-R1 remains the archived fallback; RF80, M4A, the controller and accepted ADRs are unchanged.

**NO_GO for integrated PCB commitment, procurement or replacing M5A-R1 as the fleet design.** A concrete DL3BBX-derived editable RF2M schematic and review package now exist. The evidence does not establish an affordable, currently sourceable near-upper-ERP transmitter, so the requested buildable-PCB outcome is **not complete**. No speculative PA has been substituted to hide the deficit.

The selected construction foundation is DL3BBX's physically built CQ-DL5/1992 circuit. Retained: BF981 last doubler,2N4427 driver,MRF237 final, five original adjustable coils and exact interstage/output network, collector-supply Darlington AM mechanism. New: local72MHz Si5351 drive/filter, filtered ESP32 sine, TIP127 package modernization, existing common-controller/training/fail-off integration and bounded startup sequencing. No premium driver chain, separate coupon, new MCU, Mitsubishi study or RF80 change.

## Concrete artifacts and verification

- [Editable root schematic](../hardware/2m/RF2M.kicad_sch),16 hierarchical sheets, [17-page PDF](../hardware/2m/review/M5A-R3/RF2M.pdf), [netlist](../hardware/2m/review/M5A-R3/RF2M.net.xml), [electrical manifest](../hardware/2m/RF2M.electrical.json).
- Actual KiCad10.0.6 ERC: **0 errors,14 visible OPEN footprint-filter warnings**, no suppressed footprint check. Custom symbols can have unset landings without that warning; total unset physical footprint positions is separately audited. **ERC is not physical pin/AM/RF proof.**
- Exported-netlist/manifest parity across282 positions; **4096** static logic combinations,**36** state scenarios,**12** deliberate mutations,**31** manufacturer-specific numeric pin maps,**36** reference value/net positions and16 physical enable truth rows pass.
- R1 original fallback remains at tag`m5a-r1` and [native archive](../hardware/2m/archive/M5A-R1/README.md). R0/R1/R2 review exports, RF80/M4A, README and accepted ADRs are hash-frozen. Existing R1 tests are rerun read-only against its archived native manifest/export; no historical PASS report is rewritten.
- **No PCB, DRC, Gerbers or 3D manufacturing views are claimed.** No board exists on which those checks could be meaningful. No hardware test, analog startup simulation or actual RF measurement was performed.

## Economics and performance conclusion

| Population | 6 boards, EUR/unit | 10 boards | 20 boards | Physical parts / IC |
| --- | --- | --- | --- | --- |
| BOOST2S | 95.16 | 93.16 | 93.16 | 247 / 22 |
| BUCK4S | 93.23 | 91.23 | 91.23 | 241 / 22 |
| TRAIN_ONLY | 16.33 | 16.33 | 16.33 | 102 / 14 |


R3 at10 costs€40.52 more than R1 full2S despite fewer parts (247 vs264) and one fewer IC (22 vs23). €31.90 final/€5.90 driver listings lack exact maker confirmation; coils estimated€15. Complete installed2S module allowance is€119.66 at10, before controller/battery/enclosure/labor. These are conditional costs, not quotes. See [itemized BOM](M5A_R3_BOM.md).

MaxiTX cannot support the unchanged upper objective from its published1.2W peak. DL3BBX's **>3WPEP** with AM is the best primary evidence, but does not establish5.135W connector capability at the−1dBd/80% sizing basis. At exactly3WPEP that basis gives0.736WERP without reserve,0.584W with1dB reserve; no silent target reduction is accepted. Original rectangular modulation and substituted Darlington/source have **not** demonstrated70–80% sinusoidal RF AM. Current-limit crest margin, source coupling, stability and hot SOA remain open.

The2S boost is the preferred potential build supply;4S buck full-power capacity is constrained by≈14.4V loaded dropout. In the stated unmeasured budget2S3P2450 or2S2P high-capacity are the smallest packs with20% energy margin; RF output/endurance compliance is not established. Continuous full beacon endurance is far shorter. See [AM and power](M5A_R3_AM_AND_POWER.md).

## Smallest path to one complete transmitter

1. Obtain **one exact manufacturer-specific RF set and a priced6/10/20+spares supply strategy**, not broker claims; confirm the Neosid nominal/core/landings and original chokes/trimmers. This is a procurement-evidence/geometry gap, not an invitation to design a different PA. No quote requests have been sent without authorization.
2. Independently review this schematic and its source adaptation/current/thermal limits. Decide explicitly whether the actual legacy-parts price and seven adjustments are acceptable. If only a lower verifiedERP can be achieved, that requires an explicit product-target decision; the present target stays open.
3. Only after those blockers close, lay out **one integrated transmitter** using the original RF placement, prepare manufacturing review and obtain user authorization before purchase/fabrication. Commission it through the single [build/acceptance process](M5A_R3_BUILD_PLAN.md); no separate coupons or transistor-characterization program.

Private attributed construction is the only documented DL3BBX permission. Commercial distribution requires written author permission. Proposed ADR-0013 remains proposed; this milestone records a candidate/procurement NO_GO rather than silently amending an accepted architecture. R1 remains the fallback, also unqualified hardware.

The required owner review is therefore concrete: accept or reject the legacy construction's actual economic/supply constraints, and retain or explicitly revise the upper-power objective. **No manufacturing authorization is requested or assumed.**
