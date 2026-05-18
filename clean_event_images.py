import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Ver las imágenes en la tabla eventos
cursor.execute("SELECT id, nombre, imagen, LENGTH(imagen) as len FROM eventos WHERE imagen IS NOT NULL AND imagen != ''")
eventos = cursor.fetchall()

print(f"Total de eventos con imagen: {len(eventos)}")

for ev in eventos:
    ev_id, nombre, imagen, length = ev
    if imagen and imagen.startswith('data:'):
        print(f"  Evento {ev_id} ({nombre}): {length} bytes - BASE64")
        
        # Buscar una URL pública placeholder
        if 'maraton' in nombre.lower():
            new_img = "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800"
        elif 'rock' in nombre.lower():
            new_img = "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800"
        elif ' techno' in nombre.lower():
            new_img = "https://images.unsplash.com/photo-1574169208507-84376144848b?w=800"
        else:
            new_img = "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800"
        
        cursor.execute("UPDATE eventos SET imagen = %s WHERE id = %s", (new_img, ev_id))
        print(f"    -> Actualizado a URL pública")

conn.commit()

# Verificar
cursor.execute("SELECT id, nombre, imagen FROM eventos WHERE imagen IS NOT NULL AND imagen != ''")
eventos2 = cursor.fetchall()
print(f"\nEventos con imagen después de limpiar: {len(eventos2)}")
for ev in eventos2:
    print(f"  Evento {ev[0]} ({ev[1]}): {ev[2][:60]}...")

cursor.close()
conn.close()
print("\nListo!")