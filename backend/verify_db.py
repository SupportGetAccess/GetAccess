import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

print("=== USUARIOS ===")
cur.execute("SELECT id, email, nombre, rol, verificado FROM usuarios ORDER BY id")
for row in cur.fetchall():
    print(f"ID: {row[0]} | Email: {row[1]} | Nombre: {row[2]} | Rol: {row[3]} | Verificado: {row[4]}")

print("\n=== ENTRADAS POR USUARIO ===")
cur.execute("SELECT usuario_id, COUNT(*) FROM entradas GROUP BY usuario_id ORDER BY usuario_id")
for row in cur.fetchall():
    print(f"Usuario ID {row[0]}: {row[1]} entradas")

print("\n=== SOLICITUDES ORGanizador ===")
cur.execute("SELECT id, usuario_id, estado, created_at FROM solicitud_organizer ORDER BY id")
for row in cur.fetchall():
    print(f"ID: {row[0]} | Usuario ID: {row[1]} | Estado: {row[2]} | Fecha: {row[3]}")

print("\n=== EVENTOS CREADOS POR ===")
cur.execute("SELECT id, nombre, creado_por FROM eventos ORDER BY id")
for row in cur.fetchall():
    print(f"ID: {row[0]} | Nombre: {row[1]} | Creador ID: {row[2]}")

conn.close()