# M5B-E6 assembly concept — HOLD

No native E6 placement/cutout, released drill drawing or assembly instruction exists. [Concept plan and sections](../hardware/2m/review/M5B-E6/common-cooler-concept.pdf) explain the preferred architecture only. The original E5 native three-cooler geometry and review remain immutable. Do not build the unqualified concept from this document.

Q501's native origin remains (92,55), Q401 (115,26), Q402 (133,39), all angle 0. The proposed Q401/Q402 bodies lie below the PCB toward negative Y, with their live tabs against insulated parts of one Z≈−8 mm plane. Their lead-row origins would stay fixed. This would avoid moving the 144 MHz PA/matching network. It has not been implemented or checked by E6 DRC.

[ST's THD mounting note TN1225](https://www.st.com/resource/en/technical_note/dm00238320-mounting-instructions-for-thd-through-hole-device-packages-stmicroelectronics.pdf), Rev 3 September 2026, requires forming clear of the package/wide-lead section, appropriate bend radius and body support. The concept uses a single out-of-plane 90° bend, ≥4 mm straight for TO-220, ≥3 mm for SOT-32, radius ≥1 mm, with a supported forming jig. These dimensions are tentative. ST TO-220 lead length is 13–14 mm; SOT-32 15.3–16 mm. A lead-length budget alone does not qualify seal stress or a repeatable forming operation. Never use leads or Q501 solder to support the cooler.

The tentative Q401 horizontal body projection is approximately X112.34..122.74/Y5.25..21, ahead of the board edge. Q402 is approximately X131.38..139.18/Y23.95..35. A **9 mm tool-access opening near (135.28,27.75)** is reserved conceptually. Its exact hole datum, washer/tool clearance and native copper clearance are OPEN. No cutout is added to Edge.Cuts. The final screw drawing must be based on the actual manufacturer package drawing and selected incoming parts, not generic library bodies.

## Isolation and support requirements

| Device | Native conductive thermal potential | Concept interface | Unclosed details |
| --- | --- | --- | --- |
| Q501 | Source/GND | Grounded bar, electrically insulating sheet wherever non-GND PCB routes are underneath | Contact pressure, guaranteed resistance, source-ground bond, support preload |
| Q401 | Collector VPA | GS220P mica approximately 12 × 18 × 0.05 mm, grease both sides; IB6-type insulating shoulder bush; M3 screw | Incoming hole/bush dimensions, fastener length/thread engagement and compression |
| Q402 | Collector MOD_SINK | GS32P mica approximately 8 × 11 × 0.05 mm, grease; suitable nonconductive M2.5 fastener/washer | Creep/clamp retention, hole fit and torque; TO-220 bush must not be forced into the smaller hole |

The [Fischer mica catalogue](https://www.farnell.com/datasheets/3190623.pdf) gives 5 kVAC for the mica family; the tab-sized 0.4 K/W number must not be inferred from a different GS3 test geometry. The thermal calculation uses explicit application allowances, not a universal guaranteed mica resistance. Pad/bush voltage ratings do not establish assembly insulation after burrs or incorrect screws. Solder mask, anodizing and grease provide no accepted safety insulation.

The cooler needs independent bracket/carrier support, matched-height PCB standoffs, mechanical stops and a spreader/clamp arrangement that does not bend FR4 when tightened. Existing H5/H6 source-region holes are (92,32)/(92,68); four board holes remain (25,25)/(165,25)/(165,125)/(25,125), 140 × 100 mm. Screw-tool cylinders, washer OD, tap depth, bottoming clearance and worst-case board thickness must be modeled before approving machining. M3×12 from the E5 pass stack is not automatically suitable for the thinner E6 base. No final screw length or torque is authorized here.

## Required assembly sequence after closure

1. Assemble PCB; inspect source print/reflow and first-article hidden joint/X-ray before thermal attachment.
2. Saw/deburr/drill/tap the single extrusion and bar from approved drawings. Verify flatness, electrical isolation edges and thread depth.
3. Install qualified source interface and separate live-tab mica/bush hardware, with no burrs or metal bridges.
4. Form supported transistor leads with a jig; attach bodies without loading leads or solder joints.
5. Fit independent cooler brackets and matched-height board supports; tighten in the qualified sequence/torque and inspect for board bow.
6. With relevant devices safely isolated for measurement, verify VPA-to-cooler and MOD_SINK-to-cooler insulation before/after tightening. Establish an approved test voltage that does not damage semiconductor paths; do not apply a high-voltage megger across populated electronics.
7. Verify the controlled source/GND-to-bar/cooler bond and fault-current return. Target <0.1 Ω using a four-wire/lead-compensated procedure, subject to the final bond design; an ordinary continuity beep is insufficient.
8. Bond/strain-relieve temperature sensors at their approved locations and verify open/short detection and intact-but-detached sensor limitations.
9. Install unchanged controller on independent insulating supports, keyed IDC, battery harnesses, RF pigtails and strain relief. Check USB, ESP 2.4 GHz and LoRa cable/tool access.
10. Fit a shaded ventilated guard with ≥15 mm ground/vegetation spacing; inspect every permitted orientation and accessible surfaces.
11. Perform unpowered isolation/mechanical checks, then separately authorized staged electrical/RF/thermal qualification with bounded energy and dummy loads.

The old controller carrier envelope may be conservative for a horizontal-device build, but no reduced stack height is released. M6-L2 external antenna and optional LoRa remain distinct and unchanged. Q401/Q402 must remain replaceable with ordinary screw and solder access; neither adhesive potting nor trapped fasteners is acceptable. Exploded/native 3D assembly, final cutout clearance, enclosure fit and screw-access checks are **NOT_IMPLEMENTED** at this HOLD, not silently counted as PASS.
