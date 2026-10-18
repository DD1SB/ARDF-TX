# Standard bare-PCB quotation specification — not submitted

Five individual controller boards. Native outline100.00×100.00mm, two-layer standard FR4,1.6mm finished thickness,1oz external copper, green mask, white legend, lead-free HASL, ordinary unfilled PTH vias. No controlled impedance, premium via treatment, custom laminate/stackup or supplier assembly service. JLCPCB standard web options only.

Use fabrication/ Gerbers, CTRL-PTH.drl and CTRL-NPTH.drl; drill maps are review aids. Thegbrjob bounding box includes the0.05mm outline stroke (100.05mm); the milling centerline is100.00mm square. No panel outline or final enclosure is specified. Confirm the automatic outline interpretation in a later authorized CAM review.

Actual native track minimum0.15mm; nominal via0.80/0.30mm and via/PTH minimum annulus0.25mm. Preferred0.15mm signal clearance,0.03mm mask expansion,0.10mm mask web and conservative edge/hole margins are independently checked. Finished-hole tolerances remain standard; first-article connector fit is NOT_RUN. See JLCPCB-standard-profile.json and JLCPCB-DFM.json, including manual items. The default ignored tuning-profile check is irrelevant because no tuning patterns exist; no relevant DRC category is disabled and there are no exclusions.

All four base populations share this PCB. Populate the six underside small positions before final THT assembly or use controlled local reflow; a second factory assembly service is unnecessary. Bottom clearance must remain at least10mm as in M6-C1. Inspect connector lead clipping and both sides. Exact MPN/pin orientation is mandatory; Nexperia BAT54H,SOD123F must not be confused with onsemi BAT54H,SOD323.

No factory quotation, CAM acceptance or file upload has occurred. Planning cost model is separate in COST_DELTA.md; stock and prices must be rechecked before any authorized purchase. Optional LoRa remains HOLD and is not an accepted assembly variant.
