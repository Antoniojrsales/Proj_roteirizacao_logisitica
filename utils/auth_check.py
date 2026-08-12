import streamlit as st
import hashlib
import hmac

def check_login():
    """Garante que a página só seja acessível por usuários autenticados."""
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Você precisa estar logado para acessar esta página.")
        
        # Opção 1: Botão de redirecionamento automático nativo
        if st.button("Ir para o Login"):
            st.switch_page("app.py")  # Altere para o caminho da sua página principal/login
        
        # Interrompe o carregamento do restante da página
        st.stop()

def check_password(input_password: str, stored_password_hash: str) -> bool:
    """
    Compara a senha de entrada com o hash armazenado usando comparação segura.
    """
    if not isinstance(input_password, str) or not isinstance(stored_password_hash, str):
        return False

    try:
        # Gera o hash SHA256 da senha digitada
        input_hash = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
        
        # Usa hmac.compare_digest para prevenir Timing Attacks
        return hmac.compare_digest(input_hash, stored_password_hash)
    except Exception:
        return False