# RF2M — M5B-E3 evaluation PCB

The active editable design is **M5B-E3**, an integrated **180 × 140 mm, two-layer, 1.6 mm / 1 oz FR4** 144 MHz true-AM evaluation board. It uses ordinary JLCPCB options: green mask, white legend, lead-free HASL, standard through-vias and no controlled impedance or special process. **NOT RELEASED; all physical qualification remains NOT_RUN.**

Start with the [review decision](../../docs/M5B_E3_REVIEW_DECISION.md), [engineering changes](../../docs/M5B_E3_ENGINEERING_CHANGE.md), [RF/stackup analysis](../../docs/M5B_E3_RF_STACKUP.md), [thermal/mechanical review](../../docs/M5B_E3_THERMAL_MECHANICAL.md), [DFM audit](../../docs/M5B_E3_JLCPCB_DFM.md), [manufacturing/cost report](../../docs/M5B_E3_MANUFACTURING_COST.md) and [bring-up procedure](../../docs/M5B_E3_BRINGUP.md).

The [current review package](review/M5B-E3/README.md) contains fresh schematic, copper/assembly/placement views, actual KiCad 3D renders, BOMs, logical/physical netlists, ERC/DRC, native-geometry DFM and regression reports, proposed Gerbers/drills and checksums. The native project remains `RF2M.kicad_pro`, `RF2M.kicad_sch` and `RF2M.kicad_pcb` in this directory. Full BOOST2S, BUCK4S and TRAIN_ONLY assemblies use this same PCB; the two converters are mutually exclusive.

E2 is preserved at **m5b-e2 / 2ca4c8e**. Its manufacturing-review recommendation is superseded by the standard-process E3 redesign. E1, R4 and earlier tags/archives remain historical references. Do not run historical CAD generators or point-in-time development aids against the finished board. Reproduce current checks using the commands in the package README and `tools/m5b_e3.py`.

Calculated line impedance, power losses and thermal models are engineering estimates. Actual RF gain, carrier/PEP, sine-AM depth, emissions, isolation, protection timing and endurance remain unmeasured. No upload, order, procurement, manufacture, assembly, power-up or RF operation is authorized. Independent review and explicit user authorization precede any external fabrication submission.
