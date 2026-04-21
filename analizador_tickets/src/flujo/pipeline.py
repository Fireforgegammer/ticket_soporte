import logging
from typing import Optional

# Importamos nuestros módulos (el trabajo previo)
from src.servicios import limpiador
from src.infraestructura.adaptador_ia import AdaptadorOpenAI
from src.infraestructura import repositorio_log
from src.nucleo.entidades import TicketAnalizado, CategoriaTicket, UrgenciaTicket

class PipelineProcesamiento:
    def __init__(self):
        self.ia = AdaptadorOpenAI()

    def procesar_ticket(self, texto_usuario: str) -> Optional[TicketAnalizado]:
        """
        Ejecuta el flujo completo de un ticket.
        Limpia -> Analiza -> Mapea -> Guarda.
        """
        try:
            # 1. Limpieza
            texto_limpio = limpiador.normalizar_texto(texto_usuario)
            if not texto_limpio:
                logging.warning("Ticket vacío tras la limpieza.")
                return None

            # 2. Análisis con IA
            resultado_ia = self.ia.solicitar_analisis(texto_limpio)
            if not resultado_ia:
                return None

            # 3. Transformación a Entidad (Mapeo)
            # Aquí convertimos los strings del JSON a nuestros Enums del Núcleo
            ticket = TicketAnalizado(
                texto_original=texto_usuario,
                categoria=CategoriaTicket(resultado_ia.get("categoria", "otro")),
                urgencia=UrgenciaTicket(resultado_ia.get("urgencia", "media")),
                intencion=resultado_ia.get("intencion", "Desconocida"),
                accion_sugerida=resultado_ia.get("accion_sugerida", "Revisión manual"),
                entidades=resultado_ia.get("entidades", {})
            )

            # 4. Persistencia (Logs JSON)
            repositorio_log.guardar_resultado_json(ticket)

            return ticket

        except Exception as e:
            logging.error(f"Fallo catastrófico en el pipeline: {e}")
            return None
