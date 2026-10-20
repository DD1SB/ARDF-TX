#include "foxpro2.h"
#include <string.h>

uint16_t fp_encode(uint8_t command, uint8_t data, bool response) {
    command &= 15u;
    uint8_t sum=(uint8_t)((command^(data>>4)^(data&15u)^(response?5u:10u))&15u);
    return (uint16_t)(((uint16_t)sum<<12)|((uint16_t)command<<8)|data);
}
bool fp_decode(uint16_t word, bool response, uint8_t *command, uint8_t *data) {
    uint8_t cmd=(uint8_t)((word>>8)&15u), d=(uint8_t)word;
    if (fp_encode(cmd,d,response)!=word) return false;
    if(command) *command=cmd;
    if(data) *data=d;
    return true;
}
void fp_receiver_reset(fp_receiver *r) { memset(r,0,sizeof(*r)); }
bool fp_receive_tick(fp_receiver *r, bool high, uint16_t *out) {
    if(r->waiting_idle) {
        r->high_ticks=high?(uint8_t)(r->high_ticks+1u):0u;
        if(r->high_ticks>=4u) { r->waiting_idle=false;r->high_ticks=0; }
        return false;
    }
    if(r->phase==0) {
        if(!high) { r->phase=1;r->word=0; }
        return false;
    }
    ++r->phase;
    if(r->phase==2 && high) {r->phase=0;return false;} /* false start */
    if(r->phase>=6 && r->phase<=66 && r->phase%4==2)
        r->word=(uint16_t)((r->word<<1)|(high?1u:0u));
    if(r->phase==70) {
        r->phase=0;
        if(!high) {++r->framing_errors;r->waiting_idle=true;return false;}
        *out=r->word;return true;
    }
    return false;
}
bool fp_foxid_valid(uint8_t v) { return (v&8u)==0; }
bool fp_program_valid(const uint8_t s[10]) {
    unsigned foxes=(s[1]>>4)&7u, mode=(s[3]>>4)&7u,fox=s[3]&7u;
    if(s[0]>143 || (s[1]&15u)>9 || (s[2]&63u)>59) return false;
    if(foxes<1 || foxes>5 || mode>4 || (s[3]&0x88u) || fox<1 || fox>foxes) return false;
    for(unsigned i=4;i<10;i++) if(s[i]>143 && !(i<8 && s[i]==255)) return false;
    /* Disabled test starts require disabled ends. Zero-length tests mean ten
     * 15-second passes; midnight-crossing normal schedules remain supported.
     */
    for(unsigned i=4;i<8;i+=2) if((s[i]==255)!=(s[i+1]==255)) return false;
    if(s[8]==s[9]) return false; /* undefined zero-length contest */
    return true;
}
static uint64_t now(fp_context *c) {return c->ops.rtc_us?c->ops.rtc_us(c->ops.user):0;}
static uint64_t mono(fp_context *c) {return c->ops.monotonic_us?c->ops.monotonic_us(c->ops.user):0;}
static bool allowed(fp_context *c) {return c->ops.configuration_allowed && c->ops.configuration_allowed(c->ops.user);}
static bool config_valid(const uint8_t e[19]) {
    return fp_foxid_valid(e[0]) && !(e[1]&0xf0u) && e[2]<=240u;
}
void fp_init(fp_context *c,const fp_ops *ops,const uint8_t e[19]) {
    memset(c,0,sizeof(*c));c->ops=*ops;
    if(e && config_valid(e)) memcpy(c->eeprom,e,19);
    else {c->eeprom[0]=0x71;c->eeprom[1]=7;}
    memcpy(c->staged_eeprom,c->eeprom,19);
}
void fp_reset_transaction(fp_context *c) {
    c->status_mask=0;c->eeprom_mask=0;c->dirty=false;c->snapshot_valid=false;c->pointer=0;
    memcpy(c->staged_eeprom,c->eeprom,19);
    if(c->ops.cancel_test)c->ops.cancel_test(c->ops.user);
    c->test_active=false;c->test_register=0;
}
void fp_poll(fp_context *c) {
    uint64_t t=now(c);
    if(t<c->last_us || (c->status_mask && t-c->last_us>FP_TRANSACTION_TIMEOUT_US))
        fp_reset_transaction(c);
    if(c->snapshot_valid && (t<c->snapshot_us || t-c->snapshot_us>900000u)) c->snapshot_valid=false;
    uint64_t m=mono(c);
    if(c->test_active && (m>=c->test_end_us || m<c->test_start_us || !c->ops.test_safe || !c->ops.test_safe(c->ops.user))) {
        if(c->ops.cancel_test)c->ops.cancel_test(c->ops.user);
        c->test_active=false;c->test_register=0;
    }
    /* One bounded commit after quiet, never one flash write per serial byte.
     * Partial CW-ID transfers are discarded; no data is persisted on timeout.
     */
    if(c->dirty && t>=c->dirty_us && t-c->dirty_us>=500000u) {
        if(c->persisted && m>=c->last_persist_us && m-c->last_persist_us<10000000u) return;
        bool complete=(c->eeprom_mask==1u || c->eeprom_mask==0x7fffeu || c->eeprom_mask==0x7ffffu);
        if(complete && allowed(c) && config_valid(c->staged_eeprom) && c->ops.configuration &&
           c->ops.configuration(c->ops.user,c->staged_eeprom)) {
            memcpy(c->eeprom,c->staged_eeprom,19);++c->accepted;c->persisted=true;c->last_persist_us=m;
        } else ++c->rejected;
        c->dirty=false;c->eeprom_mask=0;memcpy(c->staged_eeprom,c->eeprom,19);
    }
}
bool fp_command(fp_context *c,uint16_t word,uint16_t *out) {
    uint8_t cmd,data;uint64_t t=now(c);
    fp_poll(c);
    if(!fp_decode(word,false,&cmd,&data)) {++c->rejected;return false;}
    if(c->last_us && (t<c->last_us || t-c->last_us>FP_TRANSACTION_TIMEOUT_US)) {
        c->snapshot_valid=false;c->status_mask=0;
    }
    c->last_us=t;
    if(cmd<10u) {
        if(!allowed(c)) {++c->rejected;return false;}
        if(cmd==0) {
            c->status_mask=0;c->load_us=t;
            c->test_active=false;c->test_register=0;
            if(c->ops.cancel_test)c->ops.cancel_test(c->ops.user);
        }
        /* In-order, complete loads only; an interrupted load cannot patch the
         * live schedule a byte at a time or authorize a rearm.
         */
        if(c->status_mask != ((1u<<cmd)-1u)) {c->status_mask=0;++c->rejected;return false;}
        c->staged_status[cmd]=data;c->status_mask|=(uint16_t)(1u<<cmd);
        if(cmd==9) {
            uint64_t tod=((uint64_t)c->staged_status[0]*600u+(c->staged_status[1]&15u)*60u+(c->staged_status[2]&63u))*1000000u;
            if(fp_program_valid(c->staged_status) && c->ops.program && t>=c->load_us &&
               c->ops.program(c->ops.user,c->staged_status,(tod+t-c->load_us)%86400000000ull)) {
                c->loaded=true;c->snapshot_valid=false;++c->accepted;
            } else ++c->rejected;
            c->status_mask=0;
        }
        return false;
    }
    if(cmd==10u) {
        if(data==0) {if(c->ops.cancel_test)c->ops.cancel_test(c->ops.user);c->test_active=false;c->test_register=0;return false;}
        uint32_t ms=data<16u?(uint32_t)data*100u:(uint32_t)(data-15u)*15000u;
        if(ms>FP_MAX_TEST_MS || !c->ops.monotonic_us || !c->ops.test_safe || !c->ops.test_safe(c->ops.user) || !c->ops.test || !c->ops.test(c->ops.user,ms,data<16u)) {++c->rejected;return false;}
        c->test_active=true;c->test_register=data;c->test_start_us=mono(c);c->test_end_us=c->test_start_us+(uint64_t)ms*1000u;++c->accepted;return false;
    }
    if(cmd==11u) {
        if(!allowed(c) || !fp_foxid_valid(data)) {++c->rejected;return false;}
        c->staged_eeprom[0]=data;c->eeprom_mask|=1u;c->dirty=true;c->dirty_us=t;return false;
    }
    if(cmd==12u) {++c->unsupported;return false;} /* oscillator output not emulated */
    if(cmd==13u) {
        if(data==1u) {
            /* Begin a fresh CW transaction without losing a staged FoxID. */
            memcpy(c->staged_eeprom+1,c->eeprom+1,18);c->eeprom_mask&=1u;
            c->dirty=c->eeprom_mask!=0u;
        }
        c->pointer=data;return false;
    }
    if(cmd==14u) {
        /* Legacy CW-ID lives at1..18. Do not expose adjacent RAM or wrap to0. */
        if(c->pointer<1 || c->pointer>=FP_EEPROM_SIZE || !allowed(c)) {++c->rejected;return false;}
        if((c->pointer==1 && (data&0xf0u)) || (c->pointer==2 && data>240u)) {++c->rejected;return false;}
        c->staged_eeprom[c->pointer]=data;c->eeprom_mask|=1u<<c->pointer;++c->pointer;c->dirty=true;c->dirty_us=t;return false;
    }
    if(cmd==15u) {
        uint8_t value=0;
        if(data<10u) {
            if(data==0 || !c->snapshot_valid || c->snapshot_next!=data) {
                if(!c->ops.status || !c->ops.status(c->ops.user,c->snapshot)) {++c->rejected;return false;}
                c->snapshot_us=t;c->snapshot_valid=true;
            }
            value=c->snapshot[data];c->snapshot_next=(uint8_t)(data+1u);
        } else if(data==10u) value=c->test_active?c->test_register:0;
        else if(data==11u) {value=c->staged_eeprom[0];c->pointer=1;}
        /* 0x15 advertises the protocol generation/feature floor, NOT FJTX
         * provenance or a promise of its unsafe oscillator/test facilities.
         * Native diagnostics identify ARDF-TX M6-L2 explicitly.
         */
        else if(data==12u) value=0x15;
        else if(data==13u) value=(uint8_t)(((t%1000000u)*30u)/1000000u);
        else if(data==14u) {
            if(c->pointer<1 || c->pointer>=FP_EEPROM_SIZE) {++c->rejected;return false;}
            value=c->staged_eeprom[c->pointer++];
        } else {++c->unsupported;return false;}
        *out=fp_encode(data,value,true);return true;
    }
    ++c->unsupported;return false;
}
