# ADR-0011 — Dual-voltage packs and profile-specific endurance

Status: **Proposed amendment; user review required.**  
Date: 2026-10-14

## Context and authority

The user explicitly changes the endurance objective to 12 h at the highest selected normal RF setting and 24 h at a defined reduced competition-appropriate setting. This requirement supersession is recorded in SYS-008. The user also requests comparison of 4S1P/4S2P alongside retained 2S1P–2S4P. It does not accept a 4S circuit implementation or authorize layout/procurement.

ADR-0001's three primary PCBs, ADR-0002's separate antenna systems, and the conditionally accepted S3/RTC/optional Silicontra/local RF sources/protected low-power/fail-off functions remain intact. This proposes changes to **ADR-0006's voltage/pack/endurance implementation and ADR-0007's controller/RF supplies**, and revises the still-proposed ADR-0010's higher-power HF supply alternative. No accepted ADR text is silently replaced.

## Proposed decision

Allow a common 6.0–16.8 V controller with properly rated regulator/input FET/TVS/caps, independent pack identity/voltage validation and default-disabled RF. Keep external protected/balanced 2S packs, add 4S1P and 4S2P with physically incompatible charging interfaces. Maximum universal candidate is eight cells,2S4P or 4S2P; neither mandatory for reduced configurations.

Prefer 2S1P Foxoring on the same reduced-population 80 m board. Keep 2S economy HF; prefer 4S with one bounded buck for higher-power SignalSlinger/FlexFox80 RF core. Select 3 W full /1.2 W extended Classic initially,0.85/0.5 W Sprint, with 5 W alternative explicitly retained and separately qualified. Power mode selects bounded supply/drive; no new RF MCU/DAC/RTC, no raw 4S gate-driver feed.

Retain true 2 m AM and preferred MMIC/PD55008. Evaluate 4S buck 13.5 V with declared higher full-power cutoff and lower-rail extended 0.30 ERP profile; retain 2S boost until measured gain/PEP/headroom and accessible energy justify a 4S-only population. Reject direct unbounded PA feed and unqualified raw 4S series-modulator thermal simplification. No universal buck-boost without a quantified advantage.

Fixed event power profiles meet applicable conducted-power/ERP, timing/modulation/antenna limits. UV/fault stops RF, with no automatic in-contest power reduction. Model continuous roles separately. Universal normally activates one band; simultaneous full 12 h is not promised by this proposal.

## Consequences

Equal-cell 4S higher-power HF modeled supply consumption improves 12.6–13.4%, saving about 5.78 EUR complete material at ten;4S VHF alone adds about 2.84 EUR at equal eight-cell scope and retains an AM discharge-window risk. New controller 14.93 EUR components at ten; HF 4S3W/5 W thermal populations 20.32/21.82 EUR; Fox material 57.83 EUR versus preserved 55.24 EUR audit. All estimates/observations, not measured or quoted production costs.

P1–P6 in [the review decision](../M2_POWER_ARCHITECTURE_DECISION.md) and retained RF gates must close. Hot SOA, driver compression, buck dropout/noise, pack identity, compact isolation, charger/BMS and real 12/24 h RF endurance remain OPEN. Current conclusions support an architecture review only, not hardware release or procurement.

Supporting documents: [battery architecture](../M2_BATTERY_ARCHITECTURE.md), [power modes/rules trace](../M2_POWER_MODE_COMPARISON.md), [itemized cost comparison](../M2_BATTERY_COST_COMPARISON.md), [reproducible endurance](../M2_ENDURANCE_REWORK.md), [sources](../M2_POWER_ARCHITECTURE_SOURCES.md).
