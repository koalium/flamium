#ifndef CMD_H
#define CMD_H

#include "detect.h"
#include <arduino.h>
#include <EEPROM.h>
#include "bmp280.h"
#include "mq6_m.h"

#include "insert.h"

//
//
void sendGasMq6(){
 /* if(update_mq6==false || mq6_init_finish==false){
    return;
  }*/
  loopMq6() ;
}
void sendbmp280(){
  
  bmploop() ;
}
//



void rehandshake(){
  int i = 100;
  while(i-->0&&!handshaked){
    //Serial.println(_hi_);
    Serial.write(_handshake);
    Serial.write(_eoc);
    delay(100);
    while(Serial.available()){
      if(Serial.read()==_handshake){
        handshaked=true;
        Serial.println(F("handshake succeed...."));
        
      }
    }
  }
}
//
void stop(){

}
//
const char _default_pass ='8';

void cmdpharse(){
  switch(input[0]){
    case _fire:
      if(input[1]==_default_pass){
        
      }
      fire_in_the_hole();
      break;
    //
    case _stop:
      if(input[1]==_default_pass){
        stop();
      }
      break;
    //
    case _addoxygen:
      
      
      break;
    //
    case _addair:
      
      
      break;
    //
    case _addGas:
      
      
      break;
    //
    case _mq6:
      
      
      break;
    //
    case _alarm:
      
      
      break;
    //
    case _mix:
      
      
      break;
    //
    case _read:
      
      
      break;
    //
    case _write:
      
      
      break;
    //
    case _open:
      
      
      break;
    //
    case _close:
      
      
      break;
    //
    case _handshake:
      
      Serial.write(_handshake);
      Serial.write(_eoc);
      break;
    //
    



  }
}


bool echo = false;
void readCmd(){
  
  while(Serial.available()){
    uint32_t inchar = Serial.read();
    input[inpcount]=inchar;
    if(input[inpcount]==_eoc){
      if(inpcount>0){
        cmdpharse();
        inpcount=0;
      }
      return;
    }
    if(++inpcount>=inlen){
      inpcount=0;
    }
    if(echo){
    Serial.print(inchar);
    }
    
  }
}






#endif