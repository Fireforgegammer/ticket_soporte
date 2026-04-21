import os
import json
from pathlib import Path
from src.nucleo.entidades import TicketAnalizado, CategoriaTicket, UrgenciaTicket
from src.infraestructura.repositorio_log import guardar_resultado_json, LOG_FILE

def test_guardar_resultado_crea_archivo_y_contenido():
    # 1. Preparar datos de prueba
    ticket = TicketAnalizado(
        texto_original="Test de log",
        categoria=CategoriaTicket.OTRO,
        urgencia=UrgenciaTicket.BAJA,
        intencion="Probar persistencia",
        accion_sugerida="Ninguna"
    )
    
    # 2. Ejecutar
    exito = guardar_resultado_json(ticket)
    
    # 3. Verificar
    assert exito is True
    assert LOG_FILE.exists()
    
    # Leer la última línea para validar el JSON
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()
        ultima_linea = json.loads(lineas[-1])
        
    assert ultima_linea["categoria"] == "otro"
    assert "Test de log" in ultima_linea["texto"]