import pandas as pd

def metricas_gerais(df: pd.DataFrame) -> dict:
    base_metrics = {
        "total_entregas": 0,
        "total_concluidas": 0,
        "taxa_sucesso": 0,      
        "total_reentregas": 0,
        "total_motoristas": 0,
    }

    if df is None or df.empty:
        return base_metrics

    # Cálculo rápido dos indicadores com base no DataFrame tratado
    total_entregas = len(df)
    total_concluidas = len(df[df['status'] == 'CONCLUIDO'])
    taxa_sucesso = (total_concluidas / total_entregas * 100) if total_entregas > 0 else 0
    total_reentregas = len(df[df['eh_reentrega'] == 'Sim'])
    total_motoristas = df['motorista'].nunique() if 'motorista' in df.columns else 0

    return {
        "total_entregas":total_entregas,
        "total_concluidas": total_concluidas,
        "taxa_sucesso": taxa_sucesso,      
        "total_reentregas": total_reentregas,
        "total_motoristas": total_motoristas,
    }