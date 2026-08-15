import streamlit as st

def render_card(title: str, value, prefix: str = "", suffix: str = "", gradient: str = "#2563eb, #1d4ed8"):
    """
    Renderiza um card de KPI estilizado com suporte a números inteiros, floats, moeda e porcentagens.
    
    Exemplos:
    - Contagem: render_card("Total Entregas", 1206, gradient="#1e3a8a, #3b82f6")
    - Percentual: render_card("Taxa de Sucesso", 94.5, suffix="%", gradient="#059669, #10b981")
    - Financeiro: render_card("Custo Frete", 1450.50, prefix="R$ ", gradient="#d97706, #f59e0b")
    """
    # Formatação dinâmica do valor
    if isinstance(value, (int, float)):
        if isinstance(value, float):
            valor_str = f"{value:,.1f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        else:
            valor_str = f"{value:,}".replace(',', '.')
    else:
        valor_str = str(value)
    
    valor_formatado = f"{prefix}{valor_str}{suffix}"

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, {gradient});
        color: #ffffff;
        padding: 18px 20px;
        border-radius: 12px;
        font-family: 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 100px;
        margin-bottom: 15px;
    ">
        <span style="font-size: 0.95em; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">
            {title}
        </span>
        <span style="font-size: 1.8em; font-weight: 700; margin-top: 8px; letter-spacing: -0.5px;">
            {valor_formatado}
        </span>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)