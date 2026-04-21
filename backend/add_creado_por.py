import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
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