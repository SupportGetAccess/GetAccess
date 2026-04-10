import psycopg2

conn = psycopg2.connect('postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres')
cur = conn.cursor()

# Tabla usuarios
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    password TEXT NOT NULL,
    verificado INTEGER DEFAULT 0,
    codigo_verificacion TEXT,
    rol TEXT DEFAULT 'usuario'
)
""")

# Tabla eventos
cur.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    fecha TEXT,
    lugar TEXT,
    precio REAL,
    capacidad INTEGER DEFAULT 100,
    vendidos INTEGER DEFAULT 0,
    imagen TEXT,
    categoria TEXT
)
""")

# Tabla entradas
cur.execute("""
CREATE TABLE IF NOT EXISTS entradas (
    id SERIAL PRIMARY KEY,
    evento_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    total REAL NOT NULL,
    estado TEXT DEFAULT 'comprada',
    preference_id TEXT,
    payment_id TEXT,
    creada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usada INTEGER DEFAULT 0,
    transferida INTEGER DEFAULT 0
)
""")

# Tabla evento_imagenes
cur.execute("""
CREATE TABLE IF NOT EXISTS evento_imagenes (
    id SERIAL PRIMARY KEY,
    evento_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    orden INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Tabla validaciones
cur.execute("""
CREATE TABLE IF NOT EXISTS validaciones (
    id SERIAL PRIMARY KEY,
    entrada_id INTEGER NOT NULL,
    scanner_id INTEGER NOT NULL,
    cantidad_original INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Tabla transferencias
cur.execute("""
CREATE TABLE IF NOT EXISTS transferencias (
    id SERIAL PRIMARY KEY,
    entrada_id INTEGER NOT NULL,
    usuario_origen INTEGER NOT NULL,
    usuario_destino INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP
)
""")

# Tabla password_reset
cur.execute("""
CREATE TABLE IF NOT EXISTS password_reset (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    usado INTEGER DEFAULT 0,
    expires_at TIMESTAMP NOT NULL
)
""")

conn.commit()
print(">>> Tablas creadas en Supabase PostgreSQL")

# Seed eventos
cur.execute("SELECT COUNT(*) FROM eventos")
if cur.fetchone()[0] == 0:
    eventos_seed = [
        ("Coldplay - Music of the Spheres", "Gira mundial con producción spectacular", "2026-06-15", "Estadio River Plate, Buenos Aires", 45000, 50000, 5000, "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800", "musica"),
        ("Flamenco en Buenos Aires", "Una noche mágica con los mejores artistas del flamenco español.", "2026-04-20", "Teatro Colón, Buenos Aires", 8500, 800, 150, "https://images.unsplash.com/photo-1504609813442-a8924e83f76e?w=800", "teatro"),
        ("Superclásico Boca vs River", "El partido más apasionante del fútbol mundial.", "2026-05-10", "La Bombonera, Buenos Aires", 12000, 49000, 45000, "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800", "deportes"),
        ("Show de Stand Up", "El comediante más gracioso del país presenta su nuevo show.", "2026-04-05", "Teatro Metropolitan, Buenos Aires", 3500, 500, 200, "https://images.unsplash.com/photo-1527224857830-43a7acc85260?w=800", "comedia"),
        ("Festival Electrónico 2026", "3 escenarios, 20 DJs internacionales, 12 horas de música continua.", "2026-07-20", "Rural Palermo, Buenos Aires", 8000, 15000, 8000, "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800", "musica"),
    ]
    cur.executemany(
        "INSERT INTO eventos (nombre, descripcion, fecha, lugar, precio, capacidad, vendidos, imagen, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        eventos_seed
    )
    conn.commit()
    print(">>> Eventos de prueba creados")

cur.close()
conn.close()
print(">>> Listo!")