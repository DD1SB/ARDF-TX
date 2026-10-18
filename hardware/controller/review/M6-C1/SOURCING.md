# M6-C1 source and cost evidence

Retrieved2026-10-18. These are catalog observations, not reservations, quotations or proof of future delivery. Net EUR; VAT/freight/import/labor separately excluded. The BOM reports every unquoted position and MOQ as OPEN rather than treating a manufacturer's reel as a customer minimum.

| Item | Evidence | Quantity1 /10 /20 EUR net |
|---|---|---|
|ESP32-S3-WROOM-1-N4|Mouser356-ESP32-S3WROOM1N4, cut quantities MOQ1; indexed inventory, not reserved|4.48 /3.88 /3.88|
|RV-3032-C7-32.768KHZ-2.5PPM-TA-QA|Mouser428-203853-MG01, cut tape MOQ1; current page2278 and series index4353 disagree on stock snapshot|3.66 /2.75 /2.75|
|Silicontra option|LCSC C42381682 lists TR8-GC, manufacturer document ZTR8-GC; exact equivalence OPEN|EUR FX allowance5.60 /4.80 /4.80, NOT exact-part EU quote|
|All other components|Exact MPN/function/landing selected, distributor order codes/stock/MOQ unquoted unless individually recorded|engineering allowances, no invented supplier quantity breaks|

Price links: [MCU](https://www.mouser.de/de/ProductDetail/Espressif-Systems/ESP32-S3-WROOM-1-N4?qs=Li%252BoUPsLEnsO%2FkiJOUK0FQ%3D%3D), [RTC](https://www.mouser.de/de/ProductDetail/Micro-Crystal/RV-3032-C7-32.768kHz-2.5PPM-TA-QA?qs=MyNHzdoqoQJ7wc0xcM4bYA%3D%3D). No discount at25 is applied to a20-unit basket. An observed price does not establish the entire board cost.

BOM-all.csv lists per-reference quantities(one each), manufacturer order codes, package/footprint, groups, exact population and1/10/20 allowances. Variant CSVs are complete fitted baskets; the DNP list is separate JSON. Source URLs in the BOM are primarily manufacturer technical evidence, not a claim that a distributor has stock. Critical unquoted positions include the RTC backup holder/cell, connectors/cables, small CMOS and exact non-E4 LVC244 buffers. TCA9517 and TMUX1511 have the focused observations below. Quote/check these before procurement. LoRa remains a distinct optional population HOLD.

The selected SF-1206F100-2 is a real Bourns1A/63V fuse, not the unverified initially drafted1206L100/24YR code. Its commercial cut-quantity channel exists, but the local EUR allowance remains unquoted. Do not substitute a6V-rated PTC. Inspect the exact marked part and its documented fuse rating.

Bare-board pricing is deliberately an unquoted area/setup model. The100×100mm standard board can be entered with ordinary JLC options; no upload, automated quotation or factory CAM check has occurred. The JSON separates5/10/20-board batch estimates, freight and stencil. External CR1220 cell, IDC cables, identified fused harness and M3 supports are separate material allowances. RF boards, antenna, battery/BMS, charger, enclosure, assembly and calibration are excluded.

Additional focused observations: [TCA9517DR](https://www.mouser.de/de/ProductDetail/Texas-Instruments/TCA9517DR?qs=sGAEpiMZZMtBex5xLiqNf21FSwo%252BV6vVEEOGUmytcQY%3D)€1.09/0.809 at1/10, stock snapshots6351–6900, MOQ1; [TMUX1511PWR](https://eu.mouser.com/pl/ProductDetail/Texas-Instruments/TMUX1511PWR?qs=qSfuJ%252Bfl%2Fd5zYDGvtvg4tg%3D%3D)€0.568/0.401,55 indexed stock, MOQ1. Quantity20 uses the10break. These replace initial unquoted allowances.

[AP63203WU-7 at Mouser](https://www.mouser.de/de/ProductDetail/Diodes-Incorporated/AP63203WU-7?qs=u16ybLDytRZ1JqxbuLkMJw%3D%3D)shows0stock despite an orderable cut-tape price. It is not counted as immediately purchasable there. [LCSC C780769](https://www.lcsc.com/product-detail/DC-DC-Converters_Diodes-Incorporated-AP63203WU-7_C780769.html)shows8165stock, MOQ1, USD1.217/1.0856 at1/10. The BOM uses those amounts as an explicit1EUR/USD budgeting allowance, not a market exchange-rate claim or EUR quotation. Freight/import remain separate. Reconfirm lifecycle and delivery before fleet procurement.

The revised SN74LVC244APWR allowance uses the priced E4-suffix package comparator (€0.963/0.692); exact non-E4 price/stock remains OPEN. This comparator is classified as an estimate, not an observed exact-part price or an automatic component substitution. Remaining small CMOS/passive allowances remain unquoted.

Final controller port switches are TPS22918DBVR, active in TI’s product record, in ordinary DBV SOT-23-6. The €0.35 each allowance remains unquoted with stock/MOQ OPEN. It replaces the earlier €0.28 TPS22919 draft basket; the change adds €0.07 per fitted RF port and supplies a defensible hot-resistance budget. Manufacturer product record/datasheet: https://www.ti.com/product/TPS22918 and https://www.ti.com/lit/gpn/tps22918. No device was purchased.
