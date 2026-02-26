import sqlite3
import requests
import os

# --- CAMADA 1: REVISOR DE CÓDIGO ---
def validar_configuracoes():
    print("🔍 AGENTE REVISOR: Analisando arquivos de configuração...")
    try:
        with open("db.py", "r", encoding="utf-8") as f:
            conteudo = f.read()
            if "erro_proposital.db" in conteudo:
                print("\n❌ ERRO CRÍTICO DETECTADO!")
                print("O Agente identificou que o banco está configurado como 'erro_proposital.db'.")
                return False
        
        print("✅ AGENTE REVISOR: Configurações de banco validadas com sucesso.")
        return True
    except Exception as e:
        print(f"⚠️ AGENTE REVISOR: Falha ao tentar ler o arquivo db.py: {e}")
        return False

# --- CAMADA 2: INTELIGÊNCIA E RELATÓRIO ---
def perguntar_ao_agente_ia(total_clientes):
    print("🧠 AGENTE: Consultando a IA (TinyLlama) para gerar insight...")
    url = "http://localhost:11434/api/generate"
    
    corpo_da_pergunta = {
        "model": "tinyllama",
        "prompt": f"O sistema tem {total_clientes} clientes. Escreva uma frase curta de incentivo para o dono do projeto em português.",
        "stream": False
    }
    
    try:
        resposta = requests.post(url, json=corpo_da_pergunta, timeout=30)
        return resposta.json()['response']
    except Exception:
        return f"IA em repouso. O sistema continua operando com {total_clientes} clientes!"

def executar_agente():
    # 1. ACESSO AO BANCO DE DADOS
    conexao = sqlite3.connect('clientes.db')
    total = conexao.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    conexao.close()
    
    # 2. PROCESSAMENTO DE INSIGHT
    comentario_da_ia = perguntar_ao_agente_ia(total)
    
    relatorio = f"""
=== RELATÓRIO DO AGENTE DE IA ===
Status: OPERACIONAL
Base de Dados: {total} clientes.

Insight da IA:
{comentario_da_ia}
=================================
"""
    
    # 3. GRAVAÇÃO DO RESULTADO
    with open("relatorio_agente.txt", "w", encoding="utf-8-sig") as f:
        f.write(relatorio)
    
    print("\n✅ AGENTE: Relatório inteligente gerado com sucesso!")

    # --- CAMADA 3: AUTOMAÇÃO DE GIT SEGURA ---
    print("🤖 AGENTE: Iniciando processos de Git automáticos...")
    
    # Adicionamos apenas o relatório para evitar conflitos de permissão no banco de dados
    os.system('git add relatorio_agente.txt')
    
    # Executa o registro e o envio
    os.system('git commit -m "Automação: Relatório de clientes atualizado pelo Agente"')
    os.system('git push')

    print("🛰️ AGENTE: Alterações enviadas para o GitHub!")

# --- INICIALIZAÇÃO DO SISTEMA ---
if __name__ == "__main__":
    print("🚀 Iniciando Agente Maestro...")
    
    if validar_configuracoes():
        executar_agente()
    else:
        print("\n🛑 OPERAÇÃO CANCELADA PELO AGENTE.")
        print("Corrija o arquivo 'db.py' para prosseguir.")