# M5A-R2 sourcing gate and honest cost bridge

2026-10-15. **NO-GO for PCB commitment under the mandatory sourcing gate.** These are public observations and a counterfactual cost bridge, not a completed R2 BOM or supplier quote. No supplier was contacted and no cart/order was created.

## What is actually available as evidence

| Source/part | Retrieved observation | Still missing |
| --- | --- | --- |
| Mitsubishi official lineup, RA07/RA08N/RA08H | All three marked In production in the CSV behind the page | Fleet delivery commitment, formal application limits |
| GLYN RA07M1317M-501 | Catalog lists exact suffix | No matching entry in downloaded stock file; price, customer MOQ, 6/10/20 delivery, spares, lead time unknown |
| RF Parts RA07M1317M-501 | Live HTML: USD28.91 at1, USD27.46 at10, In Stock; new/not NOS; USD15 order minimum | Count available, 20-unit fulfillment, Germany shipping/lead time, traceable lot and delivered price |
| GLYN RA08N1317M-502 | Downloaded stock file lists **40** | Price/MOQ/allocation/lead time and spare/reorder terms; inventory is not a quote |
| RF Parts RA08N1317M-502 | USD28.91/27.46 at1/10, In Stock | Count and landed delivery terms |
| RA08H1317M-502 | GLYN catalog; RF Parts category USD32.91, as-low31.26 | Exact tier/available quantity/delivery and power-architecture justification |
| MAAV-011017-TR0500 | Mouser cut tape MOQ1/multiple1, EUR6.79/5.24/4.85 at1/10/25 | Recent EU stock is **0**, December2026/January2027 incoming, estimated24-week factory lead; delivery confirmation needed |

