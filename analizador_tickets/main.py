import sys
import logging
from src.flujo.pipeline import PipelineProcesamiento

# Configuración básica de logging para consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def mostrar_menu():
    print("\n" + "="*40)
    print("   SISTEMA DE ANÁLISIS DE TICKETS (NLP)")
    print("="*40)
    print("1. Analizar un ticket nuevo")
    print("2. Salir")
    return input("\nSeleccione una opción: ")

def ejecutar_consola():
    """Bucle principal de interacción con el usuario."""
    pipeline = PipelineProcesamiento()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            print("\nEscriba el contenido del ticket (Presione Enter para procesar):")
            texto = input("> ").strip()
            
            if not texto:
                print("⚠️ El ticket no puede estar vacío.")
                continue
                
            print("\n🤖 Procesando con IA...")
            resultado = pipeline.procesar_ticket(texto)
            
            if resultado:
                print("\n✅ ANÁLISIS COMPLETADO:")
                print(f"   📂 CATEGORÍA: {resultado.categoria.value.upper()}")
                print(f"   🚨 URGENCIA:  {resultado.urgencia.value.upper()}")
                print(f"   🎯 INTENCIÓN: {resultado.intencion}")
                print(f"   🔧 ACCIÓN:    {resultado.accion_sugerida}")
                print(f"\n💾 Resultado guardado en logs/tickets_procesados.jsonl")
            else:
                print("\n❌ No se pudo procesar el ticket. Revise su conexión o API Key.")
                
        elif opcion == "2":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    try:
        ejecutar_consola()
    except KeyboardInterrupt:
        print("\n\nAbortado por el usuario.")
        sys.exit(0)