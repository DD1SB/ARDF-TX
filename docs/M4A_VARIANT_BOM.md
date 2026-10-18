# M4A — full/Fox variants and installed cost

Date: **2026-10-15**. EUR **net**, VAT excluded; no tax treatment, quote, stock reservation or order is implied. [Itemized6/10/20 BOM](M4A_VARIANT_BOM.csv), [machine cost inputs/totals](M4A_COSTS.json), [reference-specific populations](../hardware/80m/production/review/M4A-V1/population.csv). All prices retain E2's explicit historical observation/estimate classification and supplier/MPN/MOQ/multiple fields. New PCB/harness/cooling numbers are **unquoted planning allowances**, not achieved savings.

## Populations

Full assembly fits **196 purchased physical parts /18ICs**. Fox-only fits **115 /13** on the **same physical board**. All non-test component identities, values and population fields match E2. Removing60 copper test pads changes no purchased-part count or component material cost. The two-layer board, connectors, proven RF devices and all necessary protection remain.

Full uses the normal buck/driver/IRF610/shaper/transformer/elliptic filter plus independent Fox branch. Fox-only omits every NORMAL part, including U301/U302/U312/U313/U401/Q402/Q403/T401/L410/L411/J401/TH301 and cooling hardware; fits **R228/R348/R349**. R228 fixes PA_GUARD_RAW low; the unused comparator inputs are grounded by R348/R349. PA requests cannot arm a watt output. Fox RF is powered from regulated controller3.3V through its independent limited/shaped branch; protected2S provides pack sensing, not raw voltage to the CMOS buffer. No normal PA or buck is a Fox dependency.

Fox-only keeps the same **150 × 110 mm** bare PCB and shared control/safety
area. It saves the normal-power components, windings and cooling volume;
it does not acquire a TinyFox-sized dedicated board. Its separate short
radiator, compact counterpoise and loading accessory remain necessary. This
is the explicit cost/size trade-off of one maintainable RF80 PCB and common
ESP32/RTC architecture; no fourth board or extra MCU is introduced.

The static population/power-domain checks preserve the E2 design and reject incorrectly fitted links. They do not prove silicon backpower, partial-rail behavior or RF isolation: those remain physical tests. One remote thermistor is purchased on the full BOM but externally bonded; do not buy or fit two sensors. Test pads, mounts and DNP links are not extra ICs or duplicate purchases.

| Batch | Full components/unit | Historical observed /estimated share | Fox components/unit | Historical observed /estimated share |
| --- | ---: | ---: | ---: | ---: |
|6|31.896|13.103 /18.793|12.081|4.759 /7.322|
|10|27.311|9.346 /17.965|10.815|3.593 /7.222|
|20|27.311|9.346 /17.965|10.468|3.558 /6.910|

Same-MPN needs are pooled within each population; MOQ/multiple and leftover costs are included. Historical quantity discounts are retained, not assumed newly negotiable. Full/Fox functional-block allocations and every line's required/ordered quantities are in the JSON/CSV. There is **zero achieved component saving versus E2**. No EOL or unknown marketplace transistor replaces the selected devices.

## Fabrication and panel assumptions

Candidate board150×110mm. A **two-up160×232mm** planning panel includes a2mm routed gap and5mm outer rails;6/10/20 boards require3/5/10panels with no excess boards. This is an integration proposal, **not released panel Gerbers**. The supplier must confirm tooling, breakout tabs, copper-edge distances, registration, finished-hole tolerance, mask/finish and shipment dimensions before a panel is manufactured. Unpanelized board files remain the review artifacts.

The allowance model uses **€12–25 setup/lot plus€180–350/m² of panel area**. These are engineering assumptions, not supplier observations. It yields per-board bare material allowances **€5.34–10.66 /€4.54–9.00 /€3.94–7.75** at6/10/20. **Mandatory tight-hole process surcharge remains OPEN**, as do freight and yield. These ranges are not guaranteed ceilings. The same area model would save roughly€3.23–6.29 per board versus two-up E2 geometry; no saving is booked as purchased or quoted. The frozen five-board E2€45–90 allowance remains a different lot/scope.

