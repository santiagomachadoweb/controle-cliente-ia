import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("pt_BR")

conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

TOTAL_CLIENTES = 1000
clientes_ids = []

for _ in range(TOTAL_CLIENTES):
    nome = fake.name()
    telefone = fake.phone_number()
    email = fake.email()

    cursor.execute(
        "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
        (nome, telefone, email)
    )
    clientes_ids.append(cursor.lastrowid)

conn.commit()

acoes = ["Cadastro", "Acesso", "Edição"]

for cliente_id in clientes_ids:
    qtd_logs = random.randint(1, 10)
    for _ in range(qtd_logs):
        dias_atras = random.randint(0, 60)
        data = datetime.now() - timedelta(days=dias_atras)

        cursor.execute(
            "INSERT INTO logs (cliente_id, acao, data) VALUES (?, ?, ?)",
            (cliente_id, random.choice(acoes), data.strftime("%Y-%m-%d %H:%M:%S"))
        )

conn.commit()
conn.close()

print("Banco populado com sucesso porra!!!")
