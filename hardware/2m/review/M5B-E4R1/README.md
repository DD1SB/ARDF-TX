# M5B-E4R1 source-joint evaluation candidate

GO for independent five-bare-board review only. No acceptance tag or manufacturing authorization. Last acceptedCAD: m5b-e3/95f189c; comparison candidate: E4/920da7b. Active native project: hardware/2m/RF2M.*. HistoricalE4files are untouched.

Read docs/M5B_E4R1_REVIEW_DECISION.md from repository root. source-assembly-DFM.json and acceptance-gates.json separate CAD, credible prototype process, controlled bare-board readiness and NOT_RUNphysical/operational gates. Conservative110 °C target is missed;125 °C qualification remains OPEN. Source solder coverage is not guaranteed by paste area, continuity or a model.

gerbers/ and RF2M-M5B-E4R1-fabrication-review.zip are freshly exported bare-board review data only. stencil/ contains separate Q501-only0.12 mm stainless artwork, not PCBfabrication data. development/ contains baseline/analysis/deliberate rejected mutations: never fabricate it. Native archive and all exports are bound by SHA256SUMS. Mechanicalviews include an envelope-only sink model, not manufacturer-qualified CAD. No upload/ordering tool is used.

Reproduce with /usr/bin/python3 tools/m5b_e4r1.py checks, verify, dfm, models, thermal, engineering; DISPLAY=:97 LIBGL_ALWAYS_SOFTWARE=1 /usr/bin/python3 tools/m5b_e4r1.py exports --render; then reports and delivery. KiCad 10.0.6/Pythonpcbnew and a working Xdisplay are required. Actual commands are in the check/export logs. Design implementation is tools/m5b_e4r1_design.py, which derives only from frozen920da7b; do not rerun it over unrelated active edits. Physical tests remainNOT_RUN.
