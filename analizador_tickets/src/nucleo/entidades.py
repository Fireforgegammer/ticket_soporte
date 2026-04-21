from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Dict, Any

class CategoriaTicket(Enum):
    CUENTA = "cuenta"
    TECNICO = "tecnico"
    FACTURACION = "facturacion"
    PRODUCTO = "producto"
    OTRO = "otro"

class UrgenciaTicket(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

@dataclass
class TicketAnalizado:
    texto_original: str
    categoria: CategoriaTicket
    urgencia: UrgenciaTicket
    intencion: str
    accion_sugerida: str
    entidades: Dict[str, Any] = field(default_factory=dict)
    fecha_analisis: datetime = field(default_factory=datetime.now)

    def a_diccionario(self) -> Dict[str, Any]:
        """Prepara el objeto para ser guardado como JSON."""
        return {
            "texto": self.texto_original[:100] + "...",
            "categoria": self.categoria.value,
            "urgencia": self.urgencia.value,
            "intencion": self.intencion,
            "accion_sugerida": self.accion_sugerida,
            "entidades": self.entidades,
            "fecha": self.fecha_analisis.isoformat()
        }