#!/usr/bin/env python3
"""Script para limpiar entradas pendientes de la base de datos"""

import os
import psycopg2

# Conectar a Supabase
SUPABASE_URI = os.environ.get("SUPABASE_URI", "postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres")

def main():
    print(">>> Conectando a la base de datos...")
    conn = psycopg2.connect(SUPABASE_URI)
    cur = conn.cursor()
    
    # Paso 1: Actualizar entradas pendientes con código GA- a pagada
    print(">>> Actualizando entradas pendientes con código a 'pagada'...")
    cur.execute("""
        UPDATE entradas 
        SET estado = 'pagada' 
        WHERE estado = 'pendiente' AND preference_id LIKE 'GA-%%'
    """)
    actualizadas = cur.rowcount
    print(f">>> {actualizadas} entradas actualizadas a 'pagada'")
    
    # Paso 2: Eliminar entradas pendientes sin código
    print(">>> Eliminando entradas pendientes sin código...")
    cur.execute("""
        DELETE FROM entradas 
        WHERE estado = 'pendiente' AND (preference_id IS NULL OR preference_id NOT LIKE 'GA-%%')
    """)
    eliminadas = cur.rowcount
    print(f">>> {eliminadas} entradas eliminadas")
    
    conn.commit()
    
    # Verificar resultado
    cur.execute("SELECT COUNT(*) FROM entradas WHERE estado = 'pendiente'")
    pendientes = cur.fetchone()[0]
    print(f">>> Entradas pendientes restantes: {pendientes}")
    
    cur.close()
    conn.close()
    print(">>> Limpieza completada!")

if __name__ == "__main__":
    main()