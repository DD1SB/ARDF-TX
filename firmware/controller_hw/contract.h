/* Hardware abstraction foundation. No contest scheduler or radio driver. */
#pragma once
#include <stdint.h>
#include <stdbool.h>
#include "pins.h"
typedef struct {
    void (*gpio)(unsigned pin, bool value);
    void (*spi_lock)(bool acquire);
    void (*shift16)(uint16_t value); /* MSB first: U31 bits15..8, U30 bits7..0 */
} ctl_io;
void ctl_safe_boot(const ctl_io *io);
void ctl_static_commit(const ctl_io *io, uint16_t value);
/* Call only after meaningful application progress, never a free-running ISR. */
void ctl_progress_commit(const ctl_io *io, bool level);
/* 31.25k sample/s, timer0 PWM312.5kHz/8bits, phase continuous. */
typedef struct {uint32_t phase, increment;uint8_t centre, amplitude;} ctl_audio;
uint8_t ctl_audio_sample(ctl_audio *s);
void ctl_audio_init(ctl_audio *s, unsigned tone_hz, uint8_t centre, uint8_t amplitude);
