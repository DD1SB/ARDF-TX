# ARDF-TX universal controller — M6-C1R1 candidate

Active native KiCad10 sources: CTRL.kicad_pro, CTRL.kicad_sch and CTRL.kicad_pcb with local ARDF_CTL libraries. M6-C1R1 corrects battery-ID fault exposure; it retains the justified3.3V USB ESD reference. Both RF contracts, GPIOs, controller architecture and100×100mm standard-JLCPCB construction remain.

Use [review/M6-C1R1](review/M6-C1R1/README.md) and [the decision](../../docs/M6_C1R1_REVIEW_DECISION.md). M6-C1 at31ac3eb and review/M6-C1 remain historical evidence. The new PACK_ID_FRONTEND_REV2 decoding/calibration contract is mandatory; external10k/22k ID resistors and J1 numbering are preserved. Six small positions are on the underside (five added plus relocated R3); see the mirrored bottom assembly view and bring-up instructions.

GO means independent five-bare-board review only. No acceptance tag, supplier upload, manufacturing or operational release. Optional Silicontra LoRa remains HOLD/DNP. All physical electrical, USB/ESD, RTC, RF/AM and endurance gates remain NOT_RUN. The host fixtures in firmware/controller_hw are not production or target-operating firmware.
