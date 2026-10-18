# ARDF-TX universal controller — M6-L1 candidate

Active KiCad 10 sources are CTRL.kicad_pro, CTRL.kicad_sch and CTRL.kicad_pcb, with local ARDF_CTL libraries. M6-L1 closes the optional Silicontra 433/868 MHz nominal package, pin-map, population and RF-feed review on the M6-C1R1 electrical baseline. One PCB supports NO_LORA, LORA_433 and LORA_868. The 5.25 × 0.45 mm signal feed is retained; a small top-ground intrusion in the Hirose underbody keep-out is corrected. See [the review package](review/M6-L1/README.md) and [decision](../../docs/M6_L1_REVIEW_DECISION.md).

Both RF contracts, GPIOs, RTC, safe gating, USB and the R1 pack-ID correction remain. The PACK_ID_FRONTEND_REV2 decoding/calibration contract and external 10k/22k identities remain mandatory. Five added small positions plus relocated R3 are on the underside; retain R1's mirrored assembly/bring-up instructions. M6-C1 and M6-C1R1 reviews remain historical evidence.

Choose an explicit base/radio BOM and a trusted exact module/antenna configuration; an SX1262 response cannot identify its RF band. Unknown/unusable LoRa disables LoRa TX and leaves otherwise valid autonomous ARDF operation available. Default native population is NO_LORA. Host fixtures are not production or target-operating firmware.

GO means independent five-bare-board manufacturing review and optional assembly preparation only. No acceptance tag or manufacturing/operational release. All physical electrical, USB/ESD, RTC, radio coexistence, RF/AM and endurance gates remain NOT_RUN. No supplier upload, order or physical operation is authorized.
