# M4A-V1R1 — native and fabrication DFM review

Date: 2026-10-18. **Standard-process CAD gate PASS**, subject to independent review; supplier CAM is not performed. The [native geometry report](../hardware/80m/production/review/M4A-V1R1/JLCPCB-DFM.json) checks real copper, mask, drills, holes, edge and legend, not only KiCad settings. The [profile](../hardware/80m/production/review/M4A-V1R1/JLCPCB-standard-profile.json) includes official source URLs, date and margins.

## Actual results

- KiCad **10.0.6**: ERC **0 errors / 0 warnings**; DRC **0 errors / 0 warnings**, **0 unrouted / 0 parity**. All 62 configured DRC categories remain enabled, with no DRC exclusions. Three inherited informational ERC defaults (single global label, four-way junction, absent SPICE model) are disclosed; they are not manufacturing failures downgraded for this milestone.
- 150 × 110 mm outline centreline, 1.6 mm, two 35 µm nominal outer copper layers; four 3.2 mm NPTH on 140 × 100 mm pattern. All 401 native/drill positions and sizes checked, including **397 PTH / four NPTH**, 354 ordinary 0.60/0.30 vias.
- Minimum track 0.15 mm; minimum ordinary via annulus 0.15 mm; revised component PTH annulus ≥0.25 mm. Retaining accepted via dimensions avoids unnecessary routing changes.
- Native copper pair, hole/edge/annulus, mask bridge and foreign-copper checks pass. No copper slivers or narrow-connection DRC findings. Green 1 oz mask web remains **0.10 mm**, not 0.075 mm.
- **26 essential legend items**, each ≥1.0 mm high and ≥0.15 mm stroke. Connector/pin1, battery polarity, normal/Fox output, revision, Fox links, live-tab warning and all 14 test pads are legible. Small footprint outlines/references move to fabrication/assembly layers. Final silk Gerber circular stroke apertures are audited; no undersized required markings remain.
- Project-local copies of used footprints carry the same assembly-artwork layer changes as the native board. Copper/pad/courtyard/manufacturer IDs are preserved; this resolves real library-consistency warnings rather than suppressing them. [Overlay attribution](../hardware/80m/production/assembly-libraries/README.md).

## Electrical and geometry preservation

Every non-test value, MPN, population and net remains equivalent to frozen E2. **604 pad memberships, 55 manufacturer-specific devices, 256 logic combinations, 31 states and 16 timing corners** pass on the current export. Twelve existing mutations are retained; new tests add five lead-fit mutations, fourteen DFM mutations and nine interface/population mutations. These include real native hole/ring/mask/silk changes, ordinary-vs-press-fit requirements, swapped BD140/TL431/IDC/battery/output nets and Fox-only link removal.

All 217 footprint positions/rotations, track/via objects and pad centres/nets/shapes match compact V1. The only outer-land change is J502's extra 0.20 mm width; its local GND clearance is refilled. The polygon symmetric differences are approximately **0.5564 mm² F.Cu / 0.6340 mm² B.Cu**, confined materially to X148–157/Y120–124 mm. Integer polygon roundoff elsewhere totals <0.000001 mm² per layer and is reported separately, not excluded from DRC. [Exact comparison](../hardware/80m/production/review/M4A-V1R1/local-copper-delta.json).

One connected ground network remains across 41 filled polygon regions and 112 ground vias. No changed RF component value, turn count, filter topology, trace route, controller contract or power mode is hidden in this manufacturing correction. DC/pad/logic equivalence does not establish analog timing, RF loss, thermal performance or isolation. All remain **NOT_RUN**.

The [fresh export audit](../hardware/80m/production/review/M4A-V1R1/fabrication-audit.json) compares native drill geometry, actual Gerber copper flashes and IPC pin maps, and full/Fox placement populations. The isolated eleven-file manufacturing ZIP contains no reports, maps, alternative revision or panel. Reproduction commands and hashes are in the [review README](../hardware/80m/production/review/M4A-V1R1/README.md).
