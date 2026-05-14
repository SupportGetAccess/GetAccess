import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

print('=== MIGRACION: Marcar entradas 96 y 97 como expiradas ===')
print()

# Entradas a procesar
entradas_ids = [96, 97]

for entrada_id in entradas_ids:
    # Obtener datos de la entrada
    cur.execute("SELECT id, evento_id, cantidad, estado, email_comprador FROM entradas WHERE id = %s", (entrada_id,))
    datos = cur.fetchone()
    
    if not datos:
        print(f'Entrada {entrada_id} no encontrada')
        continue
    
    print(f'Procesando entrada {entrada_id}:')
    print(f'  Evento: {datos[1]}')
    print(f'  Cantidad: {datos[2]}')
    print(f'  Estado actual: {datos[3]}')
    print(f'  Email: {datos[4]}')
    
    # Restaurar stock del evento
    cur.execute("UPDATE eventos SET vendidos = vendidos - %s WHERE id = %s", (datos[2], datos[1]))
    print(f'  Stock restaurado: vendidos - {datos[2]}')
    
    # Marcar como expirada
    cur.execute("UPDATE entradas SET estado = %s WHERE id = %s", ('expirada', entrada_id))
    print(f'  Estado cambiado a: expirada')
    print()

conn.commit()

# Verificar resultado
print('=== VERIFICACION ===')
cur.execute("""
    SELECT e.id, e.evento_id, e.estado, ev.nombre, ev.vendidos
    FROM entradas e
    JOIN eventos ev ON e.evento_id = ev.id
    WHERE e.id IN (96, 97)
""")
for row in cur.fetchall():
    print(f'Entrada {row[0]}: estado={row[2]}, evento={row[3]}, vendidos={row[4]}')

print()
print('Migracion completada!')

cur.close()
conn.close()