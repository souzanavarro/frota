import streamlit as st


def apply_styles(theme_mode: str = '🌞 Claro'):
    """Aplica CSS centralizado para temas Claro/Escuro (estilo One UI / Material Design).

    Chame esta função no início do app para aplicar estilos globais.
    """
    primary = "#1976d2"  # azul Material padrão
    accent = "#FFB800"
    danger = "#FF4B4B"

    if theme_mode == '🌞 Claro':
        bg = "#FAFAFB"
        surface = "#FFFFFF"
        text = "#1f1f1f"
        muted = "#6b6b6b"
    else:
        bg = "#0f1113"
        surface = "#1e1e1e"
        text = "#e6e6e6"
        muted = "#9a9a9a"

    st.markdown(f'''
    <style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    :root {{
      --primary: {primary};
      --accent: {accent};
      --danger: {danger};
      --bg: {bg};
      --surface: {surface};
      --text: {text};
      --muted: {muted};
      --radius: 12px;
      --shadow-1: 0 3px 12px rgba(2,6,23,0.06);
      --shadow-2: 0 8px 30px rgba(2,6,23,0.08);
    }}

    body, .stApp {{
      background: var(--bg) !important;
      color: var(--text) !important;
      font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }}

    /* Sidebar */
    .stSidebar, section[data-testid="stSidebar"] {{
      background: var(--surface) !important;
      color: var(--text) !important;
      border-radius: 16px;
      border-right: 1px solid rgba(0,0,0,0.04);
      box-shadow: var(--shadow-1);
      padding: 1rem 0.8rem 2rem 0.8rem;
    }}

    /* Menu buttons */
    .menu-btn {{
      display:flex;align-items:center;gap:0.75rem;padding:0.6rem 0.9rem;border-radius:var(--radius);border:none;background:transparent;color:var(--text);font-weight:600;cursor:pointer;transition:all .18s;
    }}
    .menu-btn:hover {{ background: rgba(25,118,210,0.06);transform:translateY(-1px);box-shadow:var(--shadow-1); }}
    .menu-btn.selected {{ color: var(--primary);background: linear-gradient(90deg, rgba(25,118,210,0.06), rgba(25,118,210,0.03)); }}
    .menu-divider {{ height:1px;background:rgba(0,0,0,0.06);margin:1rem 0;border:none }}

    /* Cards and surfaces */
    .cardbox, .cp-card {{ background: var(--surface); border-radius: 12px; padding:1rem; box-shadow: var(--shadow-1); border: 1px solid rgba(0,0,0,0.04); color:var(--text); }}
    .cardbox:hover {{ box-shadow: var(--shadow-2); transform: translateY(-4px); }}

    /* KPIs */
    .kpi {{ font-size:2.2rem;font-weight:700;color:var(--primary); }}
    .kpi-title {{ font-size:1rem;color:var(--muted);font-weight:600 }}

    /* Buttons look like Material / One UI */
    .stButton>button, .stDownloadButton>button {{
      background: var(--surface); color: var(--text); border: 1px solid rgba(0,0,0,0.06); padding:0.5rem 1rem; border-radius:10px; min-height:44px; font-weight:700; box-shadow: var(--shadow-1);
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{ transform: translateY(-2px); box-shadow: var(--shadow-2); }}

    /* Inputs / selects */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea, div[data-baseweb="select"] > div {{
        background: var(--surface) !important; color: var(--text) !important; border: 1px solid rgba(0,0,0,0.06) !important; border-radius: 10px !important; padding:10px !important;
    }}
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {{ outline: 2px solid rgba(25,118,210,0.12) !important; box-shadow: 0 4px 16px rgba(25,118,210,0.06) !important; }}

    /* One UI / Material-like components used by some pages */
    .cp-hero {{ display:flex; align-items:center; gap:1rem; margin-bottom:0.6rem; }}
    .cp-hero-icon {{ font-size:2.6rem; color:var(--accent); }}
    .cp-hero-title {{ font-size:1.4rem; font-weight:700; }}
    .cp-sub {{ color:var(--muted); margin-top:-6px }}
    .cp-grid {{ display:flex; gap:1rem; flex-wrap:wrap }}
    .cp-metric {{ background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,250,250,0.95)); padding:0.7rem; border-radius:10px; text-align:center }}
    .cp-btn {{ background:var(--primary); color:white; border-radius:10px; padding:8px 14px; border:none; font-weight:700; }}
    .cp-accent {{ color: var(--primary); font-weight:600 }}

    /* Back card + data panel: place a white card behind and data (table) visually in front */
    .back-card {{ position: relative; z-index: 1; overflow: visible; }}
    .data-panel {{ position: relative; margin-top: -30px; z-index: 5; padding: 0 0.4rem; }}
    .data-table-surface {{ background: var(--surface); border-radius: 14px; padding: 0.5rem; box-shadow: 0 10px 30px rgba(2,6,23,0.12); border: 1px solid rgba(0,0,0,0.06); overflow: auto; }}
    /* small tweak to table rows and header so they look compact */
    .data-table-surface table {{ width:100%; border-collapse:collapse; font-size:0.96rem }}
    .data-table-surface th, .data-table-surface td {{ padding:0.55rem 0.85rem; border-bottom: 1px solid rgba(0,0,0,0.04) }}
    .data-table-surface thead th {{ background: transparent; font-weight:700; color:var(--muted); text-align:left }}
    /* make the top of the white card have a soft capsule effect like the mock */
    /* Removed capsule pseudo-element to avoid extra rounded white bar */

    /* Small utilities */
    .muted {{ color: var(--muted) }}
    .rounded {{ border-radius: 10px }}

    @media (max-width: 700px) {{
      .cardbox {{ padding:0.9rem }}
      .cp-hero-title {{ font-size:1.1rem }}
    }}
    </style>
    ''', unsafe_allow_html=True)