## Complete installed RF-module allowance

| Net material/unit | Full6 | Full10 | Full20 | Fox6 | Fox10 | Fox20 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
|PCB components, including board-side connectors|31.90|27.31|27.31|12.08|10.82|10.47|
|Bare PCB base allowance|5.34–10.66|4.54–9.00|3.94–7.75|5.34–10.66|4.54–9.00|3.94–7.75|
|Additional mating harness/wiring|4–8|4–8|4–8|3–6|3–6|3–6|
|Antenna/matching/accessory materials|17.75|17.75|17.75|8.20|8.20|8.20|
|Thermal materials|2–6|2–6|2–6|0|0|0|
|Mount/insulation materials|0.80–2|0.80–2|0.80–2|0.80–2|0.80–2|0.80–2|
|**Installed RF-module base allowance**|**61.79–76.31**|**56.40–70.06**|**55.80–68.81**|**29.42–38.94**|**27.36–36.01**|**26.41–34.41**|

Add **OPEN tolerance-process surcharge, freight, tax and labor** to those base totals. Full scope includes **both independent antenna accessories**, not two concurrently transmitting paths. A Classic/Sprint-only installation can defer the€8.20 Fox accessory while retaining its PCB electronics. Board-side RF/power/control connectors are already in components and are not charged again as harness mates.

The antenna amounts are reconstructed from the preserved M1 accessory BOM: normal long-wire/counterpoise/loading/tuning/support **€9.55**, compact Fox coil/tuner/voltage-rated caps/key/support/~30cm radiator/compact return/protection **€8.20**. The old generic normal PCB RFPORT allowance is removed once because the actual J401 is already priced. The legacy compact PADRES allowance (€0.18) is also excluded: the actual PCB already includes R513/R514/R515 for nominal-output calibration. This is a duplicate allowance removed from the installed scope, not a deleted circuit or a supplier discount. Any additional field-only attenuation found necessary during antenna qualification would be a separately justified accessory change. The Fox accessory plug/identity (€0.55 ACCESSKEY) is already in matching materials; the extra harness allowance covers controller/power mates, wire and relief, and excludes that plug. When combining with a complete-transmitter ledger, replace its RF/harness/accessory scope rather than adding this entire installed subtotal on top of an already costed module. All matching values/MPNs remain candidates requiring installation/field qualification;€3 trimmers and wire are not free. The compact antenna is not a low-powered Classic wire. Antenna material allowances do not establish field reach or tuning labor.

The **common ESP32-S3 controller/RTC/optional LoRa, battery cells/BMS, chargers and final enclosure are separate system ledgers**, unchanged by this RF-only milestone. They are excluded from the table, never counted as zero complete-transmitter cost. The [Fox complete-unit audit](FOXORING_COST_AUDIT.md) remains historical scope evidence; this is not a repetition of the€77.11 accounting error.

## Labor and sourcing limits

Unpriced planning effort: manual full-board assembly2–5h, winding/installation0.5–1h; Fox assembly1–3h; later fixture calibration roughly15–30min full/10–20min Fox once qualified. These are **unmeasured allowances**, not achieved cycle times or a contracted labor price. Initial RF/thermal/field qualification and12/24h endurance are engineering work, not hidden per-unit “free testing.” Compact assembly may increase rework difficulty; a smaller board does not automatically save labor.

No connector substitution is booked: the existing keyed/physically distinct ports reduce harness mistakes and preserve interlocks. Shared0603 passives/packages and mixed hand/contract assembly are already represented in the actual BOM. Re-quote exact cut-tape quantities and verify MSL/stock/suffixes. [TI](https://www.ti.com/product/LM5134/part-details/LM5134BMF/NOPB) lists the driver active but its public page reports out of stock; the new DigiKey retrieval failed, so no new quantity/price is claimed. [ST](https://www.st.com/en/power-transistors/bd140.html) lists BD140 active in production. Tight-hole capabilities/prices, custom core supply, capacitor ESR and mating-contact variants remain procurement checks. None justify silently replacing the proven RF chain.
