import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sys

# ================= CAMINHO CORRETO =================
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
DB_PATH = os.path.join(BASE_DIR, "clientes.db")
ARQUIVO_RELATORIO = os.path.join(BASE_DIR, "relatorio.txt")
# ==================================================

EMAIL_REMETENTE = "santiago.machadoweb10@gmail.com"
EMAIL_SENHA = "fyla zlbe shlo kenl"
EMAIL_DESTINO = "santiago.machadoweb10@gmail.com"

def gerar_relatorio():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clientes WHERE email IS NULL OR email = ''")
    sem_email = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clientes WHERE telefone IS NULL OR telefone = ''")
    sem_telefone = cursor.fetchone()[0]

    conn.close()

    texto = f"""RELATÓRIO AUTOMÁTICO DE CLIENTES
===============================
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Total de clientes: {total}
Clientes sem email: {sem_email}
Clientes sem telefone: {sem_telefone}
"""

    with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as f:
        f.write(texto)

    return texto


def enviar_email(conteudo):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINO
    msg["Subject"] = "Relatório automático de clientes"

    msg.attach(MIMEText("Segue relatório em anexo.", "plain"))

    with open(ARQUIVO_RELATORIO, "rb") as f:
        anexo = MIMEText(f.read(), "base64", "utf-8")
        anexo.add_header("Content-Disposition", "attachment", filename="relatorio.txt")
        msg.attach(anexo)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
        server.send_message(msg)


def executar_rotina():
    gerar_relatorio()
    enviar_email("Relatório em anexo")
    print("Relatório enviado com sucesso em:", datetime.now())


if __name__ == "__main__":
    executar_rotina()