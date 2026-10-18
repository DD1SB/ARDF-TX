# M6-C1 — binding RF interfaces

The machine-readable [36-pin matrix](../hardware/controller/review/M6-C1/RF-interface-contracts.json) is extracted from RF80-V1 and RF2M-E4R1 native electrical manifests, including their SHA-256 identities. Native PCB pads are independently checked against it. The headers are **not interchangeable**.

| Controller connector | RF module connector | Physical part | Cable mate | Mapping |
|---|---|---|---|---|
| J4, 16 pins | RF80-V1 J101 | Würth 61201621621 | 61201623021 female IDC | straight-through 1→1, all 16 pins |
| J5, 20 pins | RF2M-E4R1 J101 | Würth 61202021621 | 61202023021 female IDC | straight-through 1→1, all 20 pins |

Use keyed sockets and strain relief, 28 AWG ribbon, initially ≤150 mm. Pin1 is the rectangular pad, triangle/assembly mark and red cable stripe. The cable is electrically straight-through even where folding changes which side the stripe appears on. Verify every pin with a continuity fixture; never infer numbering from the drawing's viewing direction. Both native RF headers have pin1 at the first row, odd pins on one column, evens on the other. Controller hole size1.10mm gives published standard-JLC range1.02–1.23mm, inside Würth's recommended0.95–1.25mm interval. Mating accessories remain unquoted.

## RF80

| Pin | Signal | Direction at controller |
|---|---|---|
|1|switched V3V3_RF80|power out,150mA budget|
|2/4/16|GND|returns|
|3/5|SCL / SDA|open-drain through U43|
|6|LEASE|out, rising edges every50ms|
|7|ARM|out, rising-edge context capture|
|8|CW_KEY|out, A1A key|
|9/10|PA_REQ / FOX_REQ|out, mutually exclusive|
|11/12|PWR0 / PWR1|out, explicitly ordered bits|
|13|MUTE_N|out, low inhibits|
|14|FAULT_N|in, open-drain; low when disarmed|
|15|PACK4_OK|out, validated4S only|

PWR0/PWR1 **00 Sprint,10 extended,01 full,11 invalid**. The earlier M3A logic audit's compact bit-order wording conflicts with its own equations. The native decode (SEL_EXT=PWR0, SEL_FULL=PWR1) and explicit bring-up table govern; no RF circuit is changed. Both PA and Fox requests high is invalid. FOX_MIN never requests PA and uses the protected2S profile.

All control outputs are3.3V through Ioff buffers and100Ω series resistors, with10k controller pull-downs plus the module's approximately47k pull-downs. Typical high-state load is0.4mA. CMOS input leakage is small compared with these pulls; buffer drive capacity exceeds the load. RF80 FAULT_N uses2.2k to its switched rail and10k host-side pull-down: approximately1.5mA sink when low, and a high level near2.7V. The status is defined low when its rail is off. With a powered controller header but no module, its pull-up can make it high; that is an invalid pre-arm status, **not** proof of a valid module. Presence requires the configured assembly identity and an isolated Si5351 acknowledgement.

Disarm ARM low≥20ms; keep key low and mute asserted, select a valid request/code, configure and read back the source. Establish actual application progress for≥100ms. Disable the branch, leave the source/bus quiet≥20ms, release mute with ARM low, then issue a deliberate ARM edge. Continue progress and wait≥250ms before the first key. Verify acceptance high; any loss while armed mutes/disarms and latches a controller fault. No automatic heartbeat recovery rearm.

## RF2M

