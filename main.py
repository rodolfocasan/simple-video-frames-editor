# main.py
import tkinter as tk

from extractor import opcion_seleccionar_videos
from extractor import opcion_seleccionar_carpeta_y_fps





class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configura la ventana principal"""
        self.root.title("Simple Video Frames Editor")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Colores del tema oscuro
        self.colors = {
            'bg': '#1E1E1E',
            'secondary_bg': '#252526',
            'accent': '#007ACC',
            'accent_hover': '#1B95E0',
            'text': '#FFFFFF',
            'text_secondary': '#CCCCCC'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Hacer que la ventana sea responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Centrar la ventana
        self.center_window()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(
            self.root,
            bg=self.colors['bg'],
            padx=40,
            pady=40
        )
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        
        title = tk.Label(
            title_frame,
            text="Simple Video Frames Editor",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Herramienta para procesar frames de video",
            font=("Helvetica", 12),
            bg=self.colors['bg'],
            fg=self.colors['text_secondary']
        )
        subtitle.pack(pady=(5, 0))
        
        # Contenedor de tarjetas
        cards_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        cards_frame.grid(row=1, column=0, sticky="nsew")
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        # Tarjeta 1: Extraer Frames
        self.create_card(
            cards_frame,
            0, 0,
            "Extraer Frames",
            "Selecciona uno o varios videos\npara extraer sus frames",
            "📹 Seleccionar Videos",
            opcion_seleccionar_videos
        )
        
        # Tarjeta 2: Unir Frames
        self.create_card(
            cards_frame,
            0, 1,
            "Unir Frames",
            "Une una secuencia de frames\npara crear un video",
            "🎞️ Seleccionar Frames",
            opcion_seleccionar_carpeta_y_fps
        )
        
    def create_card(self, parent, row, column, title, description, button_text, command):
        """Crea una tarjeta con título, descripción y botón"""
        # Frame de la tarjeta
        card = tk.Frame(
            parent,
            bg=self.colors['secondary_bg'],
            padx=25,
            pady=25,
            relief="flat",
            borderwidth=0
        )
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        # Título de la tarjeta
        card_title = tk.Label(
            card,
            text=title,
            font=("Helvetica", 16, "bold"),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text']
        )
        card_title.pack(anchor="w")
        
        # Descripción
        description_label = tk.Label(
            card,
            text=description,
            font=("Helvetica", 11),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text_secondary'],
            justify=tk.LEFT
        )
        description_label.pack(anchor="w", pady=(10, 20))
        
        # Botón
        button = tk.Button(
            card,
            text=button_text,
            font=("Helvetica", 11),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text'],
            relief="flat",
            pady=10,
            padx=15,
            command=command,
            cursor="hand2"
        )
        button.pack(anchor="w")
        
        # Efecto hover para la tarjeta
        def on_enter(e):
            card.config(bg=self.colors['secondary_bg'])
            card_title.config(bg=self.colors['secondary_bg'])
            description_label.config(bg=self.colors['secondary_bg'])
            
        def on_leave(e):
            card.config(bg=self.colors['secondary_bg'])
            card_title.config(bg=self.colors['secondary_bg'])
            description_label.config(bg=self.colors['secondary_bg'])
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()





if __name__ == "__main__":
    app = MainApp()
    app.run()