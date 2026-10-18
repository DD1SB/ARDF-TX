# Compact V1 fabrication assumptions — NOT RELEASED

This is an engineering candidate. **Do not manufacture V1 before reference
qualification, resulting corrections, independent review and user approval.**

Single board profile: 150.00 × 110.00 mm, measured at Edge.Cuts centerlines;
0.05 mm outline stroke is not an added outline allowance. FR4, 1.6 mm nominal,
35 µm nominal copper on F.Cu/B.Cu, ordinary through-vias 0.60/0.30 mm.
Copper minimum 0.15 mm, drain clearance 0.60 mm, copper-edge minimum 0.50 mm.
Mask expansion +0.025 mm, minimum mask web 0.10 mm; tent vias. Silkscreen
minimum 0.8 mm height/0.08 mm stroke; F.Fab assembly artwork is authoritative
where local reference text cannot fit. No blind/buried vias or controlled-
impedance process is requested. Confirm finish/flatness, registration, yield
and electrical inspection with the selected supplier after authorization.

Four 3.20 mm NPTH M3 mounting holes, module-relative centers (5,5), (145,5),
(145,105), (5,105) mm. All other holes are PTH; drill report and native/export
comparison are authoritative. **Finished holes:** J101 1.20 ± 0.05 mm,
J502 0.95 ± 0.05 mm, Q402/Q403 1.30 ± 0.05 mm. These are not drill-tool sizes.
Ordinary advertised supplier tolerances are insufficient evidence. Confirm
lead fit, annular ring, mask web and exact process/surcharge; all remain open.

Review Gerbers are unpanelized. The two-up 160 × 232 mm cost-panel concept
has no released tooling/tab geometry. Do not have CAM invent rail tabs or
alter copper/holes without reviewed approval. The quoted-cost field is OPEN;
planning figures are not purchase orders or accepted vendor offers.

Assembly: top-side parts, explicit full/Fox lists. Use actual maker-qualified
footprints and retained windings. ST Q403 illustrated face +PCB Y, 1B/2C/3E;
TI U311 DBZ 1K/2REF reference and 3A ground. Insulate IRF610 tab/heatsink and
remote NTC. Final thermal material/envelope and mating cable retention require
incoming inspection and physical qualification. The original E2 first-build
handoff is independent of these compact review Gerbers.
