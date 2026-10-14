# ADR-0010 — Proven 80 m RF core and economy power target

Status: **Proposed amendment; architectural review required.**  
Date: 2026-10-13

**Pending power reassessment, 2026-10-14:** [ADR-0011](ADR-0011-dual-voltage-power-and-endurance.md) proposes a 4S single-buck higher-power alternative and 3 W full / 1.2 W extended profile under the user's new 12/24 h requirement. This earlier amendment remains proposed; its RF evidence and historical cost/energy arithmetic are preserved.

## Context

The user requests comparison of actual proven schematics before developing another universal 5 W circuit. ADR-0007 conditionally accepts the modular architecture, while its detailed HF proposal and ADR-0008's seven-pole/shaping implementation remain unvalidated. The current championship ranges permit a common approximately 1 W Classic/Sprint stage, with separate settings needed for measurement margin. Existing cost and Fox fleet audit scopes must be preserved.

## Proposed amendment

Adopt the SignalSlinger/FlexFox80 Si5351, TTL-input LM5134B, single IRF610, bifilar transformer and documented elliptic filter as the normal RF core. Evaluate a 2S-compatible buck and QCX-derived integrator for an economy variant targeting 1.2 W Classic / 0.85 W Sprint. Retain 2–3 W and 5 W capability as optional higher-power population/evaluation alternatives, not silently excluded requirements or validated functions.

Evaluate TinyFox's separate logic buffer using another output of the same local synthesizer; retain the existing BJT fallback if power/shaping/quiet-state tests fail. Dedicated bounded rail, calibrated nominal 10 mW reference output, compact matching/radiator/counterpoise, separate protected port and normal-PA interlock remain mandatory. Tentative BOM deletions require test evidence before cost savings are committed.

This revises **only the HF implementation and preferred normal target** in ADR-0007 and proposed ADR-0008. It preserves accepted ADR-0001/0002, conditionally accepted local synthesis/isolated low paths/2S1P–4P, the ESP32-S3/RTC/optional Silicontra controller, and all 2 m decisions. It proposes updated HF sizing in ADR-0006 without altering pack compatibility or 24 h normal-profile requirements. Original text and costs remain history until review.

## Consequences and gates

Candidate full RF component budget is 22.41/19.76/19.68 EUR ex VAT at 6/10/20, mostly estimated. The higher-power supply option is 35.48/30.86/30.79. Fox audit budgets are retained; proposed RF simplification saves only about 0.17 EUR conditionally. Normal 1.2 W uses modeled 25R 2P rather than unproven 1P; optional 5 W needs higher-capacity qualified cells or measured improvement.

[H0–H9](../M2_80M_VALIDATION_GATES.md) are NOT RUN. Actual power/spectrum, CW shaping, safety/backfeed/isolation, thermal/SOA, compact field reach and pack endurance must pass before release. Review authorizes a topology direction only; this ADR does not authorize layout, procurement, fabrication or full firmware.

See [decision](../M2_80M_DECISION.md) and its linked source, cost and power reports. Request acceptance of the preferred target and evaluation scope before the next physical-development phase.
