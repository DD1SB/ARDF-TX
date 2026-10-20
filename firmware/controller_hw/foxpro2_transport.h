#ifndef ARDF_FOXPRO2_TRANSPORT_H
#define ARDF_FOXPRO2_TRANSPORT_H
#include "foxpro2.h"
typedef struct {
    fp_context *core;
    fp_receiver rx;
    /* GPIO44 reads the inverted MOSFET drain. GPIO43 LOW sinks only when SAFE is qualified; HIGH releases.
     * Bind to direct ESP32 GPIO/IRAM functions, never a push-pull bus wire.
     */
    bool (*read_rx_pin)(void *);
    void (*write_tx_pin)(void *,bool gpio_high);
    void *user;
    bool selected, transmitting, fault;
    uint16_t tx_word;
    uint8_t tx_tick, turnaround;
    uint32_t collisions, boot_ticks;
} fp_transport;
void fp_transport_init(fp_transport *,fp_context *,bool (*)(void *),void (*)(void *,bool),void *);
/* Physical R300/R301 vs R302/R303 population MUST match selected. Software
 * cannot switch the recovery UART wiring. Call only after disabling UART0,
 * configuring GPIO43 HIGH and validating the application startup state.
 */
void fp_transport_select(fp_transport *,bool selected);
/* Timer/GPTimer/RMT adapter invokes at4800Hz, IRAM-safe pin callbacks.
 * Protocol/application callbacks must be deferred to a task on ESP-IDF.
 * fp_transport_tick is a host/reference executor, not an ISR-safe task queue.
 */
void fp_transport_tick(fp_transport *);
/* Exact 80MHz APB count per sampling interval: 16667,16667,16666 repeating.
 * 12 intervals=4 serial bits=266666.666... APB cycles. No accumulated drift.
 */
uint32_t fp_esp32_sample_cycles(uint32_t sample_index);
#endif
