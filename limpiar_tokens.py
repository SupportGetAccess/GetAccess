import requests
import os

# Limpiar tokens de reset en producción
import os`nSUPABASE_URI = os.environ.get("SUPABASE_URI")

try:
    import psycopg2
    conn = psycopg2.connect(SUPABASE_URI)
    cur = conn.cursor()
    cur.execute("DELETE FROM password_reset")
    conn.commit()
    print("Tokens limpiados")
except Exception as e:
    print(f"Error: {e}")