import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

cur.execute('SELECT id, nombre, capacidad, vendidos FROM eventos WHERE id = 13')
r = cur.fetchone()
print(f'Evento 13: {r[1]}')
print(f'  Capacidad: {r[2]}')
print(f'  Vendidos: {r[3]}')
print(f'  Disponibles: {r[2] - r[3]}')
print()

cur.execute("""
    SELECT
        COUNT(*) as total,
        COUNT(CASE WHEN estado = 'pagada' THEN 1 END) as pagadas,
        COUNT(CASE WHEN estado = 'pendiente' THEN 1 END) as pendientes,
        COUNT(CASE WHEN estado = 'expirada' THEN 1 END) as expiradas
    FROM entradas WHERE evento_id = 13
""")
r2 = cur.fetchone()
print(f'Entradas:')
print(f'  Total: {r2[0]}')
print(f'  Pagadas: {r2[1]}')
print(f'  Pendientes: {r2[2]}')
print(f'  Expiradas: {r2[3]}')
print()

# Verificar balance
pagadas_mas_expiradas = r2[1] + r2[3]
print(f'Balance: Pagadas({r2[1]}) + Expiradas({r2[3]}) = {pagadas_mas_expiradas}')
print(f'Stock en evento: {r[3]}')
if pagadas_mas_expiradas == r[3]:
    print('✅ Balance correcto!')
else:
    print('⚠️ Diferencia detectada')

conn.close()