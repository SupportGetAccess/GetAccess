import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Agregar los eventos que faltan
eventos_faltantes = [
    ("Cirque du Soleil - O", "El espectáculo acuático más impresionante del mundo.", "2026-05-25", "Estadio GEBA, Buenos Aires", 12000, 3000, 1200, "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800", "espectaculo"),
    ("Conferencia Tech Summit 2026", "Los líderes tecnológicos del mundo comparten el futuro de la IA.", "2026-08-10", "Centro de Convenciones, Buenos Aires", 25000, 2000, 500, "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800", "conferencia"),
    ("Roger Waters - This Is Not A Drill", "El legendario líder de Pink Floyd presenta su gira de regreso.", "2026-09-15", "Estadio Monumental, Buenos Aires", 38000, 65000, 60000, "https://images.unsplash.com/photo-1598387993441-a364f854c3e1?w=800", "musica"),
]

cur.executemany(
    "INSERT INTO eventos (nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, imagen, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    eventos_faltantes
)

conn.commit()
print(">>> Eventos agregados")

cur.execute("SELECT id, nombre FROM eventos ORDER BY id")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()