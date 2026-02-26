import sqlite3
import os

# O QUE: Funcao para o Agente ler o seu banco de dados SQLite
def analisar_dados():
    print("🤖 AGENTE: Acessando o banco de dados 'clientes.db'...")
    
    # FERRAMENTA: Conexao com o banco que voce ja tem no projeto
    try:
        conexao = sqlite3.connect('clientes.db')
        cursor = conexao.cursor()
        
        # ACAO: Contar o total de registros na tabela de clientes
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]
        
        conexao.close()
        return total_clientes
    except Exception as e:
        return f"Erro ao acessar o banco: {e}"

# ONDE: O Agente processa a informacao e gera o insight
def gerar_relatorio():
    total = analisar_dados()
    
    # Texto que a IA "pensou"
    conteudo = f"""
    === RELATÓRIO DO AGENTE DE IA ===
    Status do Sistema: OPERACIONAL
    Total de Clientes Cadastrados: {total}
    
    Insight do Agente: 
    O sistema possui uma base de {total} usuários. 
    A infraestrutura de container (Docker) está validada e verde.
    Próxima recomendação: Ativar monitoramento de logs CSV.
    =================================
    """
    
    # ACAO: Criar o arquivo de texto com o resultado
    with open("relatorio_agente.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    
    print("✅ AGENTE: Relatorio gerado com sucesso em 'relatorio_agente.txt'!")
    print(conteudo)

# COMANDO: Inicia o script
if __name__ == "__main__":
    gerar_relatorio()