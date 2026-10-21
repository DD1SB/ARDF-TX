/* Mini80 M80-E1. No Arduino framework, no network, no automatic reset re-arm. */
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/cpufunc.h>
#include <avr/sleep.h>
#include <avr/eeprom.h>
#include <util/atomic.h>
#include <util/delay.h>
#include <string.h>
#include "mini80.h"
#include "power.h"
#define BOOST PIN4_bm
#define CLOCK PIN5_bm
#define ENV PIN6_bm
#define RF PIN7_bm
#define SCL PIN0_bm
#define SDA PIN1_bm
static volatile uint32_t ticks,epoch;
static volatile bool armed,synced;
static volatile uint8_t rx[96],wr,rd;
static volatile bool rx_fault;
static mini_config config;
static uint8_t EEMEM stored[sizeof(mini_config)];
static bool fault,prepared,config_ready;
static rf_sequence envelope;
ISR(RTC_CNT_vect){RTC.INTFLAGS=RTC_OVF_bm;ticks++;}
ISR(PORTA_PORT_vect){
 PORTA.INTFLAGS=PIN3_bm;
 if(armed&&!synced){epoch=ticks;synced=true;}
}
ISR(USART0_RXC_vect){
 uint8_t status=USART0.RXDATAH,b=USART0.RXDATAL,next=(wr+1)%sizeof rx;
 if(status&(USART_FERR_bm|USART_BUFOVF_bm|USART_PERR_bm)||next==rd){rx_fault=true;return;}
 rx[wr]=b;wr=next;
}
static void safe(void){
 PORTA.OUTCLR=RF|ENV;envelope.held=envelope.tail=false;
}
static void down(void){
 safe();PORTA.OUTCLR=CLOCK|BOOST;PORTB.DIRCLR=SCL|SDA;prepared=false;
}
static void low(uint8_t pin){PORTB.OUTCLR=pin;PORTB.DIRSET=pin;}
static void release(uint8_t pin){PORTB.DIRCLR=pin;}
static bool high(uint8_t pin){
 release(pin);for(uint8_t i=0;i<200;i++){if(PORTB.IN&pin)return true;_delay_us(2);}return false;
}
static bool i2c_byte(uint8_t v){
 for(uint8_t i=0;i<8;i++){low(SCL);if(v&0x80)release(SDA);else low(SDA);_delay_us(3);if(!high(SCL))return false;_delay_us(3);v<<=1;}
 low(SCL);release(SDA);_delay_us(3);if(!high(SCL))return false;bool ok=!(PORTB.IN&SDA);_delay_us(3);low(SCL);return ok;
}
static bool start(void){release(SDA);if(!high(SCL))return false;_delay_us(3);low(SDA);_delay_us(3);low(SCL);return true;}
static void stop(void){low(SDA);_delay_us(3);high(SCL);_delay_us(3);release(SDA);}
static bool write_reg(uint8_t reg,const uint8_t *v,uint8_t n){
 bool ok=start()&&i2c_byte(0xc0)&&i2c_byte(reg);
 while(ok&&n--){ok=i2c_byte(*v++);}stop();return ok;
}
static bool reg1(uint8_t reg,uint8_t val){return write_reg(reg,&val,1);}
static bool status_read(uint8_t *v){
 bool ok=start()&&i2c_byte(0xc0)&&i2c_byte(0)&&start()&&i2c_byte(0xc1);uint8_t b=0;
 if(ok){release(SDA);for(uint8_t i=0;i<8;i++){low(SCL);_delay_us(3);if(!high(SCL)){ok=false;break;}_delay_us(3);b=(b<<1)|!!(PORTB.IN&SDA);}low(SCL);release(SDA);high(SCL);_delay_us(3);low(SCL);}
 stop();*v=b;return ok;
}
static uint16_t adc(uint8_t channel){
 ADC0.MUXPOS=channel;ADC0.COMMAND=ADC_STCONV_bm;
 /* Watchdog resets to safe hardware defaults if ADC does not complete. */
 while(!(ADC0.INTFLAGS&ADC_RESRDY_bm)){}ADC0.INTFLAGS=ADC_RESRDY_bm;return ADC0.RES;
}
static uint16_t battery(void){return (uint32_t)adc(ADC_MUXPOS_AIN8_gc)*config.battery_scale/1023;}
static uint16_t v5(void){return (uint32_t)adc(ADC_MUXPOS_AIN9_gc)*7350/1023;}
static bool prepare(uint32_t hz){
 down();PORTA.OUTSET=BOOST;_delay_ms(12);
 uint16_t rail=v5();if(rail<4600||rail>5350)return false;
 PORTA.OUTSET=CLOCK;_delay_ms(10);
 uint8_t st=0xff;
 for(uint8_t i=0;i<100;i++){if(status_read(&st)&&!(st&0x80))break;_delay_ms(1);}
 if(st&0x80)return false;
 /* OE disabled throughout every frequency update; VPA is also off. */
 uint8_t pll[8],ms[8];if(!mini_si5351(hz,config.carrier_ppb,pll,ms))return false;
 if(!reg1(3,0xff)||!reg1(16,0x80)||!reg1(17,0x80)||!reg1(18,0x80)||!reg1(183,0xd2))return false;
 if(!write_reg(26,pll,8)||!write_reg(42,ms,8)||!reg1(177,0x20)||!reg1(16,0x0c)||!reg1(24,0))return false;
 for(uint8_t i=0;i<100;i++){if(!status_read(&st))return false;if(!(st&0xa0)){prepared=true;return true;}_delay_ms(1);}
 return false;
}
static void key(bool on,uint32_t now){
 uint8_t action=rf_step(&envelope,prepared,armed&&synced&&!fault,on,now);
 if(action&RF_KILL){safe();return;}
 if(action&RF_START){
  if(!reg1(3,0xfe)){fault=true;down();return;}
  PORTA.OUTSET=RF|ENV;
 }
 if(action&ENV_STOP)PORTA.OUTCLR=ENV;
 if(action&RF_STOP){PORTA.OUTCLR=RF;if(!reg1(3,0xff))fault=true;}
}
static void send(uint8_t b){while(!(USART0.STATUS&USART_DREIF_bm)){}USART0.TXDATAL=b;}
static void reply(uint8_t command,const void *data,uint8_t size){
 uint8_t frame[64]={0xa5,command,size};memcpy(frame+3,data,size);uint16_t crc=mini_crc(frame,size+3);
 for(uint8_t i=0;i<size+3;i++){send(frame[i]);}send(crc);send(crc>>8);
}
static void commands(void){
 static uint8_t frame[64],n;static uint32_t last;
 if(rx_fault){fault=true;armed=synced=false;down();rx_fault=false;}
 if(n&&ticks-last>64){n=0;armed=synced=false;down();}
 while(rd!=wr){
  uint8_t b=rx[rd];rd=(rd+1)%sizeof rx;last=ticks;
  if(!n&&b!=0xa5)continue;
  frame[n++]=b;
  if(n==3&&frame[2]>sizeof(mini_config)){n=0;armed=synced=false;down();continue;}
  if(n>=5&&n==frame[2]+5){
   uint16_t crc=(uint16_t)frame[n-2]|((uint16_t)frame[n-1]<<8);uint8_t status=1;
   if(crc!=mini_crc(frame,n-2)){armed=synced=false;down();}
   else if(frame[1]==1&&frame[2]==sizeof(mini_config)){
    armed=synced=false;down();mini_config next;memcpy(&next,frame+3,sizeof next);
    if(mini_valid(&next)){
     /* Interrupted write becomes invalid CRC; no saved arm bit. */
     uint16_t invalid=0;eeprom_update_block(&invalid,stored+sizeof(next)-2,2);
     eeprom_update_block(&next,stored,sizeof next);eeprom_read_block(&config,stored,sizeof config);config_ready=mini_valid(&config);status=!config_ready;
    }
   }else if(frame[1]==2&&frame[2]==0){reply(0x82,&config,sizeof config);n=0;continue;}
   else if(frame[1]==3&&frame[2]==0&&config_ready&&mini_valid(&config)&&battery()>=3400){
    down();fault=false;armed=true;synced=false;status=0;
   }else if(frame[1]==4&&frame[2]==0){armed=synced=false;down();status=0;}
   reply(frame[1]|0x80,&status,1);n=0;
  }
 }
}
int main(void){
 /* Port output latches are set before directions; no software boot RF pulse. */
 PORTA.OUTCLR=BOOST|CLOCK|ENV|RF;PORTA.DIRSET=BOOST|CLOCK|ENV|RF|PIN1_bm;
 PORTB.OUTCLR=SCL|SDA;PORTB.DIRCLR=SCL|SDA;
 _PROTECTED_WRITE(CLKCTRL.MCLKCTRLB,CLKCTRL_PDIV_4X_gc|CLKCTRL_PEN_bm); /* 20MHz fuse /4 =5MHz */
 _PROTECTED_WRITE(WDT.CTRLA,WDT_PERIOD_2KCLK_gc);
 eeprom_read_block(&config,stored,sizeof config);
 config_ready=mini_valid(&config);
 if(!config_ready){mini_default(&config,0,MINI50);fault=true;}
 PORTA.PIN3CTRL=PORT_ISC_RISING_gc;PORTB.PIN4CTRL=PORT_ISC_INPUT_DISABLE_gc;PORTB.PIN5CTRL=PORT_ISC_INPUT_DISABLE_gc;
 PORTMUX.CTRLB=PORTMUX_USART0_ALTERNATE_gc;
 USART0.BAUD=2083; /* 9600 baud, 5MHz clock, normal 16x */
 USART0.CTRLC=USART_CHSIZE_8BIT_gc;USART0.CTRLB=USART_RXEN_bm|USART_TXEN_bm;USART0.CTRLA=USART_RXCIE_bm;
 VREF.CTRLA=VREF_ADC0REFSEL_1V5_gc;ADC0.CTRLC=ADC_PRESC_DIV32_gc|ADC_REFSEL_INTREF_gc;ADC0.SAMPCTRL=31;ADC0.CTRLA=ADC_ENABLE_bm;
 _PROTECTED_WRITE(CLKCTRL.XOSC32KCTRLA,CLKCTRL_ENABLE_bm|CLKCTRL_RUNSTDBY_bm|CLKCTRL_CSUT_32K_gc);
 RTC.CLKSEL=RTC_CLKSEL_TOSC32K_gc;while(RTC.STATUS){}RTC.PER=255;RTC.INTCTRL=RTC_OVF_bm;RTC.CTRLA=RTC_RTCEN_bm|RTC_RUNSTDBY_bm;
 sei();uint32_t checked=0,last=~0UL;
 for(;;){
  commands();uint32_t now,base;ATOMIC_BLOCK(ATOMIC_RESTORESTATE){now=ticks;base=epoch;}
  if(now!=last){
   __asm__ __volatile__("wdr");last=now;
   if(now-checked>=MINI_HZ){checked=now;if(battery()<3200){fault=true;armed=synced=false;down();}}
   mini_output o=mini_schedule(&config,now-base,armed,synced,fault);
   if(!o.prepare){if(prepared)down();}
   else if(!prepared){if(!prepare(o.frequency)){fault=true;armed=synced=false;down();}}
   if(prepared){key(o.key,now);if(fault){armed=synced=false;down();}}
  }
  /* USART needs peripheral clock. Idle while awaiting fixture; standby once synced. */
  set_sleep_mode(synced?SLEEP_MODE_STANDBY:SLEEP_MODE_IDLE);
  cli();if(rd==wr){sleep_enable();sei();sleep_cpu();sleep_disable();}else sei();
 }
}
