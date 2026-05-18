import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Buscar eventos con imagen base64
cursor.execute("SELECT id, nombre, imagen FROM eventos WHERE imagen LIKE 'data:%' OR imagen LIKE '[%'")
eventos = cursor.fetchall()

print(f"Eventos con imagen base64/array: {len(eventos)}")

for ev in eventos:
    ev_id, nombre, imagen = ev
    # Poner una URL pública
    new_img = "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800"
    cursor.execute("UPDATE eventos SET imagen = %s WHERE id = %s", (new_img, ev_id))
    print(f"  Evento {ev_id} ({nombre}) -> Limpiado")

conn.commit()
print("Listo!")

cursor.close()
conn.close()