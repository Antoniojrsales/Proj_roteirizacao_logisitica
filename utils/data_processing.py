import pandas as pd

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica as regras de negócio e sanitização nos dados brutos das entregas.
    Retorna o DataFrame tratado e pronto para a exibição/roteirização.
    """
    # 1. Validação de DataFrame vazio ou nulo
    if df is None or df.empty:
        return pd.DataFrame()

    try:
        # Criamos uma cópia para evitar warnings de SettingWithCopy
        df_processed = df.copy()

        # -------------------------------------------------------------
        # FUTURO TRATAMENTO DE DADOS (Adicionar regras aqui conforme necessário)
        # Exemplo: df_processed['status'] = df_processed['status'].str.lower()
        # -------------------------------------------------------------

        return df_processed

    except Exception as e:
        # Retorna o DataFrame original em caso de falha no pipeline
        return df