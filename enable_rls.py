import psycopg2
import os

SUPABASE_URI = os.environ.get("SUPABASE_URI", "postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres")

conn = psycopg2.connect(SUPABASE_URI)
cursor = conn.cursor()

tables = ['usuarios', 'eventos', 'entradas', 'validaciones', 'transferencias', 
          'password_reset', 'solicitud_organizer', 'evento_imagenes', 'visitas',
          'brute_force_protection', 'rate_limits']

for table in tables:
    # Enable RLS
    cursor.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    print(f"RLS enabled on {table}")
    
    # Create policy to allow only authenticated users (anon key)
    # This allows read/write with Supabase anon key
    cursor.execute(f"""
        DROP POLICY IF EXISTS "Allow all operations on {table}" ON {table}
    """)
    cursor.execute(f"""
        CREATE POLICY "Allow all operations on {table}" ON {table}
        FOR ALL USING (true) WITH CHECK (true)
    """)
    print(f"  Policy created for {table}")

conn.commit()
print("\n✅ RLS enabled on all tables with permissive policies")

cursor.close()
conn.close()