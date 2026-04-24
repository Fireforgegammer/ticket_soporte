import os
import json
import requests
import re
from typing import Optional, Dict, Any
from src.nucleo.constantes import MODELO_POR_DEFECTO, PROMPT_SISTEMA_ANALISIS

class AdaptadorOpenAI:
    def __init__(self):
        self.modelo_local = MODELO_POR_DEFECTO  # qwen3.5:2b
        # CAMBIO CRÍTICO: grok-beta ya no existe, usamos grok-2-latest
        self.modelo_xai = "grok-2-latest" 
        
        self.url_ollama = "http://127.0.0.1:11434/api/chat"
        self.url_xai = "https://api.x.ai/v1/chat/completions"
        
        self.api_key_xai = os.getenv("GROQ_API_KEY")

    def solicitar_analisis(self, texto_limpio: str, motor: str = "ollama") -> Optional[Dict[str, Any]]:
        try:
            if motor == "groq":
                if not self.api_key_xai: return None
                
                headers = {
                    "Authorization": f"Bearer {self.api_key_xai}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.modelo_xai,
                    "messages": [
                        {"role": "system", "content": PROMPT_SISTEMA_ANALISIS},
                        {"role": "user", "content": texto_limpio}
                    ],
                    "temperature": 0
                }
                # Timeout de 60s para la nube
                response = requests.post(self.url_xai, headers=headers, json=payload, timeout=60)
            
            else:
                # OLLAMA LOCAL
                payload = {
                    "model": self.modelo_local,
                    "messages": [
                        {"role": "system", "content": PROMPT_SISTEMA_ANALISIS},
                        {"role": "user", "content": texto_limpio}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.1},
                    "think": False # Aumentamos el límite de tokens para respuestas más largas
                }
                # Subimos el timeout a 300s (5 min) para evitar el "Read timed out"
                response = requests.post(self.url_ollama, json=payload, timeout=300)

            if response.status_code == 200:
                res_json = response.json()
                contenido = res_json['choices'][0]['message']['content'] if motor == "groq" else res_json['message']['content']
                return self._limpiar_y_parsear_json(contenido)
            
            # Debug de errores específicos en consola
            print(f"⚠️ Error {response.status_code} de {motor.upper()}: {response.text}")
            return None

        except Exception as e:
            print(f"❌ Error crítico en adaptador_ia: {str(e)}")
            return None

    def _limpiar_y_parsear_json(self, texto: str) -> Optional[Dict[str, Any]]:
        try:
            # Eliminar razonamientos de modelos Qwen/DeepSeek
            texto = re.sub(r'<think>.*?</think>', '', texto, flags=re.DOTALL)
            # Extraer solo lo que está entre llaves { }
            match = re.search(r'(\{.*\})', texto, re.DOTALL)
            if match:
                return json.loads(match.group(1).strip())
            return json.loads(texto.strip())
        except Exception as e:
            print(f"⚠️ Error al parsear JSON: {e}")
            return None