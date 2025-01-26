#ifndef INSERT_H
#define INSERT_H

#include <arduino.h>


const uint8_t eeaddress_lock = 111;
const uint8_t eeaddress_lock_offset = 14;
const uint8_t lic_max = 222;
const uint8_t lic_min = 22;
const uint8_t lic_mod = 229;
//
//this is for flame arrester's tester platform



//const String on_str = " ... ON...";
//const String off_str = " ...OFF... ";
const String _str_0_ = "  0  ";
const String _str_1_ = "  1  ";
const String _str_2_ = "  2  ";
const String _str_3_ = "  3  ";
const String _str_4_ = "  4  ";
const String _str_5_ = "  5  ";

#define inlen  10
uint8_t inpcount = 0;
uint8_t input[inlen];
const char _eoc =0;
const char _eol =255;
const char _addair ='A';
const char _addoxygen ='B';
const char _addGas ='C';
const char _alarm ='D';
const char _mix ='E';
const char _fire ='F';
const char _tankgas ='G';
const char _tankpressure ='H';
const char _tanktemp ='I';
const char _gaspressure ='J';
const char _airpressure ='K';
const char _tankvalve ='L';
const char _mq6 ='M';
const char _close ='N';
const char _open='O';
const char _piezo ='P';
const char _oxypressure ='Q';
const char _read ='R';
const char _oxytemp='S';
const char _test='T';
const char _gastemp='U';
const char _airtemp='V';
const char _write='W';
const char _pass='X';
const char _baudrate='Y';
const char _handshake='Z';
const char _ir0 ='a';
const char _ir1 ='b';
const char _ir2 ='c';
const char _ir3 ='d';
const char _ir4 ='c';
const char _ir5 ='d';
const char _stop = 's';



#define SERIAL_BAUD            2000000L
//
//#define PIN_VALVE_TANK_RELAY        7
#define _VALVE_TANK_RELAY_ON_       HIGH
#define _VALVE_TANK_RELAY_OFF_      LOW
//
//
//#define PIN_VALVE_GAS_RELAY        8
#define _VALVE_GAS_RELAY_ON_       HIGH
#define _VALVE_GAS_RELAY_OFF_      LOW

//
//#define PIN_VALVE_OXY_RELAY        9
#define _VALVE_OXY_RELAY_ON_       HIGH
#define _VALVE_OXY_RELAY_OFF_      LOW
//
//
//#define PIN_VALVE_AIR_RELAY        PD10
#define _VALVE_AIR_RELAY_ON_       HIGH
#define _VALVE_AIR_RELAY_OFF_      LOW
//
//
//#define PIN_ALARM_RELAY        PD6
#define _ALARM_RELAY_ON_       HIGH
#define _ALARM_RELAY_OFF_      LOW
//
//#define PIN_FIRE_RELAY         PD5
#define _FIRE_RELAY_ON_        HIGH
#define _FIRE_RELAY_OFF_       LOW
//
//#define PIN_SENSOR_IR_0        PD2
#define _SENSOR_IR_0_TOUCHED_  LOW
#define _SENSOR_IR_0_IDLE_     HIGH
//
//#define PIN_SENSOR_IR_1        3
#define _SENSOR_IR_1_TOUCHED_  LOW
#define _SENSOR_IR_1_IDLE_     HIGH
//
//#define PIN_SENSOR_IR_2        4
#define _SENSOR_IR_2_TOUCHED_  LOW
#define _SENSOR_IR_2_IDLE_     HIGH
//
//#define PIN_START_PIEZO        10
#define _START_PIEZO_          LOW
//
#define PIN_ANAL_PIEZO         A0
#define PIN_ADC_PIEZO          0
//
#define PIN_ANAL_MQ6         A1
#define PIN_ADC_MQ6            1
//
// These constants won't change:
const int pinSensorIr_0 = 2;      // pin that the  is attached to
const int pinSensorIr_1 = 3;      // pin that the  is attached to
const int pinSensorIr_2 = 4;      // pin that the  is attached to
const int pinSensorIr_3 = 5;      // pin that the  is attached to
const int pinSensorIr_4 = 6;      // pin that the  is attached to
const int pinSensorIr_5 = 7;      // pin that the  is attached to
const int pinSensorPiezo_0 = PIN_ADC_PIEZO;      // pin that the  is attached to
const int pinSensorMq_0 = PIN_ADC_MQ6;      // pin that the  is attached to
const int pinRelayFire_0 = 8;      // pin that the  is attached to
const int pinRelayAlarm_0 = 9;      // pin that the  is attached to
const int pinValveMain_0 = 10;      // pin that the  is attached to
const int pinValveAir_0 = 11;      // pin that the  is attached to
const int pinValveOxy_0 = 12;      // pin that the  is attached to
const int pinValveGas_0 = 13;      // pin that the 
//


#define _DEF_FIRE_PASSWORD_      '8'

// Voltage Reference: AVCC pin
#define ADC_VREF_TYPE_AVCC ((0<<REFS1) | (1<<REFS0) | (0<<ADLAR))
// Voltage Reference: AREF pin
#define ADC_VREF_TYPE ((0<<REFS1) | (0<<REFS0) | (1<<ADLAR))
// Voltage Reference: Int., cap. on AREF
#define ADC_VREF_TYPE_INTL ((1<<REFS1) | (1<<REFS0) | (0<<ADLAR))
//
//
#ifndef ADC_VREF_TYPE 
#define ADC_VREF_TYPE ADC_VREF_TYPE_AREF
#endif
//
#define SET_ADC_INPUT_PIN(N)  ADMUX = N | ADC_VREF_TYPE
//
#define START_ADC_CONV              ADCSRA |= (1 << ADSC)
#define IS_ADC_COV_COMPLETE   (ADCSRA & (1 << ADIF)) 
#define CLR_ADC_COMPLETE_FLAG ADCSRA |= (1 << ADIF)
#define ADC_VALUE_FULL    ADCW
#define ADC_VALUE_LOW     ADCL
#define ADC_VALUE_HIGH    ADCH


#define IR0 2
#define IR1 3
#define IR2 4
#define IR3 5
#define IR4 6
#define IR5 7
#define  irDetected_0 (PIND&1<<IR0)
#define  irDetected_1 (PIND&1<<IR1)
#define  irDetected_2 (PIND&1<<IR2)
#define  irDetected_3 (PIND&1<<IR3)
#define  irDetected_4 (PIND&1<<IR4)
#define  irDetected_5 (PIND&1<<IR5)
#define IR_MASK  ((1<<IR0)|(1<<IR1)|(1<<IR2)|(1<<IR3)|(1<<IR4)|(1<<IR5))
#define isFlamed() PIND&IR_MASK
//
#define setFireRelay() digitalWrite(pinRelayFire_0,_FIRE_RELAY_ON_)
#define clrFireRelay() digitalWrite(pinRelayFire_0,_FIRE_RELAY_OFF_)

bool update_mq6 = false;
bool update_bm280 = false;
uint32_t sensor_ir_touched_time_0 = 0;
uint32_t sensor_ir_touched_time_1 = 0;
uint32_t sensor_ir_touched_time_2 = 0;
uint32_t sensor_ir_touched_time_3 = 0;
uint32_t sensor_ir_touched_time_4 = 0;
uint32_t sensor_ir_touched_time_5 = 0;
uint32_t fire_start_time = 0;

uint8_t errors = 0;

char pass_fire_ = _DEF_FIRE_PASSWORD_;


bool handshaked = false;



#endif