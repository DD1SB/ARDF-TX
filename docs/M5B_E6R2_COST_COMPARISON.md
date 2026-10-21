# E6R2 material and assembly comparison

[Machine-readable quantities1/5/7/10](../hardware/2m/review/M5B-E6R2/costs.json),
[thermal BOM](../hardware/2m/review/M5B-E6R2/shared-heatsink-BOM.csv) and three
population BOMs separate historical indexed prices from estimates. All figures
below are net EUR; freight/VAT and an exact supplier basket are additional.
No procurement occurred. Existing E5/E6/E6R1 figures remain historical estimates.

The source TIM is not treated as free scrap: one100×100mm86/82 sheet at the
previously indexed€22.59 net is charged in full, with10usable15×44 blanks per
sheet. One unit therefore bears the whole sheet cost; seven units bear€3.227
per unit, leaving three spare blanks. SK81100 retains the previous indexed
€7.30 gross observation (~€6.134net at19%); it is not a new quote or seven-unit
stock reservation. Bar/angle/fastener prices, MOQ and actual cut charges remain
unquoted estimates. Grease, bond strap and insulating hardware are included.

At seven units, E6R2 cooler material is approximately€11.99–19.13/unit,
€83.94–133.89/fleet, before the separate insulating carrier and protected feet/
corner posts (€5–12/unit estimate). ArchitectureC adds€2.59/unit estimated
NORMAL electrical material; TRAIN_ONLY omits it. No unqualified PA-window trip
subsystem is charged because none is fitted. Full electrical BOM estimates are
BUCK4S€55.35,BOOST2S€56.92,TRAIN_ONLY€14.11 per board at seven units. These exclude
controller,pack/BMS,antenna/feed,enclosure,RF harness and alignment/inspection.

| Seven-unit planning comparison | Separate heatsinks | Cooler material/unit | Additional electrical |
|---|---:|---:|---:|
| E5 historical |3|€31.11–38.61|—|
| E6 historical concept |1|€15.36–21.36|—|
| E6R1 historical proposal |1|€15.36–21.36|€1.53–3.61|
| E6R2 implemented |1|€11.99–19.13|€2.59 estimate|

The thermal BOM has13line items and24grouped quantity entries, including bulk grease
allocation and grouped fasteners. Expanded hardware comprises12screws,7washers,
4locknuts,1bush,2mica pads,1TIMsheet,4angles,1bar,1sink,and a braid/terminal
bond (35pieces before grease,carrier,posts andfeet). The modeled cooler assembly is248–270g;
~113g insulating carrier,enclosure andPCB masses are separate. One extrusion,
one simple stock bar,four independent support angles and two insulated direct
transistor attachments replace the three separate cooler orientations and old
pass spacer. There are4side,4foot,2bar and2device fasteners; grouped washers/
locknuts are listed explicitly. Service access is through the cutouts before
shell installation; Q401/Q402 are replaceable. No custom milling or fan.

Allow30–50minutes per cooler for cutting/drilling/tapping/deburring,interface
installation,bond/isolation checks and assembly, an engineering estimate rather
than measured labor. At€25/hour this is€12.50–20.83/unit, outside materials.
PCB soldering,source inspection/X-ray,instrumentation,RF alignment and rework
are additional. E5 allowed45–75minutes; no labor saving has been demonstrated.

Bare boards remain a five-board-lot budget of€60–100 net before shipping and
slot quotation; seven required units may require ten purchased boards. The
unchanged outline/layers/process avoids a premium thermal process, but two
ordinary routed cutouts still need actual supplier pricing. Enclosure remains
unquoted. Neither€120 nor€150 complete transmitter cost is demonstrated.

The preserved upper controller carrier and its supports are outside the cooler
delta:allow another€3–7plate and€2–5hardware if not supplied by the eventual
housing. Its~110g plate mass is separate from the new~113g lower guard/base.
Neither enclosure structure is silently counted as free.
