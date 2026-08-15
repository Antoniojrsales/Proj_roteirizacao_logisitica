import pandas as pd
import streamlit as st
from utils.metrics import metricas_gerais
from utils.auth_check import check_login
from utils.ui_components import render_card
from utils.data_processing import process_data

# Garante que o usuário está autenticado logo no topo
check_login()

# Botão de Logout na Sidebar (Menu Lateral)
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Sair da Conta", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.switch_page("1_🗝️_login.py")

# ---------------------------------------------------------
# ⚙️ CONFIGURAÇÕES INICIAIS DA INTERFACE (STREAMLIT)
# ---------------------------------------------------------
# 1. Define o título da aba e o ícone da aplicação
# 2. Configura o layout como 'wide' para usar toda a largura da tela
# 3. Adiciona os créditos do desenvolvedor na barra lateral
st.set_page_config(
    page_title="🗺️ Painel Geral",
    page_icon="🏠",
    layout="wide"
)
st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')

# ---------------------------------------------------------
# 🗂️ GESTÃO DE DADOS DA SESSÃO
# ---------------------------------------------------------
# 1. Verifica se o DataFrame principal existe no estado da sessão
# 2. Atribui os dados à variável local 'df_dados'
# 3. Emite um aviso caso os dados não sejam localizados
if 'df_Bi_Roteirizacao' in st.session_state:
    # 1. Pega os dados brutos da sessão
    df_dados = st.session_state['df_Bi_Roteirizacao']

    # 2. Aplica o processamento das regras de Lay que acabamos de validar no terminal
    df_dados = process_data(df_dados)

    # 3. Atualiza a sessão para que os cards e a tabela recebam os dados atualizados
    st.session_state['df_Bi_Roteirizacao'] = df_dados
else:
    st.warning("Dados não encontrados na sessão. Por favor, faça login novamente.")

m = metricas_gerais(df_dados)

st.header("📌 Resumo Geral de Desempenho (KPI)")

col_entregas, col_sla, col_reetregas, col_motoristas = st.columns(4)

with col_entregas:
    render_card(
        title="🚚 Total de Entregas",
        value=m['total_entregas'],
        gradient="#1e40af, #3b82f6"
    )

with col_sla:
    render_card(
            title="🎯 Taxa Conclusão (SLA)",
            value=m['taxa_sucesso'],
            suffix='%',
            gradient="#047857, #10b981"
        )

with col_reetregas:
    render_card(
            title="🚚 Reentregas",
            value=m['total_reentregas'],
            gradient="#b45309, #f59e0b"
        )

with col_motoristas:
    render_card(
            title="🚚 Motoristas Ativos",
            value=m['total_motoristas'],
            gradient="#4338ca, #6366f1"
        )