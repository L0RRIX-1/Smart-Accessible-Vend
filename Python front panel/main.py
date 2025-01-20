import tkinter as tk
import serial
import serial.tools.list_ports
import time

# Funzione per inizializzare la connessione seriale
def initialize_serial(port, baudrate):
    try:
        esp32 = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Attendi l'inizializzazione
        return esp32
    except serial.SerialException:
        return None

# Cerca automaticamente la porta seriale dell'ESP32
def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:  # Modifica se necessario
            return port.device
    return None

# Configura la connessione seriale
port = find_esp32_port()
esp32 = initialize_serial(port, 115200) if port else None

# Funzioni per inviare comandi
def led_on():
    if esp32:
        esp32.write(b'LED ON\n')
        feedback_label.config(text="LED acceso (comando inviato)")
    else:
        feedback_label.config(text="Errore: ESP32 non collegato")

def led_off():
    if esp32:
        esp32.write(b'LED OFF\n')
        feedback_label.config(text="LED spento (comando inviato)")
    else:
        feedback_label.config(text="Errore: ESP32 non collegato")

# Crea la finestra Tkinter
root = tk.Tk()
root.title("Controllo ESP32")

# Pulsanti e etichette
feedback_label = tk.Label(root, text="Stato: Nessuna azione", font=("Arial", 12))
feedback_label.pack(pady=10)

on_button = tk.Button(root, text="Accendi LED", command=led_on, font=("Arial", 12))
on_button.pack(pady=5)

off_button = tk.Button(root, text="Spegni LED", command=led_off, font=("Arial", 12))
off_button.pack(pady=5)

# Avvia la finestra
root.mainloop()

# Chiudi la connessione seriale alla chiusura della GUI
if esp32:
    esp32.close()
