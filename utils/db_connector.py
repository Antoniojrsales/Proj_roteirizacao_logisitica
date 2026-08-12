import pandas as pd
import streamlit as st

# Colunas padrão esperadas pelo Data App
COLUNAS_PADRAO = ['id', 'data', 'empresa', 'endereco', 'status']

def get_xlsx_id() -> str | None:
    """Busca o ID da planilha no secrets.toml com fallback seguro."""
    try:
        return st.secrets["XLSX"]["xlsx_id"]
    except KeyError:
        st.error("Erro de configuração: 'xlsx_id' não encontrado na seção [XLSX] do secrets.toml.")
        return None
    except Exception as e:
        st.error(f"Erro ao acessar credenciais: {e}")
        return None

@st.cache_data(ttl=600, show_spinner="Carregando dados das entregas...")  # TTL = 10 minutos (600s)
def load_data(xlsx_id: str | None) -> pd.DataFrame:
    """
    Carrega e faz o cache dos dados da planilha de entregas.
    Retorna um DataFrame com as colunas esperadas ou um DataFrame vazio estruturado em caso de falha.
    """
    if not xlsx_id or xlsx_id == "aguardando o link do arquivo":
        return pd.DataFrame(columns=COLUNAS_PADRAO)
    
    try:
        # Quando tiver o link público ou Google Sheets CSV export:
        # url = f"https://docs.google.com/spreadsheets/d/{xlsx_id}/export?format=xlsx"
        url = xlsx_id  
        
        df = pd.read_excel(url)
        
        # Higienização básica das colunas (remover espaços e padronizar minúsculas)
        df.columns = df.columns.str.strip().str.lower()
        
        return df

    except Exception as e:
        # Retorna DataFrame vazio com a estrutura correta para evitar KeyError na aplicação
        return pd.DataFrame(columns=COLUNAS_PADRAO)