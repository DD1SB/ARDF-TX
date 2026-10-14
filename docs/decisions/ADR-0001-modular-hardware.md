# ADR-0001: Three independently testable PCBs

**Status:** Accepted for architecture feasibility (not approval of an electrical design)

## Decision

Use exactly three functional PCBs as the primary modular architecture:

1. A **control PCB** with ESP32-class MCU, timing, configuration, battery monitoring, power management and an optional fitted Silicontra SX1262 LoRa module.
2. An **80 m RF PCB** encompassing RF synthesis (if local), independently testable CW output, switched Classic/Sprint output power, a 10 mW Foxoring operating mode, filtering and antenna interface.
3. A **2 m RF PCB** encompassing RF synthesis (if local), A2A generation, normal-output RF amplification, a separate very-low-power training output, filtering, sensing, and antenna interface.

All three may be connected in the full configuration. Omit either RF board and/or LoRa without firmware rebuild or modification of the other boards. A 2S4P pack represents the maximum reference pack; 2S1P through 2S4P are all supported as long as current and runtime constraints are respected.

The control board does not have to route 144 MHz RF through general-purpose control harnesses.

## Rationale

- Common control firmware and accessories; limited duplication.
- Easier low-power Foxoring-only build.
- Reproducible and separately measurable RF designs.
- Replace/upgrade the more difficult 2 m AM board without invalidating 80 m hardware.
- Preserve optional LoRa operation.

## Deferred to M1 analysis

- Per-RF-board versus common synthesizer (cost vs RF integration).
- Specific ESP32 family, module, timing reference and exact SX1262 module footprint/pinout.
- Connector pinout, high-current feed, grounding, ESD, and mechanical mounting standard.
- Power-stage design and calibrated level selection, including whether low-power and normal-power routes are separate.
- 2 m A2A implementation (keyed audio tone with continuous carrier vs keyed carrier with continuous tone).
- Charging architecture (pack-integrated BMS; whether charger is pack-side or control-side).
- Whether the 24-hour endurance requirement can be met with each pack size for each mode.

## Non-decisions

This ADR does **not** lock Si5351A, specific transistors, PA supply voltage, connector footprint, LoRa pinout, layer count, or board form factor.

## M1 proposal follow-up (2026-10-13)

Placement/safety/antenna/energy options were researched in [M1 architecture](../M1_SYSTEM_ARCHITECTURE.md). ADR-0003 through ADR-0006 propose choices for user review. This accepted ADR's status is unchanged; new proposals are not automatically accepted.
