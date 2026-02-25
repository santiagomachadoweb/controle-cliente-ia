import sqlite3

def criar_tabelas():
    conn = sqlite3.connect("clientes.db")
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
