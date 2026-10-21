#ifndef MINI80_H
#define MINI80_H
#include <stdint.h>
#include <stdbool.h>
#define MINI_HZ 128UL
#define MINI_PREP_TICKS 64UL /* 500ms source/rail preparation allowance */
#define MINI_MAGIC 0x314d3830UL
enum {SPRINT=0,FOXORING=1,CONTINUOUS=2};
enum {MINI50=0,FOX10=1};
typedef struct __attribute__((packed)) {
 uint32_t magic;
 uint8_t version,role,mode,profile,slow_wpm,fast_wpm,identifier;
 uint32_t frequency[4];
 uint32_t delay_s,run_s;
 int32_t carrier_ppb;
 int16_t timing_ppm;
 uint16_t battery_scale; /* calibration: nominal 4500mV full ADC scale */
 uint16_t crc;
} mini_config;
typedef struct {bool prepare,key;uint32_t frequency;uint8_t identifier,wpm;} mini_output;
uint16_t mini_crc(const void *,uint16_t);
bool mini_valid(const mini_config *);
void mini_default(mini_config *,uint8_t role,uint8_t profile);
mini_output mini_schedule(const mini_config *,uint32_t tick,bool armed,bool synced,bool fault);
uint32_t mini_word_ticks(uint8_t id,uint8_t wpm);
bool mini_morse(uint8_t id,uint8_t wpm,uint32_t phase,uint32_t remaining);
/* Si5351 PLLA fixed 800MHz, integer/fractional MS0 with R divider=1. */
bool mini_si5351(uint32_t hz,int32_t ppb,uint8_t pll[8],uint8_t ms[8]);
#endif
