# M4A — adjustable RF-module mechanical interface

Date: **2026-10-15**. V1 engineering assumptions, **not a confirmed enclosure/controller drawing**. [Native PCB](../hardware/80m/production/RF80_V1.kicad_pcb) is the board authority; current measured positions/envelopes are in its review package. E2 is frozen separately.

## Board and mounting convention

Board150×110mm,1.6mm nominal, top-side component assembly. Define module coordinates from the upper-left profile corner, +X right/+Y down when looking at top copper. The four **3.20mm NPTH** mounting centers are **(5,5),(145,5),(145,105),(5,105)mm**: a140×100mm pattern. Keep insulating standoffs/washers clear of copper, leads and power-device tabs. A bench support needs≥10mm bottom clearance until leads are trimmed and actual protrusion measured.

This mounting convention is a **proposal** that a later2m board can reuse if practical and cost-neutral. It does not impose that board's RF layout or thermal design. Controller dimensions, inter-board spacing and final enclosure geometry remain **OPEN**. Use flexible keyed harnesses rather than assuming unapproved board-to-board alignment. Any future outline/hole revision requires a documented interface update.

## Heights and service space

| Item | Nominal/conservative basis and constraint |
| --- | --- |
| L410/L411 | Original T60-2,20turnAWG24; flat and upright with winding allowance. Own upright envelope reaches≈18.1mm above PCB; measure actual winding height/tilt and stabilization |
| T401 | FT-50A-43,9+9turnAWG24 bifilar. Same original formed lead landing/polarity; own envelope includes winding. Verify lead strain relief and phasing |
| Q402 | Vishay IRF610 TO220,1G2D3S/tabD,1.30±0.05mm finished holes; exact incoming body/lead fit required |
| Q403 | ST BD140 SOT32,1B2C3E;1.30±0.05mm holes;2mm body stand-off. Illustrated ST face points **+PCB Y**. Insulate any conductive cooling attachment/probe |
| Thermal allowance | Initial integration assumption≤25mm above PCB and a reserved edge-access cooling path; **not a qualified heatsink size**. If measured SOA/case temperature needs more volume, enlarge envelope before enclosure commitment |
| C350 and C404 | Actual specified radial/polymer bodies and polarity, kept accessible for inspection/replacement. Heat from R350/PA must be measured; nominal capacitor ratings do not qualify the compact hot environment |
| Harness/mating height | Allow an initial30mm top-side service envelope and≥20mm cable escape/bend allowance. These are adjustable assumptions pending exact housings, contacts, wire and strain relief |

Do not attach an exposed drain/tab or collector case to grounded mounting hardware. Remote TH301 must be bonded through insulation to the intended IRF610 case and strain relieved; a board-mounted NTC is not an equivalent sensor position. Its electrical and mechanical detachment tests remain separate. The compact board's own3D models are dimensional envelopes/standard library representations, not certified thermal/mechanical qualification.

## Connectors and wiring

J101 remains the exact keyed Wurth2×8/2.54mm controller header on the left; its3.3V power/grounds, I²C, lease, ARM/KEY/path/profile/mute/status/pack-ID contract is electrically identical to E2. **No raw2S/4S voltage on J101pin1.** Route separate PA current through J301 and short multiple ground returns in the controller cable. Ribbon/harness pin1/key and continuity must be inspected.

J301 remains JST VH2way,3.96mm, pin1protected pack positive/pin2return. Normal build uses4S12–16.8V; Fox-only uses protected2S sensing with regulated3.3V from the common controller. Mating VHR-2N/appropriate SVH contacts and wire gauge are not interchangeable with the Fox housing.

J401 remains Phoenix1727010,3.81mm normalRF terminal; oriented toward the right-side cable escape. Use short coax/return to the normal antenna accessory or50Ω fixture, with external strain relief. J502 remains keyed JST XH3way,2.50mm, **1RF_FOX/2GND/3identity**, at the lower-right. Its compact30cm radiator/counterpoise/loading accessory remains independent of the long Classic/Sprint wire/counterpoise tuner.

Board-side connectors are already in the component BOM. Mating plugs, crimp contacts, cable exits, insulation and external anchors are installed-cost allowances. Production-intent geometry cannot confirm housing availability, crimp retention, moisture sealing or a finished enclosure fit. No weatherproof enclosure is designed here. Keep water/condensation off the unqualified board and establish environmental protection later without coating tuning contacts, connectors or heat-transfer surfaces indiscriminately.

Critical finished holes remain **J1011.20±0.05mm/J5020.95±0.05mm/Q402–Q4031.30±0.05mm**. Supplier confirmation is required; the compact board must not inherit an assumed ordinary drilling tolerance that violates those constraints. Dry-fit received parts and check1:1 assembly artwork before assembly authorization.
