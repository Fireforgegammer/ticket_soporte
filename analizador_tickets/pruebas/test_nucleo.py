import pytest
from datetime import datetime
from src.nucleo.entidades import TicketAnalizado, CategoriaTicket, UrgenciaTicket

def test_creacion_ticket_analizado():
    """Verifica que un ticket se instancie correctamente con sus tipos."""
    ticket = TicketAnalizado(
        texto_original="Problema de login",
        categoria=CategoriaTicket.CUENTA,
        urgencia=UrgenciaTicket.ALTA,
        intencion="Restablecer acceso",
        accion_sugerida="Enviar link de reset",
        entidades={"email": "test@error.com"}
    )
    
    assert ticket.categoria == CategoriaTicket.CUENTA
    assert ticket.urgencia == UrgenciaTicket.ALTA
    assert isinstance(ticket.fecha_analisis, datetime)

def test_metodo_a_diccionario():
    """Verifica la serialización para los logs JSON."""
    ticket = TicketAnalizado(
        texto_original="Error en factura",
        categoria=CategoriaTicket.FACTURACION,
        urgencia=UrgenciaTicket.MEDIA,
        intencion="Duda cobro",
        accion_sugerida="Revisar cuenta",
        entidades={}
    )
    
    diccionario = ticket.a_diccionario()
    
    assert diccionario["categoria"] == "facturacion"
    assert diccionario["urgencia"] == "media"
    assert "fecha" in diccionario
    # Verificar que el texto se trunca para el log si es necesario
    assert len(diccionario["texto"]) <= 105 

def test_enums_valores_correctos():
    """Asegura que los valores de los Enums no hayan cambiado (contrato de datos)."""
    assert CategoriaTicket.TECNICO.value == "tecnico"
    assert UrgenciaTicket.BAJA.value == "baja"

def test_ticket_entidades_por_defecto():
    """Verifica que el campo entidades sea un dict vacío si no se proporciona."""
    ticket = TicketAnalizado(
        "Texto", CategoriaTicket.OTRO, UrgenciaTicket.BAJA, "Intencion", "Accion"
    )
    assert ticket.entidades == {}