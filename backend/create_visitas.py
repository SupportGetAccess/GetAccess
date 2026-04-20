import sqlite3
conn = sqlite3.connect("access_on.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS visitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        fecha TEXT DEFAULT CURRENT_DATE,
        contador INTEGER DEFAULT 1,
        UNIQUE(ip, fecha)
    )
""")
conn.commit()
print("Tabla visitas creada")
conn.close()