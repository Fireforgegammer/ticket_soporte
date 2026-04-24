import logging
from typing import Optional
from src.servicios import limpiador
from src.infraestructura.adaptador_ia import AdaptadorOpenAI
from src.infraestructura import repositorio_log
from src.nucleo.entidades import TicketAnalizado, CategoriaTicket, UrgenciaTicket

class PipelineProcesamiento:
    def __init__(self):
        self.ia = AdaptadorOpenAI()

    def procesar_ticket(self, texto_usuario: str, motor: str = "ollama") -> Optional[TicketAnalizado]:
        """Flujo completo: Limpieza -> IA (motor elegido) -> Mapeo -> Log."""
        try:
            texto_limpio = limpiador.normalizar_texto(texto_usuario)
            if not texto_limpio:
                return None

            # Llamamos a la IA indicando qué motor usar
            resultado_ia = self.ia.solicitar_analisis(texto_limpio, motor=motor)
            
            if not resultado_ia:
                return None

            ticket = TicketAnalizado(
                texto_original=texto_usuario,
                categoria=CategoriaTicket(resultado_ia.get("categoria", "otro")),
                urgencia=UrgenciaTicket(resultado_ia.get("urgencia", "media")),
                intencion=resultado_ia.get("intencion", "Desconocida"),
                accion_sugerida=resultado_ia.get("accion_sugerida", "Revisión manual"),
                entidades=resultado_ia.get("entidades", {})
            )

            repositorio_log.guardar_resultado_json(ticket)
            return ticket

        except Exception as e:
            logging.error(f"Fallo en pipeline: {e}")
            return None