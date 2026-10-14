# ADR-0012 — M3A 80 m electrical implementation

Status: **Proposed — schematic review only**  
Date: 2026-10-14

Implement [M3A](../M3_80M_REVIEW_DECISION.md) as one SignalSlinger/FlexFox80 Si5351/LM5134B/IRF610/transformer/filter stage, approximately 3 W full /1.2 W extended on 4S with one bounded buck. Adapt the QCX integrator with ST BD140 and appropriate base drive/RC values. Keep the same RF PCB population variants and a separate, 2S-compatible TinyFox NAND-buffer mechanism using SN74AC00DR where HC00 drive margin is insufficient.

This amends the **implementation proposals** in ADR-0010/0011 and details of conditionally accepted ADR-0004: shared fused/reverse-protected pack input, local lease/SCL fault latch, latched rail selection, independent normal rail and driver inhibit, hot/open NTC window and independent Fox RF mute. Detector, DAC, local MCU, EEPROM and I²C-isolator allowances are omitted with explicit failure-mode assessments and validation gates.

The minimum **1 dB Fox pad**, 27 Ω source resistor and **100 mW accessory fault withstand** are proposed alongside nominal 10 mW calibration. They are unvalidated protection calculations, not a replacement for measured nominal output, fault energy and field reach. No watt-output routing to the compact port exists.

Reasons: a documented programmable RF core, 4S headroom for one buck, current component evidence, improved HF shaper thermal documentation, and a Fox branch independent of the watt PA. Full module components at ten are €25.35, above the €20 target. Necessary filters/fail-off functions are retained; unquoted magnetics/passives/ancillaries and exact driver stock remain open.

Accepted modular/controller/local-synthesis/antenna-separation decisions and the **2 m true-AM 1 W carrier ERP** target remain intact. ADR-0010/0011 remain proposed. The user's M3A instruction authorizes electrical schematic development, not blanket adoption of earlier power proposals or manufacture.

Acceptance requires electrical review, separate authorization for a small evaluation layout and the [E0–E9 tests](../M3_80M_TEST_PLAN.md) before product release. No order, fabrication or hardware-validation claim follows from this proposal.

## Proposed R1 amendment — 2026-10-14

Status remains **Proposed**, not accepted. R0 is preserved at Git tag `m3a-r0`. Adopt the corrected [R1 netlist/control model](../M3A_R1_LOGIC_AUDIT.md): HC123 Q13 lease, /Q12 bus holdoff with POR/SCL/SDA qualification, spare heartbeat witness, HC174 raw ARM/path/mode/key-low acceptance and health-cleared context, selected-request withdrawal reset, consolidated open-collector watt guards and a Fox-only population omitting watt monitoring. Delete U213/U214; use one qualified key tail with100 Ω unarmed discharge. Low-current sinks use±20 V-gate BSS138BK; high-current Q404 retains DMN2056U. R410/25SVPF47M bound driver rise subject to≤20 µs physical isolation and≤0.5 Ω transient ESR. TPS22810 input must remain≤18 V (20 V absolute);28 V is an isolated passive stress simulation outside system rating. Input transient/clamp coordination remains OPEN.

Current full/Fox components at ten are€26.60/€10.80 net estimates;18/13 ICs. These supersede this proposal's R0€25.35 figure only for the revised implementation. No proven material saving or hardware safety/performance claim follows. Conditional small evaluation-layout recommendation requires electrical review; actual layout/procurement/manufacture still need authorization. The [R1 physical gates](../M3A_R1_VERIFICATION.md) and original E0–E9 remain OPEN. No accepted ADR, module architecture or VHF target is changed.


## Proposed M3B evaluation amendment — 2026-10-14

Status remains **Proposed**, not accepted. The user authorized evaluation PCB layout/review artifacts in M3B; no order or fabrication is authorized. Adopt the [M3B-E1 evaluation implementation](../M3B_REVIEW_DECISION.md): two-layer210×160 mm board, separate normal/Fox paths and unchanged R1 safety logic; add1.5 Ω/100 µF normal-input damping with upstream pack sensing/50 V C314, local transformer-feed100 nF bypass, actual0603 fuse lands, qualified IDC holes and conservative1.3 mm IRF610 holes. Preserve transformer electrical connections and all original elliptic-filter values.

The TPS22810 remains an18 V-operating device: the TVS is not credited as an18 V clamp. Wiring/source/transient qualification and≤20 µs driver-rail withdrawal remain physical gates. Full/Fox candidate components at ten are€27.311/€10.815 net; all new prices are estimates. CAD ERC/DRC0 and current-netlist256/31/16 do not validate analog/RF/thermal safety. GO applies only to independent review and a later explicitly approved small **bare evaluation PCB** order; all physical gates remain NOT_RUN. No accepted ADR, controller or VHF target changes.
