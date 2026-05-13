import psycopg2
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import config
DATABASE_URL = config.SUPABASE_URI

def agregar_columnas():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    columnas = [
        ("email_comprador", "TEXT"),
        ("nombre_comprador", "TEXT"),
        ("apellido_comprador", "TEXT"),
        ("telefono_comprador", "TEXT")
    ]
    
    for columna, tipo in columnas:
        try:
            cur.execute(f"ALTER TABLE entradas ADD COLUMN {columna} {tipo}")
            print(f"[OK] Columna {columna} agregada")
        except psycopg2.errors.DuplicateColumn:
            print(f"[-] Columna {columna} ya existe")
    
    try:
        cur.execute("ALTER TABLE entradas ALTER COLUMN usuario_id DROP NOT NULL")
        print("[OK] usuario_id ahora es nullable")
    except Exception as e:
        print(f"[-] usuario_id: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Proceso completado")

if __name__ == "__main__":
    agregar_columnas()