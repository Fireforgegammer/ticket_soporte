# Módulo de Interface Gráfica (GUI)

## Responsabilidad
Proporcionar una capa visual para el usuario final, permitiendo la interacción con el sistema de análisis sin conocimientos de consola.

## Decisiones de Diseño
1. **Librería CustomTkinter**: Elegida por su capacidad de renderizado moderno y soporte nativo de "Dark Mode", alineándose con la estética de herramientas de IA actuales (Ollama/Llama).
2. **Asincronía (Multithreading)**: Las llamadas al `Pipeline` se ejecutan en un hilo secundario (`threading.Thread`). Esto evita el bloqueo del hilo principal de la UI (Event Loop) mientras se espera la respuesta de la API.
3. **Inyección de Dependencias**: La clase `AppAnalisis` instancia el `PipelineProcesamiento`, delegando toda la lógica de negocio y persistencia a las capas inferiores.

## Estructura Visual
- **Sidebar**: Estado del sistema y metadatos.
- **Main Area**: Entrada de texto estilo terminal.
- **Info Panel**: Visualización de los Enums (Categoría y Urgencia) procesados.