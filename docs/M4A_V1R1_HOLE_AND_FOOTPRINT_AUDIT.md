# M4A-V1R1 — finished-hole and manufacturer-footprint audit

Date: 2026-10-18. Native pads and fresh drills are the authority. The [machine-readable audit](../hardware/80m/production/review/M4A-V1R1/finished-hole-audit.json) contains every calculation, exact source URL, package drawing and uncertainty. [Before/after native geometry](../hardware/80m/production/review/M4A-V1R1/finished-hole-comparison.svg) is an original drawing, not a manufacturer drawing or physical fit result.

For rectangular leads, `Dlead = sqrt(bmax²+cmax²)`. Ordinary finished minimum is `Dnom−0.08 mm`; maximum is `Dnom+0.13 mm`. The tabulated **diametric** clearance is `Dmin−Dlead`; the screen target is ≥0.10 mm. It is not a guarantee of every multi-pin position-tolerance combination. Incoming keyed-header alignment and actual array dry-fit remain mandatory; do not force leads, ream finished plating or rely on hole precision as a locator.

| Ref / holes | Exact part / maximum lead basis | V1 → V1R1 drill mm | Finished range mm | Land mm | Minimum diametric clearance mm |
| --- | --- | --- | --- | --- | ---: |
| J101 / 16 | Würth 61201621621; 0.64 ±0.15 square, max 0.79 | 1.20 → **1.40** | 1.32–1.53 | 1.90 square | **0.203** |
| J502 / 3 | JST B3B-XH-A(LF)(SN); published 0.64 square, no lead tolerance; incoming screen ≤0.79 square | 0.95 → **1.30** | 1.22–1.43 | **1.90 × 1.95** | **0.103** |
| Q402 / 3 | Vishay IRF610PBF-BE3; external b/c max 0.91 × 0.61 | 1.30 → **1.40** | 1.32–1.53 | 1.905 × 2.00 | **0.224** |
| Q403 / 3 | ST BD140, SOT32; B/B1 max 0.88 × 0.63 | 1.30 → **1.40** | 1.32–1.53 | 1.90 square | **0.238** |
| J301 / 2 | JST B2P-VH(LF)(SN); published 1.14 square, tolerance missing; incoming screen ≤1.19 square | 1.70 → **1.90** | 1.82–2.03 | 2.70 square | **0.137** |
| J401 / 2 | Phoenix Contact 1727010; published 0.50 × 0.90, tolerance missing; incoming screen ≤0.55 × 0.95 | 1.10 → **1.30** | 1.22–1.43 | 2.00 square | **0.122** |

The last two connectors were additional genuine lead-fit concerns found during the required complete audit. Total changed holes: **29**, not only the original 25. No MPN, body, pitch, connector key, location, orientation, net or mating family changed. Only J502's outer land width increases (1.70 → 1.90 mm); its pad pitch stays 2.50 mm. The minimum revised nominal annulus is 0.25 mm. The audit separately reports geometric residual annulus at maximum finished hole and 0.075 mm eccentricity; this sensitivity is not confused with the nominal artwork annulus used by the manufacturer's DFM rules.

## Exact manufacturer evidence and limits

- [Würth 61201621621 drawing](https://www.we-online.com/components/products/datasheet/61201621621.pdf), revision 002.001, 2026-08-30: 2.54 mm pitch, 17.78 mm row span, 27.98 mm body. Its nominal recommended landing is not proof that all negative hole tolerance and maximum lead corners fit. Keep matching keyed female **61201623021** and verify straight-through cable pin 1 electrically.
- [Vishay IRF610 product](https://www.vishay.com/en/product/91023/) links the exact [92506 high-voltage TO-220 package](https://www.vishay.com/docs/92506/packageinformation_to-220ab_highvoltage.pdf), drawing 6031, revision F, 2024-09-30. Use external b/c dimensions, not base-metal b1/c1. A generic diode-family TO-220 drawing is not the selected MOSFET's authority. **1G/2D/3S, tab drain** remain unchanged.
- [ST BD140](https://www.st.com/resource/en/datasheet/bd140.pdf), May 2008 revision 5, drawing 0016114E: **1B/2C/3E**. Native 180° placement, illustrated face toward +PCB Y, 2 mm stand-off and insulated live collector are preserved. No other manufacturer's BD140 is assumed interchangeable.
- [JST XH catalog](https://www.jst.co.uk/downloads/series/eXH_1.pdf) and [VH catalog](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf) identify the actual headers and nominal square leads. They do not publish the needed maximum lead-width tolerance. The individual XH drawing download requires a contact/email request; none was sent. The stated larger limits are **engineering acceptance screens**, not invented manufacturer guarantees.
- [Phoenix 1727010 product drawing](https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mkds-1-2-381-1727010?type=pdf) identifies the 3.81 mm part and nominal 0.5 × 0.9 mm pin. Its suggested 1.1 mm hole does not supply a worst-case fit across JLCPCB's negative tolerance. The missing pin tolerance is disclosed.
- TI **TL431AIDBZR** remains the exact DBZ package, **1 cathode / 2 reference / 3 anode**, with cathode/reference on VREF_2V5 and anode on GND. [TI datasheet](https://www.ti.com/lit/ds/symlink/tl431.pdf). No historical anode/reference reversal is reintroduced.

## Hand assembly and maximum-hole behavior

Maximum holes are deliberately not interference fits. Hold each header square and seated while tacking opposed pins, then inspect every barrel and wetting/fillet; use suitable flux and ordinary through-hole soldering technique. Mechanical cable loads need strain relief rather than unsupported solder joints. Large-hole solderability and connector retention are first-article checks, not analytically proven here. Measure the actual supplied leads and dry-fit all pins before soldering; reject parts outside the screen or arrays that do not insert without force. Normal 1.6 mm connector lead length is retained.

The top-view key/pin map, actual exported nets and controller match are in [controller-compatibility.json](../hardware/80m/production/review/M4A-V1R1/controller-compatibility.json). Incoming sample measurements and physical lead fit remain **NOT_RUN**. No press-fit or individually negotiated finished-hole service remains in the order specification.
