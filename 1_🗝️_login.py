import streamlit as st
import pandas as pd
from utils.auth_check import check_password 
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
except KeyError as e:
    st.error(f"Erro de configuração: Chave '{e.args[0]}' ausente no secrets.toml.")
    st.stop()

# --- TELA DE LOGIN / REDIRECIONAMENTO ---
if not st.session_state.get('logged_in', False):
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
                st.switch_page("pages/2_🎲_dados.py")
            else:
                st.error("❌ Usuário ou senha inválidos.")
else:
    # Se o usuário já está logado e entrou nesta página, redireciona direto
    st.switch_page("pages/2_🎲_dados.py")
