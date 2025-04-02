import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Configurazioni stilistiche
LARGE_FONT = ('Helvetica', 18)
BUTTON_STYLE = {
    'font': ('Helvetica', 20, 'bold'),
    'padding': 15,
    'width': 15
}
IMAGE_SIZE = 200  # Aumento dimensione immagini
BG_COLOR = '#F5F5F5'
PRIMARY_COLOR = '#2E7D32'
TEXT_COLOR = '#263238'

# Verifica che la cartella images esista
if not os.path.exists('images'):
    os.makedirs('images')
    messagebox.showwarning("Attenzione", "La cartella 'images' è stata creata. Inserisci le immagini dei prodotti.")

products = {
    'snack': {
        'barretta': {'price': 1.50, 'image': 'barretta.png'},
        'cioccolato': {'price': 2.00, 'image': 'cioccolato.png'},
        'insalata': {'price': 3.50, 'image': 'insalata.png'},
        'panino': {'price': 4.00, 'image': 'panino.png'},
        'patatine': {'price': 2.50, 'image': 'patatine.png'},
        'pizza': {'price': 5.00, 'image': 'pizza.png'},
    },
    'bevande': {
        'acqua': {'price': 1.00, 'image': 'acqua.png'},
        'caffe': {'price': 1.20, 'image': 'caffe.png'},
        'succo': {'price': 2.00, 'image': 'succo.png'},
        'te': {'price': 1.50, 'image': 'te.png'},
    }
}

class VendingMachine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Distributore Automatico")
        self.geometry("1024x768")  # Schermo più grande
        self.configure(bg=BG_COLOR)
        
        # Configurazione stili globali
        self.style = ttk.Style()
        self.style.configure('Main.TFrame', background=BG_COLOR)
        self.style.configure('Product.TFrame', background='white', borderwidth=2, relief='groove')
        self.style.configure('Nav.TButton', font=('Helvetica', 16), padding=10)
        self.style.configure('Action.TButton', font=('Helvetica', 16, 'bold'), padding=10)
        self.style.configure('Success.TButton', font=('Helvetica', 18, 'bold'), padding=15, foreground='white', background='#388E3C')
        self.style.configure('Danger.TButton', font=('Helvetica', 18, 'bold'), padding=15, foreground='white', background='#D32F2F')
        
        container = ttk.Frame(self, style='Main.TFrame')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomeFrame, SnacksFrame, DrinksFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomeFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class BaseFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Main.TFrame')
        self.controller = controller

class HomeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        ttk.Label(self, text="DISTRIBUTORE AUTOMATICO", 
                 font=('Helvetica', 28, 'bold'), 
                 foreground=PRIMARY_COLOR).pack(pady=40)
        
        ttk.Label(self, text="Seleziona categoria:", 
                 font=LARGE_FONT, 
                 foreground=TEXT_COLOR).pack(pady=20)

        btn_style = ttk.Style()
        btn_style.configure('Big.TButton', font=BUTTON_STYLE['font'], 
                          padding=BUTTON_STYLE['padding'])
        
        ttk.Button(self, text="🍔 SNACK", 
                  style='Big.TButton',
                  command=lambda: controller.show_frame(SnacksFrame)
                  ).pack(pady=15)
        
        ttk.Button(self, text="🥤 BEVANDE", 
                  style='Big.TButton',
                  command=lambda: controller.show_frame(DrinksFrame)
                  ).pack(pady=15)

class ProductFrame(BaseFrame):
    def create_products(self, category):
        # Pulsante ritorno
        ttk.Button(self, text="◀ HOME", 
                  style='Nav.TButton',
                  command=lambda: self.controller.show_frame(HomeFrame)
                  ).grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Griglia prodotti
        row, col = 1, 0
        for product, info in products[category].items():
            product_frame = ttk.Frame(self, padding=20, style='Product.TFrame')
            product_frame.grid(row=row, column=col, padx=20, pady=20)

            # Caricamento immagine con gestione errori
            try:
                img_path = os.path.join('images', info['image'])
                img = Image.open(img_path).resize((IMAGE_SIZE, IMAGE_SIZE))
                photo = ImageTk.PhotoImage(img)
                
                img_label = ttk.Label(product_frame)
                img_label.image = photo  # Mantieni riferimento all'immagine
                img_label.configure(image=photo)
                img_label.pack(pady=10)
                
            except Exception as e:
                print(f"Errore caricamento immagine {info['image']}: {str(e)}")
                img_label = ttk.Label(product_frame, text="[IMMAGINE NON TROVATA]", 
                                     font=('Helvetica', 12), foreground='red')
                img_label.pack(pady=10)
            
            ttk.Label(product_frame, text=product.upper(), 
                     font=('Helvetica', 16, 'bold'),
                     foreground=TEXT_COLOR).pack()
            ttk.Label(product_frame, text=f"€{info['price']:.2f}", 
                     font=('Helvetica', 20),
                     foreground=PRIMARY_COLOR).pack(pady=5)
            
            ttk.Button(product_frame, text="SELEZIONA",
                      style='Action.TButton',
                      command=lambda p=product, pr=info['price']: 
                      ConfirmWindow(self.controller, p, pr)
                      ).pack(pady=10)

            col += 1
            if col > 1:  # Solo 2 colonne per migliore leggibilità
                col = 0
                row += 1

class SnacksFrame(ProductFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_products('snack')

class DrinksFrame(ProductFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_products('bevande')

class ConfirmWindow(tk.Toplevel):
    def __init__(self, controller, product, price):
        super().__init__(controller)
        self.title("Conferma Acquisto")
        self.geometry("500x300")
        self.configure(bg=BG_COLOR)
        
        main_frame = ttk.Frame(self, style='Main.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(main_frame, text="CONFERMA ACQUISTO", 
                 font=('Helvetica', 24, 'bold'),
                 foreground=PRIMARY_COLOR).pack(pady=10)
        
        ttk.Label(main_frame, text=product.upper(), 
                 font=('Helvetica', 28),
                 foreground=TEXT_COLOR).pack(pady=5)
        
        ttk.Label(main_frame, text=f"€{price:.2f}", 
                 font=('Helvetica', 32, 'bold'),
                 foreground=PRIMARY_COLOR).pack(pady=10)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="CONFERMA", 
                  style='Success.TButton',
                  command=self.confirm).pack(side="left", padx=15)
        ttk.Button(btn_frame, text="ANNULLA", 
                  style='Danger.TButton',
                  command=self.destroy).pack(side="right", padx=15)

    def confirm(self):
        messagebox.showinfo("Successo", "Prodotto erogato!")
        self.master.show_frame(HomeFrame)
        self.destroy()

if __name__ == "__main__":
    app = VendingMachine()
    app.mainloop()