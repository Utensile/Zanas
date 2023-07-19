#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

RF24 radio(9, 10);
const byte indirizzo[6] = "00001";
Servo myservo;
int pos=0, val=0;

struct val{
  int x;
  int y;
  int z;
  int r;
  int x1;
  int x2;
  bool b;
  bool c;
}valore;
//char valore[10];


void setup() {
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  myservo.attach(5);
   
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(0, indirizzo);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.startListening();
  for(int i=0; i<5; i++){
    
      digitalWrite(2, HIGH);
      delay(200); 
      digitalWrite(2, LOW);
      delay(200); 
  }
      digitalWrite(2, HIGH);
      delay(200); 
}






int i=0, g=0;







int h=0;

void loop() {

  if(radio.available()){
    
    radio.read(&valore, sizeof(valore));

    //SERVO
    pos=valore.x1;
    pos=map(pos, 0, 1023, 0, 180);
    pos=180-pos;
    pos=pos-7;
    
    if(pos>135){
      pos=135;
    }
    if(pos<45){
      pos=45;
    }
    Serial.print("x=");
    Serial.println(pos);
    myservo.write(pos);
    delay(15);
  
    //MOTORE
    
    val=valore.z;
    val=map(val, 0, 1023, -255, 255);
    if(val<-100){
      digitalWrite(7, HIGH);
      digitalWrite(8, LOW);
      val=-val;
      if(val>180){
        val=180;
      }
    } 
    else if(val<100 and val>-100){
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
    }
    else if(val>100){
      digitalWrite(7, LOW);
      digitalWrite(8, HIGH);
    }  
    //Serial.println(val);
    analogWrite(6, val);

    
    
    
    
/*
    Serial.print("y=");
    Serial.println(valore.y);
    Serial.print("z=");
    Serial.println(valore.z);*/
    
}

}




   
  
 
