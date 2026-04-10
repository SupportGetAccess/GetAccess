import psycopg2
import bcrypt

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Usuario 1: guilles10@yahoo.com.ar - Willy (Admin)
password1 = bcrypt.hashpw(b'guille123', bcrypt.gensalt()).decode('utf-8')
cur.execute("INSERT INTO usuarios (email, nombre, apellido, password, verificado, rol) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING", 
            ('guilles10@yahoo.com.ar', 'Willy', 'Guillermo', password1, 1, 'admin'))

# Usuario 2: aantoniaa1982@gmail.com - Aantii (User)
password2 = bcrypt.hashpw(b'anton123', bcrypt.gensalt()).decode('utf-8')
cur.execute("INSERT INTO usuarios (email, nombre, apellido, password, verificado, rol) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (email) DO NOTHING", 
            ('aantoniaa1982@gmail.com', 'Aantii', 'Antonia', password2, 1, 'usuario'))

conn.commit()
print(">>> Usuarios migrados")

cur.execute('SELECT id, email, nombre, rol FROM usuarios')
for row in cur.fetchall():
    print(row)

conn.close()