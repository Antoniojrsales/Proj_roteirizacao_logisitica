import pandas as pd
import streamlit as st
from utils.auth_check import check_login
from utils.data_processing import process_data
import plotly.express as px

# Garante que o usuário está autenticado logo no topo
check_login()

# ---------------------------------------------------------
# ⚙️ CONFIGURAÇÕES INICIAIS DA INTERFACE (STREAMLIT)
# ---------------------------------------------------------
# 1. Define o título da aba e o ícone da aplicação
# 2. Configura o layout como 'wide' para usar toda a largura da tela
# 3. Adiciona os créditos do desenvolvedor na barra lateral
st.set_page_config(
    page_title="📊 Tendencias",
    page_icon="📊",
    layout="wide"
)

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

# --- FILTROS NA SIDEBAR ---
with st.sidebar:
    st.subheader("🔍 Filtros da Operação")
    
    # 1. Filtro por Motorista
    lista_motoristas = sorted(df_dados['motorista'].dropna().unique().tolist())
    motoristas_selecionados = st.multiselect(
        "Motoristas:",
        options=lista_motoristas,
        default=lista_motoristas
    )
    
    # 2. Filtro por Status
    lista_status = sorted(df_dados['status'].dropna().unique().tolist()) if 'status' in df_dados.columns else []
    status_selecionados = st.multiselect(
        "Status da Entrega:",
        options=lista_status,
        default=lista_status
    )
    
    # 3. Filtro por Mês (se a coluna 'mês' existir)
    if 'mês' in df_dados.columns:
        lista_meses = sorted(df_dados['mês'].dropna().unique().tolist())
        meses_selecionados = st.multiselect(
            "Mês:",
            options=lista_meses,
            default=lista_meses
        )

# Aplicação dos filtros no DataFrame
df_filtrado = df_dados.copy()

if motoristas_selecionados:
    df_filtrado = df_filtrado[df_filtrado['motorista'].isin(motoristas_selecionados)]

if status_selecionados:
    df_filtrado = df_filtrado[df_filtrado['status'].isin(status_selecionados)]

if 'mês' in df_dados.columns and meses_selecionados:
    df_filtrado = df_filtrado[df_filtrado['mês'].isin(meses_selecionados)]

st.subheader("📊 Entregas por Motorista e Status")

if not df_filtrado.empty:
    # Agrupamento para contagem
    df_agg = (
        df_filtrado.groupby(['motorista', 'status'])
        .size()
        .reset_index(name='total')
    )
    
    fig = px.bar(
        df_agg,
        x='motorista',
        y='total',
        color='status',
        text='total',
        barmode='stack',
        color_discrete_map={
            'CONCLUIDO': '#10b981',
            'RETORNO': '#f59e0b',
            'CANCELADO': '#ef4444',
            'EM ROTA': '#3b82f6'
        },
        labels={'total': 'Qtd. Entregas', 'motorista': 'Motorista', 'status': 'Status'}
    )
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Total de Entregas",
        legend_title="Status",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')

# Botão de Logout na Sidebar (Menu Lateral)
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Sair da Conta", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.switch_page("1_🗝️_login.py")