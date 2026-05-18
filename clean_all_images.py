import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Ver las imágenes actuales
cursor.execute("SELECT id, url, evento_id, LENGTH(url) as len FROM evento_imagenes ORDER BY id")
imagenes = cursor.fetchall()

print(f"Total de imágenes: {len(imagenes)}")

for img in imagenes:
    img_id, url, evento_id, length = img
    print(f"  ID {img_id} (evento {evento_id}): length={length} - {url[:50]}...")

# Eliminar todas las imágenes (empezar limpio)
print("\nEliminando todas las imágenes...")
cursor.execute("DELETE FROM evento_imagenes")
conn.commit()
print(f"Eliminadas {cursor.rowcount} imágenes")

cursor.close()
conn.close()
print("Listo!")