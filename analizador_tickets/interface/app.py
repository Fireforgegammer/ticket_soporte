import os
import json
import tkinter as tk
import customtkinter as ctk
import socket
from threading import Thread

# Importaciones de tu lógica interna
from src.flujo.pipeline import PipelineProcesamiento

class AppSoporteNLP(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tickets Soporte NLP - Análisis de Tickets")
        self.geometry("1200x850")
        ctk.set_appearance_mode("dark")
        
        self.pipeline = PipelineProcesamiento()
        
        self.motor_selected = ctk.StringVar(value="ollama")
        self.motor_selected.trace_add("write", self.actualizar_texto_modelo)
        self.ruta_lote_seleccionado = None
        
        self._construir_interfaz()
        self.verificar_conexion_ollama()

    def actualizar_texto_modelo(self, *args):
        motor = self.motor_selected.get()
        nombre_modelo = self.pipeline.ia.modelo_xai if motor == "groq" else self.pipeline.ia.modelo_local
        self.lbl_modelo_info.configure(text=f"🤖 Modelo: {nombre_modelo}")

    def verificar_conexion_ollama(self):
        try:
            with socket.create_connection(("127.0.0.1", 11434), timeout=1):
                self.lbl_status_conexion.configure(text="✅ Ollama conectado", text_color="#4CAF50")
        except:
            self.lbl_status_conexion.configure(text="❌ Ollama desconectado", text_color="#E74C3C")

    def _construir_interfaz(self):
        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.lbl_status_conexion = ctk.CTkLabel(self.header_frame, text="🔄 Verificando...", font=ctk.CTkFont(size=12))
        self.lbl_status_conexion.pack(side="left")

        self.lbl_titulo = ctk.CTkLabel(self, text="🎫 Sistema de Análisis de Tickets de Soporte con NLP", 
                                     font=ctk.CTkFont(size=22, weight="bold"))
        self.lbl_titulo.pack(pady=(5, 15))

        self.lbl_modelo_info = ctk.CTkLabel(self.header_frame, text=f"🤖 Modelo: {self.pipeline.ia.modelo_local}", 
                                          font=ctk.CTkFont(size=12, slant="italic"))
        self.lbl_modelo_info.pack(side="right")

        # --- SELECCIÓN DE MOTOR ---
        self.motor_frame = ctk.CTkFrame(self, height=40)
        self.motor_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.motor_frame, text="Motor Activo:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=20)
        ctk.CTkRadioButton(self.motor_frame, text="Ollama (Local)", variable=self.motor_selected, value="ollama").pack(side="left", padx=10)
        ctk.CTkRadioButton(self.motor_frame, text="Groq (Cloud)", variable=self.motor_selected, value="groq").pack(side="left", padx=10)

        # --- CONTENEDOR CENTRAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Izquierda
        self.frame_left = ctk.CTkFrame(self.main_container)
        self.frame_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(self.frame_left, text="📋 Ticket a analizar", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.input_individual = ctk.CTkTextbox(self.frame_left, height=300, font=("Segoe UI", 12))
        self.input_individual.pack(fill="both", expand=True, padx=15, pady=5)

        self.btn_frame = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=15, padx=15)
        
        self.btn_cargar = ctk.CTkButton(self.btn_frame, text="📄 Cargar ejemplo", command=self.cargar_ejemplo_desde_archivo)
        self.btn_cargar.pack(side="left", padx=5, expand=True)
        
        self.btn_limpiar = ctk.CTkButton(self.btn_frame, text="🗑️ Limpiar", fg_color="#E74C3C", command=self.limpiar_campos)
        self.btn_limpiar.pack(side="left", padx=5, expand=True)
        
        self.btn_procesar = ctk.CTkButton(self.btn_frame, text="⚡ Procesar Ticket", fg_color="#E67E22", command=self.lanzar_hilo_individual)
        self.btn_procesar.pack(side="left", padx=5, expand=True)

        # Derecha
        self.frame_right = ctk.CTkFrame(self.main_container)
        self.frame_right.pack(side="left", fill="both", expand=True)

        self.tabview = ctk.CTkTabview(self.frame_right)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_pipeline = self.tabview.add("🔍 Pipeline")
        self.tab_acciones = self.tabview.add("⚡ Acciones")
        self.tab_json = self.tabview.add("📄 JSON")
        self.tab_modelos = self.tabview.add("📊 Modelos")

        self.txt_pipeline = ctk.CTkTextbox(self.tab_pipeline, font=("Consolas", 13))
        self.txt_pipeline.pack(fill="both", expand=True)
        self.txt_pipeline.tag_config("green", foreground="#4CAF50")

        self.txt_acciones = ctk.CTkTextbox(self.tab_acciones, font=("Consolas", 13))
        self.txt_acciones.pack(fill="both", expand=True)

        self.txt_json = ctk.CTkTextbox(self.tab_json, font=("Consolas", 13))
        self.txt_json.pack(fill="both", expand=True)

        self.txt_modelos = ctk.CTkTextbox(self.tab_modelos, font=("Consolas", 13))
        self.txt_modelos.pack(fill="both", expand=True)
        self.txt_modelos.insert("1.0", f"📊 Información de Modelos:\n\n- Ollama: {self.pipeline.ia.modelo_local}\n- Groq: {self.pipeline.ia.modelo_xai}")

        # --- SECCIÓN DE ESTADO Y BARRA DINÁMICA ---
        self.frame_status = ctk.CTkFrame(self)
        self.frame_status.pack(fill="x", padx=20, pady=(0, 20))

        self.progress_label = ctk.CTkLabel(self.frame_status, text="ESPERANDO INICIO", font=ctk.CTkFont(size=13, weight="bold"))
        self.progress_label.pack(pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(self.frame_status, height=12)
        self.progress_bar.pack(fill="x", padx=30, pady=(0, 15))
        self.progress_bar.set(0) # Inicialmente vacía
        
        self.lotes_btns = ctk.CTkFrame(self.frame_status, fg_color="transparent")
        self.lotes_btns.pack(fill="x", padx=15, pady=(0, 10))

        self.btn_sel_lote = ctk.CTkButton(self.lotes_btns, text="📁 Cargar JSON", fg_color="#2ECC71", command=self.seleccionar_archivo_json)
        self.btn_sel_lote.pack(side="left", padx=5, expand=True)

        self.btn_lote = ctk.CTkButton(self.lotes_btns, text="🔥 Procesar lote", fg_color="#F39C12", command=self.lanzar_hilo_lote)
        self.btn_lote.pack(side="left", padx=5, expand=True)

        self.lbl_footer = ctk.CTkLabel(self, text="⌛ Sistema listo", font=ctk.CTkFont(size=11))
        self.lbl_footer.pack(side="bottom", anchor="e", padx=20, pady=5)

    # --- FUNCIONES DE APOYO ---
    def cargar_ejemplo_desde_archivo(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta = os.path.join(base_dir, "datos", "ejemplo_ticket.txt")
            if os.path.exists(ruta):
                with open(ruta, 'r', encoding='utf-8') as f:
                    self.input_individual.delete("1.0", "end")
                    self.input_individual.insert("1.0", f.read())
                    self.lbl_footer.configure(text="✅ Ejemplo cargado correctamente", text_color="#4CAF50")
            else:
                self.lbl_footer.configure(text=f"❌ No se encontró: {ruta}", text_color="#E74C3C")
        except Exception as e:
            self.lbl_footer.configure(text=f"❌ Error: {e}", text_color="#E74C3C")

    def limpiar_campos(self):
        self.input_individual.delete("1.0", "end")
        self.txt_pipeline.delete("1.0", "end")
        self.txt_json.delete("1.0", "end")
        self.txt_acciones.delete("1.0", "end")
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.progress_label.configure(text="ESPERANDO INICIO", text_color="white")

    def seleccionar_archivo_json(self):
        from tkinter import filedialog
        ruta = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if ruta:
            self.ruta_lote_seleccionado = ruta
            self.lbl_footer.configure(text=f"📦 Archivo seleccionado: {os.path.basename(ruta)}")

    # --- LÓGICA PROCESAR INDIVIDUAL (CON EFECTO DE CARGA) ---
    def lanzar_hilo_individual(self):
        texto = self.input_individual.get("1.0", "end-1c").strip()
        if not texto: return
        
        # 1. Feedback visual inmediato
        self.btn_procesar.configure(state="disabled")
        self.progress_label.configure(text="🚀 ANALIZANDO TICKET INDIVIDUAL...", text_color="#E67E22")
        
        # 2. ACTIVAR EL EFECTO DE CARGA (La raya azul pasando en bucle)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start() 
        
        self.txt_pipeline.delete("1.0", "end")
        self.txt_pipeline.insert("end", "==============================================\n", "green")
        self.txt_pipeline.insert("end", f"⚙️ PROCESANDO CON {self.motor_selected.get().upper()}\n", "green")
        self.txt_pipeline.insert("end", "==============================================\n\n", "green")
        
        Thread(target=self.ejecutar_analisis_logica, args=(texto,), daemon=True).start()

    def ejecutar_analisis_logica(self, texto):
        try:
            motor = self.motor_selected.get()
            ticket = self.pipeline.procesar_ticket(texto, motor=motor)
            
            if ticket:
                self.txt_pipeline.insert("end", f"✅ CATEGORÍA: {ticket.categoria.value}\n")
                self.txt_pipeline.insert("end", f"🚨 URGENCIA: {ticket.urgencia.value}\n")
                self.txt_acciones.insert("end", f"▶️ ACCIÓN RECOMENDADA:\n\n{ticket.accion_sugerida}")
                
                res_dict = {
                    "categoria": ticket.categoria.value, 
                    "urgencia": ticket.urgencia.value, 
                    "intencion": ticket.intencion,
                    "accion": ticket.accion_sugerida
                }
                self.txt_json.insert("1.0", json.dumps(res_dict, indent=4, ensure_ascii=False))
                self.progress_label.configure(text="✅ ANÁLISIS FINALIZADO", text_color="#4CAF50")
            else:
                self.progress_label.configure(text="❌ LA IA NO DEVOLVIÓ DATOS", text_color="#E74C3C")
        except Exception as e:
            self.progress_label.configure(text=f"❌ ERROR: {str(e)[:50]}...", text_color="#E74C3C")
        finally:
            # 3. DETENER EL EFECTO DE CARGA
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.set(1) # Llenar al final
            self.btn_procesar.configure(state="normal")

    # --- LÓGICA PROCESAR LOTE (CON BARRA DE PROGRESO REAL) ---
    def lanzar_hilo_lote(self):
        if not self.ruta_lote_seleccionado: return
        self.btn_lote.configure(state="disabled")
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        Thread(target=self.ejecutar_logica_lote, daemon=True).start()

    def ejecutar_logica_lote(self):
        try:
            with open(self.ruta_lote_seleccionado, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
            total = len(tickets)
            motor = self.motor_selected.get()
            
            for i, texto in enumerate(tickets):
                self.progress_label.configure(text=f"⌛ PROCESANDO LOTE: {i+1} DE {total}...", text_color="#F39C12")
                self.pipeline.procesar_ticket(texto, motor=motor)
                self.progress_bar.set((i + 1) / total)
                
            self.progress_label.configure(text="✅ LOTE COMPLETADO", text_color="#2ECC71")
        except Exception as e:
            self.progress_label.configure(text=f"❌ ERROR EN LOTE: {str(e)[:50]}", text_color="#E74C3C")
        finally:
            self.btn_lote.configure(state="normal")