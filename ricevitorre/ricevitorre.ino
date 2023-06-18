#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8); // CE, CSN

const byte addresses[][6] = {"00001", "00002"};


void setup() {
  radio.begin();
  //indirizzi sono assegnati invertiti
  radio.openWritingPipe(addresses[0]); 
  radio.openReadingPipe(1, addresses[1]); 
  radio.setPALevel(RF24_PA_MIN);
}
void loop() {
  delay(5);
  radio.startListening();
  
  if ( radio.available()) {
    while (radio.available()) {
      int led;
      radio.read(&led, sizeof(led));
      Serial.print("ricevo:");
      Serial.println(led);
    }
    delay(5);
    radio.stopListening();
    int bt = digitalRead(3);
    Serial.print("invio:"); Serial.println(bt);
    radio.write(&bt, sizeof(bt));
    
  }
  
}