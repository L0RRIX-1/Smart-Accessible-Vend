#include <ESP32Servo.h>
int angolo = 0;

Servo myServo;  // Crea l'oggetto servo

void setup() {
  Serial.begin(115200);  // Avvia la comunicazione seriale
  myServo.attach(23);  // Attacca il servo al pin 23
}

void loop() {
  if (Serial.available()) {  // Se c'è qualcosa nella seriale
    String command = Serial.readString();  // Leggi il comando dalla seriale
    command.trim();

    if (command == "ROTATE_30") {
      angolo += 30;
  }
    if (angolo > 180) {
        angolo = 0;  // Resetta l'angolo a 0 gradi
      }
      myServo.write(angolo);  // Ruota il servo all'angolo aggiornato
      delay(1000);  // Pausa di 1 secondo
      Serial.print("Servo ruotato a ");
      Serial.print(angolo);
      Serial.println(" gradi.");
    } else {
      Serial.println("Comando sconosciuto");
    }
}
