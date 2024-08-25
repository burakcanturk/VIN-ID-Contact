#include<SevSeg.h>
SevSeg s;
byte digitsayisi=4;
byte digitpinleri[]={12,9,8,6};
byte segmentpinleri[]={11,7,4,2,1,10,5,3};



void setup() {
s.begin(COMMON_CATHODE,digitsayisi,digitpinleri,segmentpinleri);
}



void loop() {
s.setChars("1905");
//s.setNumber(2018,3);
s.refreshDisplay();
delay(1);



    }
  
      
