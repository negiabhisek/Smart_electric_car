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
  myPort = new Serial(this, portName, 9600);
  myClient = new Client(this, "localhost", 50009); 
 
}
 String val,val1,val2;
void draw() {
  if ( true) 
  {  // If data is available,
    print("data found");
    val = myPort.readStringUntil('.');         // read it and store it in val
    //val = "0,0:0;0.";
    val1 = "\0";
    val2 = "Now";
    //val=  val2+val1;
    
    if (val!=null)
    {
      myClient.write(val);
      print (myClient.available());
      while (myClient.available() <= 0);
      println(val); //print it out in the console
      //dataIn = myClient.read(); 
      //print(dataIn);
      myPort.write("0");
    }
  }
  
  
}
 void mousePressed() {
  myClient.stop();
  exit();
}