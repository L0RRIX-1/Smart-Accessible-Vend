import tkinter as tk
import serial
import time

# Configura la porta seriale USB del tuo ESP32
SERIAL_PORT = "COM3"  # Cambia con la porta corretta (es: "/dev/ttyUSB0" su Linux)
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Attendi la connessione seriale
except Exception as e:
    print(f"Errore apertura seriale: {e}")
    ser = None

def send_signal():
    if ser:
        ser.write(b'1')  # Invia il carattere '1' all'ESP32
        print("Dato inviato: 1")

def close_serial():
    if ser:
        ser.close()
    root.quit()

# Creazione GUI con Tkinter
root = tk.Tk()
root.title("ESP32 USB Serial Controller")

button = tk.Button(root, text="Invia Segnale", command=send_signal, font=("Arial", 14))
button.pack(pady=20)

exit_button = tk.Button(root, text="Esci", command=close_serial, font=("Arial", 12))
exit_button.pack(pady=10)

root.mainloop()
