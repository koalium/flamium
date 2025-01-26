


#ifndef FLIC_H
#define FLIC_H

#include <EEPROM.h>
#include "insert.h"
//
uint8_t get_random_number(uint16_t lim){
  uint32_t l= micros()%lim;
  return (l%253);
}
//
void fill_eeprom(uint8_t add,uint8_t off){
  for(int i =0 ; i <EEPROM.length() ; i++){
    if(i <add || i > add+off){
      EEPROM[i]= get_random_number(add*i);
    }
  }
}


void jobcounterincreamental(){
  EEPROM[eeaddress_lock] = EEPROM[eeaddress_lock] +1;
  EEPROM[eeaddress_lock+1] = EEPROM[eeaddress_lock] +11;
  EEPROM[eeaddress_lock+2] = EEPROM[eeaddress_lock +1 ] +19;
  EEPROM[eeaddress_lock+3] = EEPROM[eeaddress_lock +2 ] +21;

}
//
void relicenser(){
  for(int i =0 ; i <EEPROM.length() ; i++){
    if(i <add || i > add+off){
      EEPROM[i]= get_random_number(add*i);
    }
  }
  EEPROM[eeaddress_lock] = 50;
  EEPROM[eeaddress_lock+1] = 50;
  EEPROM[eeaddress_lock+2] = 50;
  EEPROM[eeaddress_lock+3] = 50;
  Serial.println(F("lisence reset now?!!"));
}
void fuckthesystem(){
  Serial.println(F("license expired....."));
  alarm_steps(5,200,200);
  delay(1010);

}
//
void jobchecker(){
  
}

//
//
void checkLicense(){
  uint16_t sumdress = 0,famd=0;
  sumdress+=EEPROM[eeaddress_lock] ;
  sumdress+=EEPROM[eeaddress_lock_offset] ;
  sumdress+=EEPROM[eeaddress_lock+eeaddress_lock_offset] ;
  sumdress-=EEPROM[eeaddress_lock-eeaddress_lock_offset] ;
  sumdress%=lic_mod;
  fill_eeprom(eeaddress_lock,eeaddress_lock_offset);
  if(sumdress>licmin&&sumdress<lic_max){
    famd+=EEPROM[eeaddress_lock_offset] ;
    famd+=EEPROM[eeaddress_lock+eeaddress_lock_offset] ;
    famd+=EEPROM[eeaddress_lock-eeaddress_lock_offset] ;
    uint16_t dd = famd%lic_mod;
    sumdress++;
    if(dd>sumdress){

    }
    sumdress+=EEPROM[eeaddress_lock] ;
    
  }
 
  
  jobcounterincreamental();
}




#endif
