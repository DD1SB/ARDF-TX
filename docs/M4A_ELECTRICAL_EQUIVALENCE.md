# M4A — electrical equivalence to frozen E2

Date: **2026-10-15**. Reference1245023/m3b-e2; candidateM4A-V1/RF80_V1. [Executable comparison](../tools/m4a_verify.py), [machine report](../hardware/80m/production/review/M4A-V1/electrical-equivalence.json), [actual-pin logic results](../hardware/80m/production/review/M4A-V1/logic-results.json). This is **CAD equivalence, not measured physical equivalence**.

The checker verifies every original tracked evaluation-hardware file against the frozen Git commit before comparison. Original schematic/PCB/Gerbers are never regenerated or modified. The new project has a separate name/path/revision, with stable underlying component UUIDs for traceability and copied local libraries/models. It is independently editable.

## Compared design contracts

All non-test component records are exactly equal: MPN, value, footprint identity, population, pin-net maps and sourcing metadata. Actual exported XML compares component identities and every **non-TP physical pin-to-named-net membership**; this includes connector pinout, transformer/elliptic filter, normal/Fox paths, supply selection, captured raw-ARM context, timer/latch pins, driver inhibit and deliberate rearming. Current native PCB pads must match the new XML. Native component values, footprint identities, full-population DNP flags and every footprint-local pad/lead/drill geometry are also compared; only placement/orientation changes. Only **60 test-point instances and their isolated label stubs** are removed; no circuit component or electrical value is removed with them.

The fourteen remaining test pads do not add new circuit functions. Production RF calibration uses the existing50Ω normal/Fox ports. Lower laboratory access is documented reference-by-reference in the test-feature inventory; it is not a protection deletion.

The independent manufacturer catalog checks **55 critical devices**, including actual symbol roles, approved physical footprint identity and PCB/netlist agreement. Q403 is explicitly ST BD140 **1B/2C/3E**, installed180° with physical3west/1east and illustrated face toward+PCB Y; U311 TI DBZ is **1K+2REF reference/3A ground**. No old E2 absolute x/y is falsely reused as a compact-position requirement. All other manufacturer pin assertions remain applicable.

## Regression and deliberate mutations

The existing physical-pin M3A-R1 digital engine runs against **V1's actual XML**:256static combinations,31state scenarios and16timing corners, including watchdog polarity mutation tests, no false progress on reset release, invalid request/profile inhibition, key-low arming, captured configuration, fault clearing and no held-ARM automatic rearm. These tests remain ideal logical/timing analysis; asynchronous device propagation and analog rail collapse need measurements.

The equivalence suite additionally rejects **12 mutations**: Q403 base/emitter, TL431 anode, U202 watchdog output, LM5134B inhibit, HC174 raw-ARM clock, Fox supply, Fox connector tied to the normalRF net, elliptic-filter connection, Si5351 output assignment, a real in-memory PCB Q403pad1 net mutation, a Fox-link population change and a resistor value change. Mutations are temporary data/in-memory objects; the delivered CAD is not intentionally corrupted.

Full and Fox purchased populations remain196/115parts and18/13ICs. Fox links R228/R348/R349 are fitted only in Fox, normal PA/buck/filter/heat components omitted, PA guard fixed invalid and unused comparator inputs grounded. The Fox group has no dependence on VPA/VPA_LOAD/VPA_SHAPED/DRAIN_PA/RF_NORMAL. This verifies the explicit E2 omission/bias contract. It cannot prove transistor body-diode/backfeed behavior or immunity to a solder bridge; staged partial-rail tests and assembly inspection remain mandatory.

## Layout-specific limits

ERC, DRC, schematic/PCB parity and unrouted results are recorded separately in the V1 review package. Every relevant inherited manufacturing check remains enabled, with no hidden exclusion; minimum mask web is strengthened to0.10mm for V1 only. Ordinary track/via and critical hole requirements remain. Frozen E2 is unchanged. ERC retains exactly its three informational defaults (single global label, four-way junction, missing SPICE model), explicitly listed in the coverage report; no functional ERC error or DRC category is suppressed.

No netlist test establishes equal parasitic capacitance/inductance, thermal resistance, grounding, regulator/driver transients, RF spectrum or coupling. V1 must independently repeat driver-absent fault injection, real reset race tests, PA/driver waveforms, CW/spectrum/power/efficiency, hot SOA and normal→Fox isolation. If E2 hardware requires an electrical correction, incorporate it through a reviewed V1 revision and rerun this comparison with an explicitly amended reference. Do not force a “match” by changing the accepted baseline silently.
