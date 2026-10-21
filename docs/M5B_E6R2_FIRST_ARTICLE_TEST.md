# E6R2 first-article assembly and staged bench plan

This is a future procedure, not authorization or a record of performed tests.
Gate2 concerns bare boards; Gate3 requires a correctly assembled, inhibited,
current-limited bench setup; Gate4 needs measured RF/thermal qualification.

1. Check incoming PCB size,holes,cutouts,copper and actual TO-220/TO-126/body/hole
   dimensions against the drawing. Inspect 98open source vias and underside
   flatness. Use the complete0.12mm top stencil,print inspection and recorded
   reflow profile. Inspect the ordinary unfilled CLOCK_OFF escape via near U601
   for aperture overlap/wicking; hand retouch if needed,without premium via
   filling. Source windows total6.765mm²; solder transfer/wicking/coverage
   are unknown until inspected. X-ray is a useful first-article hidden-joint
   method, not a prerequisite to ordering bare boards. Reject serious voids,
   inadequate wetting or protrusions that prevent flat TIM contact.
2. Form leads with a jig,trial-fit without stress,verify tab/mica/bush/washer
   coverage and screw engagement. Dry-fit cooler,bar,posts and brackets before
   tightening. Independently support sink weight; check PCB flatness at every
   step. Install correct rated TIM,not solder mask as insulation.
3. Before soldering formed leads,check each live tab to heatsink isolation
   (>20MΩ on an ordinary DMM) and mutual tab isolation. After soldering,normal
   circuit resistors/semiconductors create paths to ground: do not demand an
   impossible20MΩ at assembled VPA or apply a high-voltage megger to electronics.
   Isolate the device for any repeated insulator test. Verify intended source/
   heatsink ground bonding with lead compensation; inspect both fastener systems.
4. Attach electrically insulated fine thermocouples at PA source-adjacent
   (97,60.5),Q401 case(116,36),Q402 case(133,31),and sink(105,75),plus ambient.
   Verify bead attachment and thermal lag. TH801 remains attached to Q401 per
   native protection architecture. A source/NTC probe is not a Tj sensor.
5. With power absent,test continuity,exclusive supply population,module ID,
   controller contract and no tab short. With current-limited supplies and PA
   inhibited,verify rails,default-off,ARM/lease/progress,fault latch,thermal
   faults,current-trip scale and emergency override before permitting RF.
6. Verify synthesizer/reference and buffer while inhibited; test U970 threshold
   behavior and missing/shorted readiness signals. Use AF zero,KEY pulses and
   differential probes to verify U402 selection,Q404/Q405 separation,DRIVER_ON,
   CLOCK_OFF and PA gate/drain sequencing. Confirm converter stays prepared
   through normal SPACE but turns off on emergency. Measure current/voltage
   startup overshoot,MMIC supply discharge,SPACE residuals and load removal.
7. Connect a suitable144MHz50Ω dummy load with adequate continuous/PEP rating,
   calibrated directional power measurement,attenuation,spectrum measurement
   and oscilloscope envelope access. Protect instrument inputs. Keep all scope
   ground clips at GND; use differential high-side shunt measurements,never an
   ammeter across TP970/TP502 or TP971/TP303. Kelvin clip R970 directly; existing
   R309 monitors whole regulated rail. Start at the lowest valid power with
   ~1s transmissions,then5/10s only when preceding waveforms/temperatures agree.
8. Measure carrier,PEP,AM depth,envelope edge quality,frequency settling,
   harmonics/spurs,SPACE and off-slot leakage,normal/training isolation and
   actual DC power. Increase to0.25/0.5/1W ERP-equivalent conducted settings
   only with a documented antenna/feeder assumption and clean PEP reserve.
   Check hot pass gain/headroom; BF20 sensitivity is not a guaranteed corner.
9. At each level record Q401/Q402/source-region/sink/ambient traces and actual
   heat ledger. Correlate junction-related models conservatively; investigate
   rapid proxy/model disagreement rather than asserting a universal source
   temperature guarantees125°C Tj. Verify shutdown timing at bounded energy.
10. Test actual Classic60/240 and Sprint12/48 cycles through stable repetition.
    Continuous MO follows only after short tests establish margin.40°C and
    restricted-orientation tests are later controlled steps,not an initial
    full-power endurance run. Q40159.51°C model is close to60°C: use55°C as an
    initial operator stop,then engineering review before any longer exposure.
    Initially stop Q402 at70°C before its80°C criterion. Retain Q501110°C target/
    125°C ceiling; do not substitute a heatsink average for junction assessment.

Stop immediately for abnormal current/heating,instability/oscillation,modulation
overshoot,protection failure,loss of isolation/contact,smoke/odor or uncorrelated
sensor behavior. Reduce duty/power and investigate. Do not run to destruction
or prolong an unsafe test to get steady-state data. Test no-tone carriers only
for bounded service durations; existing30s controller service limit is an upper
permission bound,not a requirement to expose an unqualified PA for30s.

Before operational release,complete real RF/AM/spectrum,power sequencing,
thermal trips/source-joint correlation,continuous full-profile MO,40°C/orientation,
restricted airflow and accessible-surface/environmental tests. Use shaded,
ventilated protected feet/base; keep fins clear of leaves/grass. No fire-safety
claim follows solely from simulated temperatures.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.
