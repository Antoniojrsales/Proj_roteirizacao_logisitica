import streamlit as st
from utils.auth_check import check_password 
from utils.db_connector import load_data 
from utils.data_processing import process_data 

# -------------------------------
# ⚙️ Configuração da página
# -------------------------------
st.set_page_config(
    page_title='Login | Sistema Logístico',
    page_icon='🚚',
    layout='centered'
)

st.sidebar.markdown('Desenvolvido por [AntonioJrSales](https://antoniojrsales.github.io/meu_portfolio/)')

# ---------------------------------------------------------
# 🎨 UTILITÁRIOS DE ESTILIZAÇÃO (CSS)
# ---------------------------------------------------------
def local_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# -------------------------------
# 🗂️ Carregar Credenciais de Usuário
# -------------------------------
try:
    USERS = st.secrets["AUTH_USERS"]
    XLSX_ID = st.secrets["XLSX"]["xlsx_id"]
except KeyError as e:
    st.error(f"Erro de configuração: Chave '{e.args[0]}' ausente no secrets.toml.")
    st.stop()

# -------------------------------
# 🖼️ PAINEL PÓS-LOGIN
# -------------------------------
def render_main_page():
    """Exibe a dashboard e redireciona o usuário logado."""
    st.title(f"🎉 Bem-vindo(a), {st.session_state.get('username', 'Usuário')}!")
    
    # Logout Seguro
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.pop('logged_in', None)
        st.session_state.pop('username', None)
        st.session_state.pop('df_Bi_Roteirizacao', None)
        st.rerun()

    try:
        df_bruto = load_data(XLSX_ID) 
        
        if df_bruto is not None and not df_bruto.empty:
            df_dados = process_data(df_bruto)
            st.session_state['df_Bi_Roteirizacao'] = df_dados
            st.success("✅ Dados atualizados com sucesso!")            
            # Redirecionamento nativo
            st.switch_page("pages/2_🎲_dados.py")
        else:
            st.warning("⚠️ O sistema está pronto, mas a planilha de entregas está vazia ou aguardando configuração.")

    except Exception as e:
        st.error(f"❌ Erro ao processar dados: {e}")

# --- TELA DE LOGIN ---
if not st.session_state.get('logged_in', False):
    # Aplica o CSS customizado apenas na tela de login
    local_css('style_button_login.css')

    with st.form("login_form"):
        st.markdown("<h2 style='text-align: center; margin-bottom: 1rem;'>🔐 Login</h2>", unsafe_allow_html=True)
        
        username = st.text_input("👤 Usuário").strip()
        password = st.text_input("🔒 Senha", type="password").strip()

        submit = st.form_submit_button("Entrar")

        if submit: 
            if username in USERS and check_password(password, USERS[username]):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username 

                st.toast("✅ Login bem-sucedido!", icon='🎉')
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos.")
else:
    render_main_page()