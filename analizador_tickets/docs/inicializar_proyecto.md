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