Este archivo, te crea toda la estructura del programa, gracias a su codigo, lo unico que yo cambie fue el nombre de principal.py por main.py, y añadir la carpeta docs, pues no la tenia creada de mano, la estructura que me creo es la siguiente.


analizador_tickets/
│
├── logs/                       # Historial de tickets procesados (JSON)
│   └── tickets_procesados.log  # O un archivo por día
│
├── pruebas/                    # Directorio de tests (Pytest)
│   ├── __init__.py
│   └── test_limpiador.py
│
├── src/                        # Código fuente
│   ├── __init__.py
│   │
│   ├── nucleo/                 # Modelos de datos y constantes
│   │   ├── __init__.py
│   │   ├── entidades.py        # Clases de Ticket y Enums
│   │   └── constantes.py       # Configuraciones y Prompts
│   │
│   ├── servicios/              # Lógica de negocio (Servicios)
│   │   ├── __init__.py
│   │   ├── motor_ia.py         # Interfaz para OpenAI / Ollama
│   │   ├── limpiador.py        # Preprocesamiento de texto
│   │   └── ejecutor.py         # Lógica de acciones tras el análisis
│   │
│   ├── infraestructura/        # Salida de datos y clientes externos
│   │   ├── __init__.py
│   │   ├── adaptador_ia.py     # Implementación concreta de la API
│   │   └── repositorio_log.py  # Manejo de escritura de JSON en logs
│   │
│   └── flujo/                  # Orquestación (Pipeline)
│       ├── __init__.py
│       └── pipeline.py         # El proceso paso a paso
│
├── .env                        # Configuración de entorno
├── .gitignore
├── requirements.txt            # Dependencias
└── principal.py                # Main (Punto de entrada estándar)

 mkdir datos, logs, pruebas, src/nucleo, src/servicios, src/infraestructura, src/flujo; New-Item -Path "src/nucleo/entidades.py" -Value "# Definición de Dataclasses y Enums`n" -Force; New-Item -Path "src/nucleo/constantes.py" -Value "# Prompts y configuraciones constantes`n" -Force; New-Item -Path "src/servicios/motor_ia.py" -Value "# Interfaz lógica para motores de IA`n" -Force; New-Item -Path "src/servicios/limpiador.py" -Value "# Lógica de preprocesamiento de texto`n" -Force; New-Item -Path "src/servicios/ejecutor.py" -Value "# Lógica de acciones post-análisis`n" -Force; New-Item -Path "src/infraestructura/adaptador_ia.py" -Value "# Implementación de API OpenAI/Ollama`n" -Force; New-Item -Path "src/infraestructura/repositorio_log.py" -Value "# Persistencia de JSON en logs`n" -Force; New-Item -Path "src/flujo/pipeline.py" -Value "# Orquestación del proceso`n" -Force; New-Item -Path "pruebas/test_limpiador.py" -Value "# Tests para el módulo limpiador`n" -Force; New-Item -Path "principal.py" -Value "if __name__ == '__main__':`n    pass`n" -Force; New-Item -Path ".env" -Value "OPENAI_API_KEY=tu_clave_aqui" -Force; New-Item -Path "requirements.txt" -Value "openai`npython-dotenv`npytest" -Force; New-Item -Path ".gitignore" -Value ".env`n__pycache__/`nlogs/`n*.log" -Force