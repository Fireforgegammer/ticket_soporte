import re
from src.nucleo.constantes import MAX_CARACTERES_TICKET

def normalizar_texto(texto: str) -> str:
    """
    Limpia y normaliza el texto para optimizar el análisis de la IA.
    """
    if not texto:
        return ""

    # 1. Eliminar etiquetas HTML si existen
    texto = re.sub(r'<[^>]+>', '', texto)
    
    # 2. Eliminar caracteres de control y no imprimibles
    texto = re.sub(r'[\x00-\x1f\x7f]', '', texto)
    
    # 3. Normalizar espacios (convertir tabs/saltos múltiples en un solo espacio)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # 4. Recorte de seguridad según constante
    if len(texto) > MAX_CARACTERES_TICKET:
        texto = texto[:MAX_CARACTERES_TICKET] + "..."
        
    return texto