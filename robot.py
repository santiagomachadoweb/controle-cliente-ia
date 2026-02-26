import sqlite3

def executar_robo():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, telefone, email FROM clientes")
    clientes = cursor.fetchall()

    print("🤖 ROBÔ INICIADO...")
    print(f"Total de clientes: {len(clientes)}")
    print("-" * 50)

    for cliente in clientes:
        id_cliente, nome, telefone, email = cliente
        print(f"ID: {id_cliente} | Nome: {nome} | Tel: {telefone} | Email: {email}")

    print("-" * 50)
    print("🤖 ROBÔ FINALIZADO")

    conn.close()

if __name__ == "__main__":
    executar_robo()