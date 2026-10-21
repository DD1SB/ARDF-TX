# E6R2 common-plane assembly

The [mounting drawing](../hardware/2m/review/M5B-E6R2/mechanical/dimensioned-mounting.pdf),
[STEP stack](../hardware/2m/review/M5B-E6R2/mechanical/complete-mechanical-stack.step)
and sections are dimensioned in native PCB coordinates, mm. PCB topZ0,
bottom−1.6; common aluminum mounting planeZ−7.9. Package exterior maxima,
formed leads, screws, insulators, support angles and actual cutouts are modeled.
SK81 fin detail and transistor plastic details are simplified and identified;
no precision milling geometry is assumed. Manufacturer incoming checks remain.

| Item | Native XY / orientation / attachment |
|---|---|
| Q501 PD54008L-E |(92,55),0°,unchanged;source→vias→TIM→15×44×6bar→sink|
| H5/H6 |(92,32)/(92,68),M3×12+OD9×0.5 washers;3.6mm base engagement|
| Q401 D45H11 |pin1(113.46,47.30),0° formed footprint;hole(116,28);backZ−7.8|
| Q402 BD139 |pin1(135.28,41.25),0° formed footprint;hole(133,27.5);backZ−7.8|
| Q401 cutout |(109.5,23)..(122.5,42.3),R1 corners|
| Q402 cutout |(128,22.5)..(138,37),R1 corners|
| Shared SK81 |X42..142,Y20..120,Z−22.9..−7.9;100×100×15,base4mm|

Form leads with4.5mm supported straight length and2mm centerline bend radius
(inner radius≥1.65mm). Q401/Q402 path lengths to1mm PCB protrusion fit the
manufacturer minimum available13/15.3mm lead lengths. Use a forming jig and
support between body and bend; never pull a tab into alignment by its leads.
Use actual incoming devices to confirm tolerances before soldering. Pads2mm,
drills1.3mm; leads do not support cooler mass.

Both live tabs use **Fischer GS220P12×18×0.05mm mica**, separately, with thin
grease on both faces (~0.05mm total). The smaller GS32P was rejected because it
did not cover the modeled maximum BD139 underside envelope. Mica is rated5kV
material; this is not a certified whole-assembly dielectric rating. Do not rely
on grease, solder mask or anodizing as insulation.

Q401: VPA_PRE tab, FischerIB6 shoulder OD3.5/bore3.1/flangeOD6, shoulder1.2mm,
flange1mm; fits≥3.75mm hole and≥1.23mm tab without bottoming. M3×6 steel screw
from top,3.6mm engagement in4mm base,0.4mm bottom margin. Q402: MOD_SINK tab,
M2.5×6PA66 screw+PA66OD5/ID2.7/0.5mm washer;≥2.9mm device hole,2.5mm engagement.
Do not force a TO-220 bush into the smaller hole. Inspect polymer creep/clamp
pressure after cycling. No unsourced guaranteed torque is specified; use light,
repeatable low-torque hand clamping and manufacturer hardware guidance.

Four12mm-wide30×20×2mm aluminum angles independently carry the cooler.
Side M3 taps atX42/142,Y40/100,Z−9.9,axisX;4mm engagement,M3×6 from outside.
Foot holes(30,40),(30,100),(154,40),(154,100),M3×12+washer/4mm locknut.
The170×120×3 insulating carrier has its inner faceZ−33.6. The PCB uses four
separate 30mm insulating corner posts + 2mm spacers at its unchanged mounting pattern. Sink
and PCB are supported independently; bar screws supply light local TIM pressure.
Deburr, verify flatness, and never bow the PCB to make a gap close.

A controlled H6 ground land/washer/strap bond grounds the assembly; clean
anodizing only at the designated bond and verify lead-compensated continuity.
The full-area0.25mm86/82 source TIM also prevents live underside copper touching
the bar. Inspect protruding solder, TIM holes and edge coverage. TIM is not a
replacement for the source electrical ground path through native copper/vias.

Assembly: inspect/reflow PCB; prepare/drill/tap/deburr cooler and bar; form and
trial-fit devices without loading leads; install mica/bush/nylon fasteners and
TIM; mount cooler angles and PCB posts independently; verify isolation before
soldering formed leads; solder/inspect leads; lightly secure bar; verify ground
bond/board flatness; attach insulated thermocouples; install preserved controller
carrier above; fit ventilated housing/protected feet last. Screwdriver approach
is through the native cutouts from above; side screws are reached before shell
installation. Q401/Q402 remain replaceable without destroying PCB/cooler.
Remove the upper controller/carrier module before servicing the thermal screws.
Cooling assembly estimate248–270g excludes~113g insulating carrier and enclosure.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.

The complete mechanical STEP models component/NPTH holes and cutouts; via holes
are omitted from that mechanical envelope and are present in the native PCB3D
and manufacturing data. Controller components are an explicitly identified
stacking envelope there; native controller sources/models remain unchanged.

ST BD139 uses numeric1B/2C/3E, but its front-view physical order is3E–2C–1B
(left to right with leads down). The front-up flat footprint therefore puts
pin1/base on the right; this differs from reading a vertical footprint
coordinate row without transforming the package view. The final drawing audit
corrected the initial flat pin ordering and rerouted only MOD_BASE/MOD_E.
The original incorrect native draft is retained as a negative CAD fixture.

During dry fit,measure the actual stack before tightening. Adjust the nominal
2mm insulating post spacers with ordinary0.1/0.2mm nylon shim washers,uniformly
at all four corners,so the source TIM seats with light compression and the PCB
remains flat. Do not use H5/H6 screws to pull a tolerance mismatch closed. Form
and solder transistor leads after the insulated tabs and independent supports
are aligned; trim excess lead length last.

The upper controller/carrier reference retains the E5 study transform:180°
rotation,RF-local controller origin(65,20),controller bottomZ53,carrier bottomZ45.
In native RF coordinates the controller envelope isX85..185/Y40..140;its hole
transform is(205−CTRL_X,160−CTRL_Y). The upper170×120×3carrier retains its antenna
notch and separate5mm controller posts. It is an existing study envelope,not a
new controller or RF80 modification. Detailed upper-frame hardware remains
subject to the preserved carrier assembly/incoming check; it is outside the
complete newly dimensioned cooling BOM. The lower protected feet reachZ−51.6
and require an open prototype frame or housing allowance; no drop-in sealed
fit in the historical enclosure study is claimed.
