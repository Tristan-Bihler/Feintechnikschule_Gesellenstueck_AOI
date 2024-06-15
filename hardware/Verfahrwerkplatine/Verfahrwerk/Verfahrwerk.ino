//Bibliotheken einbinden
#include <Wire.h>
#include <Adafruit_NeoPixel.h>

//Pinbelegung definieren
#define LED_PIN    17
#define NUM_LEDS   4
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

#define SDA_PIN 14
#define SCL_PIN 15
#define I2C_ADDRESS 0x08

#define X_STEP_PIN 18
#define X_DIR_PIN 20
#define Y_STEP_PIN 19
#define Y_DIR_PIN 21

#define X_MIN_END_SWITCH_PIN 13
#define X_MAX_END_SWITCH_PIN 12
#define Y_MIN_END_SWITCH_PIN 10
#define Y_MAX_END_SWITCH_PIN 11

#define power 0

//Variablen definieren
#define STEP_DELAY 800 
int receivedCode = 0;
int responseCode = 0;
int x = 0;
int y = 0;

void setup() {

  strip.begin();
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i,strip.Color(0, 0, 0));
    delay(1);
  }
  strip.show(); 
  Wire1.setSDA(SDA_PIN);
  Wire1.setSCL(SCL_PIN);
  Wire1.begin(I2C_ADDRESS);
  Wire1.onReceive(receiveEvent);
  Wire1.onRequest(requestEvent);
  Serial.begin(9600);

  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);

  pinMode(power, INPUT);
  pinMode(X_MIN_END_SWITCH_PIN, INPUT);
  pinMode(X_MAX_END_SWITCH_PIN, INPUT);
  pinMode(Y_MIN_END_SWITCH_PIN, INPUT);
  pinMode(Y_MAX_END_SWITCH_PIN, INPUT);
    
}

//Home Funktion um zu X0 Y0 zu fahren
int homeXY() {
  Serial.println("Homing Y-axis...");
  digitalWrite(Y_DIR_PIN, LOW); //Richtung definieren
  delay(100);
  while (digitalRead(Y_MIN_END_SWITCH_PIN) == LOW) { // Solange Endschalter nicht aktiv ist zu Y0 fahren
    if (digitalRead(power)== LOW){// Schleife unterbrehchen wenn der Strom für den Motor fehlt
      receivedCode = 0;
      return 0;
    }
    stepY();
  }
  digitalWrite(Y_DIR_PIN, HIGH);
  delay(1000);
  while (digitalRead(Y_MIN_END_SWITCH_PIN) == HIGH) {// Wenn 0 erreicht ist wieder ein bisschen rausfahren um 3d Druck toleranzen auszugleichen
    if (digitalRead(power)== LOW){// Schleife unterbrehchen wenn der Strom für den Motor fehlt
      receivedCode = 0;
      return 0;
    }
    stepY();
  }
  Serial.println("Y-axis homed.");

  Serial.println("Homing X-axis...");
  delay(1000);
  digitalWrite(X_DIR_PIN, HIGH);
  delay(1000);
  while (digitalRead(X_MIN_END_SWITCH_PIN) == LOW) {// Solange Endschalter nicht aktiv ist zu X0 fahren
    if (digitalRead(power)== LOW){// Schleife unterbrehchen wenn der Strom für den Motor fehlt
      powerloss();
      return 0;
    }
    stepX();
  }
  delay(1000);
  digitalWrite(X_DIR_PIN, LOW);
  delay(1000);
  while (digitalRead(X_MIN_END_SWITCH_PIN) == HIGH) {// Wenn 0 erreicht ist wieder ein bisschen rausfahren um 3d Druck toleranzen auszugleichen
    if (digitalRead(power)== LOW){// Schleife unterbrehchen wenn der Strom für den Motor fehlt
      powerloss();
      return 0;
    }
    stepX();
  }
  
  Serial.println("X-axis homed.");
  return 0;
}

// Ein schritt in X Richtung fahren
void stepX() {
  digitalWrite(X_STEP_PIN, HIGH);
  delayMicroseconds(STEP_DELAY);
  digitalWrite(X_STEP_PIN, LOW);
  delayMicroseconds(STEP_DELAY);
}

// Ein schritt in Y Richtung fahren
void stepY() {
  digitalWrite(Y_STEP_PIN, HIGH);
  delayMicroseconds(STEP_DELAY);
  digitalWrite(Y_STEP_PIN, LOW);
  delayMicroseconds(STEP_DELAY);
}