Sources: [Mitsubishi lineup CSV](https://www.mitsubishielectric.com/semiconductors/data/silicon_rf_module.csv), [GLYN RF catalog](https://www.glyn.de/produkte/leistungselektronik/hochfrequenz-transistoren/), [GLYN stock download](https://www.glyn.de/support/kaufmaennischer-support/lagerliste/download/), [RF Parts RA07](https://www.rfparts.com/module/rfpower-mosfet/mosfetpowermod-vhflp/ra07m1317m-501.html), [RF Parts RA08N](https://www.rfparts.com/module/rfpower-mosfet/mosfetpowermod-vhflp/ra08n1317m-502.html), [RF Parts category](https://www.rfparts.com/module/rfpower-mosfet/mosfetpowermod-vhflp.html), [Mouser EU attenuator](https://eu.mouser.com/de/ProductDetail/MACOM/MAAV-011017-TR0500?qs=ZcfC38r4Poug7XjsykdSjQ%3D%3D).

The manufacturer supplies 50 modules/tray. This is **not** evidence of a 50-unit customer MOQ. RF Parts offers individual modules; that is **not** evidence that 20 are in stock. GLYN's listed40 RA08N parts can cover the requested fleet numerically, but price and customer minimum remain unanswered. GLYN lists Mitsubishi in its [linecard](https://www.glyn.de/support/kaufmaennischer-support/lieferprogramm/); manufacturer authorization for this exact supply channel was not independently confirmed. RF Parts is a credible identifiable retailer, without an assumed authorized-distributor designation. Broker/marketplace counts were not accepted as production evidence.

The RF Parts RA07 page's HTML title retains `-101`, while H1, SKU and description identify `-501`. Require exact marking/lot confirmation; do not silently substitute old suffixes. The readable indexed page omitted the ten-unit tier; the directly retrieved live HTML includes it. Old indexed MAAV stock of1,603 conflicts with recent zero-stock/incoming pages and was rejected for current availability. DigiKey's alternative MAAV listing is non-stocked with MOQ2,000; it is not a small-series source. These discrepancies are preserved in the [observation record](../hardware/2m/review/M5A-R2/supplier-observations.json).

## Net EUR and complete scope

[ECB15Oct2026](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.eu.html): EUR1=USD1.1208. Thus module comparator is EUR25.79 at6 units or EUR24.50 at10/20. This is an informational conversion of the retail USD observation, **not** an EU quote or bank settlement rate. No20-unit discount is invented. Freight, import duty/classification, handling and applicable VAT remain separate and unquoted. The [German standard VAT rate](https://www.bundesfinanzministerium.de/Web/DE/Service/FAQ_Glossar/Glossar/Functions/glossar.html?lv2=176942&lv3=507052) is19%; apply separately where appropriate. Import VAT uses the relevant landed tax base and cannot be calculated from component price alone. No legal tax classification is assumed.

The [itemized accounting CSV](../hardware/2m/review/M5A-R2/accounting-bridge.csv) includes every fitted R1 reference at6/10/20, its value/MPN/source/status and proposed retained/removed disposition. Six RF blocks remove52 old physical positions **in accounting only**: final, driver, driver supply, final matching, series modulator and gate bias. The source, fundamental filter, normal output filter, interlocks, protection, training, converter and ports remain budgeted. Their remaining estimated/open sourcing is not magically resolved by the module.

At10, removed R1 material totals EUR17.04; retained4S scope is EUR33.66. Add RA07 EUR24.50, MAAV EUR5.24, analog-control allowance EUR1.00, bounded-bias/inhibit allowance EUR1.50, supply/protection-retuning allowance EUR0.50. Result: **EUR66.40**, EUR15.70 above R1. The last three allowances are **unquoted blocks with no final component count**, not invented procurement positions. MAAV's EUR display is conservatively held as a provisional net budget pending tax/checkout confirmation.

| Fleet | R0 2S /4S | R1 2S /4S | R2 accounting scenario 2S /4S | Retained training-only baseline |
| ---: | ---: | ---: | ---: | ---: |
| 6 | 74.61 /72.77 | 54.41 /52.48 | 71.18 /69.25 | 16.37 |
| 10 | 74.61 /72.77 | 52.63 /50.70 | 68.33 /66.40 | 16.37 |
| 20 | 74.61 /72.77 | 52.63 /50.70 | 68.33 /66.40 | 16.37 |

**The 2S column is incomplete:** it provisionally carries R1's converter cost, while that boost cannot produce regulated7.2 V across6.0–8.4 V. A valid replacement price can move the total either way. The4S column is also a scope estimate, not a connected, costed R2 electrical design. Neither number is a promised complete-board price. At10 the4S scenario is EUR6.36 below R0 but EUR15.70 above R1. A circa EUR36 board is unsupported by these observations.

The preserved proposed ADR-0013 still contains an older R1 estimate52.33/50.40. This comparison uses the actual current R1 machine-readable budget52.63/50.70, including the corrected fuse allowance. The historical proposal was not silently rewritten.

| Cost outside PCB-component comparison | Separate allowance/status |
| --- | --- |
| Bare two-layer PCB at6/10/20 | EUR3–8/board estimate only; no dimensions/artwork, no quote |
| Heatsink, M2.6 mounting, thermal compound | EUR6–12/module estimate; thermal capability must be specified |
| RF harness | EUR2–4 estimate; PCB RF connectors already retained in component scope |
| Antenna/feeder | EUR8–15 inherited estimate; ERP still unqualified |
| Battery/BMS/charger/controller/enclosure | Separate system accounts; no new quote or included hardware |
| Assembly and end-to-end acceptance | Labor excluded; record actual minutes during first qualified build |
| Shared instruments, engineering | Fleet/one-time costs, not per-board purchased material |

For scale, the4S scenario plus board/cooling/harness is EUR77.40–90.40 at10, before antenna/controller/pack/enclosure/labor/freight/VAT. It is not a finished-transmitter offer. No fictitious labor saving offsets the higher module price.

R1 physical counts remain264/258/104 for2S/4S/training, with23/23/14 ICs. The accounting bridge retains212/206/104 old positions respectively; new ancillary positions are unresolved, so **R2 fitted count and IC count are unknown**. This is not a claimed52-part reduction in an implemented PCB.

## Smallest information that closes the stop

Obtain, without ordering, a written offer from GLYN or another credible source stating exact suffix, price and currency/VAT basis at6/10/20 **plus one or two spares**, available/reservable quantity, customer minimum/multiple, lead time, Germany freight/import terms, manufacturer/lot traceability and replenishment status. RA08N's counted40 makes it the narrowly justified alternative to ask about if RA07 delivery fails. Confirm the selected amplitude-control part's actual cut-tape delivery as well.

No supplier communication has been sent because it is not authorized in this session. The user has been asked whether an existing confirmation is available. Until this gate is answered, do not release a module-specific PCB as the chosen production architecture. No additional transistor research is necessary to resolve it.
