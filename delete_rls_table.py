import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

print("Conectando a Supabase...")
conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Verificar si la tabla existe
cursor.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_name = 'rls_disabled_in_public'
""")
result = cursor.fetchone()

if result:
    print(f"Eliminando tabla {result[0]}...")
    cursor.execute('DROP TABLE rls_disabled_in_public')
    conn.commit()
    print("Tabla eliminada correctamente")
else:
    print("La tabla no existe")

cursor.close()
conn.close()