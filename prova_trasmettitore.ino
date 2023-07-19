#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);
const byte indirizzo[6] = "00001";

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

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(indirizzo);
  radio.setPALevel(RF24_PA_MAX);
  radio.setDataRate(RF24_250KBPS);
  radio.stopListening();
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(2, OUTPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  delay(100);
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(200);
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(200);
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(200);
  digitalWrite(2, HIGH);
  delay(1000);
  digitalWrite(2, LOW);
  delay(200);
}



void loop() {
  
  valore.x=analogRead(A0);
  valore.y=analogRead(A1);
  valore.z=analogRead(A2);
  valore.r=analogRead(A3);
  valore.x1=analogRead(A4);
  valore.x2=analogRead(A5);

  
  valore.b=digitalRead(3);
  valore.c=digitalRead(4);

  
  radio.write(&valore, sizeof(valore));
  delay(15);
}
