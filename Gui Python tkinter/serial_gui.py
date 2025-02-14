import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import serial
import time

# Percorso assoluto della directory contenente lo script
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "images")

# Configurazione della connessione seriale con ESP32 sulla porta COM3
# Modifica la porta e il baud rate se necessario
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)  # Attendi che la connessione seriale si stabilisca
if ser.is_open:
    print("Connessione stabilita con successo")
    


# Funzione per gestire l'acquisto di un elemento
def purchase_item(item, price):
    # Mostra una finestra di messaggio di conferma dell'acquisto
    messagebox.showinfo("Acquisto completato", f"Hai acquistato: {item} per €{price:.2f}")
    
    # Invia i dati via seriale all'ESP32
    purchase_message = f"Acquisto: {item} - €{price:.2f}\n"
    if ser.is_open:
        ser.write(purchase_message.encode())  # Invia il messaggio seriale all'ESP32
        print(f"Messaggio inviato a ESP32: {purchase_message}")
        
        # Invia il comando per girare il servo di 30 gradi
        ser.write(b'ROTATE_30')  # Comando per girare il servo di 30 gradi
        print("Comando per girare il servo inviato!")

# Funzione per creare un'immagine circolare
def create_circle_image(image_path, size=(100, 100)):
    try:
        img = Image.open(image_path)
        img = img.resize(size, Image.LANCZOS)  # Ingigantiamo l'immagine
        
        # Crea una maschera circolare
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)

        # Applica la maschera all'immagine
        img.putalpha(mask)

        img = img.convert("RGB")  # Converti a RGB per la visualizzazione corretta
        img = ImageTk.PhotoImage(img)
        return img
    except FileNotFoundError:
        print(f"File non trovato: {image_path}")
        return None

# Funzione per mostrare gli articoli di una categoria
def show_items(category):
    for widget in items_frame.winfo_children():
        widget.destroy()

    row = 0
    col = 0
    max_cols = 2  # Numero massimo di colonne per gli articoli

    for item, price, color, image_path in categories[category]:
        item_frame = tk.Frame(items_frame, bg="#2C3E50", pady=20)
        item_frame.grid(row=row, column=col, padx=30, pady=10, sticky="w")

        # Calcola il percorso assoluto per l'immagine
        full_image_path = os.path.join(image_dir, image_path)

        img = create_circle_image(full_image_path, size=(120, 120))  # Circolare e ingrandita

        if img:
            img_label = tk.Label(item_frame, image=img, bg="#2C3E50")
            img_label.image = img  # Necessario per mantenere un riferimento all'immagine
            img_label.pack(side=tk.TOP, pady=10)

        item_button = tk.Button(
            item_frame,
            text=f"{item} - €{price:.2f}",
            font=("Arial", 24, "bold"),
            width=24,
            height=2,
            bg=color,
            fg="white",
            command=lambda i=item, p=price: purchase_item(i, p)
        )
        item_button.pack(side=tk.TOP, pady=10)

        col += 1
        if col == max_cols:
            col = 0
            row += 1

# Funzione per mostrare tutti gli articoli sulla schermata Home
def show_all_items():
    for widget in items_frame.winfo_children():
        widget.destroy()

    row = 0
    col = 0
    max_cols = 3  # Numero massimo di colonne per gli articoli

    for category in categories:
        for item, price, color, image_path in categories[category]:
            item_frame = tk.Frame(items_frame, bg="#2C3E50", pady=20)
            item_frame.grid(row=row, column=col, padx=30, pady=10, sticky="w")

            # Calcola il percorso assoluto per l'immagine
            full_image_path = os.path.join(image_dir, image_path)

            img = create_circle_image(full_image_path, size=(120, 120))  # Circolare e ingrandita

            if img:
                img_label = tk.Label(item_frame, image=img, bg="#2C3E50")
                img_label.image = img  # Necessario per mantenere un riferimento all'immagine
                img_label.pack(side=tk.TOP, pady=10)

            item_button = tk.Button(
                item_frame,
                text=f"{item} - €{price:.2f}",
                font=("Arial", 18, "bold"),
                width=30,
                height=2,
                bg=color,
                fg="white",
                command=lambda i=item, p=price: purchase_item(i, p)
            )
            item_button.pack(side=tk.TOP, pady=10)

            col += 1
            if col == max_cols:
                col = 0
                row += 1

# Configurazione della finestra principale
root = tk.Tk()
root.title("Vending Machine")
root.geometry("800x600")
root.resizable(False, False)
root.config(bg="#2C3E50")

# Titolo della vending machine
title_label = tk.Label(root, text="Benvenuto nella Vending Machine", font=("Arial", 24, "bold"), pady=30, fg="white", bg="#2C3E50")
title_label.pack()

# Frame principale per la barra laterale e gli articoli
main_frame = tk.Frame(root, bg="#2C3E50")
main_frame.pack(fill=tk.BOTH, expand=True)

# Sidebar per le categorie
sidebar = tk.Frame(main_frame, bg="#34495E", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Pulsante Home (in alto sopra le categorie)
home_button = tk.Button(
    sidebar,
    text="Home",
    font=("Arial", 28, "bold"),
    width=15,
    height=2,
    bg="#34495E",
    fg="white",
    command=show_all_items
)
home_button.pack(pady=20)

# Frame per mostrare gli oggetti
items_frame = tk.Frame(main_frame, bg="#2C3E50")
items_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Definizione delle categorie e degli oggetti con prezzi, colori e immagini
categories = {
    "Cibo": [
        ("Panino", 4.50, "#E74C3C", "panino.png"),
        ("Pizza", 6.00, "#C0392B", "pizza.png"),
        ("Insalata", 5.00, "#27AE60", "insalata.png"),
    ],
    "Bevande": [
        ("Acqua", 1.00, "#3498DB", "acqua.png"),
        ("Caffè", 1.50, "#6C3483", "caffe.png"),
        ("Tè", 1.20, "#1ABC9C", "te.png"),
        ("Succo", 2.00, "#F1C40F", "succo.png"),
    ],
    "Snack": [
        ("Barretta", 1.80, "#E67E22", "barretta.png"),
        ("Patatine", 2.50, "#D35400", "patatine.png"),
        ("Cioccolato", 2.00, "#8E44AD", "cioccolato.png"),
    ],
}

# Creazione dei pulsanti per le categorie
for category in categories:
    category_button = tk.Button(
        sidebar,
        text=category,
        font=("Arial", 24, "bold"),
        width=15,
        height=2,
        bg="#34495E",
        fg="white",
        command=lambda c=category: show_items(c)
    )
    category_button.pack(pady=20)

# Footer
footer_label = tk.Label(root, text="Smart Accessible Vend by Lorrix", font=("Arial", 14), pady=20, fg="white", bg="#2C3E50")
footer_label.pack(side=tk.BOTTOM)

# Mostra gli articoli inizialmente
show_all_items()

# Avvio della finestra principale
root.mainloop()

# Chiudi la connessione seriale quando il programma termina
ser.close()
