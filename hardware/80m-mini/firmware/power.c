#include "power.h"
uint8_t rf_step(rf_sequence *s,bool prepared,bool authorized,bool key,uint32_t now){
 uint8_t action=0;
 if(!prepared||!authorized){s->held=s->tail=false;return RF_KILL;}
 if(key&&!s->held){s->held=true;s->tail=false;return RF_START;}
 if(!key&&s->held){s->held=false;s->tail=true;s->until=now+2;action|=ENV_STOP;}
 if(s->tail&&(int32_t)(now-s->until)>=0){s->tail=false;action|=RF_STOP;}
 return action;
}
