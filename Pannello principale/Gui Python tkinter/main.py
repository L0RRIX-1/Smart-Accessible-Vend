import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os

# Percorso assoluto della directory contenente lo script
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "images")
def complete_purchase(window, item, price):
    print(f"Acquisto completato: {item} - {price}€")
    window.destroy()


# Funzione per gestire l'acquisto di un elemento
def confirm_purchase(item, price, image_path):
    confirm_window = tk.Toplevel(root)
    confirm_window.title("Conferma Acquisto")
    confirm_window.geometry("400x400")
    confirm_window.config(bg="#2C3E50")

    # Caricamento immagine
    full_image_path = os.path.join(image_dir, image_path)
    img = create_circle_image(full_image_path, size=(200, 200))
    if img:
        img_label = tk.Label(confirm_window, image=img, bg="#2C3E50")
        img_label.image = img  # Mantiene il riferimento all'immagine
        img_label.pack(pady=20)

    label = tk.Label(confirm_window, text=f"Acquistare {item} per €{price:.2f}?", font=("Arial", 16), fg="white", bg="#2C3E50")
    label.pack(pady=10)

    button_frame = tk.Frame(confirm_window, bg="#2C3E50")
    button_frame.pack(pady=20)

    

    confirm_button = tk.Button(
        button_frame, text="✔", font=("Arial", 20, "bold"), fg="white", bg="#27AE60",
        width=5, height=2, command=lambda: complete_purchase(confirm_window, item, price)
    )
    confirm_button.grid(row=0, column=0, padx=10)

    cancel_button = tk.Button(
        button_frame, text="✖", font=("Arial", 20, "bold"), fg="white", bg="#E74C3C",
        width=5, height=2, command=confirm_window.destroy
    )
    cancel_button.grid(row=0, column=1, padx=10)
import time

def complete_purchase(window, item, price):
    # Cancella il contenuto della finestra di conferma
    for widget in window.winfo_children():
        widget.destroy()
    
    window.title("Acquisto Completato")

    # Icona di spunta verde
    check_label = tk.Label(window, text="✔", font=("Arial", 50, "bold"), fg="#27AE60", bg="#2C3E50")
    check_label.pack(pady=20)

    # Messaggio di successo
    success_label = tk.Label(window, text="Acquisto completato con successo!", font=("Arial", 16), fg="white", bg="#2C3E50")
    success_label.pack(pady=10)

    # Chiude la finestra dopo 3 secondi
    window.after(3000, window.destroy)


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
# Funzione per gestire la selezione di un articolo
def purchase_item(item, price, image_path):
    confirm_purchase(item, price, image_path)


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
            command=lambda i=item, p=price, img=image_path: purchase_item(i, p, img)
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
                command=lambda i=item, p=price, img=image_path: purchase_item(i, p, img)
            )
            item_button.pack(side=tk.TOP, pady=10)

            col += 1
            if col == max_cols:
                col = 0
                row += 1

# Configurazione della finestra principale
root = tk.Tk()
root.title("Vending Machine")
root.geometry("1860x1000")
root.resizable(False, False)
root.config(bg="#2C3E50")

# Funzione per cercare gli articoli
def search_items(event=None):
    query = search_entry.get().lower().strip()

    # Pulisce la visualizzazione corrente
    for widget in items_frame.winfo_children():
        widget.destroy()

    # Controlla se la ricerca è vuota, in tal caso mostra tutto
    if query == "":
        show_all_items()
        return

    row = 0
    col = 0
    max_cols = 3
    found = False  # Flag per controllare se sono stati trovati risultati

    # Cerca in tutte le categorie
    for category in categories:
        for item, price, color, image_path in categories[category]:
            # Controlla se il nome dell'articolo contiene il testo inserito
            if query in item.lower():
                found = True
                item_frame = tk.Frame(items_frame, bg="#2C3E50", pady=20)
                item_frame.grid(row=row, column=col, padx=30, pady=10, sticky="w")

                full_image_path = os.path.join(image_dir, image_path)
                img = create_circle_image(full_image_path, size=(120, 120))

                if img:
                    img_label = tk.Label(item_frame, image=img, bg="#2C3E50")
                    img_label.image = img
                    img_label.pack(side=tk.TOP, pady=10)

                item_button = tk.Button(
                    item_frame,
                    text=f"{item} - €{price:.2f}",
                    font=("Arial", 18, "bold"),
                    width=30,
                    height=2,
                    bg=color,
                    fg="white",
                    command=lambda i=item, p=price, img=image_path: purchase_item(i, p, img)
                )
                item_button.pack(side=tk.TOP, pady=10)

                col += 1
                if col == max_cols:
                    col = 0
                    row += 1

    # Se nessun risultato è stato trovato, mostra un messaggio
    if not found:
        no_result_label = tk.Label(
            items_frame,
            text="Nessun articolo trovato.",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#2C3E50"
        )
        no_result_label.pack(pady=50)

# Barra di ricerca (in alto a destra)
search_frame = tk.Frame(root, bg="#2C3E50")
search_frame.place(x=1500, y=20)  # Posizione in alto a destra

search_label = tk.Label(search_frame, text="Cerca:", font=("Arial", 18), fg="white", bg="#2C3E50")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, font=("Arial", 18), width=20)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(
    search_frame,
    text="Cerca",
    font=("Arial", 18),
    bg="#16A085",
    fg="white",
    command=lambda: search_items()  # Esegui la ricerca al clic
)
search_button.pack(side=tk.LEFT, padx=5)

# Aggiunta dell'evento per la ricerca quando si digita
search_entry.bind("<KeyRelease>", search_items)

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
