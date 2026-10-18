# Standard fabrication configuration — review only

Proposed quantity: **five bare PCBs**, one initially populated in stages. Do not submit files or order without explicit authorization.

| Option | Select |
|---|---|
| Outline | 100.00 ×100.00 mm route centerline, single board |
| Layers/material | 2 /standard FR4 |
| Finished thickness | 1.6 mm, ordinary ±10% tolerance |
| External copper | standard1 oz, nominal35µm |
| Mask/legend | green /white |
| Finish | lead-free HASL |
| Vias | ordinary plated through, unfilled; no guaranteed tent closure |
| Impedance/special processes | none |
| Assembly | separate manual/stencil reflow and hand-soldering; no JLC assembly dependency |

The Gerber job bounding box includes the0.05 mm outline stroke and reports100.05 mm; native and exported route centerline is100.00 mm. Enter the actual100.00 mm dimensions and inspect any future automatic quote interpretation. No promotional price eligibility is claimed.

Use only the nine Gerber layers and separate PTH/NPTH drill files in `fabrication/`. Paste files support an ordinary stainless stencil; drill maps/job metadata are review aids. No custom dielectric is requested: native1.51 mm FR4 core metadata is a nominal visualization model within the1.6 mm finished board, not a negotiated stackup. No RF-board manufacturing file is included or changed.

Actual minimum track width is0.15 mm. Ordinary vias are0.80/0.30 mm (0.25 mm nominal annulus). Component PTH annuli are at least0.25 mm. There are381 vias,42 round1.10 mm component holes, four0.60 mm plated slots, two0.65 mm unplated USB locator holes and four3.20 mm unplated mounting holes. Native drill and export counts agree. Published hole-size allowance is−0.08/+0.13 mm and position±0.075 mm; no tighter finished-hole request is hidden in the design. First-part connector fit remains a physical check.

HASL is a standard candidate finish for these land pitches. Use a standard0.10–0.12 mm stainless stencil and controlled paste-compatible reflow; check RTC/USB/ESP seating and solder joints on the first assembly. Omit LoRa, DEBUG header if unused and every documented variant DNP position. The backup holder's central contact has no paste; its surface cleanliness, spring pressure and actual backup retention require inspection. No premium via treatment is relied upon for hidden solder joints.

Independent native geometry and KiCad DRC both pass. This is **local DFM evidence**, not a supplier quotation, acceptance of commercial CAM, first-article fit or electrical/thermal qualification. Review official [JLC capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/) and the versioned `JLCPCB-standard-profile.json` when preparing any authorized quotation. Prices, delivery, freight and tax remain separate.

Initial mounting uses nylon M3 screws/standoffs/washers with10 mm underside and15 mm upper controller component reserves. Trim leads and inspect clearance; do not use solder mask as insulation for conductive hardware. RF2M needs its separate25.2 mm underside cooling envelope and at least30 mm mechanical support space; this does not qualify enclosure airflow. Keep metal/cables out of the ESP antenna keepout. Use side-by-side boards and continuity-tested150 mm keyed IDC cables before considering any stacking.
