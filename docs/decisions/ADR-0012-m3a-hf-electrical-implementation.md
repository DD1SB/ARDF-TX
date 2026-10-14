# ADR-0012 — M3A 80 m electrical implementation

Status: **Proposed — schematic review only**  
Date: 2026-10-14

Implement [M3A](../M3_80M_REVIEW_DECISION.md) as one SignalSlinger/FlexFox80 Si5351/LM5134B/IRF610/transformer/filter stage, approximately 3 W full /1.2 W extended on 4S with one bounded buck. Adapt the QCX integrator with ST BD140 and appropriate base drive/RC values. Keep the same RF PCB population variants and a separate, 2S-compatible TinyFox NAND-buffer mechanism using SN74AC00DR where HC00 drive margin is insufficient.

This amends the **implementation proposals** in ADR-0010/0011 and details of conditionally accepted ADR-0004: shared fused/reverse-protected pack input, local lease/SCL fault latch, latched rail selection, independent normal rail and driver inhibit, hot/open NTC window and independent Fox RF mute. Detector, DAC, local MCU, EEPROM and I²C-isolator allowances are omitted with explicit failure-mode assessments and validation gates.

The minimum **1 dB Fox pad**, 27 Ω source resistor and **100 mW accessory fault withstand** are proposed alongside nominal 10 mW calibration. They are unvalidated protection calculations, not a replacement for measured nominal output, fault energy and field reach. No watt-output routing to the compact port exists.

Reasons: a documented programmable RF core, 4S headroom for one buck, current component evidence, improved HF shaper thermal documentation, and a Fox branch independent of the watt PA. Full module components at ten are €25.35, above the €20 target. Necessary filters/fail-off functions are retained; unquoted magnetics/passives/ancillaries and exact driver stock remain open.

Accepted modular/controller/local-synthesis/antenna-separation decisions and the **2 m true-AM 1 W carrier ERP** target remain intact. ADR-0010/0011 remain proposed. The user's M3A instruction authorizes electrical schematic development, not blanket adoption of earlier power proposals or manufacture.

Acceptance requires electrical review, separate authorization for a small evaluation layout and the [E0–E9 tests](../M3_80M_TEST_PLAN.md) before product release. No order, fabrication or hardware-validation claim follows from this proposal.
