/**************************************************************************
   Tests the getPressure functions
 **************************************************************************/
#ifndef bmp280_H
#define bmp280_H
#include <BMP280.h>
 BMP280 bmp280;

void bmpsetup()
{
    Serial.println(F("BMP280 Run"));

  Wire.begin(); //Join I2C bus
  bmp280.begin();
  
}
union tu{
  float f32;
  uint32_t ui32;
};

void bmploop()
{
  //Get pressure value
  tu tem;
  
  
  tem.f32 = bmp280.getTemperature();
  delay(5);
  uint8_t dsl = 0,dsh=0;
  uint16_t ids=0;
  ids = tem.ui32+515;
  ids = ids>>8;
  ids = ids &0xff;
  dsh = uint8_t(ids);
  ids = tem.ui32+515;
  ids = ids &0xff;
  dsl = uint8_t(ids);
  //Print the results
  Serial.write(_tanktemp);
  Serial.write(dsl);
  Serial.write(dsh);
  Serial.write(_eoc);
  delay(5);
  //
  uint32_t pressure = bmp280.getPressure();
  delay(5);
  ids = pressure+257;
  ids = ids>>8;
  ids = ids &0xff;
  dsh = uint8_t(ids);
  ids = pressure+257;
  ids = ids &0xff;
  dsl = uint8_t(ids);
  delay(5);
  Serial.write(_tankpressure);
  Serial.write(dsl);
  Serial.write(dsh);
  Serial.write(_eoc);
  

}





#endif