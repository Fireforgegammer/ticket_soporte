import json
import logging
from pathlib import Path
from src.nucleo.entidades import TicketAnalizado

# Configuración del logger profesional
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "tickets_procesados.jsonl"

def guardar_resultado_json(ticket: TicketAnalizado) -> bool:
    """
    Persiste el ticket analizado en un archivo de log en formato JSON Lines.
    Retorna True si la operación fue exitosa.
    """
    try:
        # Usamos el método que definimos en la entidad
        datos = ticket.a_diccionario()
        
        # Guardamos como una línea nueva en el archivo (formato JSONL)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(datos, ensure_ascii=False) + "\n")
            
        return True
    except Exception as e:
        logging.error(f"Error al persistir el ticket: {e}")
        return False
