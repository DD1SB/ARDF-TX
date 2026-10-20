/* Host-only application/RTC/RF fixtures for the actual C compatibility core.
 * No fixture safety evidence may be used on a target or to energize hardware.
 */
#include "foxpro2.h"
#include "foxpro2_transport.h"
#include <string.h>
static fp_context c;
static fp_receiver rx;
static fp_transport transport;
static uint64_t rtc, monotonic, anchor;
static uint8_t base[10], committed[19];
static uint32_t safety, commits, program_commits, tests, cancellations;
static bool configuration_ok, input_high, sink;
static uint64_t rtc_read(void *u) {(void)u;return rtc;}
static uint64_t mono_read(void *u) {(void)u;return monotonic;}
static bool test_safe(void *u) {(void)u;return safety==0x1ffu;}
static bool config_allowed(void *u) {(void)u;return configuration_ok && !(safety&1u);}
static unsigned seconds(const uint8_t *s) {return s[0]*600u+(s[1]&15u)*60u+(s[2]&63u);}
static void one_second(uint8_t s[10]) {
    unsigned tod=(seconds(s)+1u)%86400u;
    s[0]=(uint8_t)(tod/600u);s[1]=(uint8_t)((s[1]&0xf0u)+(tod/60u)%10u);s[2]=(uint8_t)((s[2]&0xc0u)+tod%60u);
    unsigned slot[4]={60,30,15,12},mode=s[3]>>4,foxes=(s[1]>>4)&7u;
    unsigned period=slot[s[2]>>6];
    if((mode==1 && s[4]==s[5]) || (mode==2 && s[6]==s[7])) period=15;
    if(mode && tod%period==0) s[3]=(uint8_t)((mode<<4)|((s[3]&7u)%foxes+1u));
    if(tod%600u==0) {
        unsigned n=tod/600u;
        if(mode==3 && n==s[9])s[3]=0x41;
        else if(mode==0 && n==s[4])s[3]=0x11;
        else if(mode==1 && n==s[5])s[3]=1;
        else if(mode==0 && n==s[6])s[3]=0x21;
        else if(mode==2 && n==s[7])s[3]=1;
        else if(mode==0 && n==s[8])s[3]=0x31;
    }
}
static bool read_status(void *u,uint8_t out[10]) {
    (void)u;
    uint64_t ticks=rtc/1000000u-anchor/1000000u;
    memcpy(out,base,10);
    while(ticks--)one_second(out);
    return true;
}
static bool import_program(void *u,const uint8_t status[10],uint64_t sync) {
    (void)u;if(!config_allowed(0))return false;
    memcpy(base,status,10);
    rtc=(rtc/86400000000ull)*86400000000ull+sync;
    /* The native RTC is updated atomically, and the native scheduler records
     * this anchor. No compatibility-owned ticking clock exists. */
    anchor=rtc-(sync-(uint64_t)seconds(status)*1000000u);
    ++program_commits;return true;
}
static bool commit_config(void *u,const uint8_t data[19]) {
    (void)u;if(!config_allowed(0))return false;
    memcpy(committed,data,19);++commits;return true;
}
static bool request_test(void *u,uint32_t ms,bool carrier) {
    (void)u;(void)carrier;
    if(safety!=0x1ffu || !ms || ms>FP_MAX_TEST_MS)return false;
    ++tests;return true;
}
static void cancel(void *u) {(void)u;++cancellations;}
static bool rd(void *u) {(void)u;return !(input_high && !sink);}
static void wr(void *u,bool v) {(void)u;sink=!v;}
void bridge_init(void) {
    rtc=43200000000ull;monotonic=0;anchor=rtc;
    uint8_t initial[10]={72,0x50,0,1,255,255,255,255,78,90};memcpy(base,initial,10);
    memset(committed,0,sizeof(committed));committed[0]=0x71;committed[1]=7;
    safety=commits=program_commits=tests=cancellations=0;configuration_ok=true;
    fp_ops ops={rtc_read,mono_read,config_allowed,import_program,read_status,commit_config,request_test,test_safe,cancel,0};
    fp_init(&c,&ops,committed);fp_receiver_reset(&rx);input_high=true;sink=false;
    fp_transport_init(&transport,&c,rd,wr,0);
}
void bridge_advance(uint64_t us) {rtc+=us;monotonic+=us;fp_poll(&c);}
void bridge_set_time(uint64_t us) {rtc=us;}
void bridge_safety(uint32_t bits) {safety=bits;}
void bridge_allow(int allow) {configuration_ok=allow!=0;}
int bridge_command(uint16_t word) {uint16_t response=0;return fp_command(&c,word,&response)?response:-1;}
int bridge_receive(int high) {uint16_t word=0;return fp_receive_tick(&rx,high!=0,&word)?word:-1;}
void bridge_reset(void) {fp_reset_transaction(&c);fp_receiver_reset(&rx);fp_transport_select(&transport,false);}
void bridge_select(int selected) {fp_transport_select(&transport,selected!=0);}
int bridge_tick(int high) {input_high=high!=0;fp_transport_tick(&transport);return sink;}
uint32_t bridge_get(unsigned which) {
    switch(which) {
    case 0:return c.rejected;case 1:return c.unsupported;case 2:return commits;
    case 3:return program_commits;case 4:return tests;case 5:return c.pointer;
    case 6:return c.test_active;case 7:return rx.framing_errors;case 8:return transport.collisions;
    case 9:return cancellations;default:return 0;
    }
}
int bridge_committed(unsigned i) {return i<19?committed[i]:-1;}
