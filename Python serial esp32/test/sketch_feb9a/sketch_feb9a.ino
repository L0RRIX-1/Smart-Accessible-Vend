#include <Servo.h>

Servo myServo;  // Crea l'oggetto servo

void setup() {
  Serial.begin(115200);  // Avvia la comunicazione seriale
  myServo.attach(9);  // Attacca il servo al pin 9 (modifica se necessario)
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();  // Leggi il comando seriale

    if (command == "ROTATE_30") {
      myServo.write(30);  // Ruota il servo a 30 gradi
      delay(1000);  // Pausa per 1 secondo
      Serial.println("Servo girato di 30 gradi.");
    }
  }
}
