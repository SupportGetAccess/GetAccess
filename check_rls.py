import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

# Ver todas las tablas y su estado RLS
cursor.execute("""
    SELECT 
        t.table_name,
        CASE WHEN r.rls_enabled THEN 'ON' ELSE 'OFF' END as rls_status
    FROM information_schema.tables t
    LEFT JOIN pg_tables pt ON pt.tablename = t.table_name AND pt.schemaname = 'public'
    LEFT JOIN pg_policies p ON p.tablename = t.table_name
    LEFT JOIN (SELECT relname, relrowsecurity as rls_enabled FROM pg_class) r ON r.relname = t.table_name
    WHERE t.table_schema = 'public'
    AND t.table_type = 'BASE TABLE'
    ORDER BY t.table_name
""")

print("Tablas y estado RLS:")
print("-" * 50)
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")

# Ver columnas sensibles
print("\n\nColumnas con datos sensibles (sin RLS):")
print("-" * 50)

cursor.execute("""
    SELECT table_name, column_name 
    FROM information_schema.columns 
    WHERE table_schema = 'public'
    AND column_name IN ('password', 'password_hash', 'codigo_verificacion', 'token', 'secret', 'api_key')
    ORDER BY table_name
""")

for row in cursor.fetchall():
    print(f"  {row[0]}.{row[1]}")

cursor.close()
conn.close()