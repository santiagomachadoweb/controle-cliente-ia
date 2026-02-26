import streamlit as st
import sqlite3
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Dashboard Agente Maestro", page_icon="📊")

st.title("📊 Painel de Controle - Agente Maestro")
st.markdown("---")

# Conexão com o Banco de Dados
def carregar_dados():
    conexao = sqlite3.connect('clientes.db')
    df = pd.read_sql_query("SELECT * FROM clientes", conexao)
    conexao.close()
    return df

try:
    df_clientes = carregar_dados()

    # Métrica Principal
    total_clientes = len(df_clientes)
    st.metric(label="Total de Clientes na Base", value=total_clientes)

    # Visualização de Dados
    st.subheader("📋 Lista de Clientes Ativos")
    st.dataframe(df_clientes, use_container_width=True)

    # Gráfico Simples (Ex: Clientes por ID para ilustrar volume)
    st.subheader("📈 Crescimento da Base")
    st.line_chart(df_clientes.index)

except Exception as e:
    st.error(f"Erro ao carregar o banco de dados: {e}")

# Exibição do Relatório do Agente
st.sidebar.header("🤖 Insight do Agente")
if st.sidebar.button("Ler Último Relatório"):
    try:
        with open("relatorio_agente.txt", "r", encoding="utf-8-sig") as f:
            conteudo = f.read()
            st.sidebar.text_area("Relatório Atual:", conteudo, height=300)
    except:
        st.sidebar.warning("Relatório ainda não gerado.")