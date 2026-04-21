import customtkinter as ctk
from src.flujo.pipeline import PipelineProcesamiento
from src.nucleo.constantes import MODELO_POR_DEFECTO
from threading import Thread

# Configuración visual global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppSoporteNLP(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tickets Soporte NLP - Análisis de Tickets")
        self.geometry("1150x750")
        
        # Orquestador lógico
        self.pipeline = PipelineProcesamiento()

        # Configuración del Grid Principal (Layout de paneles)
        self.grid_columnconfigure(0, weight=1) # Panel Izquierdo
        self.grid_columnconfigure(1, weight=1) # Panel Derecho
        self.grid_rowconfigure(2, weight=1)    # Fila de contenido central

        self._construir_interfaz()

    def _construir_interfaz(self):
        """Organiza todos los componentes visuales."""
        self._crear_header()
        self._crear_bloque_entrada()
        self._crear_bloque_lotes()
        self._crear_bloque_visualizacion()
        self._crear_footer()

    def _crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="ew")
        
        ctk.CTkLabel(header, text="📑 Sistema de Análisis de Tickets de Soporte con NLP", 
                     font=ctk.CTkFont(size=22, weight="bold")).pack()

        status_bar = ctk.CTkFrame(self, height=35, fg_color="#2b2b2b")
        status_bar.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(status_bar, text="✅ Ollama conectado", text_color="#4CAF50").pack(side="left", padx=20)
        ctk.CTkLabel(status_bar, text=f"🤖 Modelo: {MODELO_POR_DEFECTO}", font=("Segoe UI", 12)).pack(side="right", padx=20)

    def _crear_bloque_entrada(self):
        panel = ctk.CTkFrame(self)
        panel.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")
        
        ctk.CTkLabel(panel, text="📝 Ticket a analizar", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))

        self.input_individual = ctk.CTkTextbox(panel, font=("Consolas", 14), border_width=1)
        self.input_individual.pack(padx=15, pady=5, fill="both", expand=True)

        btn_frame = ctk.CTkFrame(panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkButton(btn_frame, text="📄 Cargar ejemplo", fg_color="#3b8ed0").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="🗑️ Limpiar", fg_color="#E74C3C", command=self.limpiar_campos).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_procesar = ctk.CTkButton(btn_frame, text="⚡ Procesar Ticket", fg_color="#E07C3B", 
                                         hover_color="#C06C30", command=self.lanzar_hilo_analisis)
        self.btn_procesar.pack(side="left", fill="x", expand=True)

    def _crear_bloque_lotes(self):
        panel = ctk.CTkFrame(self)
        panel.grid(row=3, column=0, padx=(20, 10), pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(panel, text="📦 Procesamiento por lotes", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=10)

        btn_frame = ctk.CTkFrame(panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(btn_frame, text="📁 Cargar JSON", fg_color="#2ECC71").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="🔥 Procesar Lote", fg_color="#F39C12").pack(side="left", fill="x", expand=True)

    def _crear_bloque_visualizacion(self):
        panel = ctk.CTkFrame(self)
        panel.grid(row=2, column=1, rowspan=2, padx=(10, 20), pady=10, sticky="nsew")
        
        self.tabs = ctk.CTkTabview(panel)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab_pipe = self.tabs.add("🔍 Pipeline")
        self.tabs.add("📋 Acciones")
        self.tabs.add("📄 JSON")
        self.tabs.add("📊 Modelos")
        
        self.txt_output = ctk.CTkTextbox(tab_pipe, font=("Consolas", 13), text_color="#2ECC71")
        self.txt_output.pack(fill="both", expand=True, padx=5, pady=5)
        self.txt_output.insert("1.0", "⚙️ SISTEMA LISTO. ESPERANDO ENTRADA...\n")

    def _crear_footer(self):
        footer = ctk.CTkFrame(self, height=40, fg_color="#1e1e1e")
        footer.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(footer, width=400)
        self.progress_bar.pack(side="left", padx=20, pady=10)
        self.progress_bar.set(0)

        self.lbl_status = ctk.CTkLabel(footer, text="Esperando ticket...")
        self.lbl_status.pack(side="right", padx=20)

    # --- Lógica de Interface ---
    def limpiar_campos(self):
        self.input_individual.delete("1.0", "end")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", "⚙️ SISTEMA LISTO...\n")

    def lanzar_hilo_analisis(self):
        self.btn_procesar.configure(state="disabled", text="⌛ Analizando...")
        self.txt_output.delete("1.0", "end")
        Thread(target=self.ejecutar_analisis_logica).start()

    def ejecutar_analisis_logica(self):
        texto = self.input_individual.get("1.0", "end-1c").strip()
        if not texto:
            self.txt_output.insert("end", "⚠️ ERROR: Ingrese texto para analizar.\n")
            self.btn_procesar.configure(state="normal", text="⚡ Procesar Ticket")
            return

        self.txt_output.insert("end", "🚀 INICIANDO ANÁLISIS NLP...\n")
        self.txt_output.insert("end", "-"*50 + "\n")
        
        ticket = self.pipeline.procesar_ticket(texto)
        
        if ticket:
            self.txt_output.insert("end", f"📌 CATEGORÍA: {ticket.categoria.value.upper()}\n")
            self.txt_output.insert("end", f"🚨 URGENCIA:  {ticket.urgencia.value.upper()}\n")
            self.txt_output.insert("end", f"🎯 INTENCIÓN: {ticket.intencion}\n")
            self.txt_output.insert("end", f"💡 ACCIÓN:    {ticket.accion_sugerida}\n")
            self.txt_output.insert("end", "-"*50 + "\n")
            self.txt_output.insert("end", "✅ PROCESO FINALIZADO CON ÉXITO.\n")
            self.lbl_status.configure(text="Ticket procesado correctamente")
        else:
            self.txt_output.insert("end", "❌ ERROR: Fallo en el motor de IA.\n")
        
        self.btn_procesar.configure(state="normal", text="⚡ Procesar Ticket")