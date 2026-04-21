import psycopg2
import traceback
conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

try:
    cur.execute("SELECT COUNT(*) as cnt, COALESCE(SUM(total), 0) as total, COALESCE(SUM(cantidad), 0) as cnt_total FROM entradas WHERE estado = 'pagada'")
    print("Query 1:", cur.fetchone())
except Exception as e:
    print("Error Query 1:", e)
    traceback.print_exc()

try:
    cur.execute("SELECT COUNT(*) FROM validaciones")
    print("Query 2:", cur.fetchone())
except Exception as e:
    print("Error Query 2:", e)

conn.close()