AVR_PREFIX ?= avr-
CC := $(AVR_PREFIX)gcc
OBJCOPY := $(AVR_PREFIX)objcopy
SIZE := $(AVR_PREFIX)size
DFP ?=
PACKFLAGS = $(if $(DFP),-B$(DFP)/gcc/dev/attiny1616/ -I$(DFP)/include)
CFLAGS = -mmcu=attiny1616 -DF_CPU=5000000UL -Os -std=gnu11 -Wall -Wextra -Werror -ffunction-sections -fdata-sections $(PACKFLAGS)
LDFLAGS = -Wl,--gc-sections,-Map=build/mini80.map
.PHONY: all test clean
all: build/mini80.hex
build:
	mkdir -p build
build/mini80.elf: main.c core.c power.c mini80.h power.h | build
	$(CC) $(CFLAGS) main.c core.c power.c $(LDFLAGS) -o $@
	$(SIZE) $@
build/mini80.hex: build/mini80.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@
test: | build
	gcc -std=c11 -Wall -Wextra -Werror core.c power.c test_core.c -o build/test_core
	./build/test_core
clean:
	$(RM) -r build