| Pin | Signal | Direction at controller |
|---|---|---|
|1|switched V3V3_RF2M|power out,150mA budget|
|2/17/18|GND|returns|
|3/4|I2C_SDA / I2C_SCL|open-drain through U53|
|5|ARM|out, deliberate rising edge|
|6|SLOT|out, scheduled carrier window|
|7|KEY|out, keyed tone selection inside SLOT|
|8|PROGRESS|out, falling edges every50ms|
|9|MUTE_N|out, low inhibits|
|10|PA_RAIL_ADC|in, upstream rail divided120k/10k plus1k|
|11|PATH_TRAIN|out,1 selects independent training|
|12|PROFILE_FULL|out,1 full normal; train requires0|
|13/14|AF_PWM / LEVEL_PWM|out,312.5kHz,0..3.3V|
|15|PREPARE|out, local source/config preparation|
|16|FAULT_N|in, push-pull VALID_ARM through local1k|
|19|MODULE_ID|in, passive resistor to ground|
|20|PA_PREPARE|out, separate converter precharge permission|

The old M5A-R0 interface document is obsolete for identity and rails. Current IDs are **18.2k BOOST2S,39.2k BUCK4S,82k TRAIN_ONLY**. Host pull-up33k gives nominal1.173/1.792/2.353V and better ADC margin than10k. Validate calibrated ADC gain, rail/resistor tolerances and nonoverlapping windows; open/short/unknown values inhibit normal RF. The PA sense is VREG_RAW/13, approximately0.694V for9.02V, not the old13.5V rail. Sense is not an RF-power measurement.

RF2M controls have100Ω host series damping and10k pulls in addition to local100k pulls. FAULT_N is a push-pull arm-accepted signal, not RF80's open drain. Its local1k and host10k pull-down give about3V high. Low during disarmed operation is expected. Do not join the status lines.

Keep ARM/SLOT/KEY low and mute asserted while validating the passive population and pack. Power the selected logic port, begin application-owned PROGRESS and allow≥250ms for the local watchdog startup/reset interval. Native **SRC_ON=PREPARE & SAFE_N & MUTE_N**: release MUTE_N and assert PREPARE with ARM/SLOT/KEY still low before programming the source. **CONV_EN=SRC_ON & PA_PREPARE**: PA_PREPARE separately precharges the normal converter; it is not a prerequisite for source programming. This resolves a misleading earlier draft sequence. For normal mode validate the selected rail and program/read back the synthesizer; training leaves PA_PREPARE0. Disconnect I²C, allow≥10ms quiet and≥100ms genuine progress, then deliberately raise ARM with SLOT/KEY low. Require arm acceptance,≥50ms stabilization and an acceptable PA rail before SLOT. KEY selects reconstructed sine versus matching LEVEL DC; SLOT owns scheduled carrier inhibition. Retuning first clears SLOT/KEY, asserts mute and lowers ARM; source access again requires mute release with ARM low. Training uses PATH_TRAIN1, PROFILE_FULL0 and PA_PREPARE0; no watt-level converter or PA is required.

## Isolation and independent power

Nominal interface supply is3.3V; RF80 requires3.135–3.465V and the connector absolute maximum is3.6V. Neither connector accepts5V logic. Current estimates include pull loads; harness/rail transients must be measured. J301 PA pack currents use the separate fused harness described in the power document.

I2C0 serves RTC0x52 and the **A side** of RF80 TCA9517; I2C1 serves the second TCA9517. Both RF synthesizers may remain0x60. Each B side is powered from its own switched module rail. Bus-enable GPIO-register bits are ANDed in hardware with NOT ARM. Consequently RTC polling never clocks an armed RF80. A stuck branch can be disabled over SPI without using the stuck bus. Keep100kHz initially;4.7k pull-ups at150pF imply approximately0.60µs rise time. Source-side pull-ups already exist on both RF modules. No extra undifferentiated synthesizer bus is introduced.

The controller is the sole source of interface3.3V. A raw RF pack may be connected with controller power absent; Ioff logic/status buffers, unpowered-high-Z bus repeaters and TMUX1511 powered-off analog protection isolate the signals. Analog filter capacitors are **before** TMUX1511. Separately injecting3.3V into a connected RF header is not supported. Backfeed, brownout, source startup and partial-cable fault behavior remain physical qualification gates. Do not hot-plug an armed cable.
