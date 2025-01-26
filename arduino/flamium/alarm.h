
#ifndef ALARM_H
#define ALARM_H



//
void setAlarmRelay(){
  Serial.print(F("ALERT ... fire in the hole"));
  Serial.println(F(" ... ON..."));
  digitalWrite(pinRelayAlarm_0,_ALARM_RELAY_ON_);
  
}
void clrAlarmRelay(){
  Serial.print(F("ALERT ... fire in the hole"));
  Serial.println(F(" ...OFF... "));
  digitalWrite(pinRelayAlarm_0,_ALARM_RELAY_OFF_);
}
void alarm_steps(uint8_t num,uint16_t don,uint16_t doff){
  Serial.print(F("   "));
  Serial.print(num);
  Serial.print(F("   "));
  setAlarmRelay();
  delay(don);
  Serial.print(F("   "));
  Serial.print(num);
  Serial.print(F("   "));
  setAlarmRelay();
  delay(doff);
}
//
void alarming_before_fire(){
  alarm_steps(5,200,800);
  alarm_steps(4,300,700);
  alarm_steps(3,400,600);
  alarm_steps(2,600,400);
  alarm_steps(1,800,200);
  alarm_steps(0,1000,10);
  //
  Serial.println(F(" ALARM FINISHED ... fire in the hole "));
  //
}



#endif