# M5B-E6R2 implemented evaluation controller-compatible RF2M

Native authority: [`hardware/2m/RF2M.kicad_pro`](../hardware/2m/RF2M.kicad_pro).
Starting commit `b48865fed332ced9257559e174f0b6fceaaec096`, local branch
`m5b-e6-unified-heatsink`. E5 native baseline is additionally preserved in
[baseline-E5-native.zip](../hardware/2m/review/M5B-E6R2/baseline-E5-native.zip).
All older review packages, M6-L2 and RF80 are guarded by SHA-256 comparisons.

This revision implements Architecture C in a new native sheet13, routes the
local control/modulator changes, replaces Q401/Q402 footprints with dimensioned
formed-lead underside packages and adds two ordinary rounded routed cutouts.
The150×110mm outline,140×100 mounting pattern,20-pin controller contract, normal
and training RF ports and critical144MHz component poses/traces are retained.
One SK81 assembly now cools all three devices. No PA transistor substitution.
The selected ST PD54008L-E is manufacturer **PowerFLAT5×5**, with G/D/S terminal
regions; the earlier task's PowerSO-10RF designation is not its footprint.

Added U970 TLV7032DGKR, U971 SN74LVC1G00DBVR, U972 SN74LVC2G32DCTR,
U973 SN74LVC1G04DBVR, R970–R986, C970–C973 and TP970–TP976.
U972 uses DCT0.65mm pitch, with the same manufacturer8-pin dual-OR map,
for ordinary two-layer fanout. U970's comparison inputs stay below their7V
absolute limit with the100k/33k dividers even at16.8V input. Normal operating
common-mode and supply remain3.3V. Fault extremes require controlled bench checks.

The pass-current shunt R970 is0.05Ω/1W; Q401 collector becomes VPA_PRE and
feedback still senses VPA downstream. Kelvin measurement clips belong directly
on the resistor terminations. TP970/TP502 are coarse voltage access, not an
accurate Kelvin current measurement. Existing R3090.068Ω remains the protected
whole-rail current monitor; TP971/TP303 provide its two supply-node voltages.

A real nonlinear-fixture issue was corrected: normal SPACE previously drove
Q404 and Q405 through a shared base node, injecting input-clamp current. Q405
now has emergency-only R98510k/R986100k and MOD_COMMAND_OFF_BASE. Q404 alone
uses normal LOCAL_MOD_OFF. Before/after decks and traces are preserved.

Existing hardware thermal/current/ARM/lease/fault protection remains mandatory.
No uncorrelated new PA-temperature trip was added. Native probe/thermocouple
access supports staged first-article evaluation. Contest firmware integration
and spectral qualification are incomplete; this is engineering hardware.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.

The native copper contact graph caught an isolated C409150µF reservoir ground
pad caused by a control route cutting the local pour. That route was opened,
two short0.6mm GND connections/vias were reserved to the bottom plane,then
DRIVER_ON was rerouted. Final DRC and the independent ground contact graph
must both confirm continuity; no exclusion substitutes for this correction.
