#include "mini80.h"
#include "power.h"
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
static void seal(mini_config *c){c->crc=mini_crc(c,offsetof(mini_config,crc));}
static double divider(uint8_t r[8]){
 uint32_t c=((uint32_t)(r[5]&0xf0)<<12)|((uint32_t)r[0]<<8)|r[1];
 uint32_t p1=((uint32_t)(r[2]&3)<<16)|((uint32_t)r[3]<<8)|r[4];
 uint32_t p2=((uint32_t)(r[5]&15)<<16)|((uint32_t)r[6]<<8)|r[7];
 return (p1+512+(double)p2/c)/128.;
}
int main(void){
 for(unsigned mask=0;mask<32;mask++){
  rf_sequence s={!!(mask&1),!!(mask&2),50};
  bool prepared=mask&4,authorized=mask&8,key=mask&16;
  unsigned a=rf_step(&s,prepared,authorized,key,42);
  if(!prepared||!authorized){assert(a==RF_KILL);assert(!s.held&&!s.tail);}
  if(a&RF_START)assert(prepared&&authorized&&key);
 }
 rf_sequence s={0};assert(rf_step(&s,true,true,true,0)==RF_START);
 assert(rf_step(&s,true,true,false,10)==ENV_STOP);
 assert(!rf_step(&s,true,true,false,11));assert(rf_step(&s,true,true,false,12)==RF_STOP);
 assert(rf_step(&s,true,true,true,13)==RF_START);
 assert(rf_step(&s,true,false,true,14)==RF_KILL);assert(!s.held&&!s.tail);
 s=(rf_sequence){0};rf_step(&s,true,true,true,0xfffffffeUL);
 assert(rf_step(&s,true,true,false,0xffffffffUL)==ENV_STOP);
 assert(!rf_step(&s,true,true,false,0));assert(rf_step(&s,true,true,false,1)==RF_STOP);
 mini_config c[12];for(int r=0;r<12;r++){mini_default(c+r,r,MINI50);assert(mini_valid(c+r));}
 /* All adjacent role pairs with opposite +/-20ppm residual errors, at the
    end of a twelve-hour session. Include a two-tick RF tail conservatively. */
 for(int first=0;first<5;first++)for(uint32_t t=43200UL*128;t<43260UL*128;t++){
  unsigned on=0;
  for(int r=0;r<5;r++){
   int32_t ppm=r==first?20:-20;
   uint32_t raw=(uint64_t)t*(1000000L+ppm)/1000000UL;
   bool key=false;
   for(unsigned tail=0;tail<=2;tail++)key|=mini_schedule(c+r,raw-tail,true,true,false).key;
   on+=key;
  }
  assert(on<=1);
 }
 for(uint32_t t=0;t<128UL*190;t++){
  int active[2]={0};
  for(int r=0;r<12;r++){
   mini_output o=mini_schedule(c+r,t,true,true,false);
   assert(!mini_schedule(c+r,t,false,true,false).key);assert(!mini_schedule(c+r,t,true,false,false).key);assert(!mini_schedule(c+r,t,true,true,true).prepare);
   if(o.key){assert(o.prepare);assert(t>=60UL*128);if(r<10){uint32_t p=(t-60UL*128)%(60UL*128);assert(p/1536==(unsigned)r%5);active[r/5]++;}}
  }assert(active[0]<=1&&active[1]<=1);
 }
 for(int r=0;r<12;r++){
  unsigned marks=0;for(uint32_t t=60*128;t<120*128;t++)marks+=mini_schedule(c+r,t,true,true,false).key;assert(marks>0);
  c[r].mode=FOXORING;assert(!mini_valid(c+r));c[r].profile=FOX10;seal(c+r);
  if(r>=10){assert(!mini_valid(c+r));c[r].mode=CONTINUOUS;seal(c+r);}
  assert(mini_valid(c+r));assert(mini_schedule(c+r,61*128,true,true,false).prepare);
 }
 mini_default(c,0,MINI50);c->frequency[1]=3531000;seal(c);assert(!mini_valid(c));
 mini_default(c,5,FOX10);c->mode=FOXORING;c->frequency[2]=3580000;seal(c);assert(!mini_valid(c));
 mini_default(c,0,MINI50);
 assert(!mini_schedule(c,(60UL+43200)*128,true,true,false).prepare);
 assert(!mini_schedule(c,59UL*128,true,true,false).key);
 c->delay_s=86400;c->run_s=86400;seal(c);assert(mini_valid(c));
 assert(!mini_schedule(c,172800UL*128,true,true,false).prepare);
 for(int id=0;id<7;id++)for(int w=8;w<=15;w++){uint32_t n=mini_word_ticks(id,w);assert(n>0&&n<12*128);assert(!mini_morse(id,w,0,n-1));assert(mini_morse(id,w,0,n));}
 /* Every single bit corruption is rejected, including CRC bits. */
 mini_default(c,0,MINI50);for(unsigned i=0;i<sizeof *c;i++)for(int bit=0;bit<8;bit++){((uint8_t*)c)[i]^=1<<bit;assert(!mini_valid(c));((uint8_t*)c)[i]^=1<<bit;}
 uint8_t pll[8],ms[8];
 for(uint32_t f=3510000;f<=3600000;f+=250){assert(mini_si5351(f,0,pll,ms));double actual=25000000.*divider(pll)/divider(ms);assert(actual/f>0.99999999&&actual/f<1.00000001);}
 assert(!mini_si5351(3601000,0,pll,ms));
 puts("PASS: RF safety states/tail/wrap, twelve roles, slot exclusion, 12h +/-20ppm drift guards, defaults, CRC bit faults, Morse 8-15WPM, 361 synthesizer frequencies");
}
