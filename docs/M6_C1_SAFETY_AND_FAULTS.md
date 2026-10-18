# M6-C1 — safe states and fault handling

The hardware starts with no transmitter permission. MCU_EN, INIT_OK and independent pack presence must all be high before U33 enables the static register outputs. The storage latch inside a595 is **not** reset by SRCLR: software must latch an all-zero word before raising INIT_OK. All static outputs and direct ARM, MUTE_RELEASE, KEY, SLOT, PROGRESS, AF/LEVEL controls have real10k pull-downs. GPIO0/3/45/46 are not transmitter enables. INIT_OK uses GPIO14 rather than GPIO40/MTDO, avoiding a pad-JTAG output dependency. GPIO40 carries only optional LoRa RESET; initialize all reused JTAG pins as GPIO before raising INIT_OK. STOP holds MCU_EN low, independently withdrawing hardware permission.

U34/U35 decode a single BAND2 bit into mutually exclusive RF80/RF2M buffer permissions. The unselected bank is high impedance, with module-side pulls inactive. Each bank has its own switched3.3V rail and Ioff-rated buffers. The two I²C repeaters are enabled only while ARM is low. Branch power and bus connectivity are separately controlled. No schedule, RTC, LoRa command or USB operation is allowed to bypass these electrical conditions.

| Condition | Required behavior |
|---|---|
|Reset, bootloader, brownout, STOP|INIT/ARM/mute release low; outputs inhibited; no automatic rearm|
|USB only, absent/unknown/wrong pack|independent pack-present permission absent; software compatibility refuses arming|
|Uninitialized RTC, invalid date/time, failed I²C|inhibit, report cause; no schedule inferred|
|Missing RF board|passive assembly/identity and disarmed-status checks fail; FAULT low alone is not absence detection|
|One branch stuck low|withdraw ARM/mute; disable affected repeater over SPI; RTC/other branch retained where physically possible|
|Both-band request|reject before latching; hardware selects at most one buffer bank|
|Fault or missing local arm acceptance|SLOT/KEY0, mute0, ARM0, local source/converter preparation0; latch software fault|
|Application stops making progress|GPIO39 stops; RF modules' existing independent watchdogs withdraw local permission|
|LoRa absent/lost|valid autonomous RTC operation continues; no automatic remote rearm|
|Cable removal, controller rail loss with RF pack live|module local pulls/watchdog and powered-off isolation withdraw permission; physical decay test remains NOT_RUN|

A hardware timer must not generate the health signal autonomously. Firmware toggles it only after checking clock/configuration, pack/module compatibility, safety status and the control loop's successful progress. The MCU task watchdog may reset a stalled processor, but local RF-board watchdogs remain independent. An ISR or LoRa worker continuing to run is not evidence of application health.

Module-specific sequences are binding in [the RF interface contract](M6_C1_RF_INTERFACE.md). RF80 and RF2M differ in preparation, status polarity/electrical type, I²C behavior and stabilization. The controller does not modify either RF circuit. Fault recovery requires deliberate operator action followed by complete validation and arming; restoring a heartbeat, cable or radio link does not restart transmission.

The host foundation under `firmware/controller_hw/` exercises state arithmetic and native-net mutations. It does not demonstrate real analog reset timing, watchdog latency, Ioff leakage, USB backfeed or RF silence. Those remain staged physical acceptance gates. Boot ROM and USB recovery must be scoped with module raw power present before any operational approval.
