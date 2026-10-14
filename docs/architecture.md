# Logical architecture — preliminary

**Power review, 2026-10-14:** the [2S/4S comparison](M2_BATTERY_ARCHITECTURE.md) and [proposed decision](M2_POWER_ARCHITECTURE_DECISION.md) evaluate a dual-voltage controller and mode-dependent RF supply/pack capabilities under the revised 12 h full / 24 h reduced requirement. [ADR-0011](decisions/ADR-0011-dual-voltage-power-and-endurance.md) remains proposed. The original 2S sketch below is retained history, not authorization to connect its old components to 4S.

**M1 cost rework, 2026-10-13:** the detailed [M1 system architecture](M1_SYSTEM_ARCHITECTURE.md), now conditionally accepted, specifies direct ESP32 control of inexpensive local sources, minimal discrete RF stages, nine logical interface functions plus separate power, local persistent fail-off and separate bounded low-power paths. [ADR-0007](decisions/ADR-0007-cost-optimized-m1.md) revises the implementation proposals; **complete layout/procurement remains gated by RF evaluation**. The [M2 preparation](M2_PREPARATION.md) develops reviewable circuits and bench gates. This initial logical sketch remains context; the revised document governs proposed semantics and open issues.

```text
                External protected 2S1P ... 2S4P battery pack
                                |
                    protection / regulated rails
                                |
              +-----------------+-----------------+
              |                                   |
       CONTROL PCB                             Power distribution
  ESP32 + timer/timebase                       (fused/filtered)
  config + sensors + safety                         |
  optional Silicontra SX1262                       |
              |                          +----------+-----------+
              |                          |                      |
        control & I2C               80 m RF PCB             2 m RF PCB
              +-------------------> CW synthesis            AM synthesis
              |                    CW key shaping           keyed tone/envelope
              +-------------------------------------------> PA/modulator
                                   selectable 10 mW         normal 0.25–1 W ERP
                                   / 0.3–1 W /1–5 W         and isolated training
                                   LPF + 80 m tuner         filter + RF outputs
```

Synthesis may be local to each RF PCB or shared; M1 must evaluate both and decide based on cost, crosstalk, connectors, and testability. Keep 144 MHz off unshielded digital harnesses unless validated.

## 80 m antenna systems — independent RF qualification

The *same 80 m RF board* must support two substantially different physical installations:

| Attribute | Classic / Sprint | Foxoring field transmitter |
| --- | --- | --- |
| Antenna | Longer vertical wire and practical earth/counterpoise arrangement (an example is approximately 8 m vertical wire and 6 m ground wire) | Very short vertical radiator, approximately 30 cm in the IARU rules, with a compact, defined counterpoise |
| RF level | Profile-dependent watts (Classic/Sprint) | 10 mW output, continuously keyed CW |
| Matching | Designed and tested for longer-wire setup | Separately analyzed loading/matching/coupling; do not assume the long-wire tuner or a 50-ohm connector automatically matches the short radiator |
| Objective | Appropriate competitive coverage | Audible at marked position and 30 m; not audible at 250 m, with representative receiver and terrain conditions |
| Safety | Proper RF current/voltage ratings | Protect the low-power path and short-antenna match against accidental full-power selection |

Do **not** infer radiated ERP or audibility from nominal conducted 10 mW. The 30 cm radiator is electrically very short at 3.5 MHz, so displacement currents, losses, body/ground coupling, location, moisture, nearby objects, and counterpoise can dominate field results. Define a conducted RF reference point **and** field-validation procedure. Make the user-installable antenna/matching arrangement compact enough for a 2S1P Foxoring build.

**M1 implementation decision remains open:** separate antenna sockets, selectable internal matching, or an external passive matching adaptor. Analyze BOM cost, complexity, mistakes in the field, and whether mode selection can inadvertently drive the short-antenna path with watt-level RF. All necessary matching hardware counts toward total mode-specific cost.


## Proposed *logical* module control contract

- Dedicated `RF_ENABLE` (hardwired fail-off) and `KEY` per populated RF board.
- At least two power-select inputs, or equivalent robust serial control with a fail-safe fixed limit.
- Shared configuration interface (e.g., I2C) for local RF synthesizer, module ID/limits and sensing.
- Separate power and return capacity suitable for the actual PA currents, not necessarily routed through the logic connector.
- Optional `FAULT`, `PRESENT` (or equivalent verifiable passive identification) and power-good signals.
- Actual voltage levels, protective resistors, pull states, pinout, thermal and RF grounding **not yet specified**.

### Important signal distinction

80 m `KEY` means shaped A1A RF carrier gating. 2 m `KEY` means A2A Morse envelope control; `RF_ENABLE` controls overall carrier activation. Tone generation/envelope shaping may be on the RF board; simple CW gating must not inadvertently convert 2 m A2A into A1A.

## Safe operating states

1. Battery insertion / ESP32 boot: all RF hardware forcibly disabled independent of GPIO initialization.
2. Unknown module, LoRa absent, time invalid, battery unsafe, PA thermal fault: follow documented policy and keep transmit path off where unsafe.
3. Idle/non-slot: no RF emitted from synthesizer, PA, leakage or antenna (§T2.4).
4. Frequency changes: mute power path, apply synthesizer update, verify settle, then enable in next scheduled window.
5. Loss of remote contact: already verified contest schedule continues locally; stale/unauthenticated remote commands ignored.

## Mechanical strategy

A shared set of board-to-board design guidelines and harness/interface specs is required, but **do not** presuppose identical connectors if PA power/current requires distinct protected distribution. Receiver/LoRa isolation, antenna separation, and coupling across 3.5/144/868 MHz require design reviews.


## M3A electrical implementation for review — 2026-10-14

The [80 m schematic](../hardware/80m/RF80.kicad_sch) now implements the narrowly authorized3 W/1.2 W4S normal path and separate2S-compatible Fox population. Its [circuit review](M3_80M_SCHEMATIC_REVIEW.md) defines the16-contact logical interface, bounded3.3 V domain, independent raw-power pair and dissimilar antenna ports. [ADR-0012](decisions/ADR-0012-m3a-hf-electrical-implementation.md) is proposed; accepted ADRs and pendingADR-0010/0011 are preserved. Controller dual-voltage qualification and VHF A2A/PEP remain separate gates. No layout/manufacture or validated hardware follows from schematic/ERC completion.
