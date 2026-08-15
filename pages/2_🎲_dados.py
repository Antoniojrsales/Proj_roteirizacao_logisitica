import streamlit as st
from utils.auth_check import check_login
from utils.data_processing import process_data, carregar_planilha_robusta
import pandas as pd

st.set_page_config(
    page_title="Dados e Roteirização",
    page_icon="🎲",
    layout="wide"  # <--- Isso faz a tela ocupar 100% da largura do navegador
)

# 1. Garante que o usuário está autenticado logo no topo
check_login()

st.title("🎲 Painel de Dados e Roteirização")

with st.sidebar:
    st.write(f"👤 Usuário: **{st.session_state.get('username', '')}**")
    
    uploaded_file = st.file_uploader(
        "Selecione a planilha de entregas:", 
        type=["xlsx", "xls", "csv"]
    )
    
    if uploaded_file is not None:
        try:
            # 1. Lê direto do buffer do upload
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = carregar_planilha_robusta(uploaded_file)
            
            # 2. Processa e armazena na sessão (DENTRO do bloco if)
            st.session_state['df_Bi_Roteirizacao'] = process_data(df_raw)
            st.session_state['arquivo_nome'] = uploaded_file.name
            st.sidebar.success(f"Arquivo `{uploaded_file.name}` carregado!")
            
        except Exception as e:
            st.sidebar.error(f"Erro ao processar arquivo: {e}")
    

# 3. Exibição dos Dados na Página Principal
if 'df_Bi_Roteirizacao' in st.session_state and not st.session_state['df_Bi_Roteirizacao'].empty:
    df = st.session_state['df_Bi_Roteirizacao']
    
    st.subheader(f"📋 Entregas Carregadas ({len(df)} registros)")
    st.dataframe(df, width='stretch')
else:
    st.info("👈 Por favor, faça o upload de uma planilha no menu lateral para visualizar as entregas e gerar a rota.")

with st.sidebar:
    if st.button("🚪 Sair da Conta", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.switch_page("./1_🗝️_login.py")
