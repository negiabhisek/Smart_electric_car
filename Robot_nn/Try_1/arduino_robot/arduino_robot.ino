void setup() {
  pinMode(38,INPUT);
  pinMode(39,INPUT);
  pinMode(40,INPUT);
  pinMode(41,INPUT);
  
  pinMode(22,OUTPUT);
  pinMode(23,OUTPUT);
  pinMode(24,OUTPUT);
  pinMode(25,OUTPUT);
  
  Serial.begin(9600);
  analogWrite(6,225);
  analogWrite(7,225);
  
//  pinMode(6,OUTPUT);
//  pinMode(7,OUTPUT);
//  digitalWrite(6,HIGH);
//  digitalWrite(7,HIGH);
  
  // put your setup code here, to run once:

}
int a,b,c,d;
void loop() {
  a = digitalRead(39);
  b = digitalRead(41);
  c = digitalRead(40);
  d = digitalRead(38);
  
//  Serial.print(a);
//  Serial.print(b);
//  Serial.print(c);
//  Serial.println(d);
  Serial.println(String(a)+","+String(b)+":"+String(c)+";"+String(d)+".");
  if ((b== 1 && d==1)||(a==1 && c==1))
  {
    analogWrite(6,180);
    analogWrite(7,180);
  }
  digitalWrite(25,a);
  digitalWrite(23,b);
  digitalWrite(22,c);
  digitalWrite(24,d);
  
  // put your main code here, to run repeatedly:
  analogWrite(6,225);
  analogWrite(7,225);
}
