# M5B-E5 review decision

**GO for independent evaluation-board review.** No acceptance tag, manufacture or transmitter release is authorized.

Native board: 150 × 110 mm, common 140 × 100 mm pattern, standard two-layer 1.6 mm / 1 oz FR4. E4R1 component values, manufacturer pad mappings, 20-pin controller contract, protections and all three populations are retained. The driver/PA/matching/filter/source/bar group translates rigidly 20 mm left; support circuits and connectors are placed and rerouted. Local washer-ground hazards are explicitly corrected. RF80 and controller CAD are unchanged.

Current CAD report: 0 DRC errors, 0 unrouted, 0 parity differences. Warning categories: {'missing_courtyard': 11}. Native equivalence, full logic/package/ST regression, source assembly, actual copper DFM, power returns and fabrication consistency are separate mandatory gates in review-gates.json. A missing/failed gate keeps HOLD; an old PASS is not substituted.

Mandatory single-RF/controller arrangements have dimensioned envelopes. The optional dual-RF stack remains HOLD for enclosure/thermal/EMC integration. Source-joint and cooling geometry are retained; same-boundary 40°C/4 W predictions are about 91/122/138°C nominal/conservative/poor contact. The conservative 110°C target is unmet, and the 125°C physical thermal gate stays OPEN. Enclosure heating may exceed it. The initial source joint, contact flatness, convection and temperature must be qualified before RF use.

Electronics budget is unchanged with substantial unquoted material. Bare-board savings are only a setup/area budget estimate, not a quote. Supplier CAM, quote and purchasing require later authorization. All physical RF gain, PEP/ERP, true AM, stability, emissions, port isolation, controller immunity, protection timing, hot SOA and endurance tests remain NOT_RUN. Read the staged bring-up procedure before any population.
