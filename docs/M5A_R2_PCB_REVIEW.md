# M5A-R2 PCB review — explicit pre-layout stop

2026-10-15. **NO PCB CREATED.** The required fleet-sourcing gate was not satisfied. This file reports the exact artifact status; it is not a layout review of a nonexistent board.

## Preserved baseline

R1 is preserved by commit`4785057`/tag`m5a-r1`. Its [native RF2M project](../hardware/2m/RF2M.kicad_pro), [schematic](../hardware/2m/RF2M.kicad_sch), [electrical manifest](../hardware/2m/RF2M.electrical.json) and [R1 PDF](../hardware/2m/review/M5A-R1/RF2M.pdf) remain unchanged. No R1 drawing or PDF is relabeled as Mitsubishi R2.

The new [R2 review directory](../hardware/2m/review/M5A-R2/README.md) contains sourced facts, calculations, an itemized accounting bridge and integrity/regression reports. It contains **no R2 Gerbers, drills, assembly drawings, renders or schematic PDF**. There is no separate coupon project or replacement primary PCB.

## What was independently resolved

- Official dynamic manufacturer table retrieved; all three allowed module families In production.
- RA07 manufacturer outline and terminal order inspected visually, including flange-ground pin5 and tolerances. No guessed SIP footprint created.
- GLYN stock download examined rather than relying only on catalog text:40 RA08N-502 listed; RA07/RA08H not listed there.
- RF Parts live individual/ten-unit price retrieved; no unsupported stock count or authorized-channel claim.
- Required connector/module PEP and filter-loss sensitivity calculated; FM rating never substituted for AM crest qualification.
- A specific analog RF attenuator route identified, with its current delivery problem retained.

## What stops commitment

Neither the primary RA07 nor an allowed alternative has a confirmed complete6/10/20-unit price/MOQ/lead-time offer. GLYN's RA08N inventory is promising, but is not a purchasing offer; the primary retail source does not publish quantity. The proposed analog attenuator also has zero current EU stock. These are concrete commercial inputs, not a request for another RF architecture study. See [sourcing/cost](M5A_R2_SOURCING_COST.md).

The source-only technical review also does not establish clean crest power, sufficient direct-clock drive, a valid complete2S converter, or final board-to-heatsink/lead geometry. Those are openly identified engineering tasks; none has been hidden behind a generic footprint or successful ERC.

## Tool status and exact scope

Commands run against the **preserved R1**:

```sh
kicad-cli version
kicad-cli sch erc --format json --output /tmp/m5ar2-r1-erc.json hardware/2m/RF2M.kicad_sch
kicad-cli sch export netlist --format kicadxml --output /tmp/m5ar2-r1.net.xml hardware/2m/RF2M.kicad_sch
python3 tools/m5a_r2_review.py
```

KiCad10.0.6: R1 ERC0 errors/3 existing OPEN-footprint warnings (J301/J701/C409). Fresh exported R1 connectivity is compared with the frozen R1 netlist.4096 R1 Boolean combinations,36 state scenarios and critical-pin audit regressions pass; selected mutations are rejected. The [verification report](../hardware/2m/review/M5A-R2/verification.json) distinguishes this from R2 status.440 baseline files and the original335-file HF/ADR snapshot remain unchanged.

| R2 artifact/check | Status |
| --- | --- |
| Editable Mitsubishi schematic /netlist /BOM | **NOT_CREATED — sourcing gate** |
| PCB placement/routing /unrouted/parity /DRC | **NOT_RUN — no PCB** |
| Manufacturer pad-to-net assertion | **NOT_RUN — drawing transcribed, no R2 CAD** |
| Gerbers/drills/3D/assembly exports | **NOT_CREATED** |
| Physical RF/AM/safety/thermal/endurance | **NOT_RUN** |

No production architecture was accepted, no accepted ADR was changed, and no procurement/manufacturing activity occurred.

## Resume boundary

After the exact sourcing inputs are available, develop **one integrated two-layer RF2M board**: edge-mounted grounded-flange module with specified heatsink attachment, short50 Ω paths and solid returns, power conversion separated from the source/analog control, output LPF near normal port, training branch/port physically separate. Dimension the flange/PCB/heatsink assembly from the actual drawing before creating pads. Maintain hand assembly, mounting-first sequence, bias/current access and a small set of useful test pads.

The output LPF remains indispensable. The retained R1 50 Ω nine-pole network can be evaluated at identical scope; its calculated loss and actual harmonic rejection need confirmation. No LPF value was changed in this milestone. Compact digital and RF routing cannot be qualified from the netlist. This boundary does not authorize a new coupon program or any order.
