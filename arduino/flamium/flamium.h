//#include <Arduino_BuiltIn.h>


#ifndef FLAMIUM_CONST_H
#define FLAMIUM_CONST_H
#include "insert.h"
#include "bmp280.h"

const char c_s_show_lock_0[] PROGMEM = "main fault?";
const char c_s_show_lock_1[] PROGMEM = "1st need?";
const char c_s_show_lock_2[] PROGMEM = "2n need?";
const char c_s_show_lock_3[] PROGMEM = "3rd need?";
const char c_s_show_lock_4[] PROGMEM = "4th need?";
const char c_s_show_lock_5[] PROGMEM = "how it work?";
const char * const c_s_show_lock[] PROGMEM = {c_s_show_lock_0, c_s_show_lock_1, c_s_show_lock_2, c_s_show_lock_3, c_s_show_lock_4, c_s_show_lock_5};

const char c_s_rst_lock_0[] PROGMEM = "az mokhtari bepors";
const char c_s_rst_lock_1[] PROGMEM = "kash mifahmidam";
const char c_s_rst_lock_2[] PROGMEM = "kash mifahmidi";
const char c_s_rst_lock_3[] PROGMEM = "kash mifahmidim";
const char c_s_rst_lock_4[] PROGMEM = "armoon>>mohebi";
const char c_s_rst_lock_5[] PROGMEM = "simple";
const char * const c_s_rst_lock[] PROGMEM={c_s_rst_lock_0,c_s_rst_lock_1, c_s_rst_lock_2,c_s_rst_lock_3,c_s_rst_lock_4,c_s_rst_lock_5};

const char c_s_main_instructions_0[] PROGMEM = "test";
const char c_s_main_instructions_1[] PROGMEM = "fire";
const char c_s_main_instructions_2[] PROGMEM = "adc-res";
const char c_s_main_instructions_3[] PROGMEM = "srl-bd";
const char c_s_main_instructions_4[] PROGMEM = "hi";
const char c_s_main_instructions_5[] PROGMEM = "diag";
const char * const c_s_main_instructions[] PROGMEM={c_s_main_instructions_0,c_s_main_instructions_1, c_s_main_instructions_2,c_s_main_instructions_3,c_s_main_instructions_4,c_s_main_instructions_5};


const String c_s_handshake_seq[]={"hi","ok","bye" };
const String c_s_def_pass[]={"8","551364","09161313797" };


/*
  MQUnifiedsensor Library - reading an MQ6

  Demonstrates the use a MQ6 sensor.
  Library originally added 01 may 2019
  by Miguel A Califa, Yersson Carrillo, Ghiordy Contreras, Mario Rodriguez
 
  Added example
  modified 23 May 2019
  by Miguel Califa 

  Updated library usage
  modified 26 March 2020
  by Miguel Califa 

  Wiring:
  https://github.com/miguel5612/MQSensorsLib_Docs/blob/master/static/img/MQ_Arduino.PNG
  Please make sure arduino A0 pin represents the analog input configured on #define pin

 This example code is in the public domain.

*/










void init_gpio(){
  //
  pinMode(PIN_ANAL_PIEZO,INPUT);
  pinMode(PIN_ANAL_MQ6,INPUT);
  //
  digitalWrite(pinRelayAlarm_0,_ALARM_RELAY_OFF_);
  pinMode(pinRelayAlarm_0,OUTPUT);
  digitalWrite(pinRelayAlarm_0,_ALARM_RELAY_OFF_);
  //
  digitalWrite(pinRelayFire_0,_FIRE_RELAY_OFF_);
  pinMode(pinRelayFire_0,OUTPUT);
  digitalWrite(pinRelayFire_0,_FIRE_RELAY_OFF_);
  //
  digitalWrite(pinSensorIr_0,HIGH);
  pinMode(pinSensorIr_0,INPUT_PULLUP);
  digitalWrite(pinSensorIr_1,HIGH);
  pinMode(pinSensorIr_1,INPUT_PULLUP);
  digitalWrite(pinSensorIr_2,HIGH);
  pinMode(pinSensorIr_2,INPUT_PULLUP);
  //
//  pinMode(PIN_START_PIEZO,INPUT_PULLUP);
  digitalWrite(pinValveMain_0,_ALARM_RELAY_OFF_);
  pinMode(pinValveMain_0,OUTPUT);
  digitalWrite(pinValveMain_0,_ALARM_RELAY_OFF_);
  //
  digitalWrite(pinValveAir_0,_ALARM_RELAY_OFF_);
  pinMode(pinValveAir_0,OUTPUT);
  digitalWrite(pinValveAir_0,_ALARM_RELAY_OFF_);
  //
  digitalWrite(pinValveOxy_0,_ALARM_RELAY_OFF_);
  pinMode(pinValveOxy_0,OUTPUT);
  digitalWrite(pinValveOxy_0,_ALARM_RELAY_OFF_);
  //
  digitalWrite(pinValveGas_0,_ALARM_RELAY_OFF_);
  pinMode(pinValveGas_0,OUTPUT);
  digitalWrite(pinValveGas_0,_ALARM_RELAY_OFF_);
}
//



void interface_pass(String cpass){
  Serial.println(F("password:"));
 
}
//
bool getSensorIr(uint8_t n){

}

void adctoserial(int ch){
  
  Serial.println(analogRead( map(analogRead(ch), 0, 1023, 0, 10000)));
  
  delay(100);
}



bool check_strings(String main,int mainset,String ins){
  if(main.substring(mainset,ins.length())==ins){
    return true;
  }
  return false;
}

void rstSensorCatch(){

}
//



///
#endif