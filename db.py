import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
DB_PATH = os.path.join(BASE_DIR, "clientes.db")

def criar_tabelas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        acao TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados inicializado com sucesso.")