# ADR-0004 — Separate bounded low-power paths and compact Foxoring cartridge

Status: **Conditionally accepted at architecture level via ADR-0007; detailed electrical implementation remains Proposed**  
Date: 2026-10-13

## Context

ADR-0002 accepts different long and approximately 30 cm 80 m antenna installations. A common output connector makes a compact loading network vulnerable to watt RF; 2 m training has a similar problem. [Feasibility](../M1_FEASIBILITY.md) compares adapter, switched matching and separate-source approaches, including compact counterpoise and reactive stress. Ten milliwatts conducted does not prove range.

## Proposal

80 m: normal watt port for external long-wire match; independent bounded low-power source/filter/reference port feeding a keyed compact cartridge with short radiator, defined compact counterpoise, loading/coupling, protection and passive identity. Cartridge presence independently inhibits normal PA. No switch routes normal PA output into cartridge. The same primary RF PCB supports a cheaper Fox-only population without watt stage/boost.

2 m: normal PA port and separate low-level AM/attenuator/filter training port, with independent PA-disable interlock. No PA-output selector can connect watt RF to training socket. Use dissimilar keyed connectors; footprints remain open.

## Alternatives and cost

Common socket/passive adapters save connector cost but need independent watt-rated protection and do not isolate misrouting. Switched onboard matching needs rated RF switch/relay and places sensitive compact coils near normal PA/converters. Historical broad allowances were compact **7–15 EUR**, long-wire **8–18 EUR**; the itemized M1 material estimates are **€8.38 compact / €10.25 long-wire**, carried into [M2 circuit proposals](../M2_HF_CIRCUIT_PROPOSALS.md) with quotes and qualification still open. VHF separate training electronics were included in the RF board estimate. All protective/connective components are counted even off-board.

## Consequences / acceptance

Extra sockets and assembly interlock; compact cartridge tune depends on actual enclosure/pack/soil. Require V80F/VFIELD with fixed nominal 10 mW and reproducible 30/250 m observations, plus VSAFE/V2TRAIN wrong-mode/fault/coupling tests. Matching coil/capacitor values, antenna return geometry, reference tolerance and connector packages not approved. Mechanical keying does not guarantee isolation if deliberate external adapters bypass it; document that boundary.
