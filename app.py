import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Dashboard Maestro", page_icon="📊", layout="wide")

# --- SEU CSS PRESERVADO + NOVO CSS DE PAGINAÇÃO PROFISSIONAL ---
st.markdown("""
    <style>
    header[data-testid="stHeader"] { background-color: #f0f2f6 !important; }
    
    .main-header {
        background-color: #fff;
        padding: 1.5rem 2rem;
        margin: -4rem -5rem 1rem -5rem;
    }

    .stApp { background-color: #ffffff !important; }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 7px 7px 27px -20px;
    }

    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
        justify-content: center !important;
    }

    [data-testid="stSidebarContent"] { padding-top: 0rem !important; }

    /* BOTÃO SIDEBAR */
    .stSidebar .stButton > button {
        background-color: #0078D4 !important;
        color: white !important;
        width: 100% !important;
    }

    /* ESTILIZAÇÃO DA PAGINAÇÃO (IGUAL À IMAGEM image_42bac0) */
    .pag-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
    }

    /* Botões Prev/Next estilo Pílula */
    .stButton > button[key^="p_"] {
        border-radius: 20px !important;
        padding: 5px 20px !important;
        background-color: #1E90FF !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* Botões Numéricos estilo Círculo */
    .stButton > button[key^="num_"] {
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        background-color: transparent !important;
        color: #555 !important;
        border: 1px solid #ddd !important;
    }

    /* Estilo para Página Ativa (Azul Preenchido) */
    .stButton > button[key^="active_"] {
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        background-color: #1E90FF !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }

    .sidebar-footer {
        position: fixed;
        bottom: 15px;
        left: 20px;
        font-size: 11px;
        color: #888;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="main-header">
        <h2 style='margin:0;'>📊 Central de Inteligência - Maestro</h2>
        <p style='margin:0;'>Status: Operacional | Data: {datetime.now().strftime('%d/%m/%Y')}</p>
    </div>
    """, unsafe_allow_html=True)

def carregar_dados():
    if not os.path.exists('clientes.db'): return None
    conn = sqlite3.connect('clientes.db')
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()
    return df

df = carregar_dados()

if df is not None:
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 1

    m1, m2, m3 = st.columns(3)
    m1.metric("Total de Clientes", len(df), "Sincronizado")
    m2.metric("Meta Mensal", "1500", f"{len(df)-1500}", delta_color="inverse")
    m3.metric("Média p/ Dia", f"{len(df)//30}", "Projeção")

    st.divider()

    c1, c2 = st.columns([4, 1])
    busca = c1.text_input("🔍 Localizar por nome:", placeholder="Pesquise aqui...")
    df_f = df[df['nome'].str.contains(busca, case=False, na=False)] if busca else df
    
    c2.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    c2.download_button("📥 Baixar CSV", df_f.to_csv(index=False).encode('utf-8'), "clientes.csv")

    itens_por_pagina = 10
    total_itens = len(df_f)
    total_paginas = max(1, (total_itens // itens_por_pagina) + (1 if total_itens % itens_por_pagina > 0 else 0))
    
    if st.session_state.pagina > total_paginas:
        st.session_state.pagina = total_paginas

    aba1, aba2 = st.tabs(["📋 Lista de Clientes", "📈 Gráficos"])
    
    with aba1:
        inicio = (st.session_state.pagina - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina
        st.dataframe(df_f.iloc[inicio:fim], use_container_width=True, hide_index=True, height=380)

        # NAVEGAÇÃO IGUAL AO EXEMPLO (image_42bac0)
        st.write("")
        # Usamos várias colunas para simular o espaçamento da imagem
        p_cols = st.columns([1.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.5])
        
        with p_cols[0]:
            if st.button("← Prev", key="p_prev", disabled=(st.session_state.pagina == 1)):
                st.session_state.pagina -= 1
                st.rerun()

        # Janela de números (exibe até 5 números por vez)
        inicio_janela = max(1, st.session_state.pagina - 2)
        fim_janela = min(total_paginas, inicio_janela + 4)
        if fim_janela - inicio_janela < 4:
            inicio_janela = max(1, fim_janela - 4)

        for i, pag_num in enumerate(range(inicio_janela, fim_janela + 1)):
            with p_cols[i+1]:
                # Chave diferente para o botão ativo para aplicar CSS de círculo preenchido
                btn_key = f"active_{pag_num}" if pag_num == st.session_state.pagina else f"num_{pag_num}"
                if st.button(str(pag_num), key=btn_key):
                    st.session_state.pagina = pag_num
                    st.rerun()

        with p_cols[6]:
            if st.button("Next →", key="p_next", disabled=(st.session_state.pagina == total_paginas)):
                st.session_state.pagina += 1
                st.rerun()

    with aba2:
        st.line_chart(df.index)

with st.sidebar:
    st.header("© Cérebro do Agente")
    st.button("Gerar Novo Insight")
    st.markdown(f'<div class="sidebar-footer">v1.5 - Sistema Maestro</div>', unsafe_allow_html=True)