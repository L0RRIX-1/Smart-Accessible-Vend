import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os

# Percorso assoluto della directory contenente lo script
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "images")

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
        img_label.image = img  # Necessario per mantenere il riferimento
        img_label.pack(pady=20)
    
    label = tk.Label(confirm_window, text=f"Acquistare {item} per €{price:.2f}?", font=("Arial", 16), fg="white", bg="#2C3E50")
    label.pack(pady=10)
    
    button_frame = tk.Frame(confirm_window, bg="#2C3E50")
    button_frame.pack(pady=20)
    
    confirm_button = tk.Button(button_frame, text="✔", font=("Arial", 20, "bold"), fg="white", bg="#27AE60", width=5, height=2, command=lambda: complete_purchase(confirm_window, item, price))
    confirm_button.grid(row=0, column=0, padx=10)
    
    cancel_button = tk.Button(button_frame, text="✖", font=("Arial", 20, "bold"), fg="white", bg="#E74C3C", width=5, height=2, command=confirm_window.destroy)
    cancel_button.grid(row=0, column=1, padx=10)

def complete_purchase(window, item, price):
    window.destroy()
    messagebox.showinfo("Acquisto Completato", f"Hai acquistato: {item} per €{price:.2f}")

def create_circle_image(image_path, size=(100, 100)):
    try:
        img = Image.open(image_path).resize(size, Image.LANCZOS)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        img.putalpha(mask)
        img = img.convert("RGB")
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print(f"File non trovato: {image_path}")
        return None

def purchase_item(item, price, image_path):
    confirm_purchase(item, price, image_path)

# Configurazione finestra principale
root = tk.Tk()
root.title("Vending Machine")
root.geometry("800x600")
root.config(bg="#2C3E50")

# Esempio di chiamata alla funzione (da sostituire con un'implementazione nel codice esistente)
purchase_item("Panino", 4.50, "panino.png")

root.mainloop()
