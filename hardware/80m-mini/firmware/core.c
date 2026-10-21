#include "mini80.h"
#include <stddef.h>
#include <string.h>
static const char *const ids[]={"MOE","MOI","MOS","MOH","MO5","S","MO"};
static const char *code(char c){
 switch(c){case 'M':return "--";case 'O':return "---";case 'E':return ".";case 'I':return "..";case 'S':return "...";case 'H':return "....";case '5':return ".....";default:return "";}
}
uint16_t mini_crc(const void *v,uint16_t n){
 const uint8_t *p=v;uint16_t crc=0xffff;
 while(n--){crc^=(uint16_t)*p++<<8;for(uint8_t i=0;i<8;i++)crc=(crc&0x8000)?(crc<<1)^0x1021:crc<<1;}return crc;
}
bool mini_valid(const mini_config *c){
 if(c->magic!=MINI_MAGIC||c->version!=1||c->role>11||c->mode>CONTINUOUS||c->profile>FOX10||c->identifier>6)return false;
 if(c->slow_wpm<8||c->slow_wpm>15||c->fast_wpm<8||c->fast_wpm>15)return false;
 if(c->mode==FOXORING&&(c->profile!=FOX10||c->role>=10||c->identifier>4))return false;
 if(c->delay_s<1||c->delay_s>86400UL||c->run_s<1||c->run_s>86400UL)return false;
 if(c->carrier_ppb < -100000L||c->carrier_ppb>100000L||c->timing_ppm < -200||c->timing_ppm>200)return false;
 if(c->battery_scale<4200||c->battery_scale>4800)return false;
 for(uint8_t i=0;i<4;i++)if(c->frequency[i]<3510000UL||c->frequency[i]>3600000UL)return false;
 if(c->mode==SPRINT){
  for(uint8_t i=0;i<4;i++)for(uint8_t j=i+1;j<4;j++){
   uint32_t d=c->frequency[i]>c->frequency[j]?c->frequency[i]-c->frequency[j]:c->frequency[j]-c->frequency[i];
   if(d<20000UL)return false;
  }
 }
 if(c->mode==FOXORING){
  uint32_t f=c->frequency[c->role<5?0:2],beacon=c->frequency[3];
  if((f>beacon?f-beacon:beacon-f)<30000UL)return false;
 }
 return mini_crc(c,offsetof(mini_config,crc))==c->crc;
}
void mini_default(mini_config *c,uint8_t role,uint8_t profile){
 memset(c,0,sizeof *c);c->magic=MINI_MAGIC;c->version=1;c->role=role;c->mode=SPRINT;c->profile=profile;c->slow_wpm=10;c->fast_wpm=15;
 c->identifier=role<10?role%5:role==10?5:6;
 c->frequency[0]=3530000;c->frequency[1]=3550000;c->frequency[2]=3570000;c->frequency[3]=3600000;
 c->delay_s=60;c->run_s=12UL*3600;c->battery_scale=4500;c->crc=mini_crc(c,offsetof(mini_config,crc));
}
static uint32_t utick(uint16_t units,uint8_t wpm){return ((uint32_t)units*MINI_HZ*6+((uint16_t)wpm*5)/2)/((uint16_t)wpm*5);}
uint32_t mini_word_ticks(uint8_t id,uint8_t wpm){
 if(id>6||wpm<8||wpm>15)return 0;
 uint16_t units=0;const char *s=ids[id];
 for(;*s;s++){const char *m=code(*s);for(;*m;m++)units+=(*m=='-'?3:1)+(m[1]?1:0);units+=s[1]?3:7;}
 return utick(units,wpm);
}
bool mini_morse(uint8_t id,uint8_t wpm,uint32_t phase,uint32_t remaining){
 uint32_t len=mini_word_ticks(id,wpm);if(!len)return false;
 uint32_t offset=phase%len;if(remaining<len-offset)return false; /* only whole identifiers */
 uint16_t u=0;const char *s=ids[id];
 for(;*s;s++){const char *m=code(*s);for(;*m;m++){
  uint32_t start=utick(u,wpm);u+=*m=='-'?3:1;
  if(offset>=start&&offset<utick(u,wpm))return true;
  if(m[1])u++;
 }u+=s[1]?3:7;}
 return false;
}
mini_output mini_schedule(const mini_config *c,uint32_t raw,bool armed,bool synced,bool fault){
 mini_output o={0};if(!armed||!synced||fault||!mini_valid(c))return o;
 /* raw tick stays < 2^25 in the bounded 48h lifetime; signed ppm correction. */
 uint32_t tick=(uint32_t)((int64_t)raw*1000000L/(1000000L+c->timing_ppm));
 uint32_t start=c->delay_s*MINI_HZ,end=start+c->run_s*MINI_HZ;
 if(tick>=end)return o;
 uint8_t group=c->role<5?0:c->role<10?2:c->role==10?1:3;
 o.frequency=c->frequency[group];o.identifier=c->identifier;o.wpm=c->role>=5&&c->role<10?c->fast_wpm:c->slow_wpm;
 if(c->mode!=SPRINT||c->role>=10){
  o.prepare=tick+MINI_PREP_TICKS>=start;
  if(tick>=start&&tick+4<end)o.key=mini_morse(o.identifier,o.wpm,tick-start,end-tick-4);
  return o;
 }
 uint32_t slot=(c->role%5)*12UL*MINI_HZ;
 uint32_t elapsed=tick>=start?tick-start:0;
 uint32_t cycle=elapsed/(60UL*MINI_HZ);
 uint32_t a=start+cycle*60UL*MINI_HZ+slot,z=a+12UL*MINI_HZ;
 /* Prepare next cycle even at role 0's 60s boundary. */
 if(tick>=z){a+=60UL*MINI_HZ;z+=60UL*MINI_HZ;}
 if(z>end)z=end;
 o.prepare=tick+MINI_PREP_TICKS>=a&&tick<z;
 /* One-second guards at both slot edges tolerate opposite-sign calibrated
    20ppm clocks for a 12h session (1.728s relative drift, plus RF tail).
    Temperature/load error must be included in that measured 20ppm budget. */
 if(tick>=a+MINI_HZ&&tick+MINI_HZ<z)
  o.key=mini_morse(o.identifier,o.wpm,tick-a-MINI_HZ,z-tick-MINI_HZ);
 return o;
}
static void params(uint32_t a,uint32_t b,uint32_t c,uint8_t out[8]){
 uint32_t k=(128UL*b)/c,p1=128UL*a+k-512,p2=128UL*b-c*k;
 out[0]=c>>8;out[1]=c;out[2]=(p1>>16)&3;out[3]=p1>>8;out[4]=p1;
 out[5]=((c>>12)&0xf0)|((p2>>16)&15);out[6]=p2>>8;out[7]=p2;
}
bool mini_si5351(uint32_t hz,int32_t ppb,uint8_t pll[8],uint8_t ms[8]){
 if(hz<3510000||hz>3600000||ppb< -100000||ppb>100000)return false;
 /* correct the 25MHz reference in the multisynth calculation; PLL remains x32 */
 uint64_t vco=800000000ULL*(uint32_t)(1000000000L+ppb)/1000000000UL;
 uint32_t a=vco/hz,b=((vco%hz)*1048575ULL+hz/2)/hz;
 if(b==1048575UL){a++;b=0;}
 params(32,0,1,pll);params(a,b,1048575UL,ms);return true;
}
