import psycopg2
import bcrypt

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

password = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode('utf-8')

cur.execute("INSERT INTO usuarios (email, nombre, apellido, password, verificado, rol) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING", 
            ('admin@getaccess.com', 'Admin', 'Admin', password, 1, 'admin'))

conn.commit()
print("Admin creado correctamente")

cur.execute("SELECT id, email, verificado, rol FROM usuarios WHERE email = %s", ('admin@getaccess.com',))
print(cur.fetchone())

cur.close()
conn.close()