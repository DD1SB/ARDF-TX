# Mini80 M80-E2 — final bare-PCB manufacturing gate

**GO for ordering five bare evaluation PCBs using the unchanged M80-E1 package.** No PCB manufacturing blocker was found. Assemble one FOX10 first article initially; the other four boards remain evaluation spares. RF qualification, antenna calibration and a populated fleet release remain on HOLD. No order, push, merge or tag was performed.

This gate was run on 22 October 2026 against commit `bdac015766cab5aa62fc106aefb151f634e7f109`, branch `mini80-smd-evaluation`. **M80-E2 names this review, not a copper revision:** the native CAD, M80-E1 marking, firmware, released ZIPs and all existing hardware families are unchanged. The findings and procurement plan here are new local review files.

Use the [exact order sheet](JLCPCB-ORDER.md), [one-unit FOX10 procurement CSV](FOX10-one-unit-procurement.csv), and [first-article/fixture instructions](FOX10-FIRST-ARTICLE.md). Machine-readable measurements, fresh reports and source hashes are in [evidence](evidence/provenance.json).

**Verification results**

KiCad CLI and PCB Python bindings were **10.0.6**. A disposable checkout made with `git archive` supplied the committed sources and local libraries. Export/check tools ran only there; audit settings changed only disposable project copies.

| Check | Result and evidence |
|---|---|
| Fresh schematic ERC | **0 violations**: [erc.json](evidence/erc.json) |
| Fresh PCB DRC with schematic parity | **0 violations, 0 unconnected items, 0 parity issues**: [drc.json](evidence/drc.json) |
| Source/pinout regression | **PASS**, 229 connected-pin comparisons, 85 manufacturer-pin comparisons: [verification.json](evidence/verification.json) |
| Both ignored DRC checks enabled | One via-centering warning only; no tuning warning: [all-style-checks-enabled.json](evidence/all-style-checks-enabled.json) |
| Additional fabrication rules | Mask opening to foreign-net copper **0.09 mm**, connection width **0.075 mm**: **0 violations** in a disposable copy: [fabrication-extra-checks.json](evidence/fabrication-extra-checks.json) |
| Gerber/drill regeneration | All **7 fabrication Gerbers, 2 drill files, 3 stencil Gerbers and 2 job descriptions** match the committed outputs after ignoring creation timestamps only. Both released ZIPs contain the committed files byte for byte: [geometry/output evidence](evidence/geometry-and-output-consistency.json) |
| FOX10 stencil population | Exactly **74 fitted component references**, no missing or unexpected references; **L30–L34 and C30 absent**. B.Paste empty. J2/test pads have no paste. |
| Fresh firmware host regression | **PASS** for the actual shared scheduler/power modules: [firmware-host-test.log](evidence/firmware-host-test.log). AVR peripheral execution and RF measurements remain unperformed. |

The KiCad Python exporter prints upstream PROPERTY_ENUM assertions and temporary-footprint SWIG leak messages. The CLI processes complete, checks pass and regenerated geometry matches; those diagnostics are retained in the logs rather than mistaken for PCB defects.

**Every disabled DRC check reviewed**

There are exactly two `ignore` entries in the committed DRC severity map and no per-item DRC exclusions.

| Disabled check | Individual re-run and assessment |
|---|---|
| `track_not_centered_on_via` | Enabling it finds one FIX_RX warning. B.Cu track UUID `fc75c5a7-6d38-4c52-b846-d261ef2ed7e2`, width **0.15 mm**, ends at **(56.550000, 66.850000) mm**. Via UUID `abf59c7c-9cf9-4a9d-9715-990eae3dc79d` is at **(56.550000, 66.849999) mm**, diameter/drill **0.45/0.20 mm**. The offset is **0.000001 mm (1 nm)**; the track enters the via essentially through its center. This is coordinate rounding, with no open, thin neck or fabrication problem. No correction is necessary. [Individual report](evidence/track-centering-enabled.json). |
| `tuning_profile_track_geometries` | Enabling it produces **0 violations**. No length-tuned timing/differential-pair geometry is used; 3.5 MHz RF operation does not require such a profile. It hides no manufacturing defect. [Individual report](evidence/tuning-enabled.json). |

