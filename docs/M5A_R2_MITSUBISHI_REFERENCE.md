# M5A-R2 Mitsubishi reference and sourcing gate

2026-10-15. **PRE-CAD REVIEW — BLOCKED. No R2 schematic, PCB or manufacturing release is claimed.** R1 is preserved at commit `4785057`, tag `m5a-r1`. The existing editable RF2M project still describes R1. RF80, M4A, the controller and accepted ADRs are unchanged.

The user's section 10 requires actual small-quantity sourcing before PCB commitment. That gate remains OPEN. This report records the independent work that can be completed without bypassing it. It does not substitute a paper architecture for the requested integrated board.

## Primary evidence

The [official lineup](https://www.mitsubishielectric.com/semiconductors/hf/products/lineup/index.html) loads a [manufacturer CSV](https://www.mitsubishielectric.com/semiconductors/data/silicon_rf_module.csv). On the access date it lists RA07M1317M, RA08N1317M and RA08H1317M as **In production**. This is stronger evidence than an old datasheet alone. Exact order suffixes come from their respective datasheets.

The [RA07 datasheet, Jun. 2019](https://www.mitsubishielectric.com/semiconductors/hf/products/datasheet/ra07m1317m.pdf), pp.1–3, permits input-power-controlled linear modulation after setting quiescent current with gate bias. Its specified 6.5 W result uses 7.2 V, 20 mW input and 3.5 V gate bias. Neither a linear-AM compression limit nor an AM distortion guarantee is supplied. The typical input/output curves were visually inspected; they must not be read as a production gain guarantee at a different idle bias.

The conditional absolute ratings matter: 12 V drain applies with gate zero/input zero; gate maximum is 4 V under the stated drain/input conditions; input maximum is 30 mW under its stated conditions. The 9.2 V stability/mismatch tests do not authorize raw 4S or establish clean AM. Published harmonic limits require an external output filter.

## Physical record

Page 6 was downloaded and visually inspected. H46S is not a five-lead SIP: terminals 1/2/3/4 are RF input/VGG/VDD/RF output, and 5 is the grounded flange. The drawing shows 30 × 10 mm body, parenthesized 5.4 mm overall height, 26.6 mm mounting-slot spacing, and lead centers 6.1/13.7/18.8/23.9 mm from the left reference. The large lead-position tolerances require a deliberate lead/PCB/heatsink construction.

The [machine-readable drawing transcription](../hardware/2m/review/M5A-R2/manufacturer-pin-record.json) includes tolerances and viewing convention. **It is not a symbol-to-PCB pinout PASS:** no R2 footprint or installed assembly exists. Do not copy a superficially similar module footprint.

Mount to a flat heatsink before soldering; use the manufacturer's thermal compound, flatness, screw and soldering instructions. Two M2.6 screws use approximately 0.177–0.294 N·m. The flange is an RF return and thermal path. It is not an isolated live transistor tab.

## Narrow alternatives and decision

| Exact alternative | Relevant difference | Sourcing evidence | Disposition |
| --- | --- | --- | --- |
| RA08N1317M-502 | 9.6 V, 8 W nonlinear reference; its own conditional ratings | GLYN stock file lists 40; RF Parts retail price/tier exists | Best bounded alternative for a supplier confirmation; no silent substitution |
| RA08H1317M-502 | 12.5 V, 8 W reference; different supply/thermal constraints | GLYN catalog and RF Parts listing; no counted GLYN stock row | Does not close fleet sourcing or 4S-endpoint headroom |

The [RA08N](https://www.mitsubishielectric.com/semiconductors/hf/products/datasheet/ra08n1317m.pdf) and [RA08H](https://www.mitsubishielectric.com/semiconductors/hf/products/datasheet/ra08h1317m.pdf) are separate devices, not drop-in approved populations. An 8 W FM rating still does not guarantee linear AM.

**RA07 remains the primary technical candidate, not an accepted production selection.** No allowed candidate has a confirmed complete 6/10/20-unit price/MOQ/delivery offer. See the [specific sourcing gaps and cost bridge](M5A_R2_SOURCING_COST.md). No broader transistor search is recommended.

All retrieved source URLs, dates, file hashes and supplier observations are in the [source log](../hardware/2m/review/M5A-R2/sources.json) and [extracted observations](../hardware/2m/review/M5A-R2/supplier-observations.json). Third-party PDFs, artwork and the full stock list are not redistributed.
