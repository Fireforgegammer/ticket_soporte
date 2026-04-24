import os
from dotenv import load_dotenv
from interface.app import AppSoporteNLP

def main():
    # 1. Forzar carga del .env desde la raíz
    load_dotenv()
    
    # 2. Debug para estar 100% seguros
    key = os.getenv("GROQ_API_KEY")
    if key:
        print(f"✅ Llave cargada correctamente: {key[:8]}...")
    else:
        print("❌ ERROR: No se lee la variable GROQ_API_KEY del .env")

    print("🚀 Iniciando Interface Gráfica...")
    app = AppSoporteNLP()
    app.mainloop()

if __name__ == "__main__":
    main()