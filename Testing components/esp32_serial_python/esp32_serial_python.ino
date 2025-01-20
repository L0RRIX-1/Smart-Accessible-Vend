void setup() {
  Serial.begin(115200);   // Avvia la comunicazione seriale
  pinMode(2, OUTPUT);     // Configura il pin GPIO 2 come uscita (per il LED)
  digitalWrite(2, LOW);   // Assicura che il LED sia spento all'avvio

  // Messaggio di debug per confermare l'avvio
  Serial.println("ESP32 pronto. Attendo comandi...");
}

void loop() {
  if (Serial.available() > 0) {             // Controlla se ci sono dati ricevuti
    String command = Serial.readStringUntil('\n'); // Legge i dati fino al newline
    command.trim();                         // Rimuove eventuali spazi o newline extra

    // Esegue un'azione in base al comando ricevuto
    if (command == "LED ON") {
      digitalWrite(2, HIGH);               // Accendi il LED
      Serial.println("LED acceso");       // Risposta seriale
    } else if (command == "LED OFF") {
      digitalWrite(2, LOW);                // Spegni il LED
      Serial.println("LED spento");       // Risposta seriale
    } else {
      Serial.println("Comando non riconosciuto: " + command);
    }
  }
}
