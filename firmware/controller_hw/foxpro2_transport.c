#include "foxpro2_transport.h"
#include <string.h>
uint32_t fp_esp32_sample_cycles(uint32_t i) {return i%3u==2u?16666u:16667u;}
void fp_transport_init(fp_transport *t,fp_context *c,bool (*rd)(void *),void (*wr)(void *,bool),void *u) {
    memset(t,0,sizeof(*t));t->core=c;t->read_rx_pin=rd;t->write_tx_pin=wr;t->user=u;
    wr(u,true);
}
void fp_transport_select(fp_transport *t,bool selected) {
    t->write_tx_pin(t->user,true);t->selected=selected;t->transmitting=false;t->fault=false;
    fp_receiver_reset(&t->rx);fp_reset_transaction(t->core);
}
static bool tx_bit(fp_transport *t) {
    unsigned bit=t->tx_tick/4u;
    if(bit==0u)return false;
    if(bit==17u)return true;
    return ((t->tx_word>>(16u-bit))&1u)!=0;
}
void fp_transport_tick(fp_transport *t) {
    if(!t->selected) {t->write_tx_pin(t->user,true);++t->boot_ticks;return;}
    bool bus_high=!t->read_rx_pin(t->user);
    if(t->transmitting) {
        if(t->turnaround) {
            --t->turnaround;
            if(!t->turnaround)t->write_tx_pin(t->user,false);
            return;
        }
        /* Mid-bit echo identifies a released HIGH pulled LOW by another
         * endpoint. Identical simultaneous frames cannot be distinguished.
         */
        if(t->tx_tick%4u==2u && tx_bit(t) && !bus_high) {
            ++t->collisions;t->fault=true;t->transmitting=false;t->write_tx_pin(t->user,true);
            t->rx.waiting_idle=true;return;
        }
        ++t->tx_tick;
        if(t->tx_tick>=72u) {t->transmitting=false;t->write_tx_pin(t->user,true);fp_receiver_reset(&t->rx);return;}
        t->write_tx_pin(t->user,tx_bit(t));return;
    }
    uint16_t word,response;
    if(fp_receive_tick(&t->rx,bus_high,&word)) {
        if(fp_command(t->core,word,&response)) {
            /* Leave the rest of the request stop bit HIGH. Turnaround is one
             * complete bit after stop-centre sampling:1.25ms after data ends.
             */
            t->tx_word=response;t->tx_tick=0;t->turnaround=4;t->transmitting=true;
            t->write_tx_pin(t->user,true);
        }
    }
}
