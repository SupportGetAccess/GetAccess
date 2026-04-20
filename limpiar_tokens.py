import requests
import os

# Limpiar tokens de reset en producción
SUPABASE_URI = "postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

try:
    import psycopg2
    conn = psycopg2.connect(SUPABASE_URI)
    cur = conn.cursor()
    cur.execute("DELETE FROM password_reset")
    conn.commit()
    print("Tokens limpiados")
except Exception as e:
    print(f"Error: {e}")