import customtkinter as ctk
from src.flujo.pipeline import PipelineProcesamiento
from threading import Thread

class AppAnalisis(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración estética global
        self.title("NLP Ticket Analyzer")
        self.geometry("1000x650")
        ctk.set_appearance_mode("dark")
        
        self.pipeline = PipelineProcesamiento()

        # Layout: Sidebar (Izquierda) y Contenido (Derecha)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="SOPORTE AI", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=30, padx=20)

        self.status_label = ctk.CTkLabel(self.sidebar, text="● Sistema Activo", 
                                        text_color="#4CAF50", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

        # --- CONTENIDO PRINCIPAL ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(self.main_frame, text="Análisis de Ticket", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, pady=(0, 20), sticky="w")

        # Campo de entrada (Estilo consola)
        self.input_text = ctk.CTkTextbox(self.main_frame, font=("Consolas", 14), 
                                        border_width=1, border_color="#333333")
        self.input_text.grid(row=1, column=0, sticky="nsew")

        # --- PANEL DE RESULTADOS ---
        self.info_panel = ctk.CTkFrame(self.main_frame, height=100)
        self.info_panel.grid(row=2, column=0, pady=(20, 0), sticky="ew")
        
        self.cat_label = ctk.CTkLabel(self.info_panel, text="CATEGORÍA: --", font=ctk.CTkFont(weight="bold"))
        self.cat_label.pack(side="left", padx=40, pady=20)
        
        self.urg_label = ctk.CTkLabel(self.info_panel, text="URGENCIA: --", font=ctk.CTkFont(weight="bold"))
        self.urg_label.pack(side="left", padx=40, pady=20)

        # Botón de ejecución
        self.btn_run = ctk.CTkButton(self.main_frame, text="EJECUTAR ANÁLISIS", 
                                     fg_color="#1f538d", hover_color="#14375e",
                                     command=self.procesar_hilo)
        self.btn_run.grid(row=3, column=0, pady=(20, 0), sticky="e")

    def procesar_hilo(self):
        """Lanza el análisis en un hilo secundario para no congelar la interface."""
        self.btn_run.configure(state="disabled", text="Procesando...")
        Thread(target=self.ejecutar_analisis).start()

    # En interface/app.py

    def ejecutar_analisis(self, texto_forzado=None):
        # Si pasamos texto por parámetro (para el test), lo usamos; 
        # si no, lo cogemos de la caja de texto (uso normal)
        texto = texto_forzado if texto_forzado else self.input_text.get("1.0", "end-1c").strip()
        
        if texto:
            resultado = self.pipeline.procesar_ticket(texto)
            if resultado:
                self.cat_label.configure(text=f"CATEGORÍA: {resultado.categoria.value.upper()}")
                self.urg_label.configure(text=f"URGENCIA: {resultado.urgencia.value.upper()}")
        
        self.btn_run.configure(state="normal", text="EJECUTAR ANÁLISIS")