# M5B-E3 review decision

**GO for independent review and, after explicit user authorization, upload of the five-board standard-JLCPCB dataset for quotation.** No manufacturing release is granted. E2 remains frozen at `m5b-e2` / `2ca4c8e`; its manufacturing recommendation is superseded.

The completed native board is **180 × 140 mm, two-layer standard FR4, 1.6 mm, 1 oz, green mask, white legend and lead-free HASL**. It requires ordinary through-vias and no controlled impedance, custom core or premium process. The schematic architecture, purchased MPNs/values, controller contract, protection behavior and population variants are preserved.

Implemented changes include 2.741 mm RF lines with approximately 1.88% shorter lengths, matching placement shifts of at most 0.519 mm, flat junctions and a tapered SMA launch. Power routes are selectively wider. The PA source now has 32 ordinary preferred-size thermal/ground vias. Connector holes and legend have standard-process margins. Local control escapes and ground connections were repaired without moving the RF ports or mounting holes.

**KiCad 10.0.6 results:** ERC zero errors and warnings; DRC zero errors; zero unrouted connections; zero schematic/PCB parity issues; eleven individually justified bodyless-feature warnings; zero exclusions. No manufacturing category is suppressed. Preserved coverage passes: 4,096 logic combinations, 39 states, 37 mutations, 42 manufacturer pin maps, 26 ST network positions and 320 package/pad sets. The independent native-geometry DFM gate, eleven new DFM mutations and three additional RF/thermal geometry mutations pass. Exact results and commands are in the review package.

Calculated nominal microstrip impedance is 50.005 Ω. Combined ordinary-process extremes span 39.39–63.44 Ω; the short matching lines, component junctions and launch still need end-to-end RF alignment. These calculations do not establish gain, ERP, clean AM or emissions.

The source thermal model predicts approximately 109°C junction at 4 W heat and 40°C ambient with 18 µm average barrels, but approximately 133°C at 10 µm. No guaranteed minimum plating or filled-via process is hidden in the purchase specification. Staged assembly must establish joint quality and thermal margin, using the initial 4 W heat budget, 125°C junction engineering limit and retained 60°C pass-case limit. Live D45H11/BD139 tabs require insulated hardware. Continuous full no-tone carrier, actual RF/AM, isolation, antenna ERP and 12 h / 24 h endurance remain **NOT_RUN**.

Quantity-ten component budgets remain **€50.27 BOOST2S / €49.03 BUCK4S / €14.11 TRAIN_ONLY**. Their unquoted portions remain €28.09 / €27.95 / €10.02. Five bare boards have an unquoted engineering allowance of **€41.50–83 before shipping and VAT**. Actual JLCPCB pricing and factory CAM acceptance are pending. No achieved price saving or supplier stock reservation is claimed.

Fresh schematic, BOMs, copper/assembly/placement views, actual KiCad renders, logical/physical netlists, Gerbers, separate drills/maps, native and fabrication-review archives, and SHA-256 inventory are under `hardware/2m/review/M5B-E3/`. The fabrication ZIP contains only nine Gerbers and two drill files; analysis and development data are separate. Source and drill coordinates/counts are checked against the final native board.

There is no remaining identified CAD fabrication blocker. Next steps are independent review, explicit authorization before external submission or ordering, and separately authorized staged assembly/commissioning of one board. RF80, M4A, accepted ADRs and historical revisions are preserved. No upload, purchase, manufacturing, assembly, power-up or RF operation occurred.
