# M6-C1R1 independent review decision

**GO for independent review of five unpopulated controller evaluation PCBs. No manufacturing authorization or acceptance tag.**

Finding A is corrected in the native schematic and routed PCB using a pack-derived, reverse-isolated resistor-ID excitation,180k/33k positive-fault divider, negative clamp and100k ADC discharge/load. This adds five inexpensive purchased parts and no IC. External10k/22k codes, J1 numbering, all GPIOs and all36 RF connector pins remain. The hardware/decoder binding is now **PACK_ID_FRONTEND_REV2**; the former3.3V-excited decoder must not be used. [Input engineering](M6_C1R1_INPUT_PROTECTION.md).

Finding B closes with a **justified no-change** decision. U3 pin5 remains V3V3 with C10; both the USB electrical topology and copper are unchanged. The assessment uses ST's rail-to-rail mechanism/working-voltage rating, upstream device example and VCC-bias guidance, rather than treating the pin name as a requirement. It does not claim IEC immunity. [USB review](M6_C1R1_USB_ESD_REVIEW.md).

The100×100mm board retains standard two-layer1.6mm FR4/1oz, green mask, white legend, lead-free HASL and ordinary0.80/0.30mm vias. No custom process or active-IC redesign. Protection is concentrated near J1; the established long ID route is reused on the protected side. R19 is a local ADC pull-down. Six small positions (five added plus relocated R3) are on the underside; preserve at least the prior10mm underside clearance and trim THT leads. Connector/mounting locations and RF contracts are unchanged. All existing footprints except relocated R3 retain their positions.

ERC/DRC each have **0 errors and0 warnings**, unrouted/parity0, no exclusions. The native DFM and electrical/artifact/host regressions pass. [Exact coverage](M6_C1R1_ELECTRICAL_VALIDATION.md) includes704 pads,4096 enables,20 retained electrical mutations,16 new protection checks,7 DFM mutations,40 host tests and the strict C11 fixture. All111 original M6-C1 review files and1220 RF files are preserved.

Quantity-ten estimates become **FOX_MIN18.99 EUR, RF80_FULL19.26 EUR, RF2M_FULL19.30 EUR, UNIVERSAL22.34 EUR net/unit**: +0.28 each. Significant unquoted material remains; D23's live EU stock/price needs confirmation. [Complete q1/10/20 costs](../hardware/controller/review/M6-C1R1/COST_DELTA.md). Bare-board process/price model is unchanged and unquoted. Optional LoRa remains **HOLD/DNP**.

| Gate | Status |
|---|---|
|A electrical/CAD correction|PASS for defined DC faults and manufacturer-backed topology assessment; commissioning assumptions explicitly identified|
|B ordinary JLCPCB manufacturability|PASS local native/artifact checks; factory CAM not submitted|
|C five bare evaluation boards|GO for independent review/quotation preparation; user approval and supplier CAM remain separate|
|D controlled electrical commissioning|NOT_RUN: qualified ID/ADC calibration, cold/continuous negative clamp, startup/brownout/abrupt loss, backfeed and USB/RTC/fail-off measurements required|
|E transmitter operation|NOT_RUN; RF80/RF2M RF, AM, spectral, thermal, antenna and endurance gates remain|

A0.29V cold-clamp sensitivity and the illustrative VF/leakage calibration bounds are **not manufacturer guarantees or measured results**. Do not fit/enable the MCU for fault tests until the staged power-only checks establish safe conditions. Rail ramps and IEC pulses are not certified by DC calculations. Failure of a physical gate requires correction before use; it does not turn the bare-board review into an operational approval.

Use the [new review package](../hardware/controller/review/M6-C1R1/README.md) and its final fabrication directory. No files were uploaded, parts/boards ordered, hardware assembled/powered, or RF transmitted. Commit the engineering candidate without an acceptance tag and stop for independent review.
