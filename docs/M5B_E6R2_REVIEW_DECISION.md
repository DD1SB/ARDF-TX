# M5B-E6R2 review decision

**GO for five bare RF2M E6R2 evaluation boards.** This is an engineering
candidate for independent review, not powered-operation or production acceptance.
No boards/stencils were ordered, hardware energized, Git branch pushed or tag created.

Starting `b48865fed332ced9257559e174f0b6fceaaec096`, branch `m5b-e6-unified-heatsink`.
Final local commit is recorded by Git history. Native PCB SHA-256:
`0bdf01a6907b35927f6f1d9ad55acf9c7eb7e893835982afc9e9652c51417baf`.

| Gate | Disposition | Evidence |
|---|---|---|
|1.Native electrical/mechanical implementation|PASS|Complete native schematic/PCB; one supported cooler; insulation and exact device lead views audited|
|2.Five bare evaluation PCBs|GO|CAD/electrical/DFM/reproduction gates below; no known intrinsic blocker remains|
|3.Initial powered prototype|NOT_RUN|Requires assembled interfaces,verified isolation,inhibit,current-limited supply and dummy-load instrumentation|
|4.Operational transmitter|NOT_RUN|Measured RF/AM,spectrum,thermal,shutdown,continuous beacon and environment qualification required|

Executed: ERC 0 errors/0 warnings; DRC 0 errors, 0 unrouted, 0 parity issues. All 11
missing-courtyard warnings exactly match E5. The project configuration is
byte-identical: no new exclusions or ignored checks. Python enum/image-handler
diagnostics are recorded in raw logs; they are not hidden CAD violations.

Electrical/native checks: 352 footprints, 51 critical manufacturer maps,
4,096 enable combinations, 36 safety scenarios, 16 local-keying rows,
68 negative cases. Source process: 16 native/input mutations and 4 adverse
thermal-model cases rejected; these are not physical fault-detection results.
The final source/mask/paste/98-via geometry is independently checked unchanged.
Two actual solid-collision negatives exercise the carrier/tab checks. Ground
contact graph: one component. All 12 main-current copper paths remain connected.

Ngspice: 8 transient cases, 2 AC return-ratio cases, 14 numerical tests. Loaded/
unloaded modeled loop margins are 85.87°/68.92°. The TI model is external;
ST BJTs and PA load are bounded generic/envelope models, not characterized RF
models. Converter switching-loop/RF spectra and hot device corners remain open.
BF20 clips the modeled crest; it is explicitly not full-profile qualification.

Standard-JLCPCB DFM PASS, 11 native mutations detected. Actual minimum track 0.15 mm,
via annulus 0.15 mm, component PTH annulus 0.275 mm. Ordinary 0.6/0.3 mm via margin
exceptions remain individually listed. No special stackup, filled/capped vias
or controlled-impedance service. 150×110 mm, 2 layers, 1.6 mm FR4, 1 oz, green/white, HASL.
Nine Gerbers + separate PTH/NPTH drills (953/6 hits) reproduce from native.
Fresh 11 CAM files are geometrically identical; only export timestamps differ.
Five source-paste windows still total 6.765 mm². Full top stencil is supplied.

The new flat BD139 footprint initially mirrored the manufacturer front view.
It was corrected to physical 3E–2C–1B left-to-right, while numeric 1B/2C/3E remains.
The rejected draft is preserved and detected by a native negative test. The
shared Q404/Q405 normal-key clamp injection was also corrected by separating
Q405's emergency base network. An isolated C409 reservoir-ground pour found by
the actual contact graph was corrected before final routing. Mechanical review
corrected carrier/foot overlap and foot-screw engagement. These were real
implementation corrections; all final relevant gates pass.

One SK81 100 SA 100×100×15 mm, 15×44×6 mm bar, rated 0.25 mm source TIM, two mica interfaces,
IB6/steel Q401 fastening and PA66 Q402 fastening form one independently supported
assembly. Calculated/indexed hardware mass 252.2 g before braid/compound,
approximately 254 g assembled allowance; not weighed. Lower carrier ~113 g and the
preserved upper carrier are separate. Seven-unit cooler material estimate
€11.99–19.13/unit plus €2.59 keying parts;
base, posts, housing, labor and minimum stock costs are stated separately.
No complete €120/€150 transmitter price is demonstrated.

E6R1's modeled 1 W/40°C Classic/Sprint/continuous-MO PA peaks remain
74.31/73.72/87.76°C; Q401 46.43/46.03/59.51°C. The continuous-beacon margin is
only 0.49°C. The 134.72°C degraded-contact scenario remains an assembly/qualification
risk. Preserve 110°C PA target, 125°C ceiling, Q401 60°C and Q402 80°C criteria.
No source-region sensor is claimed to measure Tj; no threshold was raised.
First-article solder/contact/insulation/current/RF/temperature measurements
must precede prolonged full-power use. These uncertainties do not prohibit bare
boards under the requested evaluation gates.

Controller M6-L2, RF80 M4A-V1R1 and every historical review/archive pass the
preserved-start hash guard. Protected RF signal copper, matching/filter geometry,
Q501 position and all 20 controller pins are retained. Current core native sources
are revised only for RF2M. No acceptance tag or production release.

See [manufacturing](M5B_E6R2_MANUFACTURING.md), [first article](M5B_E6R2_FIRST_ARTICLE_TEST.md)
and [review/reproduction](../hardware/2m/review/M5B-E6R2/README.md).
