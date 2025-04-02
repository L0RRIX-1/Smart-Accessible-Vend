import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Configurazioni stilistiche - TEMA SCURO
DARK_BG = '#121212'
DARK_FG = '#FFFFFF'
DARK_ACCENT = '#1F1F1F'
PRIMARY_COLOR = '#4CAF50'  # Verde acceso per contrasto
SECONDARY_COLOR = '#FF5722'  # Arancione per azioni
TEXT_COLOR = '#E0E0E0'

LARGE_FONT = ('Helvetica', 20)
BUTTON_STYLE = {
    'font': ('Helvetica', 22, 'bold'),
    'padding': 20,
    'width': 18
}
IMAGE_SIZE = 180  # Dimensione ottimizzata per tema scuro

# Verifica cartella immagini
if not os.path.exists('images'):
    os.makedirs('images')
    messagebox.showwarning("Attenzione", "Creata cartella 'images'. Inserire le immagini dei prodotti.")

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

class DarkVendingMachine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DARK VEND")
        self.geometry("1200x800")  # Schermo più ampio
        self.configure(bg=DARK_BG)
        
        # Configurazione stili globali
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Tema più adattabile
        
        # Stili personalizzati
        self.style.configure('Main.TFrame', background=DARK_BG)
        self.style.configure('Dark.TFrame', background=DARK_ACCENT)
        self.style.configure('Product.TFrame', background=DARK_ACCENT, 
                           borderwidth=0, relief='flat')
        self.style.configure('Nav.TButton', font=('Helvetica', 18), 
                           padding=12, background=DARK_ACCENT, 
                           foreground=TEXT_COLOR)
        self.style.configure('Action.TButton', font=('Helvetica', 18, 'bold'), 
                            padding=15, background=PRIMARY_COLOR, 
                            foreground='white')
        self.style.configure('Title.TLabel', font=('Helvetica', 32, 'bold'), 
                           foreground=PRIMARY_COLOR, background=DARK_BG)
        self.style.configure('Subtitle.TLabel', font=('Helvetica', 24), 
                            foreground=TEXT_COLOR, background=DARK_BG)
        self.style.configure('Product.TLabel', font=('Helvetica', 18), 
                           foreground=TEXT_COLOR, background=DARK_ACCENT)
        self.style.configure('Price.TLabel', font=('Helvetica', 22, 'bold'), 
                           foreground=PRIMARY_COLOR, background=DARK_ACCENT)
        
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
        
        # Titolo principale
        ttk.Label(self, text="DARK VEND", style='Title.TLabel').pack(pady=40)
        
        # Sottotitolo
        ttk.Label(self, text="Seleziona categoria:", style='Subtitle.TLabel').pack(pady=30)
        
        # Pulsanti categoria
        btn_frame = ttk.Frame(self, style='Main.TFrame')
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="🍔 SNACK", 
                  style='Action.TButton',
                  command=lambda: controller.show_frame(SnacksFrame)
                  ).pack(pady=25, ipadx=30)
        
        ttk.Button(btn_frame, text="🥤 BEVANDE", 
                  style='Action.TButton',
                  command=lambda: controller.show_frame(DrinksFrame)
                  ).pack(pady=25, ipadx=30)

