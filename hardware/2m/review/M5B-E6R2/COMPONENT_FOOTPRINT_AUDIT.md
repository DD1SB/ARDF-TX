# E6R2 manufacturer/package audit

The exported netlist,352 actual native footprints and51 critical pin maps are
checked by `tools/m5b_e6r2_verify.py`. `pinout-audit.json` lists the complete
maps. These checks do not establish soldering,RF or thermal performance.

| Device | Manufacturer source / native interpretation |
|---|---|
| Q501 ST PD54008L-E | [ST datasheet](https://www.st.com/resource/en/datasheet/pd54008l-e.pdf): PowerFLAT5×5;Gleft,Dright,Scentral/GND. Exact E5 land/mask/paste/98vias retained; no PowerSO-10 substitute. |
| Q401 ST D45H11 | [ST Rev5](https://www.st.com/resource/en/datasheet/d45h11.pdf): TO-2201B2C3E,collector tab; front-up row1–2–3. Tab is VPA_PRE through added50mΩ shunt. |
| Q402 ST BD139 | [ST Rev5](https://www.st.com/resource/en/datasheet/bd139.pdf): SOT-32 numeric1B2C3E; front-view physical row3E–2C–1B. Final flat pin1 is on the right. Do not read a rear-view/vertical coordinate row as front-up. |
| U970 TLV7032DGKR | [TI family](https://www.ti.com/lit/ds/symlink/tlv7032.pdf): DGK8,VSSOP3×3/0.65pitch;1OUTA2INA−3INA+4GND5INB+6INB−7OUTB8VCC. |
| U971 SN74LVC1G00DBVR | [TI](https://www.ti.com/lit/ds/symlink/sn74lvc1g00.pdf): DBV5;1A2B3GND4Y5VCC. |
| U972 SN74LVC2G32DCTR | [TI](https://www.ti.com/lit/ds/symlink/sn74lvc2g32.pdf): DCT8SSOP2.95×2.8/0.65pitch;1/2→7,5/6→3,GND4,VCC8. DCT chosen for ordinary fanout. |
| U973 SN74LVC1G04DBVR | [TI](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf): DBV5;NC1,A2,GND3,Y4,VCC5. |
| R970 WSL2512R0500FEA | [Vishay WSL](https://www.vishay.com/docs/30100/wsl.pdf):50mΩ,1%,2512/1W;use Kelvin clips directly on terminations. |
| C970–C973 GRM188R71H104KA93D | [Murata GRM family](https://www.murata.com/en-global/products/capacitor/ceramiccapacitor):0603,100nF,X7R,50V. |
| R971–R986 | Yageo RT0603 precision/divider/pull resistors;values and exact MPNs in population BOMs. |

The corrected BD139 orientation was cross-checked against ST's manufacturer-
authored mechanical drawing0016114/B (2001) as well as the Rev5front3–2–1
package illustration. The mirrored initial native draft is retained in
`development/pre-flat-pin-correction/` and must fail the new physical-order
negative test. It is explicitly rejected,not a manufacturing option. No original
manufacturer PDF is republished under MIT.

D45H11 andBD139 maximum package envelopes,lead length/bend allowances,hole and
tab dimensions are in `mechanical-source.json`. New formed footprints retain
1.3mm drills/2mm lands; their opposite front-view order is deliberate. Incoming
marking,diode identification and actual dimensions must be checked before forming.

U970 dividers limit a16.8V fault input to~4.17V,below its7V absolute input bound,
although above3.3V normal common-mode. Readiness is not an overvoltage safety
substitute: original independent voltage/current/fault inhibition remains in
series. Typical comparator-delay assumptions are not guaranteed timing limits.

The local small-IC footprints retain standard manufacturer-compatible copper;
legend strokes were moved to fabrication layers where needed. KiCad standard
library models are referenced; new power/cooling STEP models are project-
generated dimensional envelopes,not falsely labeled manufacturer STEP data.
