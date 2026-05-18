import os
import psycopg2
import bcrypt

conn = psycopg2.connect(os.environ.get("SUPABASE_URI"))
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