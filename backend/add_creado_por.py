import os
import psycopg2
conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE eventos ADD COLUMN creado_por INTEGER")
    print("Columna creada_por agregada")
except Exception as e:
    print(f"Error: {e}")

# Actualizar eventos existentes para que sean del admin (asumiendo que admin tiene id 1 o 2)
try:
    cur.execute("UPDATE eventos SET creado_por = 1 WHERE creado_por IS NULL")
    conn.commit()
    print("Eventos existentes actualizados")
except Exception as e:
    print(f"Error actualizando: {e}")

conn.close()
print("Listo")