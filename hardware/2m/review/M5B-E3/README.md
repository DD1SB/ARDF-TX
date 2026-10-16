# M5B-E3 standard JLCPCB review package

**CAD milestone — NOT RELEASED.** Active native project: `../../RF2M.kicad_pro`, `../../RF2M.kicad_sch` and `../../RF2M.kicad_pcb`. Frozen comparison baseline: `m5b-e2` / `2ca4c8e`. Start with the [review decision](../../../../docs/M5B_E3_REVIEW_DECISION.md).

The proposed standard options are five boards, 180 × 140 mm, two-layer FR4, 1.6 mm, 1 oz, green mask, white legend and lead-free HASL. No controlled impedance or special process is required. The fabrication-review ZIP contains exactly nine Gerbers and two drill files. The native ZIP contains the editable project and libraries. Neither archive authorizes an upload or order.

Only `gerbers/` and the fabrication-review ZIP contain proposed fabrication data. Analysis reports and `development/` are not fabrication inputs. Logical and physical IPC files document intentional RF net aliases; ordinary factory electrical test can derive connectivity directly from the Gerber copper. No special netlist service is required.

Reproduce from the repository root with KiCad 10.0.6 and `/usr/bin/python3` providing pcbnew and Pillow:

```sh
/usr/bin/python3 tools/m5b_e3.py checks
/usr/bin/python3 tools/m5b_e3.py verify
/usr/bin/python3 tools/m5b_e3.py models
/usr/bin/python3 tools/m5b_e3_engineering.py
/usr/bin/python3 tools/m5b_e3.py dfm
DISPLAY=:97 /usr/bin/python3 tools/m5b_e3.py exports --render
/usr/bin/python3 tools/m5b_e3.py reports
/usr/bin/python3 tools/m5b_e3_delivery.py
/usr/bin/python3 tools/m5b_e3.py artifacts
sha256sum -c hardware/2m/review/M5B-E3/SHA256SUMS
```

Rendering needs an existing X display or Xvfb with software OpenGL. Exact CLI commands and rendering environment are recorded in `check-commands.json` and `export-commands.json`. Historical generators and archived implementation aids must not be run against the finished board.

The eleven DRC warnings describe intentional bodyless RF copper/probe features. No manufacturing category is suppressed. Manual HASL/hidden-joint inspection, thermal contact, RF/AM, supply-fault, antenna and endurance qualification remain **NOT_RUN**. Standard published capability and local DFM compatibility are separate from quotation and factory CAM acceptance. No files have been submitted externally.

The three fresh KiCad renders show all native component positions, including mutually exclusive converter alternatives. The population-specific assembly drawings and BOMs determine actual fitment. Custom models are dimensional envelopes; missing connector body models are disclosed in `3D-model-status.json`.
