# Módulo de Limpieza (Servicios)

## Responsabilidad
Este servicio se encarga de la **sanitización** de la entrada. Su objetivo es reducir el ruido en los datos para mejorar la precisión del modelo NLP y reducir el consumo de tokens.

## Lógica de Procesamiento
1. **Des-HTML**: Elimina etiquetas para evitar que la IA intente interpretar código.
2. **Limpieza de Control**: Elimina caracteres invisibles que rompen los parsers JSON.
3. **Colapso de Espacios**: Unifica el texto para que la IA se centre en las palabras, no en el formato.
4. **Truncado**: Garantiza que nunca se exceda el límite definido en `constantes.py`.