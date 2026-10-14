# Codex kickoff task — ARDF-TX M1 (English)

You are starting **M1 — Feasibility & Architecture** for a low-cost, modular ARDF transmitter family. Work in this repository and use `README.md`, `docs/requirements.md`, `docs/architecture.md`, `docs/research-register.md`, `docs/m1-acceptance.md`, and `docs/decisions/ADR-0001-modular-hardware.md` as the current project baseline.

## Product goal

Develop a reproducible, inexpensive, competition-suitable transmitter platform for **80 m Classic/Sprint/Foxoring** and **2 m Classic (true A2A AM) + ultra-low-power training**. The system consists of three interchangeable PCBs:

1. **Controller:** ESP32-class MCU, accurate autonomous contest timing, power management, monitoring, optional Silicontra SX1262 LoRa module (automatically detected; no LoRa is a fully supported condition).
2. **80 m RF module:** CW/A1A synthesis, filtering, 1–5 W Classic, 0.3–1 W Sprint, 10 mW continuous Foxoring, different programmed frequencies and **two physically distinct 80 m antenna configurations**: longer vertical wire with ground/counterpoise for Classic/Sprint (e.g. 8 m + 6 m as an example, not a rule) versus an approximately 30 cm short vertical radiator and compact counterpoise for Foxoring. Analyze the separate matching/loading/coupling requirements and mode-specific cost.
3. **2 m RF module:** actual amplitude modulation/A2A, suitable carrier and PA for 0.25–1 W ERP Classic with 70–80% modulation, protected and separate very-low-power training output. Allow flexible frequency selection across the locally permitted 2 m amateur band; the official IARU competition profile must independently enforce its narrower frequency range.

A protected external **2S Li-ion** battery pack is interchangeable between 2S1P, 2S2P, 2S3P, and 2S4P. **2S4P is the maximum configuration, not a mandatory one**. Our endurance target is 24 hours for normal contest profiles at maximum specified TX setting, including continuously transmitting Foxoring (10 mW). Analyze continuous full-power finish/spectator beacon endurance as a separate case. Cost is a prime objective: target 6–10 repeatable units. Use realistic MOQ and distributor quantity pricing; no assumptions about 3,000-piece reel MOQ or unavailable legacy parts.

## Mandatory work

A. Confirm every RF level, emission mode, frequency, timing and antenna constraint **directly against** IARU Region 1 *Rules for Championships in ARDF, Part B (2025)*. Distinguish RF connector output power, ERP, PEP and field-range criteria. Two Sprint groups work concurrently on different configurable frequencies with 12-second slots; spectator and finish beacons may require their own frequencies and continuous TX. Check what requirements are actually applicable and separately identify applicable country/regional legal obligations. Never present IARU rules as legal transmitter authorization.

B. Research and compare existing, demonstrably tested RF designs before creating anything new. At minimum assess the documented Netherlands/G3ZOI/PA0JBG examples, SmartFOX (software under MIT; 2 m FM not A2A, 80 m direct Si5351 CW), HG0HK 80-m transmitter, practical Si5351/PLL VHF implementations, and the low-cost modified UV-5R alternative. Search other current designs if they offer meaningful cost, performance or repeatability improvements. Build an evidence matrix distinguishing publisher claims, test measurements, extrapolations and missing data.

C. Compare **synthesizer-on-each-RF-board** with **shared controller-board synthesis**. Account for 144 MHz interconnect, harmonic/close-in spur treatment, shielding, RF/ground distribution, test isolation, build variants and total BOM. Do not decide from schematic simplicity alone.

D. Investigate power-level switching/calibration: 80 m Classic/Sprint versus 10 mW Foxoring; 2 m normal A2A versus physically isolated very-low-power training. **Do not treat 80 m Foxoring as simply running the long-wire Classic antenna at lower PA power.** Compare antenna connections and dedicated matching, loading or coupling for an approximately 30 cm Foxoring radiator vs. the conventional longer 80 m wire/counterpoise. Quantify the distinct conducted-power and field-range acceptance tests, installation and environment sensitivity, and the risk of full-power RF being sent into the Foxoring matching network. Include the required matching network, connectors and protective components in the costed mode-specific BOM, even if physically placed off-board. Include PA modulation depth and PEP headroom; do not treat a fixed FM sidetone transmitter as A2A. Define a reliable fail-off hardware concept and power stage muting during retuning.

E. Produce a concrete 2S1P/2S2P/2S3P/2S4P energy and peak-current budget for the operating profiles (Classic duty 20%; Sprint 20%; Foxoring continuous; beacon continuous), with all MCU, timebase, LoRa standby/listening, synthesizer, regulator and RF-board standby consumption. Include realistic usable-energy margins and verify which packs meet 24 h. Do not invent measured currents.

F. Propose control/connector contracts for both RF modules. Optimize for a small number of pins but prioritize robust isolation, safety, fault reporting, TX inhibit and independent testing. Document exact needed electrical interface functions without prematurely locking connector footprints.

G. Evaluate availability, footprints, actual small-quantity pricing and MOQ for candidate components from multiple reputable distributors. Include an explicit cost baseline for modified handheld radios. Publish a full **candidate** BOM, not a released ordering list.

H. Plan measurable qualification: output RF power and PEP, A2A envelope/70–80% modulation, unwanted emissions, CW rise/fall and keying clicks, **separate 80 m Classic/Sprint and compact Foxoring antenna matching/coupling tests, reference-load measurement of the nominal 10 mW, reproducible 30 m audible / 250 m not-audible field evaluation**, antenna/ERP and Foxoring reach, drift/timing, safe startup/faults, thermal behavior, battery life, LoRa optional operation and simultaneous RF/LoRa immunity. Document required instruments and acceptance methods.

## Deliverables

Create all documents listed in `docs/m1-acceptance.md` and improve the initial baseline where a primary source contradicts it. Maintain a dated source log and requirement traceability. Issue structured ADR proposals for any decisions not already accepted. Mark all unverified assumptions prominently.

**Do not** design/route PCBs, generate Gerbers, lock a production BOM, purchase parts, implement firmware beyond optional throwaway analysis scripts, or declare hardware validated. Do not invent links, datasheet claims, tests or prices. Leave source material attributed and comply with licenses.

## Output and quality bar

1. Work in English in the repository.
2. State what was verified from primary documentation and what remains unknown.
3. Prioritize cost-efficient, available, repeatable hardware, not feature count.
4. Explain the trade-off between 80 m/2 m integration and the size of the Foxoring-only configuration, **including the short 80 m antenna, compact counterpoise and matching network rather than assuming a Classic wire antenna**.
5. End with a succinct **M1 review summary**: recommended topology, candidate cost per hardware configuration, energy budget by pack/profile, unresolved risks, and explicit user decisions required before M2.
6. Run any available documentation consistency/link checks. If an external source cannot be accessed, report it rather than guessing.

Start by reading the baseline files and building a requirements-to-source matrix. Work systematically to completion of M1 documents; do not stop after producing an outline.
