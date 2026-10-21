# E6R2 RF/electrical preservation

The independent checker reads exported native netlist, manifest, native pads,
tracks/vias, cutouts and mechanical source dimensions. It checks all352 physical
footprint instances,51 manufacturer-critical maps, all20 controller pins,
4,096 high-level enable combinations,36 safety scenarios and16 new local-keying
truth-table rows. Negative cases mutate real pin dictionaries, native pads,
component values and mechanical dimensions; actual counts are in verification.json.
The preserved source-joint native mutation suite and standard DFM mutations are
rerun separately, not inferred from historical PASS strings.

Q501 remains(92,55),0°. Gate/drain/source land coordinates, source mask,
five paste windows and98via dimensions/positions/tenting are checked against
starting native E5. All protected RF signal tracks/vias and matching/filter
component pad poses/sizes/nets are equal. No new microstrip length, width or
matching value is introduced. Retain E5's standard1.6mmFR4/1oz matching-geometry
model and its physical tuning requirements. New cutouts modify the remote
modulator ground boundary; retain local source copper and RF-line ground
keepouts. Source stability/AM/spectrum must still be measured on the assembly.
The logic cluster was moved south of the retained B.Cu no-track RF reference
band; no relaxation of the keepout was used to finish routing.

NORMAL BUCK4S, NORMAL BOOST2S and TRAIN_ONLY population BOMs and assembly
positions derive from the same native board. Supply-selection exclusivity,
hardware default-off,ARM/lease,fault latch,overcurrent,thermal interlock and
safe retuning remain present. Keying never changes the20-pin contract.
No controller or RF80 changes are permitted by the preserved-start hash guard.

Native ERC,DRC/parity,independent DFM,source process and simulation reports are
revision-specific in the review package. Inherited courtyard warnings are
explicitly retained and dispositioned; they are not hidden by exclusions.
Ngspice analog results are envelope/load-model results, not144MHz RF validation.
Clean1W ERP/5.135W connector PEP reserve,70–80% AM,off-slot silence,training-port
protection,harmonics/spurs,frequency settling and device stability remain
first-article RF measurements.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.

The ground-contact audit independently unions actual pad/track/via copper and
each filled-zone island. It must report one component,including the C409bulk
driver-reservoir ground. Twelve native high-current paths are checked separately,
with the new VPA_PRE→R970→VPA split; thin long sense branches cannot substitute
for a main-current route. These are copper-path calculations,not temperature
or current-rating measurements.