**Standard fabrication assessment**

The table distinguishes measured dimensions from lower bounds checked by DRC. Limits were compared with [JLCPCB's current fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities). This is a local engineering assessment; a manufacturer CAM acceptance or quotation has not been obtained.

| Feature | Committed design / check | Assessment |
|---|---|---|
| Closed outline | Centerline rectangle **35.000 × 35.000 mm**, absolute (50,50) to (85,85) | Regular CNC routing; 35.05 mm stroke bounding box is not the finished size. |
| Construction | 2 layers, 1.6 mm FR4, 0.035 mm nominal copper each side, ENIG, green mask | Standard process. Native dielectric thickness is descriptive, not a required custom stackup. |
| Tracks / foreign-net spacing | Measured minimum track **0.10 mm**; DRC enforces clearance **≥0.10 mm** | Within standard 1 oz limits; do not substitute 2 oz. |
| Different-net pad spacing | DRC enforces **≥0.15 mm** | Includes U3's corners and adjacent leads. |
| Vias | 50 × **0.45/0.20**, 35 × **0.60/0.20**, 22 × **0.60/0.30 mm** diameter/drill | All mechanical through vias. Smallest drill 0.20 mm and diameter 0.45 mm avoid the published smaller-via surcharge category. |
| Via annulus | Measured minimum **0.125 mm radial** | Via-specific requirement applies; do not misapply the larger component PTH ring requirement to vias. |
| J3 component PTH pads | Two **2.20 mm pads / 1.00 mm holes**, **0.60 mm radial ring** | Ample component PTH annulus. J3 pitch 3.0 mm. |
| Holes | **109 plated** (107 vias + 2 J3); **2 non-plated** mounting holes | Separate metric drill files. No slots, countersinks or controlled-depth work. |
| Hole/copper and hole/hole clearance | Native checks enforce **≥0.20 mm** | J3's 0.60 mm ring plus foreign-net copper clearance also exceeds the stricter component-hole/track requirement. J3 hole-to-hole edge gap is 2.0 mm. |
| Copper to routed edge | DRC enforces **≥0.30 mm** | Above standard routed-edge requirement. |
| Fine-pitch U3 | 0.40 mm pitch; all twenty peripheral lands have **0.25 mm** narrow dimension; nominal adjacent gap **0.15 mm** | Standard etched QFN lands, no microvia/HDI escape. U4 pitch 0.50 mm; U2/U5 pitch 0.65 mm. |
| Mask | 1:1 pad openings; configured minimum web **0.10 mm**; additional **0.09 mm** foreign-copper clearance passes | Use green mask and retain supplied artwork. |
| Important legends | All five visible text objects **1.0 mm** text / **0.15 mm** stroke | Pogo legend and battery polarity remain identified. Some stock component outlines use 0.12 mm lines and can print weakly or be clipped; cosmetic only. |

**Exposed-pad vias and stencil: assembly risks, not bare-board blockers**

U2 and U3 each have one **0.45 mm copper / 0.20 mm drill GND through via** centered in their exposed pad: U2 **(77,55) mm**, U3 **(58,68) mm**. Although native via settings request front/back tenting, the actual Gerbers contain a **front opening and no bottom opening** at each center. The front hole is exposed by the EP aperture. Bottom tenting is not a guaranteed solder plug; molten solder can wick into either via. **No filled/capped via process is required for this limited first article.** Inspect and rework the first assembly before repeating it.

External microscopy can find bridges and exposed-joint defects; it cannot quantify hidden EP voiding. Use X-ray if available. Otherwise, rail/current/thermal and programming checks provide limited functional evidence, and hidden-joint repeatability remains an assembly risk before any fleet release.

| Part | EP and paste geometry | Specific risk |
|---|---|---|
| U2 TPS61099 | EP **1.00 × 1.60 mm**. Two rounded **0.81 × 0.64 mm** windows; actual area coverage **62.05%** | The central paste gap is **0.16 mm**, narrower than the **0.20 mm** drill. Paste overlaps the drill by **0.020 mm** at each cap, total area about **0.00327 mm²**. This small geometric overlap does not establish how much molten solder will wick. Check EP wetting/voiding and the boost rail before RF tests. |
| U3 ATtiny1616 | EP **1.70 × 1.70 mm**. Four rounded **0.69 × 0.69 mm** windows; coverage **62.36%** | Nearest rounded paste edge clears the drill by about **0.0846 mm**. There is no direct printed-paste overlap, but reflow can still draw solder into the exposed via. Check EP/ground continuity and programming. |

A **0.10 mm** stencil is appropriate for the 0.4 mm QFN and 0402 population. The smallest calculated rectangular/rounded aperture area ratio is **0.987** at U3's peripheral lands; EP windows have larger ratios. This is a geometric release estimate, not a printed-paste measurement. All 213 evaluated apertures have unchanged 1:1 native paste sizes. Follow the exact supplied F.Paste rather than synthesizing openings from solder mask. Measurements are in [mask/stencil evidence](evidence/mask-and-stencil.json) and [geometry evidence](evidence/geometry-and-output-consistency.json).

**J2 and mounting**

**J2, `Mini80:Pogo6`, B.Cu, flipped, native rotation 180°**, has six **1.10 × 1.10 mm rectangular copper and mask openings**, **2.00 mm pitch in both axes**, no paste or fitted connector. Actual B.Mask polygons confirm all six openings. The pad edge gap is 0.90 mm; the contact array spans 5.10 × 3.10 mm. There are no bottom-side component bodies obstructing the probe approach. The bottom legend reads `1 G  2 V  3 U` / `4 RX 5 TX 6 SY`. See the [full connection/fixture table](FOX10-FIRST-ARTICLE.md).

H1/H2 are **2.20 mm NPTH**, at native **(52.5,52.5)** / **(82.5,82.5) mm**, or **(2.5,2.5)** / **(32.5,32.5) mm** from the outline's upper-left in the top CAD view. Edge-to-hole margin is **1.40 mm**; hole-center spacing is **42.426 mm** diagonally. Use insulating M2 fasteners/spacers and avoid broad conductive washers over nearby copper. Allow standard board/hole tolerances in the fixture.

The two diagonal holes **do not key orientation**: their pattern is 180° symmetric. Add an asymmetric fixture stop/orientation mark and verify the pogo wiring unpowered. A 0.64 mm probe tip leaves nominal **±0.23 mm** center tolerance on a 1.10 mm pad before fabrication/fixture errors; adjustable registration and a supported clamp are appropriate. Actual contact repeatability remains a first-article check.

**Decision boundaries**

| Category | Disposition |
|---|---|
| Manufacturing blockers | **None found. GO for five bare boards**, with the exact standard-process order specification. No copper correction is proposed. |
| Assembly risks | Exposed EP via solder wicking, 0.4 mm QFN reflow/inspection, small 0402 handling, fixture orientation/alignment, and supplier basket confirmation. Assemble **one FOX10** using eight 560 Ω ballasts and inspect it before further assembly. |
| RF and hardware tests | Conducted power, HCT parallel-output skew/current, rail transitions, harmonics/key clicks, coil losses, frequency/RTC accuracy, supply currents/runtime and realistic antenna loads remain physical tests. FOX10 30 m/250 m field results are unproven. Follow [FIRST_ARTICLE.md](../../FIRST_ARTICLE.md); none of these measurements can be required before bare-board manufacture. |
| Non-blocking documentation | Older pricing/MOQs need the fresh observations in this gate; stock-footprint outline linewidths may be clipped; fixture drawings should retain explicit bottom-view orientation. M80-E1 copper/markings and released archives intentionally remain unchanged. |

MINI50 remains informal training hardware, below official Sprint power. FOX10 remains a calibration candidate; neither a measured 10 mW into a dummy load nor this manufacturing GO establishes Foxoring field compliance. Existing RF80/RF2M/controller manufacturing packages and history are unaffected.
