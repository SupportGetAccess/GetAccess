#!/usr/bin/env python3
"""
Get Access - Backup Script
Guarda un backup de la base de datos en archivos CSV

Usage:
    python backup.py

Requiere:
    pip install psycopg2-binary
"""

import os
import csv
from datetime import datetime
import psycopg2
from pathlib import Path

# Configuración - cambiar si es necesario
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres.xgwbcepopluehupublkz:%40Supabase1982@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"
)

TABLAS = [
    "usuarios",
    "eventos", 
    "entradas",
    "transferencias",
    "validaciones",
    "evento_imagenes",
    "password_reset",
    "solicitud_organizer",
    "visitas",
    "rate_limits",
    "brute_force_protection"
]

def hacer_backup():
    print("=== Get Access Backup ===")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Crear carpeta de backup
    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    carpeta = Path(f"backups/{fecha}")
    carpeta.mkdir(parents=True, exist_ok=True)
    
    try:
        # Conectar a la base de datos
        print("Conectando a Supabase...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✓ Conectado\n")
        
        # Exportar cada tabla
        for tabla in TABLAS:
            try:
                print(f"Backup {tabla}...", end=" ")
                cursor.execute(f"SELECT * FROM {tabla}")
                columnas = [desc[0] for desc in cursor.description]
                filas = cursor.fetchall()
                
                # Guardar en CSV
                archivo = carpeta / f"{tabla}.csv"
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columnas)
                    writer.writerows(filas)
                
                print(f"✓ ({len(filas)} filas)")
                
            except Exception as e:
                print(f"✗ Error: {e}")
        
        cursor.close()
        conn.close()
        
        print()
        print(f"=== Backup completado ===")
        print(f"Ubicación: {carpeta.absolute()}")
        print()
        print("Archivos guardados:")
        for f in carpeta.glob("*.csv"):
            print(f"  - {f.name}")
            
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        print("\nPara configurar la URL de la base de datos:")
        print("  export DATABASE_URL='postgresql://user:pass@host:port/db'")
        print("  python backup.py")

if __name__ == "__main__":
    hacer_backup()