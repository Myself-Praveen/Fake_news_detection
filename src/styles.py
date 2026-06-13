"""styles.py — CSS constants for the News Verifier Pro Enterprise UI."""

APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #0a0e17;
        --bg-card: rgba(15, 20, 35, 0.85);
        --bg-card-hover: rgba(20, 28, 50, 0.9);
        --bg-input: rgba(10, 14, 25, 0.9);
        --accent-blue: #3b82f6;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --accent-amber: #f59e0b;
        --accent-purple: #8b5cf6;
        --text-bright: #f1f5f9;
        --text-main: #cbd5e1;
        --text-dim: #64748b;
        --text-faint: #475569;
        --border: rgba(148, 163, 184, 0.08);
        --border-hover: rgba(148, 163, 184, 0.18);
        --glow-blue: rgba(59, 130, 246, 0.12);
        --glow-green: rgba(16, 185, 129, 0.1);
        --glow-red: rgba(239, 68, 68, 0.1);
    }

    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #0f172a 50%, #0a0e17 100%) !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    header, footer, #MainMenu { visibility: hidden; }

    .block-container {
        padding: 1.5rem 1rem 3rem 1rem !important;
        max-width: 820px;
    }

    /* Hero */
    .hero-section {
        text-align: center;
        padding: 2rem 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    .hero-badge {
        display: inline-block;
        font-size: 0.65rem;
        font-weight: 700;
        color: var(--accent-cyan);
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.2);
        padding: 0.2rem 0.7rem;
        border-radius: 4px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--text-bright);
        letter-spacing: -0.5px;
        margin-bottom: 0.3rem;
    }
    .hero-sub {
        font-size: 0.85rem;
        color: var(--text-dim);
        font-weight: 400;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    .tag-row {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .tag {
        font-size: 0.68rem;
        font-weight: 600;
        padding: 0.25rem 0.7rem;
        border-radius: 4px;
        letter-spacing: 0.3px;
        border: 1px solid var(--border);
        color: var(--text-dim);
        background: rgba(255,255,255,0.02);
    }
    .tag-blue { border-color: rgba(59,130,246,0.3); color: var(--accent-blue); }
    .tag-cyan { border-color: rgba(6,182,212,0.3); color: var(--accent-cyan); }
    .tag-purple { border-color: rgba(139,92,246,0.3); color: var(--accent-purple); }

    /* Input */
    .section-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.6rem;
    }
    .stTextArea textarea {
        background: var(--bg-input) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }
    .stTextArea div[data-baseweb="textarea"],
    .stTextArea div[data-baseweb="base-input"],
    .stTextArea [class*="InputContainer"] {
        background: transparent !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px var(--glow-blue) !important;
    }

    /* Button */
    .stButton { display: flex; justify-content: center; }
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.3px !important;
        min-width: 260px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
    }

    /* Verdict */
    .verdict-panel {
        text-align: center;
        padding: 1.8rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(14px);
    }
    .verdict-fake {
        background: var(--glow-red);
        border: 1px solid rgba(239,68,68,0.2);
    }
    .verdict-real {
        background: var(--glow-green);
        border: 1px solid rgba(16,185,129,0.2);
    }
    .verdict-icon { font-size: 2rem; margin-bottom: 0.4rem; }
    .verdict-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.3rem; }
    .verdict-fake .verdict-title { color: var(--accent-red); }
    .verdict-real .verdict-title { color: var(--accent-green); }
    .verdict-body { color: var(--text-dim); font-size: 0.85rem; line-height: 1.4; }
    .verdict-conf {
        font-size: 2rem; font-weight: 800; margin-top: 0.5rem;
    }
    .verdict-fake .verdict-conf { color: var(--accent-red); }
    .verdict-real .verdict-conf { color: var(--accent-green); }

    /* Metrics Grid */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.6rem;
        margin-top: 1rem;
    }
    .metric-box {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .metric-box:hover { border-color: var(--border-hover); }
    .metric-label {
        font-size: 0.6rem;
        font-weight: 700;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-bright);
    }
    .mv-blue { color: var(--accent-blue); }
    .mv-green { color: var(--accent-green); }
    .mv-red { color: var(--accent-red); }
    .mv-cyan { color: var(--accent-cyan); }
    .mv-amber { color: var(--accent-amber); }

    /* XAI Highlights */
    .xai-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.2rem;
        margin-top: 1rem;
    }
    .xai-title {
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--accent-purple);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }
    .xai-text {
        font-size: 0.88rem;
        color: var(--text-main);
        line-height: 1.8;
        word-wrap: break-word;
    }
    .xai-text .hw-fake {
        background: rgba(239,68,68,0.2);
        color: #fca5a5;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        font-weight: 600;
    }
    .xai-text .hw-real {
        background: rgba(16,185,129,0.15);
        color: #6ee7b7;
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        font-weight: 600;
    }

    /* Source Cards */
    .source-card {
        display: block;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        text-decoration: none;
        transition: all 0.2s;
    }
    .source-card:hover {
        border-color: var(--accent-blue);
        transform: translateY(-1px);
    }
    .source-headline {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-bright);
        line-height: 1.3;
        margin-bottom: 0.4rem;
    }
    .source-meta {
        font-size: 0.72rem;
        color: var(--text-faint);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .source-badge {
        background: rgba(6,182,212,0.1);
        color: var(--accent-cyan);
        font-size: 0.62rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: transparent; gap: 0.4rem; }
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 6px;
        color: var(--text-dim);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 0.4rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: var(--glow-blue) !important;
        border-color: rgba(59,130,246,0.3) !important;
        color: var(--accent-blue) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Misc */
    .no-results-box {
        text-align: center;
        padding: 2rem 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
    }
    .no-results-title { font-size: 0.9rem; font-weight: 600; color: var(--text-main); margin-bottom: 0.3rem; }
    .no-results-desc { font-size: 0.78rem; color: var(--text-faint); line-height: 1.5; }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 1.5rem 0;
    }
    .app-footer {
        text-align: center;
        color: var(--text-faint);
        font-size: 0.7rem;
        padding: 0.5rem 0;
        letter-spacing: 0.3px;
    }

    .arch-box {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.8rem;
    }
    .arch-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.4rem;
    }
    .arch-label {
        font-size: 0.65rem;
        font-weight: 700;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        min-width: 100px;
    }
    .arch-val {
        font-size: 0.8rem;
        color: var(--text-main);
        font-weight: 500;
    }
</style>
"""
