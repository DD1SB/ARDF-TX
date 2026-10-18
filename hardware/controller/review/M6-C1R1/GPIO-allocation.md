# M6-C1 complete GPIO allocation

| GPIO | Signal |
|---:|---|
|0|BOOT|
|1|BAT_ADC|
|2|PACK_ID_ADC|
|3|STRAP_RESERVED|
|4|MODULE_ID_ADC|
|5|PA_RAIL_ADC|
|6|AF_PWM|
|7|LEVEL_PWM|
|8|RTC80_SDA|
|9|RTC80_SCL|
|10|LORA_NSS|
|11|SPI_MOSI|
|12|SPI_SCK|
|13|SPI_MISO|
|14|INIT_OK|
|15|LORA_BUSY|
|16|LORA_DIO1|
|17|RF2M_SDA|
|18|RF2M_SCL|
|19|USB_DM|
|20|USB_DP|
|21|RF2M_FAULT|
|35|RF80_FAULT|
|36|START_N|
|37|USB_VBUS_N|
|38|SHIFT_LATCH|
|39|PROGRESS|
|40|LORA_RESET|
|41|ARM|
|42|MUTE_RELEASE|
|43|UART_TX|
|44|UART_RX|
|45|STRAP_RESERVED|
|46|STRAP_RESERVED|
|47|KEY|
|48|SLOT|

Static595 register bits (not extra MCU GPIO):

| Bit | Signal |
|---:|---|
|0|PA_REQ|
|1|FOX_REQ|
|2|PWR0|
|3|PWR1|
|4|PACK4_SOFT|
|5|PATH_TRAIN|
|6|PROFILE_FULL|
|7|PREPARE|
|8|PA_PREPARE|
|9|POWER80|
|10|POWER2M|
|11|BUS80|
|12|BUS2M|
|13|LED_ARM|
|14|LED_FAULT|
|15|BAND2|

I2C0=GPIO8/9, RTC and isolated RF80; I2C1=GPIO17/18, isolated RF2M. SPI=GPIO10–13 with independent595 latch38. LEDC0/1 share timer0 onGPIO6/7; use separate GPTimer/RMT resources for DDS sampling and slot/Morse edges. USB19/20 and UART43/44 are reserved. GPIO14 is the non-JTAG INIT permission; initialize JTAG-reused39–42 as safe GPIO before granting it. GPIO3/45/46 remain unused straps. Physical timing and operation NOT_RUN.
