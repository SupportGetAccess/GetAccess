import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Buscar y limpiar TODAS las imágenes base64
cursor.execute("SELECT id, nombre, imagen FROM eventos WHERE imagen LIKE 'data:%' OR imagen LIKE '[%'")
eventos = cursor.fetchall()

print(f"Eventos con imagen problematica: {len(eventos)}")

for ev in eventos:
    ev_id, nombre, imagen = ev
    print(f"  Limpiando evento {ev_id}: {nombre[:30]}...")
    # Poner URL vacía
    cursor.execute("UPDATE eventos SET imagen = '' WHERE id = %s", (ev_id,))

conn.commit()
print(f"\nTotal limpiados: {len(eventos)}")

cursor.close()
conn.close()