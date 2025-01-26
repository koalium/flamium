//

#include "insert.h"
#include "detect.h"
#include "cmd.h"
#include "flamium.h"
//




//
//
void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(2000000);
  while(!Serial){}
  init_gpio();
  bmpsetup();
  //setupMq6() ;
  delay(110);
  //sendCapsulated(_hi_);
  handshaked=false;
  rehandshake();
 
  delay(110);


}
//
void loop() {


  
  
  
  readCmd();
  //sendGasMq6();
  sendbmp280() ;
  delay(150);
}





