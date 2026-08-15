import pandas as pd
import streamlit as st

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Higieniza e trata os dados das entregas."""
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Padroniza nomes das colunas (sem espaços e tudo em minúsculo)
    df.columns = df.columns.str.strip().str.lower()
    
    # Outros tratamentos futuros (ex: remover nulos, formatar status, etc.)
    return df

def carregar_planilha_robusta(uploaded_file) -> pd.DataFrame:
    """
    Localiza o cabeçalho correto da tabela de entregas e trata colunas duplicadas.
    """
    try:
        # 1. Carrega o arquivo Excel completo
        excel_file = pd.ExcelFile(uploaded_file)
        
        # Se houver mais de uma aba, seleciona a primeira ou a que contiver 'base'/'dados'
        nome_aba = excel_file.sheet_names[0]
        for sheet in excel_file.sheet_names:
            if any(term in sheet.lower() for term in ['base', 'dados', 'entrega', 'rotas']):
                nome_aba = sheet
                break

        # 2. Lê as primeiras 50 linhas sem definir cabeçalho para caçar a linha certa
        df_preview = pd.read_excel(excel_file, sheet_name=nome_aba, header=None, nrows=50)

        linha_cabecalho = None
        for idx, row in df_preview.iterrows():
            valores = [str(val).strip().upper() for val in row.dropna().values]
            # Procura pela linha que contém 'CLIENTE' e 'STATUS' ou 'NF'
            if any("CLIENTE" in v for v in valores) and (any("STATUS" in v for v in valores) or any("NF" in v for v in valores)):
                linha_cabecalho = idx
                break

        # 3. Lê os dados a partir da linha encontrada
        if linha_cabecalho is not None:
            df = pd.read_excel(excel_file, sheet_name=nome_aba, header=linha_cabecalho)
        else:
            # Fallback caso não encontre automaticamente
            df = pd.read_excel(excel_file, sheet_name=nome_aba)

        # 4. Remove colunas 100% vazias ou não identificadas (Unnamed)
        df = df.loc[:, ~df.columns.astype(str).str.startswith('Unnamed:')]
        df = df.dropna(how='all')

        # 5. Tratamento de nomes de colunas duplicadas e limpeza
        cols_limpas = []
        cols_vistas = {}
        for col in df.columns:
            nome = str(col).strip().lower().replace(" ", "_")
            if nome in ['nan', '', 'none']:
                nome = 'coluna_extra'
            
            # Se for duplicada, renomeia adicionando sufixo numérico (ex: status, status_1)
            if nome in cols_vistas:
                cols_vistas[nome] += 1
                cols_limpas.append(f"{nome}_{cols_vistas[nome]}")
            else:
                cols_vistas[nome] = 0
                cols_limpas.append(nome)

        df.columns = cols_limpas
        return df

    except Exception as e:
        st.error(f"Erro ao ler e tratar o arquivo: {e}")
        return pd.DataFrame()