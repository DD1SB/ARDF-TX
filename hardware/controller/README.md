# ARDF-TX universal controller — M6-C1 engineering candidate

Native KiCad10 project: `CTRL.kicad_pro`, root `CTRL.kicad_sch`, `CTRL.kicad_pcb` and local ARDF_CTL libraries. The controller supports the actual RF80-V1 and RF2M-M5B-E4R1 connector contracts. The RF boards themselves are unchanged.

Current engineering findings, assembly populations, checks and physical qualification gates are in `review/M6-C1/`. No acceptance tag, manufacturing release or hardware qualification is implied. In particular, the optional Silicontra radio population remains on sourcing/package HOLD and is DNP for base operation.

See the `docs/M6_C1_*` documents and `firmware/controller_hw/` host contract foundation. Firmware production implementation, physical power/USB/timing/RTC tests, RF immunity and transmitter qualification are outside this CAD milestone.
