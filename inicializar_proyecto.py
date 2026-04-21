import os

def crear_estructura_proyecto():
    # Nombre de la carpeta raíz
    raiz = "analizador_tickets"

    # Definición de la jerarquía de carpetas
    carpetas = [
        "datos",
        "logs",
        "pruebas",
        "src/nucleo",
        "src/servicios",
        "src/infraestructura",
        "src/flujo",
    ]

    # Definición de archivos base (vacíos o con estructura mínima)
    archivos = {
        "src/nucleo/entidades.py": "# Definición de Dataclasses y Enums\n",
        "src/nucleo/constantes.py": "# Prompts y configuraciones constantes\n",
        "src/servicios/motor_ia.py": "# Interfaz lógica para motores de IA\n",
        "src/servicios/limpiador.py": "# Lógica de preprocesamiento de texto\n",
        "src/servicios/ejecutor.py": "# Lógica de acciones post-análisis\n",
        "src/infraestructura/adaptador_ia.py": "# Implementación de API OpenAI/Ollama\n",
        "src/infraestructura/repositorio_log.py": "# Persistencia de JSON en logs\n",
        "src/flujo/pipeline.py": "# Orquestación del proceso\n",
        "pruebas/test_limpiador.py": "# Tests para el módulo limpiador\n",
        "principal.py": "if __name__ == '__main__':\n    pass\n",
        ".env": "OPENAI_API_KEY=tu_clave_aqui\n",
        "requirements.txt": "openai\npython-dotenv\npytest\n",
        ".gitignore": ".env\n__pycache__/\nlogs/\n*.log\n"
    }

    print(f"🚀 Iniciando creación del proyecto: {raiz}")

    # Crear carpetas
    for carpeta in carpetas:
        ruta_completa = os.path.join(raiz, carpeta)
        os.makedirs(ruta_completa, exist_ok=True)
        # Crear __init__.py para que sean paquetes válidos de Python
        if "src" in carpeta or "pruebas" in carpeta:
            with open(os.path.join(ruta_completa, "__init__.py"), "w") as f:
                pass
        print(f"✅ Carpeta creada: {ruta_completa}")

    # Crear archivos
    for ruta_archivo, contenido in archivos.items():
        ruta_completa = os.path.join(raiz, ruta_archivo)
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"📄 Archivo creado: {ruta_completa}")

    print("\n✨ Estructura modular profesional creada con éxito.")

if __name__ == "__main__":
    crear_estructura_proyecto()