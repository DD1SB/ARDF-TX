# RF2M — M5A-R1 electrical evaluation candidate

**NOT RELEASED. No layout, purchasing, fabrication, assembly or RF operation.**

The existing [editable project](RF2M.kicad_pro) now contains the PD54008L-E/PHA-1+ evaluation candidate, revised true-AM supply, unchanged hardware fail-off and independent training branch. Read the [R1 decision](../../docs/M5A_R1_REVIEW_DECISION.md) and [schematic PDF](review/M5A-R1/RF2M.pdf).

**Coupon layout is NO-GO:** the original ST matching drawings and final-device physical landing remain OPEN. The schematic deliberately exposes those gaps. ERC and digital tests do not qualify RF, thermal, analog startup or package geometry.

R0 remains at Git tag `m5a-r0` / commit `ea671c1`, in [native archive](archive/M5A-R0/) and [historical review package](review/M5A-R0/). R0 documents describe that revision; the active native project is R1. Use the R1 tools in [reproduction instructions](review/M5A-R1/README.md); running R0 generators against the current tree would overwrite R1.

[Variant BOM](review/M5A-R1/RF2M_BOM.csv) covers BOOST2S, BUCK4S and TRAIN_ONLY. Only one converter population is fitted. Normal MODULE_ID values are 12.1 kΩ / 27.4 kΩ; training remains 47 kΩ. Training omits normal power components and fits its documented health/input terminations. Calibration, exact parts and physical variant operation remain unqualified.

RF80/M4A and accepted architecture files are unchanged. No additional MCU or primary PCB is introduced. Local symbols retain the supplied [KiCad library license/design exception](LICENSE-KICAD-SYMBOLS.md). ST references are attributed in the [source audit](../../docs/M5A_R1_ST_REFERENCE_AUDIT.md); unread proprietary artwork is not copied or represented as inspected.
