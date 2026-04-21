import pytest
from unittest.mock import MagicMock
from src.flujo.pipeline import PipelineProcesamiento
from src.nucleo.entidades import TicketAnalizado

def test_pipeline_flujo_completo(monkeypatch):
    # Simulamos la respuesta de la IA
    mock_respuesta_ia = {
        "categoria": "tecnico",
        "urgencia": "alta",
        "intencion": "reportar bug",
        "accion_sugerida": "revisar logs",
        "entidades": {}
    }

    # Creamos instancia del pipeline
    pipeline = PipelineProcesamiento()
    
    # "Mockeamos" el método de solicitar_analisis para no gastar dinero
    pipeline.ia.solicitar_analisis = MagicMock(return_value=mock_respuesta_ia)

    # Ejecutamos
    resultado = pipeline.procesar_ticket("Mi app no abre")

    # Verificamos
    assert isinstance(resultado, TicketAnalizado)
    assert resultado.categoria.value == "tecnico"
    assert resultado.urgencia.value == "alta"