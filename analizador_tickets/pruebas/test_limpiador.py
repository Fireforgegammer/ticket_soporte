import pytest
from src.servicios.limpiador import normalizar_texto

def test_limpiar_html_y_espacios():
    entrada = "   <p>Hola</p>    mundo \n\n  "
    esperado = "Hola mundo"
    assert normalizar_texto(entrada) == esperado

def test_limpiar_caracteres_control():
    # \x01 es un carácter de control (Start of Heading)
    entrada = "Texto\x01 con ruido"
    esperado = "Texto con ruido"
    assert normalizar_texto(entrada) == esperado

def test_manejo_entrada_vacia():
    assert normalizar_texto("") == ""
    assert normalizar_texto(None) == ""

def test_truncado_maximo(monkeypatch):
    # Forzamos una constante pequeña para el test
    import src.servicios.limpiador as limpiador
    monkeypatch.setattr("src.servicios.limpiador.MAX_CARACTERES_TICKET", 5)
    
    entrada = "Texto muy largo"
    resultado = normalizar_texto(entrada)
    assert len(resultado) <= 8 # 5 caracteres + "..."
    assert resultado.endswith("...")
