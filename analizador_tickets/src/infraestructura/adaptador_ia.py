import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

from src.nucleo.constantes import PROMPT_SISTEMA_ANALISIS, MODELO_POR_DEFECTO

load_dotenv()

class AdaptadorOpenAI:
    def __init__(self):
        self.cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.modelo = MODELO_POR_DEFECTO

    def solicitar_analisis(self, texto_limpio: str) -> Optional[Dict[str, Any]]:
        """
        Envía el texto a la API y retorna el diccionario con el análisis.
        """
        try:
            respuesta = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": PROMPT_SISTEMA_ANALISIS},
                    {"role": "user", "content": texto_limpio}
                ],
                temperature=0,
                response_format={"type": "json_object"}  # Forzamos salida JSON
            )
            
            contenido = respuesta.choices[0].message.content
            return json.loads(contenido)
            
        except Exception as e:
            # En un entorno real, aquí usaríamos logging.error
            print(f"Error en la llamada a la IA: {e}")
            return None
