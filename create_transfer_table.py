import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
conn.execute("""
    CREATE TABLE IF NOT EXISTS transferencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entrada_id INTEGER NOT NULL,
        usuario_origen INTEGER NOT NULL,
        usuario_destino TEXT NOT NULL,
        token TEXT UNIQUE NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        accepted_at TEXT,
        FOREIGN KEY (entrada_id) REFERENCES entradas(id),
        FOREIGN KEY (usuario_origen) REFERENCES usuarios(id)
    )
""")
conn.commit()
print("Tabla transferencias creada")
conn.close()
