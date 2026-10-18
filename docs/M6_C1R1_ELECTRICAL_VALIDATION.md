# M6-C1R1 electrical and manufacturing validation

KiCad **10.0.6** was run on the final native board. All values below are actual CAD/host checks, not physical tests.

| Check | Result |
|---|---|
| ERC errors/warnings |0 /0|
| DRC errors/warnings |0 /0|
| Unrouted/parity |0 /0|
| Exclusions |none|
| Ignored category |default tuning_profile_track_geometries only; no tuning patterns|
| Baseline pad coverage |693 retained, with3 intentional net changes|
| Current native pad assertions |704|
| Manufacturer maps |38 baseline plus2 new diode maps|
| RF connector pins |36 unchanged|
| Enable combinations |4096|
| Baseline electrical mutations |20 rejected|
| New native/numerical protection checks |16 pass, including unsafe mutations rejected|
| Native DFM mutations |7 rejected|
| Host Python tests |40; all32 baseline tests retained with legitimate ID-decoder update|
| C fixture |strict C11 -Wall -Wextra -Werror compile and execution PASS|
| RF80 read-only replay |256 truth cases,31 states,16 RC corners,2 polarity mutations|
| RF2M read-only replay |4096 combinations,39 states,16 preparation rows|
| Native JLCPCB geometry |PASS; 52566 foreign-copper pair checks; no slivers|
| Fabrication artifact audit |9 Gerbers,436 PTH/6 NPTH,704 pad/390 via IPC records|
| Historical preservation |111 M6-C1 review files and1220 RF files unchanged|

Independent positive-fault calculations give less than2.74V at U21.5 unpowered and2.11V powered for16.8V at J1.3 with resistor/leakage corners. Resistor-only bounds are2.6472/2.0713V. ThePACK_ID channel uses calibrated ATTEN1/2.5dB and rejects>=0.93V/saturation. Independent1.7% initial/temperature resistor corners are included. Static VDD=0 ADC leakage bound is±0.204V. R8 dissipation is at most1.23mW in the positive-fault cases. Finite U21 RON≤4.5ohm contributes below0.1mV DC error at these currents; it is below the qualified ADC-error budget, not asserted to be an ideal physical switch.

The complete fault rows, currents, recognition envelopes and explicit parameter assumptions are in [input-protection.json](../hardware/controller/review/M6-C1R1/input-protection.json). The3.3V USB steering reference and all USB copper remain unchanged; [USB review](M6_C1R1_USB_ESD_REVIEW.md) distinguishes normal power states, forced unpowered data injection and IEC transients.

Required negative-test coverage is tied to actual nets/model inputs: raw16.8V and absent U21 supply (numerical divider/off leakage), missing R8/R9/R19 and incorrect bias or clamp connections (native mutations), open/short/wrong identity and excessive/absent calibration (host interval reader), incorrect USB rail/pins (native mutations), unchanged RF connector identity (baseline/native mutation), USB-only/MCU reset/brownout/no progress/conflicting bands (native4096 truth and host states). No label-only result substitutes for a circuit or model check.

Physical ADC calibration, leakage over temperature, negative clamp behavior, transient isolation, rail decay/backfeed, USB ESD/enumeration/eye, RTC and RF integration are **NOT_RUN**. The explicit calibration record must be qualified over the intended operating envelope. Unqualified, stale, ambiguous or wrong frontend-version data cannot authorize a pack identity. The normal scheduling/application firmware is not delivered here.

Reproduction commands and frozen-source requirements: [REPRODUCE.md](../hardware/controller/review/M6-C1R1/REPRODUCE.md). Historical helpers are reused through the R1 wrapper so their old review directory is never overwritten.