class ProductFrame(BaseFrame):
    def create_products(self, category):
        # Pulsante ritorno con stile migliorato
        ttk.Button(self, text="◀ HOME", 
                  style='Nav.TButton',
                  command=lambda: self.controller.show_frame(HomeFrame)
                  ).grid(row=0, column=0, padx=30, pady=30, sticky="nw")

        # Titolo categoria
        category_title = ttk.Label(self, text=category.upper(), 
                                 style='Subtitle.TLabel')
        category_title.grid(row=0, column=1, columnspan=2, pady=30)

        # Griglia prodotti
        row, col = 1, 0
        for product, info in products[category].items():
            product_frame = ttk.Frame(self, style='Product.TFrame', padding=15)
            product_frame.grid(row=row, column=col, padx=25, pady=25, ipadx=10, ipady=10)

            # Cornice immagine con bordo sottile
            img_frame = ttk.Frame(product_frame, style='Dark.TFrame', padding=5)
            img_frame.pack(pady=(0, 15))

            # Caricamento immagine
            try:
                img_path = os.path.join('images', info['image'])
                img = Image.open(img_path).resize((IMAGE_SIZE, IMAGE_SIZE))
                photo = ImageTk.PhotoImage(img)
                
                img_label = ttk.Label(img_frame)
                img_label.image = photo
                img_label.configure(image=photo)
                img_label.pack()
                
            except Exception as e:
                error_img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), color=DARK_ACCENT)
                photo = ImageTk.PhotoImage(error_img)
                img_label = ttk.Label(img_frame, image=photo, 
                                    text="NO IMAGE", compound='center',
                                    style='Product.TLabel')
                img_label.image = photo
                img_label.pack()
            
            # Nome prodotto e prezzo
            ttk.Label(product_frame, text=product.upper(), 
                     style='Product.TLabel').pack()
            ttk.Label(product_frame, text=f"€{info['price']:.2f}", 
                     style='Price.TLabel').pack(pady=10)
            
            # Pulsante selezione
            ttk.Button(product_frame, text="SELEZIONA",
                      style='Action.TButton',
                      command=lambda p=product, pr=info['price']: 
                      ConfirmWindow(self.controller, p, pr)
                      ).pack(fill='x', pady=(10, 0))

            col += 1
            if col > 2:  # 3 colonne per layout bilanciato
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
        self.product = product
        self.title("CONFERMA ACQUISTO")
        self.geometry("500x400")
        self.configure(bg=DARK_BG)
        self.resizable(False, False)
        
        # Centra la finestra
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        main_frame = ttk.Frame(self, style='Main.TFrame')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Contenuto principale
        content_frame = ttk.Frame(main_frame, style='Main.TFrame')
        content_frame.pack(expand=True, fill='both')
        
        # Icona prodotto
        icon_frame = ttk.Frame(content_frame, style='Dark.TFrame', width=120, height=120)
        icon_frame.pack(pady=(0, 20))
        icon_frame.pack_propagate(False)
        
        try:
            category = 'snack' if product in products['snack'] else 'bevande'
            img_path = os.path.join('images', products[category][product]['image'])
            img = Image.open(img_path).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            icon_label = ttk.Label(icon_frame, image=photo, background=DARK_ACCENT)
            icon_label.image = photo
            icon_label.pack(expand=True)
        except:
            icon_label = ttk.Label(icon_frame, text="🛒", font=('Helvetica', 48),
                                 style='Product.TLabel')
            icon_label.pack(expand=True)
        
        # Messaggio di conferma
        ttk.Label(content_frame, text="CONFERMI L'ACQUISTO?", 
                 font=('Helvetica', 20, 'bold'),
                 foreground=TEXT_COLOR, background=DARK_BG).pack(pady=(0, 10))
        
        # Nome prodotto
        ttk.Label(content_frame, text=product.upper(), 
                 font=('Helvetica', 24, 'bold'),
                 foreground=PRIMARY_COLOR, background=DARK_BG).pack()
        
        # Prezzo
        ttk.Label(content_frame, text=f"€{price:.2f}", 
                 font=('Helvetica', 28, 'bold'),
                 foreground=PRIMARY_COLOR, background=DARK_BG).pack(pady=15)
        
        # Pulsanti azione - ORA BEN VISIBILI
        btn_frame = ttk.Frame(content_frame, style='Main.TFrame')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        # Pulsante CONFERMA (verde grande)
        confirm_btn = tk.Button(btn_frame, 
                              text="CONFERMA", 
                              font=('Helvetica', 16, 'bold'),
                              bg='#4CAF50',
                              fg='white',
                              activebackground='#388E3C',
                              activeforeground='white',
                              relief='flat',
                              bd=0,
                              padx=30,
                              pady=12,
                              command=self.confirm)
        confirm_btn.pack(side='left', expand=True, fill='x', padx=5)
        
        # Pulsante ANNULLA (rosso grande)
        cancel_btn = tk.Button(btn_frame, 
                             text="ANNULLA", 
                             font=('Helvetica', 16, 'bold'),
                             bg='#F44336',
                             fg='white',
                             activebackground='#D32F2F',
                             activeforeground='white',
                             relief='flat',
                             bd=0,
                             padx=30,
                             pady=12,
                             command=self.destroy)
        cancel_btn.pack(side='right', expand=True, fill='x', padx=5)

        # Effetti hover
        confirm_btn.bind("<Enter>", lambda e: confirm_btn.config(bg='#388E3C'))
        confirm_btn.bind("<Leave>", lambda e: confirm_btn.config(bg='#4CAF50'))
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg='#D32F2F'))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg='#F44336'))

    def confirm(self):
        messagebox.showinfo("Acquisto confermato", 
                          f"Hai acquistato: {self.product.upper()}",
                          parent=self)
        self.master.show_frame(HomeFrame)
        self.destroy()

if __name__ == "__main__":
    app = DarkVendingMachine()
    app.mainloop()