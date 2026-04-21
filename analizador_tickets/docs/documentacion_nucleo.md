# Documentación del Módulo Núcleo (Core)

## Descripción
El paquete `src.nucleo` contiene las definiciones fundamentales del sistema. Está diseñado siguiendo el principio de **Independencia del Dominio**, lo que significa que estas clases no conocen la existencia de la IA ni de la base de datos.

## Componentes Principales

### 1. Entidades (`entidades.py`)
Utiliza `dataclasses` para definir la estructura de datos de los tickets procesados.
- **TicketAnalizado**: Clase principal que centraliza el resultado del análisis.
    - Método `a_diccionario()`: Facilita la serialización para el guardado en archivos de log JSON.

### 2. Tipos Constantes (`entidades.py` - Enums)
Se utilizan `Enum` para garantizar la integridad de los datos:
- `CategoriaTicket`: Define las categorías permitidas.
- `UrgenciaTicket`: Define los niveles de prioridad.

### 3. Configuraciones (`constantes.py`)
Centraliza los valores estáticos y el `PROMPT_SISTEMA`. Separar el prompt permite realizar "Prompt Engineering" sin modificar la lógica de ejecución.

---

## Estándares de Nomenclatura
- **Clases**: PascalCase (ej. `TicketAnalizado`).
- **Constantes**: SCREAMING_SNAKE_CASE (ej. `PROMPT_SISTEMA_ANALISIS`).
- **Métodos/Funciones**: snake_case (ej. `a_diccionario`).