import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

print("=== SOLICITUDES PENDIENTES ===\n")
cur.execute("""
    SELECT s.id, s.usuario_id, s.estado, s.created_at, u.email, u.nombre, u.apellido
    FROM solicitud_organizer s
    JOIN usuarios u ON s.usuario_id = u.id
    WHERE s.estado = 'pendiente'
    ORDER BY s.created_at DESC
""")

for row in cur.fetchall():
    print(f"ID Solicitud: {row[0]}")
    print(f"  Usuario ID: {row[1]}")
    print(f"  Email: {row[4]}")
    print(f"  Nombre: {row[5]} {row[6]}")
    print(f"  Estado: {row[2]}")
    print(f"  Fecha: {row[3]}")
    print()

conn.close()