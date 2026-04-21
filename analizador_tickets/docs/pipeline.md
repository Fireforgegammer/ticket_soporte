# Módulo de Flujo - Pipeline de Procesamiento

## Responsabilidad
Este módulo actúa como el **Orquestador Central**. Conecta las capas de Servicios e Infraestructura para cumplir el objetivo de negocio.

## Flujo de Datos
1. **Entrada**: String crudo del usuario.
2. **Transformación**: El `limpiador` elimina ruido.
3. **Enriquecimiento**: El `adaptador_ia` añade contexto semántico (categoría, urgencia).
4. **Validación**: Se fuerza el mapeo a tipos `Enum` para asegurar consistencia.
5. **Salida/Persistencia**: El `repositorio_log` asegura que el resultado sea auditable en formato JSON.

## Manejo de Errores
El pipeline utiliza bloques `try-except` y retornos `Optional` para garantizar que, si un ticket falla (ej. error de API), el sistema pueda continuar procesando el siguiente ticket en una carga por lotes.