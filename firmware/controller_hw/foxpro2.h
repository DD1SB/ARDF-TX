/* Independently written FoxPro2 compatibility core, C11, no target dependencies.
 * Original protocol: Nick Roethe DF1FO, FJTX/FOXPRO2 (not MIT relicensed).
 * Nothing in this API grants permission to arm or directly controls an RF pin.
 */
#ifndef ARDF_FOXPRO2_H
#define ARDF_FOXPRO2_H
#include <stdbool.h>
#include <stdint.h>
#define FP_BAUD 1200u
#define FP_EEPROM_SIZE 19u
#define FP_TRANSACTION_TIMEOUT_US 1000000u
#define FP_MAX_TEST_MS 30000u
typedef struct {
    /* The application's existing RTC is the sole wall-time authority. */
    uint64_t (*rtc_us)(void *user);
    uint64_t (*monotonic_us)(void *user);
    bool (*configuration_allowed)(void *user);
    /* Atomically validate/import schedule and optional wall-time correction.
     * sync_rtc_us is time-of-day at completion of the load, not an arm request.
     * On false, neither configuration nor RTC may be changed.
     */
    bool (*program)(void *user, const uint8_t status[10], uint64_t sync_rtc_us);
    /* Produce a coherent ten-byte legacy view of the NATIVE scheduler/RTC.
     * Never fabricate an active RF state from these compatibility bytes.
     */
    bool (*status)(void *user, uint8_t status[10]);
    bool (*configuration)(void *user, const uint8_t eeprom[19]);
    /* Calls the existing arm/rearm/interlock controller. true means actually
     * accepted, not merely queued. Must honor module/pack/thermal/PA/antenna/
     * profile/commissioning evidence and a monotonic bounded deadline.
     */
    bool (*test)(void *user, uint32_t duration_ms, bool carrier);
    bool (*test_safe)(void *user);
    void (*cancel_test)(void *user);
    void *user;
} fp_ops;
typedef struct {
    fp_ops ops;
    uint8_t eeprom[19], staged_eeprom[19], staged_status[10], snapshot[10];
    uint16_t pointer, status_mask;
    uint32_t eeprom_mask;
    uint64_t last_us, load_us, snapshot_us, dirty_us;
    bool dirty, snapshot_valid, loaded, test_active;
    uint64_t test_end_us, test_start_us, last_persist_us;
    bool persisted;
    uint8_t snapshot_next, test_register;
    uint32_t rejected, unsupported, accepted;
} fp_context;
typedef struct {
    uint16_t word;
    uint8_t phase, high_ticks;
    bool waiting_idle;
    uint32_t framing_errors;
} fp_receiver;
uint16_t fp_encode(uint8_t command, uint8_t data, bool response);
bool fp_decode(uint16_t word, bool response, uint8_t *command, uint8_t *data);
void fp_receiver_reset(fp_receiver *r);
/* Call from a hardware 4800Hz sampler, no I2C or ordinary 8N1 UART involved. */
bool fp_receive_tick(fp_receiver *r, bool bus_high, uint16_t *word);
void fp_init(fp_context *c, const fp_ops *ops, const uint8_t eeprom[19]);
void fp_reset_transaction(fp_context *c);
void fp_poll(fp_context *c);
bool fp_program_valid(const uint8_t s[10]);
bool fp_foxid_valid(uint8_t value);
/* Return true only when a response frame exists. Writes have no legacy ACK.
 * Inspect rejected/unsupported and actual readback; silence is not success.
 */
bool fp_command(fp_context *c, uint16_t command_frame, uint16_t *response);
#endif
