#ifndef MINI80_POWER_H
#define MINI80_POWER_H
#include <stdint.h>
#include <stdbool.h>
enum {RF_START=1,ENV_STOP=2,RF_STOP=4,RF_KILL=8};
typedef struct {bool held,tail;uint32_t until;} rf_sequence;
/* Two 128Hz ticks allow envelope decay. Safety inhibit overrides the tail. */
uint8_t rf_step(rf_sequence *,bool prepared,bool authorized,bool key,uint32_t now);
#endif
