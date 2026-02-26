import sqlite3
import requests
import os

# --- CAMADA 1: REVISOR DE CÓDIGO ---
def validar_configuracoes():
    print("🔍 AGENTE REVISOR: Analisando arquivos de configuração...")
    try:
        # O Agente abre o arquivo db.py para ler o que você escreveu
        with open("db.py", "r", encoding="utf-8") as f:
            conteudo = f.read()
            # Se ele achar o nome do banco de erro, ele bloqueia a execução
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
    # 1. LER BANCO DE DADOS REAL
    conexao = sqlite3.connect('clientes.db')
    total = conexao.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    conexao.close()
    
    # 2. GERAR INSIGHT E RELATÓRIO
    comentario_da_ia = perguntar_ao_agente_ia(total)
    
    relatorio = f"""
=== RELATÓRIO DO AGENTE DE IA ===
Status: OPERACIONAL
Base de Dados: {total} clientes.

Insight da IA:
{comentario_da_ia}
=================================
"""
    
    # SALVAR ARQUIVO LOCALMENTE
    with open("relatorio_agente.txt", "w", encoding="utf-8-sig") as f:
        f.write(relatorio)
    
    print("\n✅ AGENTE: Relatório inteligente gerado com sucesso!")

    # --- CAMADA 3: AUTOMAÇÃO DE GIT (AJUSTADA PARA EVITAR ERRO DE PERMISSÃO) ---
    print("🤖 AGENTE: Iniciando processos de Git automáticos...")
    
    # Em vez de 'git add .', adicionamos apenas os arquivos necessários para evitar travar no clientes.db
    os.system('git add relatorio_agente.txt')
    os.system('git add docker-compose.yml')
    os.system('git add agente_analista.py')
    
    # Commit e Push
    os.system('git commit -m "Automação: Relatório e Infraestrutura (Docker-Compose) atualizados"')
    os.system('git push')

    print("🛰️ AGENTE: Alterações enviadas para o GitHub!")

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    print("🚀 Iniciando Agente Maestro...")
    
    # O Agente só executa se passar pela revisão de código
    if validar_configuracoes():
        executar_agente()
    else:
        print("\n🛑 OPERAÇÃO CANCELADA PELO AGENTE.")
        print("Corrija o arquivo 'db.py' antes de tentar subir o código.")