# M3B-E2 — manufacturing-rule coverage

Date: **2026-10-15**, KiCad **10.0.6**. [Full native settings/custom rules/result metadata](../hardware/80m/review/M3B-E2/drc-coverage.json), [every check and E1/E2 severity](../hardware/80m/review/M3B-E2/drc-coverage.csv), [DRC JSON](../hardware/80m/review/M3B-E2/DRC.json), [text report](../hardware/80m/review/M3B-E2/DRC.rpt), [ERC](../hardware/80m/review/M3B-E2/ERC.json). The current native project is authoritative; the audit reproduces rather than replaces its rule configuration.

**Result: 0 DRC violations, 0 schematic-parity issues, 0 unrouted connections. No ignored DRC category and no DRC exclusion.** CLI includes errors, warnings and exclusions, with `--exit-code-violations --schematic-parity`. Ground zones were refilled before checking. Passing DRC does not verify transistor pin functions, heatsink isolation, analog safety, winding geometry or RF behavior.

## Restored coverage and real corrections

| E1 ignored category | E2 treatment |
| --- | --- |
| `footprint_filters_mismatch` | Warning enabled. Expanded E1 audit found **69 parity warnings**: inherited DIP/generic filters did not match actual approved SOIC/custom landings. Local symbol filters now name the exact used footprints, with no blanket wildcard |
| `footprint_type_mismatch` | Warning enabled; actual SMD/through-hole/probe classifications checked, no waived item |
| `missing_courtyard` | Warning enabled, no missing-courtyard finding; wound/custom parts retain dimensional envelopes |
| `track_not_centered_on_via` | Warning enabled; no final violation. Copper continuity alone is no longer its justification for disabling coverage |
| `tuning_profile_track_geometries` | Warning enabled even though there are no tuned/differential nets |

The expanded E1 output is preserved as [E1_EXPANDED_DRC.json](../hardware/80m/review/M3B-E2/E1_EXPANDED_DRC.json). E1's original zero report had less coverage; it must not be represented as equivalent to this one. Larger Q403 pads initially produced two silk-clearance findings. Moving the Q403 reference resolved these; the warnings were not suppressed.

## Numeric manufacturing constraints

| Constraint | E2 setting / disposition |
| --- | --- |
| Ordinary copper clearance | ≥0.15 mm; drain-specific custom clearance remains0.60 mm |
| Track / connection neck | ≥0.15 mm; actual track widths0.15/0.20/0.28/0.30/0.55/0.75/1.00 mm |
| Via diameter / drill / annular ring | ≥0.60 /0.30 /0.15 mm; no blind/buried/microvias used |
| Through-hole drill minimum | 0.30 mm. Nominal drill sizes/counts in [drill report](../hardware/80m/review/M3B-E2/drill-report.rpt) |
| Copper-to-edge | ≥0.50 mm; straight210×160 mm outline, four3.20 mm NPTH mounting holes |
| Copper-to-hole / hole-to-hole | ≥0.25 /0.25 mm; NPTH/PTH-in-courtyard interference checks enabled |
| Solder mask | **+0.025 mm expansion,0.075 mm minimum web**, via tenting retained. E1 used0/0; this is a documented global manufacturing change. Mask-bridge check is ERROR; no bridge allowance enabled |
| Silk | ≥0.10 mm clearance, ≥0.80 mm height, ≥0.08 mm stroke; silk/mask overlap, silk overlap, edge and legibility warnings enabled |
| Courtyard / board structure | Missing/malformed/overlap, padstack, footprint/library mismatch, duplicate/missing/extra footprint, outline checks enabled |
| Connectivity / planes | Unconnected, short, crossing, dangling tracks/vias, starved thermal, isolated copper and zone intersection checks enabled. Two ground zones refilled; no required ground connection left unrouted |
| Finished-hole tolerance | Quote must meet **J1011.20±0.05 mm; J5020.95±0.05 mm**, Q402/Q4031.30±0.05 mm. This is supplier capability, not a tolerance proof from DRC |

Stack-up remains two outer copper layers, nominal1.6 mm FR4,35 µm copper; ordinary plated through holes. Specify the actual profile centerline210×160 mm; the Gerber job's210.05×160.05 mm includes the0.05 mm drawing-stroke bounds. No slots, controlled impedance or high-density fabrication process is required. A quote must confirm the small mask web, drill/registration/annular-ring capabilities, finished-hole tolerance and chosen finish. “Finish:None” in the CAD job is an unspecified finish, not an instruction to deliver bare oxidizing copper; choose an economical solderable finish at quote/review.

## ERC, tool limits and reproducibility

E2 also enables `footprint_filter` in ERC. **ERC0** retains three KiCad-default ignored informational categories: `single_global_label` (intentional labeled test/interface nets can occur once), `four_way_junction` (connection topology is checked against XML and PCB rather than banning every four-way junction), `simulation_model_issue` (this schematic is not assigned complete SPICE models). These do not waive electrical pin conflicts. No ERC item is excluded. The exact ignored list is recorded in the exported ERC JSON.

KiCad's Python binding does not expose an independently enumerable DRC-item registry in this installation. Coverage evidence is the complete native rule table, `ignored_checks:[]` from CLI and actual error/warning/exclusion report, not a claim to have exercised every hidden/plugin checker. Enabled length/tuning/microvia checks have no matching objects here. No artificial test violating those irrelevant geometries is added to this RF correction task. There is no independent CAM etch simulation or incoming board inspection.

```sh
python3 tools/m3b_exports.py                 # includes ERC, parity/DRC and all 2D exports
/usr/bin/python3 tools/m3b_verify.py         # 664 pad memberships; R1 logic on current XML
/usr/bin/python3 tools/m3be2_pinouts.py      # 55 manufacturer role/pad assertions,10 negative cases
/usr/bin/python3 tools/m3be2_audit.py        # coverage, E1/E2 geometry, drill/export audits
```

The comparison asserts every old track/via is unchanged except **four U311 branches removed**, with **eight local replacement segments and one GND via** added; Q403/U311 are the only footprints with geometry/net changes. No RF/source/gate/drain/filter routing is changed. Separate JSONs retain exact net memberships and coordinates. Physical ground impedance, thermal effectiveness and port isolation remain measurement gates, even with zero disconnected zones reported.
