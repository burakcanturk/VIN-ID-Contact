#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

#define gps_tx 2
#define gps_rx 3

SoftwareSerial gpsUart(gps_tx, gps_rx);
TinyGPSPlus gps;

char val;
String message = "";

int date_time[6] = {0, 0, 0, 0, 0, 0};
float locations[2] = {0, 0};
int lat[4] = {0, 0, 0, 0};
int lng[4] = {0, 0, 0, 0};

unsigned long one_day_seconds = 86400;
char *vin = "3G1YZ23J9P5800001-";

void setup() {
  Serial.begin(9600);
  gpsUart.begin(9600);
}

void loop() {
  
  if (gpsUart.available() > 0) {
    
    if (gps.encode(gpsUart.read())) {
      
      if (gps.location.isValid()) {
        locations[0] = gps.location.lat();
        locations[1] = gps.location.lng();
      }
      
      if (gps.date.isValid()) {
        date_time[0] = gps.date.day();
        date_time[1] = gps.date.month();
        date_time[2] = gps.date.year();
      }
      
      if (gps.time.isValid()) {
        date_time[3] = gps.time.hour();
        date_time[4] = gps.time.minute();
        date_time[5] = gps.time.second();
      }
    }
  }
  
  if (Serial.available() > 0) {
    
    val = Serial.read();
    
    if (not (val == '-')) {
      message += val;
    }
    
    if ((val == '-') and (message.length() == 17) and (not (message == "1HGEG644387712345"))) {
      long row = 0;
      if (not (EEPROM.read(one_day_seconds * 32 - 1) == 255)) {
        for (long i = 0; i < one_day_seconds * 34; i++) {
          EEPROM.write(i, 255);
        }
      }
      for (int i = 0; i < (one_day_seconds * 32); i++) {
        if (EEPROM.read(i) == 255) {
          break;
        }
        row++;
      }
      for (int i = 0; i < 17; i++) {
        EEPROM.write(row + i, message[i]);
      }
      unsigned long latitude = float(locations[0]) * pow(10, 6);
      for (int i = 0; i < 4; i++) {
        lat[i] = (latitude / long(pow(100, i))) % 100;
      }
      for (int i = 0; i < 4; i++) {
        EEPROM.write(row + 17 + i, lat[i]);
      }
      unsigned long longitude = float(locations[1]) * pow(10, 6);
      for (int i = 0; i < 4; i++) {
        lng[i] = (longitude / long(pow(100, i))) % 100;
      }
      for (int i = 0; i < 4; i++) {
        EEPROM.write(row + 21 + i, lng[i]);
      }
      EEPROM.write(row + 25, date_time[0]);
      EEPROM.write(row + 26, date_time[1]);
      for (int i = 0; i < 2; i++) {
        EEPROM.write(row + 27 + i, (date_time[2] / int(pow(100, i))) % 100);
      }
      
      EEPROM.write(row + 29, date_time[3] + 3);
      EEPROM.write(row + 30, date_time[4]);
      EEPROM.write(row + 31, date_time[5]);
      
      Serial.print("\Saved:\tvin-id: ");
      Serial.print(message);
      Serial.print("\tlocation: ");
      Serial.print(locations[0]);
      Serial.print(",");
      Serial.print(locations[1]);
      Serial.print("\tdate-time: ");
      Serial.print(((date_time[0] < 10) ? "0" : "") + String(date_time[0]));
      Serial.print("/");
      Serial.print(((date_time[1] < 10) ? "0" : "") + String(date_time[1]));
      Serial.print("/");
      Serial.print(date_time[2]);
      Serial.print(" ");
      Serial.print(((date_time[3] < 10) ? "0" : "") + String(date_time[3]));
      Serial.print(":");
      Serial.print(((date_time[4] < 10) ? "0" : "") + String(date_time[4]));
      Serial.print(":");
      Serial.println(((date_time[5] < 10) ? "0" : "") + String(date_time[5]));
      for (int i = 0; i < 5; i++) {
        lat[i] = 0;
        lng[i] = 0;
      }
      message = "";
      delay(100);
    }
  }
  
  else {
    Serial.write(vin);
    delay(1000);
  }
}
