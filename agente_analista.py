import sqlite3
import requests

def perguntar_ao_agente_ia(total_clientes):
    print("🧠 AGENTE: Consultando a IA (TinyLlama)...")
    url = "http://localhost:11434/api/generate"
    
    corpo_da_pergunta = {
        "model": "tinyllama",
        "prompt": f"O sistema tem {total_clientes} clientes. Escreva uma frase curta de incentivo para o dono do projeto em português.",
        "stream": False
    }
    
    try:
        resposta = requests.post(url, json=corpo_da_pergunta, timeout=30)
        return resposta.json()['response']
    except Exception as e:
        return "IA em repouso. O sistema continua operando com {total_clientes} clientes!"

def executar_agente():
    conexao = sqlite3.connect('clientes.db')
    total = conexao.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    conexao.close()
    
    # AQUI ESTÁ A MÁGICA:
    comentario_da_ia = perguntar_ao_agente_ia(total)
    
    relatorio = f"""
=== RELATÓRIO DO AGENTE DE IA ===
Status: OPERACIONAL
Base de Dados: {total} clientes.

Insight da IA:
{comentario_da_ia}
=================================
"""
    
    with open("relatorio_agente.txt", "w", encoding="utf-8") as f:
        f.write(relatorio)
    
    print("\n✅ AGENTE: Relatório inteligente gerado!")

if __name__ == "__main__":
    executar_agente()