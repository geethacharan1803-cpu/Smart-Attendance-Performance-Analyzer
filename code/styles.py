import streamlit as st

def inject_custom_css():
    """
    Injects high-contrast Light Theme styling with crisp dark typography,
    pure white card surfaces, soft borders, vibrant metrics, 
    and clear math callout containers.
    """
    custom_css = """
    <style>
    /* Main container background & primary typography */
    .main, .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Global Text Contrast Rules */
    p, span, label, h1, h2, h3, h4, h5, h6, li, div, caption {
        color: #0f172a !important;
    }
    
    /* Header card container */
    .header-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #0284c7, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .header-subtitle {
        color: #475569 !important;
        font-size: 1.05rem;
        font-weight: 600;
    }
    
    /* Metric Cards */
    .stat-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        border-color: #0284c7;
    }
    .stat-val {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0284c7 !important;
    }
    .stat-lbl {
        font-size: 0.85rem;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
        font-weight: 700;
    }
    
    /* Control Panel & Card Boxes */
    [data-testid="stSidebar"], .control-panel-box {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px;
        padding: 18px;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    .control-panel-box label, .control-panel-box p, .control-panel-box span {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    /* Multiselect Tags & Selectbox Contrast */
    span[data-baseweb="tag"] {
        background-color: #e2e8f0 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }
    span[data-baseweb="tag"] span {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }

    /* Streamlit Dataframe Contrast */
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    /* Tab navigation styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px;
        color: #475569 !important;
        font-weight: 700 !important;
        padding: 0 18px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }
    
    /* Content Box Containers */
    .content-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 22px;
        margin-top: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .content-box h3, .content-box h4 {
        color: #0284c7 !important;
        margin-bottom: 12px;
    }

    /* Math & Worked Example Formula Callout Container */
    .math-callout {
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        border-left: 5px solid #0284c7 !important;
        padding: 20px 24px !important;
        border-radius: 8px 12px 12px 8px !important;
        margin: 16px 0 !important;
        color: #0f172a !important;
        line-height: 1.7 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
    }

    .math-callout strong {
        color: #0284c7 !important;
    }

    .math-callout code {
        background-color: #e2e8f0 !important;
        color: #0369a1 !important;
        padding: 2px 8px !important;
        border-radius: 4px !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 700 !important;
    }

    /* High Contrast Risk Badges (Light Theme) */
    .badge-safe {
        background-color: #dcfce7 !important;
        color: #166534 !important;
        padding: 5px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #22c55e;
    }
    .badge-moderate {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        padding: 5px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #f59e0b;
    }
    .badge-high-risk {
        background-color: #fee2e2 !important;
        color: #991b1b !important;
        padding: 5px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #ef4444;
    }
    
    /* Code block contrast fix */
    pre, code {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        border-radius: 6px !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
