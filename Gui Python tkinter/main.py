import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Percorso assoluto della directory contenente lo script
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "images")

# Funzione per gestire l'acquisto di un elemento
def purchase_item(item, price):
    messagebox.showinfo("Acquisto completato", f"Hai acquistato: {item} per €{price:.2f}")

# Funzione per mostrare gli elementi di una categoria
def show_items(category):
    for widget in items_frame.winfo_children():
        widget.destroy()

    for item, price, color, image_path in categories[category]:
        item_frame = tk.Frame(items_frame, bg="#ECF0F1", pady=10)
        item_frame.pack(fill=tk.X, padx=20, pady=5)

        # Calcola il percorso assoluto per l'immagine
        full_image_path = os.path.join(image_dir, image_path)

        try:
            img = Image.open(full_image_path)
            img = img.resize((50, 50), Image.LANCZOS)  # Sostituito ANTIALIAS con LANCZOS
            img = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"File non trovato: {full_image_path}")
            continue

        img_label = tk.Label(item_frame, image=img, bg="#ECF0F1")
        img_label.image = img  # Necessario per mantenere un riferimento all'immagine
        img_label.pack(side=tk.LEFT, padx=10)

        item_button = tk.Button(
            item_frame,
            text=f"{item} - €{price:.2f}",
            font=("Arial", 16),
            width=20,
            bg=color,
            fg="white",
            command=lambda i=item, p=price: purchase_item(i, p)
        )
        item_button.pack(side=tk.LEFT, padx=10)

# Configurazione della finestra principale
root = tk.Tk()
root.title("Vending Machine")
root.geometry("1200x700")
root.resizable(False, False)

# Titolo della vending machine
title_label = tk.Label(root, text="Benvenuto nella Vending Machine", font=("Arial", 24, "bold"), pady=20)
title_label.pack()

# Frame principale per la barra laterale e gli articoli
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Sidebar per le categorie
sidebar = tk.Frame(main_frame, bg="#2C3E50", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

sidebar_label = tk.Label(sidebar, text="Categorie", font=("Arial", 20, "bold"), bg="#2C3E50", fg="white")
sidebar_label.pack(pady=20)

# Frame per mostrare gli oggetti
items_frame = tk.Frame(main_frame, bg="#ECF0F1")
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
        font=("Arial", 16),
        width=15,
        bg="#34495E",
        fg="white",
        command=lambda c=category: show_items(c)
    )
    category_button.pack(pady=10)

# Footer
footer_label = tk.Label(root, text="Grazie per aver usato la nostra Vending Machine!", font=("Arial", 14), pady=10)
footer_label.pack(side=tk.BOTTOM)

# Avvio della finestra principale
root.mainloop()
