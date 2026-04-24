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

        # 1. Configuración de la ventana principal
        self.title("Tickets Soporte NLP - Análisis de Tickets")
        self.geometry("1100, 750")
        ctk.set_appearance_mode("dark")
        
        # Inicializar el Pipeline de procesamiento
        self.pipeline = PipelineProcesamiento()
        
        # 2. Variables de control y rastreo (Trace)
        self.motor_selected = ctk.StringVar(value="ollama")
        # Vincular el cambio de motor a la actualización automática de la etiqueta de modelo
        self.motor_selected.trace_add("write", self.actualizar_texto_modelo)
        
        self.ruta_lote_seleccionado = None
        
        # 3. Construir los elementos de la interfaz
        self._construir_interfaz()

    def actualizar_texto_modelo(self, *args):
        """Actualiza inmediatamente el nombre del modelo arriba a la derecha al cambiar el motor."""
        motor = self.motor_selected.get()
        if motor == "groq":
            nombre_modelo = self.pipeline.ia.modelo_xai
        else:
            nombre_modelo = self.pipeline.ia.modelo_local
        
        self.lbl_modelo_info.configure(text=f"🤖 Modelo: {nombre_modelo}")

    def _construir_interfaz(self):
        # --- Cabecera ---
        self.lbl_titulo = ctk.CTkLabel(self, text="📄 Sistema de Análisis de Tickets de Soporte con NLP", 
                                      font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.pack(pady=20)

        # --- Frame Superior: Control de Motor e Información ---
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.frame_top, text="Motor Activo:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        
        self.rb_ollama = ctk.CTkRadioButton(self.frame_top, text="Ollama (Local)", variable=self.motor_selected, value="ollama")
        self.rb_ollama.pack(side="left", padx=10)
        
        self.rb_groq = ctk.CTkRadioButton(self.frame_top, text="Groq (Cloud)", variable=self.motor_selected, value="groq")
        self.rb_groq.pack(side="left", padx=10)

        # Indicador de Modelos (Recuperado y dinámico)
        self.lbl_modelo_info = ctk.CTkLabel(self.frame_top, 
                                           text=f"🤖 Modelo: {self.pipeline.ia.modelo_local}", 
                                           font=ctk.CTkFont(size=11, slant="italic"))
        self.lbl_modelo_info.pack(side="right", padx=20)

        # --- Panel Principal de Trabajo ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Columna Izquierda: Entrada de Ticket
        self.frame_left = ctk.CTkFrame(self.main_container)
        self.frame_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(self.frame_left, text="📝 Ticket a analizar", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.input_individual = ctk.CTkTextbox(self.frame_left, height=350)
        self.input_individual.pack(fill="both", expand=True, padx=15, pady=10)

        self.frame_btns_inv = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        self.frame_btns_inv.pack(fill="x", pady=10)

        self.btn_cargar = ctk.CTkButton(self.frame_btns_inv, text="📄 Cargar ejemplo", command=self.cargar_ejemplo_desde_archivo)
        self.btn_cargar.pack(side="left", padx=5, expand=True)

        self.btn_limpiar = ctk.CTkButton(self.frame_btns_inv, text="🗑️ Limpiar", fg_color="#E74C3C", hover_color="#C0392B", command=lambda: self.input_individual.delete("1.0", "end"))
        self.btn_limpiar.pack(side="left", padx=5, expand=True)

        self.btn_procesar = ctk.CTkButton(self.frame_btns_inv, text="⚡ Procesar Ticket", fg_color="#E67E22", hover_color="#D35400", command=self.lanzar_hilo_individual)
        self.btn_procesar.pack(side="left", padx=5, expand=True)

        # Columna Derecha: Resultados (Tabs)
        self.frame_right = ctk.CTkFrame(self.main_container)
        self.frame_right.pack(side="left", fill="both", expand=True)

        self.tabview = ctk.CTkTabview(self.frame_right)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_pipeline = self.tabview.add("🔍 Pipeline")
        self.tab_json = self.tabview.add("📁 JSON")

        self.txt_pipeline = ctk.CTkTextbox(self.tab_pipeline, font=ctk.CTkFont(family="Consolas"))
        self.txt_pipeline.pack(fill="both", expand=True)

        self.txt_json = ctk.CTkTextbox(self.tab_json, font=ctk.CTkFont(family="Consolas"))
        self.txt_json.pack(fill="both", expand=True)

        # --- Sección Inferior: Procesamiento por Lotes ---
        self.frame_lotes = ctk.CTkFrame(self)
        self.frame_lotes.pack(fill="x", padx=20, pady=15)

        self.btn_sel_lote = ctk.CTkButton(self.frame_lotes, text="📂 Cargar JSON", fg_color="#2ECC71", command=self.seleccionar_archivo_json)
        self.btn_sel_lote.pack(side="left", padx=10, pady=10)

        self.btn_lote = ctk.CTkButton(self.frame_lotes, text="🔥 Procesar Lote", fg_color="#F39C12", command=self.lanzar_hilo_lote)
        self.btn_lote.pack(side="left", padx=10, pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.frame_lotes)
        self.progress_bar.pack(side="left", fill="x", expand=True, padx=10)
        self.progress_bar.set(0)

        self.lbl_status = ctk.CTkLabel(self, text="Listo", font=ctk.CTkFont(size=12))
        self.lbl_status.pack(side="bottom", anchor="e", padx=20, pady=5)

    # --- Lógica de Manejo de Archivos ---

    def cargar_ejemplo_desde_archivo(self):
        try:
            dir_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_ejemplo = os.path.normpath(os.path.join(dir_actual, "..", "datos", "ejemplo_ticket.txt"))
            
            if os.path.exists(ruta_ejemplo):
                with open(ruta_ejemplo, 'r', encoding='utf-8') as f:
                    self.input_individual.delete("1.0", "end")
                    self.input_individual.insert("1.0", f.read())
                    self.lbl_status.configure(text="✅ Ejemplo cargado", text_color="#4CAF50")
            else:
                self.lbl_status.configure(text="⚠️ Archivo ejemplo_ticket.txt no encontrado", text_color="#E74C3C")
        except Exception as e:
            self.lbl_status.configure(text=f"Error: {str(e)}", text_color="#E74C3C")

    def seleccionar_archivo_json(self):
        from tkinter import filedialog
        ruta = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if ruta:
            self.ruta_lote_seleccionado = ruta
            self.lbl_status.configure(text=f"📦 Archivo seleccionado: {os.path.basename(ruta)}", text_color="white")

    # --- Lógica de Procesamiento ---

    def lanzar_hilo_individual(self):
        texto = self.input_individual.get("1.0", "end-1c").strip()
        if not texto: return
        
        self.btn_procesar.configure(state="disabled")
        self.txt_pipeline.delete("1.0", "end")
        self.txt_pipeline.insert("end", f"🚀 ANALIZANDO CON {self.motor_selected.get().upper()}...\n" + "-"*40 + "\n")
        
        # Ejecutar en hilo secundario para no congelar la interfaz
        Thread(target=self.ejecutar_analisis_logica, args=(texto,), daemon=True).start()

    def ejecutar_analisis_logica(self, texto):
        try:
            socket.setdefaulttimeout(120) # Evitar cortes prematuros en Ollama
            motor = self.motor_selected.get()
            ticket = self.pipeline.procesar_ticket(texto, motor=motor)
            
            if ticket:
                # Mostrar resultados en la pestaña Pipeline
                self.txt_pipeline.insert("end", f"✅ CATEGORÍA: {ticket.categoria.value}\n")
                self.txt_pipeline.insert("end", f"🚨 URGENCIA: {ticket.urgencia.value}\n")
                self.txt_pipeline.insert("end", f"🎯 INTENCIÓN: {ticket.intencion}\n")
                self.txt_pipeline.insert("end", f"🛠️ ACCIÓN: {ticket.accion_sugerida}\n")
                
                # Generar JSON para la pestaña JSON
                dict_res = {
                    "categoria": ticket.categoria.value, "urgencia": ticket.urgencia.value,
                    "intencion": ticket.intencion, "accion": ticket.accion_sugerida,
                    "entidades": ticket.entidades
                }
                self.txt_json.delete("1.0", "end")
                self.txt_json.insert("1.0", json.dumps(dict_res, indent=4, ensure_ascii=False))
                self.lbl_status.configure(text="✅ Análisis completado", text_color="#4CAF50")
            else:
                self.txt_pipeline.insert("end", "\n❌ ERROR: La IA devolvió una respuesta vacía o inválida.")
                self.lbl_status.configure(text="❌ Error en el análisis", text_color="#E74C3C")
        except Exception as e:
            self.txt_pipeline.insert("end", f"\n❌ ERROR CRÍTICO: {str(e)}")
        finally:
            self.btn_procesar.configure(state="normal")

    def lanzar_hilo_lote(self):
        if not self.ruta_lote_seleccionado:
            self.lbl_status.configure(text="⚠️ Selecciona primero un archivo JSON", text_color="#E74C3C")
            return
        self.btn_lote.configure(state="disabled")
        Thread(target=self.ejecutar_logica_lote, daemon=True).start()

    def ejecutar_logica_lote(self):
        try:
            with open(self.ruta_lote_seleccionado, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
            
            motor = self.motor_selected.get()
            for i, texto in enumerate(tickets):
                self.pipeline.procesar_ticket(texto, motor=motor)
                self.progress_bar.set((i + 1) / len(tickets))
                
            self.lbl_status.configure(text="✅ Procesamiento por lotes finalizado", text_color="#4CAF50")
        except Exception as e:
            self.lbl_status.configure(text="❌ Error procesando el lote", text_color="#E74C3C")
        finally:
            self.btn_lote.configure(state="normal")