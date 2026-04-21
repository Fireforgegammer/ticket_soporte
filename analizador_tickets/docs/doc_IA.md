# Módulo de Infraestructura - Adaptador de IA

## Responsabilidad
Gestionar la comunicación externa con los Modelos de Lenguaje (LLM).

## Decisiones Técnicas
1. **Response Format JSON**: Se utiliza el parámetro nativo de la API para garantizar que la respuesta sea un JSON válido, evitando errores de parseo manual.
2. **Temperatura 0**: Crucial para tareas de clasificación; queremos respuestas deterministas y consistentes, no creativas.
3. **Variables de Entorno**: La API Key nunca reside en el código, se carga mediante `python-dotenv`.