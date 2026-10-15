# ADR-0013 — low-voltage VHF evaluation candidate

Status: **Proposed — blocked on source/package trace; not accepted.**
Date:2026-10-15.

Proposed implementation amendment to ADR0007's VHF candidate and still-proposed ADR0008/0011 details: investigate PD54008L-E/PHA-1+ with fixed 5 V driver LDO and 10 V full/7.5 V reduced upstream rails, preserving genuine final-drain AM, isolated training output, controller interface and autonomous fail-off. Existing architecture and all accepted requirements remain.

Rationale: quantity-ten component allowance 52.33/50.40EURnet for 2S/4S versus 74.61/72.77R0. Stocked cut-tape final and economical MMIC provide most of the conditional saving; no obsolete PD84001. Neither gain nor clean 70–80%RF AM is established. Original matching drawings/Power FLAT land remain blocking OPEN.

No final-device substitution is accepted for production. Preserve R0 at tag m5a-r0 as fallback. Close the reference trace/pin map, then review a small externally driven coupon layout; measure gain/compression, crest, RF envelope, stability, spectrum and hot SOA before committing the integrated PCB. Reject the cheap chain if those gates fail rather than weakening carrier ERP/PEP requirements.

See [review decision](../M5A_R1_REVIEW_DECISION.md), [cost delta](../M5A_R1_COST_DELTA.md), [reference audit](../M5A_R1_ST_REFERENCE_AUDIT.md). No procurement, manufacturing or RF authorization follows from this proposal.
