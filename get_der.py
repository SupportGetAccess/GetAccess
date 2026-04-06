import sqlite3
conn = sqlite3.connect('C:/Users/guill/eventos_tickets_full/backend/access_on.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]

print("=" * 60)
print("DIAGRAMA ENTIDAD-RELACIÓN - GetAccess")
print("=" * 60)

for t in tables:
    if t.startswith('sqlite'):
        continue
    print(f"\n### {t.upper()}")
    cols = conn.execute(f'PRAGMA table_info({t})').fetchall()
    for c in cols:
        print(f"  - {c[1]}: {c[2]}")
    
    # Foreign keys
    fks = conn.execute(f'PRAGMA foreign_key_list({t})').fetchall()
    for fk in fks:
        print(f"  FK -> {fk[2]}")

conn.close()
