import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Ver las imágenes actuales
cursor.execute("SELECT id, url, evento_id FROM evento_imagenes ORDER BY id")
imagenes = cursor.fetchall()

print(f"Total de imágenes: {len(imagenes)}")
print("\nImágenes guardadas:")

for img in imagenes:
    img_id, url, evento_id = img
    if url and url.startswith('data:'):
        print(f"  ID {img_id} (evento {evento_id}): {url[:80]}... (BASE64 - PROBLEMA)")
    else:
        print(f"  ID {img_id} (evento {evento_id}): {url[:80]}... (URL OK)")

print("\nEliminando imágenes base64...")
cursor.execute("DELETE FROM evento_imagenes WHERE url LIKE 'data:%'")
conn.commit()
print(f"Eliminadas {cursor.rowcount} imágenes problemáticas")

cursor.close()
conn.close()