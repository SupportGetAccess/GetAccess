import psycopg2
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Actualizar entradas
cur.execute("UPDATE entradas SET usuario_id = 1 WHERE usuario_id = 999")
print("entradas actualizadas")

# Actualizar solicitud_organizer  
cur.execute("UPDATE solicitud_organizer SET usuario_id = 2 WHERE usuario_id = 4")
print("solicitud_organizer actualizada")

conn.commit()

print("\n=== Verificacion final ===")

# Entradas
cur.execute("SELECT id, usuario_id, evento_id FROM entradas ORDER BY id")
print("\nEntradas:")
for row in cur.fetchall():
    print(row)

# Eventos creados por
cur.execute("SELECT id, nombre, creado_por FROM eventos ORDER BY id")
print("\nEventos:")
for row in cur.fetchall():
    print(row)

# Solicitudes
cur.execute("SELECT id, usuario_id, estado FROM solicitud_organizer ORDER BY id")
print("\nSolicitudes:")
for row in cur.fetchall():
    print(row)

conn.close()