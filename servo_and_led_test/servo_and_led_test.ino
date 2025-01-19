#include <Arduino.h>
#include <ESP32Servo.h>
Servo myServo;

int servopin = 22;


void setup() {
  pinMode(23, OUTPUT);
  myServo.attach(servopin);
  myServo.write(0);
 

}

void loop() {

  digitalWrite(23, HIGH);
  myServo.write(90);
  delay(1000);
  digitalWrite(23, LOW);
  myServo.write(180);
  delay(1000);


}