//Wenn der Strom für die Motoren nicht vorhanden ist Neopixel auf rot schalten und Raspberry Pi benachrichtigen
void powerloss(){
  receivedCode = 0;
  responseCode = 90;
  for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i,strip.Color(255, 0, 0));
      delay(1);
    }
    strip.show(); 
}

//Auf x Position fahren
int GoToX(int x){
  delay(1000);
  digitalWrite(X_DIR_PIN, LOW);// Motor in die richtige richtung fahren lassen
  delay(1000);
  for (int i = 0; i <= x; i++){
    stepX();//ein Schritt fahren
    if (digitalRead(power)== LOW){// Wenn Strom unterbrochen ist Raspberry Pi benachrichtgen und schleife verlassen
      powerloss();
      return 0;
    }
  }
  return 0;
}

//Auf y Position fahren
int GoToY(int y){
  delay(1000);
  digitalWrite(Y_DIR_PIN, HIGH); // Motor in die richtige richtung fahren lassen
  delay(1000);
  for (int i = 0; i <= y; i++){
    stepY(); //ein Schritt fahren
    if (digitalRead(power)== LOW){ // Wenn Strom unterbrochen ist Raspberry Pi benachrichtgen und schleife verlassen
      powerloss();
      return 0;
    }
  }
  return 0;
}

int programm(){ //Programm funktion erstellen um einfacher die schleife zu unterbrechen, falls die Stromversorgung für die Motoren fehlt
  if (receivedCode == 120){
    for (int i = 0; i < strip.numPixels(); i++) {   //LED´s am start ausschalten
      strip.setPixelColor(i,strip.Color(0, 0, 0));
      delay(1);
    } 
    strip.show(); 
    homeXY(); // Automatisch auf X0 Y0 fahren
    delay(1000);
    if (x <= 100){
      x = map(x, 0, 100, 0, 38780); // überprüfen das x auch ein nützlicher Wert ist und auf X fahren
      GoToX(x);
    }
    else{ // Schleife unterbrechen wenn X nicht richtig übernommen worden ist
      powerloss();
      return 0;
    }
    delay(1000);
    if (y <= 100){ // überprüfen das y auch ein nützlicher Wert ist und auf X fahren
      y = map(y, 0, 100, 0, 12076);
      GoToY(y);
    }
    else{// Schleife unterbrechen wenn y nicht richtig übernommen worden ist
      powerloss();
      return 0;
    }
    receivedCode = 0;
    responseCode = 40; // Wenn die Position erreicht ist, Raspberry Pi benachrichtigen.
  }
  if (receivedCode == 130){ // Wenn der Raspberry Pi bereit ist ein bild zu schiesen leds anschalten
    for (int i = 0; i < strip.numPixels(); i++) {
      strip.setPixelColor(i,strip.Color(255, 255, 255));
      delay(1);
    }
    strip.show();
    delay(1000);
    receivedCode = 0;
    responseCode = 50; // Raspberry Pi benachrichtigen ein Bild aufzunehmen
 }
  if (receivedCode == 140){ // Wenn der Raspberry Pi fertig ist mit dem Bild die Neopixel auschalten und zu Home fahren.
    delay(1000);
      for (int i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i,strip.Color(0, 0, 0));
        delay(1);
      }
      strip.show(); 
      homeXY();
      receivedCode = 0;
      responseCode = 60; // Raspberry Pi benachrichtigen das es wieder auf Home ist.
    }
  return 0;
}
void loop() {
  if (digitalRead(power)== LOW){
    powerloss();
  }
  else{
    programm();
  }
}

void receiveEvent(int howMany) {
  while (Wire1.available()) { //Alle Bytes auch richtig auslesen
    receivedCode = Wire1.read();
    Serial.print("Received: ");
    Serial.println(receivedCode);
  }
  if (receivedCode == 110){//I2C Verbindung bestätigen
    responseCode = 10;
  }
  else if (responseCode == 20 && receivedCode <= 100){  //Den erhaltenen I2C Wert auf Y übernehmen
    y = receivedCode;
    responseCode = 30;
  }
  else if (responseCode == 10 && receivedCode <= 100){  //Den erhaltenen I2C Wert auf X übernehmen
    x = receivedCode;
    responseCode = 20;
  }
  
}
void requestEvent() {
  Wire1.write(responseCode); // Wenn Raspberry Pi Daten erhalten möchte den responseCode auch zurücksenden
  Serial.print("Sent: ");
  Serial.println(responseCode);
}