import os
import sys

# Forzar modo producción para probar Supabase
os.environ["RENDER"] = "true"

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

# Importar y ejecutar uvicorn
import uvicorn
from main import app

if __name__ == "__main__":
    print(">>> Iniciando backend con Supabase PostgreSQL...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)