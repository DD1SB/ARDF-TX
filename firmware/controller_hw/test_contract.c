#include "contract.h"
#include <assert.h>
static bool states[49],locked;
static uint16_t shifted;
static void gpio(unsigned p,bool v){assert(p<49);states[p]=v;}
static void lock(bool v){locked=v;}
static void shift(uint16_t v){assert(locked);assert(states[CTL_LORA_NSS]);assert(!states[CTL_SHIFT_LATCH]);shifted=v;}
int main(void){
    ctl_io io={gpio,lock,shift};ctl_safe_boot(&io);
    assert(!states[CTL_INIT_OK]&&!states[CTL_ARM]&&!states[CTL_MUTE_RELEASE]);
    assert(shifted==0&&!locked);ctl_static_commit(&io,0x1357);assert(shifted==0x1357&&!locked);
    ctl_audio a;ctl_audio_init(&a,800,110,82);unsigned lo=255,hi=0;
    for(unsigned i=0;i<31250;i++){unsigned v=ctl_audio_sample(&a);if(v<lo)lo=v;if(v>hi)hi=v;}
    assert(lo==28&&hi==192);return 0;
}
