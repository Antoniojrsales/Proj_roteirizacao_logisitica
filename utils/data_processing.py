import pandas as pd
import streamlit as st
import numpy as np

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Higieniza e trata os dados das entregas."""
    if df is None or df.empty:
        return pd.DataFrame()
    
    df = df.copy()
    
    # Padroniza os nomes das colunas (sem espaços, minúsculas e sem barras/hífens)
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
        .str.replace("-", "_")
    )

    # Padronização amigável de nomes-chave de colunas
    renomear = {
        'veiculo__motorista': 'motorista',
        'veículo__motorista': 'motorista',
        'data_saida': 'data_saída'
    }
    df = df.rename(columns={k: v for k, v in renomear.items() if k in df.columns})
    
    # Lista de colunas de texto para higienização
    text_cols = ['cliente', 'motorista', 'tipo', 'status', 'obs']
    
    for col in text_cols:
        if col in df.columns:
            # Remove espaços nas pontas, unifica em caixa alta e trata múltiplos espaços internos
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.upper()
                .str.replace(r"\s+", " ", regex=True)
            )
            # Retorna valores 'NAN' e 'NONE' gerados por conversão de string para valores nulos limpos
            df[col] = df[col].replace(['NAN', 'NONE', ''], None)

    # Tratamento padrão para Observações vazias
    if 'obs' in df.columns:
        df['obs'] = df['obs'].fillna('SEM OCORRÊNCIA')

    # 4. Criação do identificador único (blindado contra nulos)
    col_nf = df['nf'].fillna('S_NF').astype(str) if 'nf' in df.columns else 'S_NF'
    col_cli = df['cliente'].fillna('SEM_CLIENTE').astype(str) if 'cliente' in df.columns else 'SEM_CLIENTE'
    col_tipo = df['tipo'].fillna('ENTREGA').astype(str) if 'tipo' in df.columns else 'ENTREGA'

    # Converte para string para evitar erros e concatena com um separador legível
    df['id_entrega'] = col_nf + " - " + col_cli + "_" + col_tipo

    # 5. Flags Analíticas
    if 'tipo' in df.columns:
        df['eh_reentrega'] = np.where(df['tipo'].str.contains('REENTREGA', na=False), 'Sim', 'Não')

    if 'status' in df.columns:
        df['sucesso_entrega'] = np.where(df['status'] == 'CONCLUIDO', 'Sucesso', 'Ocorrência/Pendente')

    # Lista de colunas de data para converter
    cols_data = ['data_prevista', 'data_saída']

    # Conversão segura com detecção automática de formato
    for col in cols_data:
        if col in df.columns:
            # errors='coerce' converte valores inválidos/None para NaT sem quebrar o código
            # dayfirst=True garante prioridade para padrão brasileiro (DD/MM/AAAA) quando aplicável
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
            
            # Remove a hora zerada (00:00:00) mantendo apenas o objeto de data
            df[col] = df[col].dt.date

    # Tratamento de nulos sem descartar entregas
    # Preenche data_prevista vazia com a data_saída (ou vice-versa) se necessário para a operação
    if 'data_prevista' in df.columns and 'data_saída' in df.columns:
        df['data_prevista'] = df['data_prevista'].fillna(df['data_saída'])

    cols_data = ['data_prevista', 'data_saída']
    for col in cols_data:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True).dt.date
    
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