# M5B-E3 JLCPCB manufacturability audit

The versioned [JLCPCB-standard-profile.json](../hardware/2m/review/M5B-E3/JLCPCB-standard-profile.json) records official source URLs,2026-10-16 retrieval, hard capability limits, preferred margins and manual checks. It distinguishes nominal 1 oz from actual plated external copper. The requested old production-time URL is unavailable; the official equivalent is [PCB fabrication services and production time](https://jlcpcb.com/help/article/pcb-fabrication-services-and-production-time). No commercialCAM review, accepted quote or upload occurred.

`tools/m5b_e3_dfm.py` reads the **native PCB**: actual layer/thickness/stack properties, track shapes, copper graphics, pads, drill geometry, hole spacing, annuli, edge distances, mask apertures/webs, visible legend and filled-zone polygon slivers. It checks physical TL aliases instead of reporting intentional net ties as shorts. Its spatial pair tests do not merely read configured KiCad rule minima. Native KiCad's actual narrow-connection/thermal checker remains an additional mandatory gate. Combined coverage is recorded in `DRC-coverage.json`, `JLCPCB-DFM.json`, `engineering-regression.json` and `final-checks.json`.

| Constraint | Published capability / E3 policy |
| --- | --- |
| Layers/thickness/copper | Standard2L FR4 /1.6 mm±10% /nominal 1 oz |
| Track/space | Vendor1 oz0.10/0.10; actual policy≥0.15/0.15 |
| Via | Preferred0.80/0.30;0.70/0.30 and 0.60/0.30 where congested; all ordinary PTH |
| Annulus | ComponentPTH≥0.25; actual minimum 0.275 mm. Via preferred0.25; local0.20/0.15 exceptions explicitly inventoried |
| Holes | Via hole gap≥0.20; component hole gap≥0.45. Hole-to-foreignCu≥0.20 via/NPTH,≥0.28 componentPTH |
| Mask | Green1 oz web≥0.10; actual apertures inspected; ordinary tenting only |
| Legend | Visible height≥1.0, stroke≥0.15, mask gap≥0.15 |
| Routed edge | VendorCu≥0.20; board policy0.50 |
| Special process | None; no controlled impedance, custom core, filled/capped/blind/buried vias or factory assembly |

The final via sizes/counts and every preferred-margin exception are in `JLCPCB-DFM.json` and `via-connectivity.csv`. Smaller lands are intentional local congestion decisions, **not a supplier process exception**. They retain0.3 mm holes and lands well above JLC's small-via/premium thresholds. All32 PA source vias use the preferred0.8 mm land. No global enlarging or blanket DRC exclusion is used.

Final KiCad 10.0.6: **ERC0 errors/0 warnings; DRC0 errors;0 unrouted;0 parity;11 warnings;0 exclusions**. Every manufacturing category is enabled. Only `tuning_profile_track_geometries` is ignored because no tuning-profile geometry exists. ERC default informational ignores are disclosed, including footprint filters; the PCB's corresponding filter warning and actual package/pad comparison are active.

The11 retained warnings are TL603–609 and TP601–604. Each is classifiedB, intentional non-component. They have no purchased body, paste,3D body or assembly volume; a component courtyard would be fictitious. TLs are mask-covered copper net ties, and probes have intentional0.6 mm mask openings. The native copper/mask/edge checks remain enabled. Exact coordinates and individual dispositions are in `DRC-warning-dispositions.json`.

Regression testing rejects E2's thickness/copper/finish/legend under the E3 profile. Mutations detect wrong thickness, narrow tracks, insufficient annuli, blind vias, premium microdrills, undersized legend,2 oz copper, unsupported finish and an actual 0.05 mm copper gap. Three additional native RF/source mutations supplement the preserved37 electrical/physical mutations. The engineering gate also checks TL length/width,32 grounded source vias, source mask policy, thermal-window isolation, connector holes and unchanged purchased circuitry.

Manual reviews are explicit: HASL flatness and hidden-pad solder quality; mask coverage; incoming connector dimensions; TIM/heat-sink insulation and actual thermal contact; and independent finalCAM/assembly inspection. They are not fabricated automated PASS results. Ordinary drill/etch variation and measured RF/thermal behavior remain qualification gates. The locally verified result establishes standard-process design compatibility; it does not assert factory CAM acceptance.
