#include <Wire.h>
#define stepPin 0
#define dirPin 1
char c;
// LED on pin 13

void setup() {

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

void loop() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(500);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(500);
}