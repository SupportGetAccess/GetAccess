import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Listar todas las tablas
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    ORDER BY table_name
""")

print("=== TABLAS EN LA BASE DE DATOS ===\n")
tablas = []
for row in cur.fetchall():
    tabla = row[0]
    tablas.append(tabla)
    print(f"• {tabla}")

# Para cada tabla, buscar columnas que contengan 'user' o 'usuario'
print("\n=== REFERENCIAS A USUARIOS POR TABLA ===\n")
for tabla in tablas:
    cur.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{tabla}' 
        AND (column_name LIKE '%user%' OR column_name LIKE '%usuario%')
    """)
    cols = cur.fetchall()
    if cols:
        print(f"{tabla}:")
        for c in cols:
            print(f"  - {c[0]}")

conn.close()