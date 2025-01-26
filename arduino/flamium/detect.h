#ifndef DETECT_H
#define DETECT_H

#include "alarm.h"
#include "insert.h"
//
bool check_sensore_state(){

}
//
//

// Read the AD conversion result
void read_adc(unsigned char adc_input) {
  SET_ADC_INPUT_PIN(adc_input);
  // Start the AD conversion
  START_ADC_CONV;
  // Wait for the AD conversion to complete
  while (IS_ADC_COV_COMPLETE== 0)
    ;
  CLR_ADC_COMPLETE_FLAG;
  //return ADCW;
}
//
void init_adc_piezo(uint8_t adc_input) {

SET_ADC_INPUT_PIN(adc_input);
// Analog Comparator initialization
// Analog Comparator: Off
// The Analog Comparator's positive input is
// connected to the AIN0 pin
// The Analog Comparator's negative input is
// connected to the AIN1 pin
ACSR=(1<<ACD) | (0<<ACBG) | (0<<ACO) | (0<<ACI) | (0<<ACIE) | (0<<ACIC) | (0<<ACIS1) | (0<<ACIS0);
// Digital input buffer on AIN0: On
// Digital input buffer on AIN1: On
DIDR1=(0<<AIN0D) | (0<<AIN1D);
SET_ADC_INPUT_PIN(adc_input);
// ADC initialization
// ADC Clock frequency: 1000.000 kHz
// ADC Voltage Reference: AREF pin
// ADC Auto Trigger Source: Free Running
// Only the 8 most significant bits of
// the AD conversion result are used
// Digital input buffers on ADC0: Off, ADC1: Off, ADC2: On, ADC3: On
// ADC4: On, ADC5: On
DIDR0=(0<<ADC5D) | (0<<ADC4D) | (0<<ADC3D) | (0<<ADC2D) | (1<<ADC1D) | (1<<ADC0D);
ADMUX=ADC_VREF_TYPE;
ADCSRA=(1<<ADEN) | (0<<ADSC) | (1<<ADATE) | (0<<ADIF) | (0<<ADIE) | (1<<ADPS2) | (0<<ADPS1) | (0<<ADPS0);
ADCSRB=(0<<ADTS2) | (0<<ADTS1) | (0<<ADTS0);

  
}
//



bool adch_change_flag = false;
//
void set_adc_input(uint8_t adc_input){
  ADMUX = adc_input | ADC_VREF_TYPE;
}


void adc_stop(){
  ADCSRA=(0<<ADEN) | (0<<ADSC) | (1<<ADATE) | (0<<ADIF) | (0<<ADIE) | (1<<ADPS2) | (0<<ADPS1) | (0<<ADPS0);
}

void run_adc_piezo(){
  init_adc_piezo(A5);
  START_ADC_CONV;
  // Wait for the AD conversion to complete
  while (IS_ADC_COV_COMPLETE == 0)
    ;
  CLR_ADC_COMPLETE_FLAG;
  read_adc(A5);
}

void readsensorflameir(){
  static uint8_t irdetected=0;
  if(isFlamed()){
        switch(irdetected){
          case 0:
            if(irDetected_0){
              sensor_ir_touched_time_0 = micros();
              irdetected=1;
            }
            if(irDetected_1){
              sensor_ir_touched_time_1 = micros();
              irdetected=2;
            }
            if(irDetected_2){
              sensor_ir_touched_time_2 = micros();
              irdetected=3;
            }
            break;
          //
          case 1:
            if(irDetected_1){
              sensor_ir_touched_time_1 = micros();
              irdetected=2;
            }
            if(irDetected_2){
              sensor_ir_touched_time_2 = micros();
              irdetected=3;
            }
            break;
          //
          case 2:
            if(irDetected_2){
              sensor_ir_touched_time_2 = micros();
              irdetected=3;
            }
            if(irDetected_3){
              sensor_ir_touched_time_3 = micros();
              irdetected=4;
            }
            if(irDetected_4){
              sensor_ir_touched_time_4 = micros();
              irdetected=5;
            }
            break;
          //
          case 3:
            if(irDetected_3){
              sensor_ir_touched_time_3 = micros();
              irdetected=4;
            }
            if(irDetected_4){
              sensor_ir_touched_time_4 = micros();
              irdetected=5;
            }
            if(irDetected_5){
              sensor_ir_touched_time_5 = micros();
              irdetected=6;
            }
            break;
          //
          case 4:
            if(irDetected_4){
              sensor_ir_touched_time_4 = micros();
              irdetected=5;
            }
            if(irDetected_5){
              sensor_ir_touched_time_5 = micros();
              irdetected=6;
            }
            break;
          //
          case 5:
            if(irDetected_5){
              sensor_ir_touched_time_5 = micros();
              irdetected=6;
            }
            break;
          // 
        }
      //
      }
}

void purefire(){
  init_adc_piezo(A5);
  run_adc_piezo();
  START_ADC_CONV;
  
  uint32_t mil = millis() + 1250;
  
  Serial.print(F("bihbih"));
  delay(50);
  fire_start_time = micros();
  setFireRelay();
    while (millis() < mil) {
      
      readsensorflameir();
      
      Serial.write(ADCH);
      CLR_ADC_COMPLETE_FLAG; 
    }
  delay(50);
  
  Serial.println(F("migmig"));
}

void sendafterfire(){
  
  
  Serial.println(F("test started at : "));
Serial.print(F("__stf"));
  Serial.println(fire_start_time);
  Serial.println(F("1st ir sensor triggered at : "));
  Serial.print(F("__ir1"));
  Serial.println(sensor_ir_touched_time_0);
  Serial.print(F("__tir1")); 
  Serial.println(fire_start_time-sensor_ir_touched_time_0);
  Serial.println(F("2nt ir sensor triggered at : "));
   Serial.print(F("__ir2"));
  Serial.println(sensor_ir_touched_time_1);
   Serial.print(F("__tir2"));
  Serial.println(fire_start_time-sensor_ir_touched_time_2);
  Serial.println(F("3rd ir sensor triggered at : "));
   Serial.print(F("__ir3"));
  Serial.println(sensor_ir_touched_time_2);
   Serial.print(F("__tir3"));
  Serial.println(fire_start_time-sensor_ir_touched_time_2);

  clrFireRelay();
  clrAlarmRelay();
  Serial.println(F("flamiumLtd"));
}
//
void fire_in_the_hole(){
  static uint8_t p_adch = 0;
  init_adc_piezo(pinSensorPiezo_0) ;
  
  alarming_before_fire();
  purefire();
  sendafterfire();
  
  
}
//




bool check_ir_sensor_0(){
  Serial.print(F(" testing ... "));
  Serial.println(F("light it"));
  //
  
  Serial.print(F("light it"));
  Serial.println(_str_0_);

  Serial.print(F("cover it"));
  Serial.print("    ");
  delay(1000);
  while(irDetected_0)
  ;
  Serial.println(F("rej"));
  //
  Serial.print(F("cover it"));
  Serial.print(F("    "));
  delay(1000);
  while(irDetected_0)
  ;
  Serial.println(F("passed"));
  
}
//

void diag_sensors(){
  //
  if(irDetected_0)
  {
    errors |= (1<<0);
  }
  //
  if(irDetected_0)
  {
    errors |= (1<<1);
  }
  //
  if(irDetected_0)
  {
    errors |= (1<<2);
  }

  Serial.println(errors);
  while(errors){
     errors = Serial.read()-'0';
  }
}
//

#endif


