import sqlite3
import requests
import os

# --- CAMADA 1: REVISOR DE CÓDIGO (SEGURANÇA) ---
def validar_configuracoes():
    """O Agente revisa o db.py para evitar que erros de config subam para o Git."""
    print("🔍 AGENTE REVISOR: Analisando arquivos de configuração...")
    try:
        with open("db.py", "r", encoding="utf-8") as f:
            conteudo = f.read()
            if "erro_proposital.db" in conteudo:
                print("\n❌ ERRO CRÍTICO DETECTADO: Banco de erro configurado!")
                return False
        
        print("✅ AGENTE REVISOR: Configurações validadas.")
        return True
    except Exception as e:
        print(f"⚠️ AGENTE REVISOR: Erro ao ler config: {e}")
        return False

# --- CAMADA 2: INTELIGÊNCIA ARTIFICIAL (IA) ---
def perguntar_ao_agente_ia(total_clientes):
    """Gera insight inteligente usando o modelo local TinyLlama via Ollama."""
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
        return f"IA Offline. Sistema operando com {total_clientes} clientes!"

def executar_agente():
    """Orquestra leitura do banco, IA, Dashboard e envio automático para o GitHub."""
    # 1. LEITURA DOS DADOS DO BANCO SQLITE
    conexao = sqlite3.connect('clientes.db')
    total = conexao.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    conexao.close()
    
    # 2. GERAÇÃO DO RELATÓRIO EM TEXTO
    comentario_ia = perguntar_ao_agente_ia(total)
    relatorio = f"""
=== RELATÓRIO AUTOMÁTICO DO AGENTE ===
Status: 100% OPERACIONAL
Clientes na Base: {total}

Insight da IA:
{comentario_ia}
======================================
"""
    with open("relatorio_agente.txt", "w", encoding="utf-8-sig") as f:
        f.write(relatorio)
    
    print("\n✅ AGENTE: Relatório gerado com sucesso!")

    # --- CAMADA 3: AUTOMAÇÃO DE GIT (AUTONOMIA TOTAL) ---
    print("🤖 AGENTE: Sincronizando e enviando para o GitHub...")
    
    # PASSO DE SEGURANÇA: Adiciona tudo antes do pull para evitar erro de 'unstaged changes'
    os.system('git add .')
    
    # Sincronização automática via rebase para evitar abertura do editor Vim
    os.system('git pull origin main --rebase')
    
    # Adicionando especificamente os arquivos da nossa arquitetura
    os.system('git add relatorio_agente.txt')
    os.system('git add agente_analista.py')
    os.system('git add app.py')  
    os.system('git add docker-compose.yml')
    os.system('git add .github/workflows/main.yml')
    os.system('git add README.md')
    
    # Realiza o commit e o envio oficial para a branch principal
    os.system('git commit -m "Automação: Agente Maestro atualizou código, relatório e Dashboard"')
    os.system('git push origin main')

    print("🛰️ AGENTE: Tudo enviado e sincronizado automaticamente!")

# --- EXECUÇÃO DO SCRIPT ---
if __name__ == "__main__":
    print("🚀 Iniciando Agente Maestro...")
    if validar_configuracoes():
        executar_agente()
    else:
        print("\n🛑 OPERAÇÃO CANCELADA PELO AGENTE.")