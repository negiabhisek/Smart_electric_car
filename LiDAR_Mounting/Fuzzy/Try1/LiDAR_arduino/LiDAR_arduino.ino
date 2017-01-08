/* =============================================================================

=========================================================================== */

#include <Wire.h>
#include <LIDARLite.h>
#include <Servo.h>

int sensorPins[] = {22,23,24}; // Array of pins connected to the sensor Power Enable lines
unsigned char addresses[] = {0x66,0x68,0x64};
int i = 0;
int j = 0;
char val; // Data received from the serial port
int ledPin = 13; // Set the pin to digital I/O 13
//boolean ledState = LOW; //to toggle our LED


// Create a new LIDARLite instance
LIDARLite myLidarLite;
Servo myServo1;
Servo myServo2;

void setup() {
  Serial.begin(115200);
  myLidarLite.begin();
  myLidarLite.changeAddressMultiPwrEn(3,sensorPins,addresses,false);
  myServo1.attach(11); // Servo motor sinyal pini
  myServo2.attach(12);
  pinMode(ledPin, OUTPUT); // Set pin as OUTPUT
  //establishContact();  // send a byte to establish contact until receiver responds 
}

void loop() 
{
    receive_data();
}

void receive_data()
{
  /*if (Serial.available() > 0)     // If data is available to read,
  { 
    val = Serial.read(); // read it and store it in val

    if(val == '1') //if we get a 1
    {
       digitalWrite(ledPin, HIGH); 
    }
    else if(val == '0') //if we get a 1
    {
       digitalWrite(ledPin, LOW); 
    }
  }
  else
    {*/
     lidar_data(); 
   // }
    //delay(10);
    
}

/* void establishContact() {
  while (Serial.available() <= 0) {
  Serial.println("A");   // send a capital A
  delay(300);
  }
} */

void lidar_data()
{
  for(i=30;i<=150;i++){ 
      //receive_data();
      myServo2.write(i);
      j= 180-i;
      myServo1.write(j);  
      delay(40);
      
      Serial.print(String(i)+","+String(myLidarLite.distance(true,true,0x64))+":"+String(myLidarLite.distance(true,true,0x66))+";"+String(myLidarLite.distance(true,true,0x68))+".");

      //receive_data();
      }
  
    for(i=150;i>30;i--){  
      //receive_data();
      myServo2.write(i);
      j= 180-i;
      myServo1.write(j);
      delay(40);
      Serial.print(String(i)+","+String(myLidarLite.distance(true,true,0x64))+":"+String(myLidarLite.distance(true,true,0x66))+";"+String(myLidarLite.distance(true,true,0x68))+".");

      }
}

