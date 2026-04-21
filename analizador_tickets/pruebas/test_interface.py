import pytest
from unittest.mock import MagicMock, patch
from interface.app import AppAnalisis
from src.nucleo.entidades import TicketAnalizado, CategoriaTicket, UrgenciaTicket

@pytest.fixture
def app():
    # El patch de mainloop es correcto para no abrir la ventana
    with patch('customtkinter.CTk.mainloop'):
        return AppAnalisis()

def test_actualizacion_visual_tras_analisis(app):
    """Verifica que los labels de la interface se actualizan con los datos del ticket."""
    ticket_mock = TicketAnalizado(
        texto_original="Prueba",
        categoria=CategoriaTicket.TECNICO,
        urgencia=UrgenciaTicket.ALTA,
        intencion="Test",
        accion_sugerida="Reparar"
    )
    
    app.pipeline.procesar_ticket = MagicMock(return_value=ticket_mock)
    
    # IMPORTANTE: Llamamos a ejecutar_analisis directamente pasando un texto
    # Esto evita que el test intente leer del widget de Tkinter (evita el RuntimeError)
    app.ejecutar_analisis(texto_forzado="Mi app no funciona")
    
    # Forzamos la actualización de eventos pendientes de Tkinter
    app.update_idletasks()
    
    assert app.cat_label.cget("text") == "CATEGORÍA: TECNICO"
    assert app.urg_label.cget("text") == "URGENCIA: ALTA"