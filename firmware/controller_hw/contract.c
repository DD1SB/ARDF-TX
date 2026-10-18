#include "contract.h"
#include <math.h>
#include <assert.h>
void ctl_static_commit(const ctl_io *io, uint16_t value) {
    io->spi_lock(true);
    io->gpio(CTL_LORA_NSS,true);
    io->gpio(CTL_SHIFT_LATCH,false);
    io->shift16(value);
    io->gpio(CTL_SHIFT_LATCH,true);
    io->gpio(CTL_SHIFT_LATCH,false);
    io->spi_lock(false);
}
void ctl_safe_boot(const ctl_io *io) {
    const unsigned low[]={CTL_INIT_OK,CTL_ARM,CTL_MUTE_RELEASE,CTL_PROGRESS,CTL_KEY,
        CTL_SLOT,CTL_AF_PWM,CTL_LEVEL_PWM,CTL_LORA_RESET};
    for(unsigned i=0;i<sizeof(low)/sizeof(low[0]);i++)io->gpio(low[i],false);
    ctl_static_commit(io,0);
    /* INIT_OK remains low. Caller must validate time, pack, modules and settings. */
}
void ctl_progress_commit(const ctl_io *io,bool level){io->gpio(CTL_PROGRESS,level);}
void ctl_audio_init(ctl_audio *s,unsigned tone,uint8_t centre,uint8_t amplitude){
    assert(tone>=300 && tone<=1500);
    assert(amplitude<=centre && (unsigned)centre+amplitude<=255);
    s->phase=0;s->increment=(uint32_t)((4294967296.0*tone)/31250.0+0.5);
    s->centre=centre;s->amplitude=amplitude;
}
uint8_t ctl_audio_sample(ctl_audio *s){
    /* Host reference implementation; target ISR uses a RAM sine LUT instead
       of libm. Do not put sin()/flash calls into an ESP interrupt handler. */
    double v=s->centre+s->amplitude*sin(6.283185307179586*(double)s->phase/4294967296.0);
    s->phase+=s->increment;
    return (uint8_t)lround(v);
}
