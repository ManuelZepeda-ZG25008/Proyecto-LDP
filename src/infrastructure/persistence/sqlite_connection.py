import sqlite3
import os

DB_PATH = "paqueteria.db"

def get_db_connection():
    """Retorna una conexión activa a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos creando las tablas base si no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL
        );
    """)
    
    conn.commit()
    conn.close()