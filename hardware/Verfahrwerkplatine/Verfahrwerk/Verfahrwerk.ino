#include <Wire.h>
#define stepPin 2
#define dirPin 3
char c;
// LED on pin 13

void setup() {
  // Join I2C bus as slave with address 8
  Serial.begin(9600);
  Wire.setSDA(0);
  Wire.setSCL(1);
  Wire.begin(0x8);
  // Call receiveEvent when data received
  Wire.onReceive(receiveEvent);

  // Setup pin 13 as output and turn LED off
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) {  // loop through all but the last
    char c = Wire.read();     // receive byte as a character
    Serial.write(c);
    Serial.println(c);
  }
  
  if (c == HIGH) {
    digitalWrite(dirPin, c);  // Enables the motor to move in a particular direction
    // Makes 200 pulses for making one full cycle rotation
    for (int x = 0; x < 800; x++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(700);  // by changing this time delay between the steps we can change the rotation speed
      digitalWrite(stepPin, LOW);
      delayMicroseconds(700);
    }
    delay(1000);  // One second delay
  } else if (c == LOW) {
    digitalWrite(dirPin, c);  //Changes the rotations direction
    // Makes 400 pulses for making two full cycle rotation
    for (int x = 0; x < 1600; x++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(700);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(700);
    }
  }
}
void loop() {
  Wire.onReceive(receiveEvent);
  delay(1000);
}