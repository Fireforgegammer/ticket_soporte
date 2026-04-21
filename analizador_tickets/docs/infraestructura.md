# Módulo de Infraestructura - Persistencia

## Responsabilidad
Gestionar la salida de datos del sistema. En esta fase, se implementa una persistencia basada en archivos planos para logs.

## Decisiones Técnicas
1. **Formato JSONL (JSON Lines)**: Cada línea es un objeto JSON válido. Esto permite:
   - Procesar archivos gigantes sin cargar todo en memoria.
   - Robustez: si el proceso se corta, solo se pierde la última línea.
2. **Uso de Pathlib**: Para asegurar que el código funcione igual en Windows y Linux.
3. **Desacoplamiento**: El sistema no sabe *dónde* se guarda (podría ser una DB mañana), solo llama a la función de guardado.