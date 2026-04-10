import os
import sys

# Forzar modo producción para probar Supabase
os.environ["RENDER"] = "true"
os.environ["SUPABASE_URI"] = "postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

# Importar config para que tome la variable
import config
config.DATABASE_URL = config.SUPABASE_URI

# Importar y ejecutar uvicorn
import uvicorn
from main import app

if __name__ == "__main__":
    print(">>> Iniciando backend con Supabase PostgreSQL...")
    print(f">>> DATABASE_URL: {config.DATABASE_URL}")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)