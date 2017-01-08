// Proje Hocam - Radar Projesi
// Murat DURAN - V2
import processing.serial.*; // kütüphane entegresi
import java.awt.event.KeyEvent; 
import java.io.IOException;
import processing.net.*; 

 
Serial myPort; 
 
Client myClient; 
int dataIn; 

 
void setup() {

 String portName = Serial.list()[0]; //change the 0 to a 1 or 2 etc. to match your port
  myPort = new Serial(this, portName, 115200);
  myClient = new Client(this, "localhost", 50002); 
 
}
 String val,val1,val2;
void draw() {
  //
  //{
    if ( myPort.available() > 0) 
    {  // If data is available,
      val = myPort.readStringUntil('.');         // read it and store it in val
      val1 = "\0";
      val2 = "Now";
      //val=  val2+val1;
      //if (myClient.available() > 0)
      if (val!=null)
        myClient.write(val);
      println(val); //print it out in the console
    }
  //}
  
  
}
 void mousePressed() {
  myClient.stop();
  exit();
}