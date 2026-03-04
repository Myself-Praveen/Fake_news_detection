import streamlit as st
import os
import sys
import joblib
import requests
import time
import streamlit.components.v1 as components
from utils import clean_text

st.set_page_config(
    page_title="News Verifier Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

NEWS_API_KEY = "7d2e0341566e473e8c4c9b7b7986b5a6"
NEWS_API_URL = "https://newsapi.org/v2/everything"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {
        --surface: rgba(18, 18, 18, 0.75);
        --surface-light: rgba(30, 30, 30, 0.65);
        --surface-bright: rgba(40, 40, 40, 0.7);
        --accent: #bb86fc;
        --accent-glow: rgba(187, 134, 252, 0.15);
        --teal: #03dac6;
        --teal-glow: rgba(3, 218, 198, 0.12);
        --red: #cf6679;
        --red-glow: rgba(207, 102, 121, 0.12);
        --text-bright: #ffffff;
        --text-main: #e0e0e0;
        --text-dim: #9e9e9e;
        --text-faint: #616161;
        --border: rgba(255, 255, 255, 0.07);
        --border-hover: rgba(255, 255, 255, 0.15);
    }

    .stApp {
        background-color: transparent !important;
        font-family: 'Outfit', sans-serif;
    }

    header, footer, #MainMenu { visibility: hidden; }

    .block-container {
        padding: 2rem 1rem 4rem 1rem !important;
        max-width: 760px;
    }

    .hero-section {
        text-align: center;
        padding: 3rem 2rem 2.5rem;
        margin-bottom: 2rem;
        background: var(--surface);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border);
        border-radius: 16px;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: var(--text-bright);
        letter-spacing: -0.5px;
        margin-bottom: 0.4rem;
    }

    .hero-sub {
        font-size: 1rem;
        color: var(--text-dim);
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    .tag-row {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        flex-wrap: wrap;
    }

    .tag {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.3rem 0.9rem;
        border-radius: 100px;
        letter-spacing: 0.3px;
        border: 1px solid var(--border);
        color: var(--text-dim);
        background: rgba(255,255,255,0.03);
    }

    .tag-teal { border-color: rgba(3,218,198,0.3); color: var(--teal); }
    .tag-purple { border-color: rgba(187,134,252,0.3); color: var(--accent); }

    .input-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.75rem;
    }



    .stTextArea textarea {
        background: rgba(10, 10, 10, 0.85) !important;
        color: #e0e0e0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
    }

    .stTextArea div[data-baseweb="textarea"],
    .stTextArea div[data-baseweb="base-input"],
    .stTextArea [class*="InputContainer"],
    .stTextArea [class*="stTextArea"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-glow) !important;
    }

    .stButton {
        display: flex;
        justify-content: center;
    }

    .stButton > button {
        background: var(--accent) !important;
        color: #121212 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 2.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        width: auto !important;
        min-width: 280px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 20px var(--accent-glow) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 30px rgba(187, 134, 252, 0.3) !important;
    }

    .verdict-panel {
        text-align: center;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
    }

    .verdict-fake {
        background: var(--red-glow);
        border: 1px solid rgba(207, 102, 121, 0.25);
    }

    .verdict-real {
        background: var(--teal-glow);
        border: 1px solid rgba(3, 218, 198, 0.25);
    }

    .verdict-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .verdict-fake .verdict-title { color: var(--red); }
    .verdict-real .verdict-title { color: var(--teal); }

    .verdict-body {
        color: var(--text-dim);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .metrics-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .metric-box {
        background: var(--surface);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        transition: border-color 0.2s ease;
    }

    .metric-box:hover {
        border-color: var(--border-hover);
    }

    .metric-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-bright);
    }

    .metric-value-teal { color: var(--teal); }
    .metric-value-red { color: var(--red); }

    .source-card {
        display: block;
        background: var(--surface-light);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        text-decoration: none;
        transition: all 0.2s ease;
    }

    .source-card:hover {
        border-color: var(--accent);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    .source-headline {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-bright);
        line-height: 1.4;
        margin-bottom: 0.6rem;
    }

    .source-pub {
        font-size: 0.8rem;
        color: var(--text-faint);
        display: flex;
        justify-content: space-between;
    }

    .source-badge {
        background: var(--teal-glow);
        color: var(--teal);
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--surface-light);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text-dim);
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 0.5rem 1.2rem;
    }

    .stTabs [aria-selected="true"] {
        background: var(--accent-glow) !important;
        border-color: rgba(187, 134, 252, 0.4) !important;
        color: var(--accent) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }

    .app-footer {
        text-align: center;
        color: var(--text-faint);
        font-size: 0.8rem;
        padding: 1rem 0;
    }

    .no-results-box {
        text-align: center;
        padding: 3rem 1rem;
        background: var(--surface);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin-top: 1rem;
    }

    .no-results-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-main);
        margin-bottom: 0.5rem;
    }

    .no-results-desc {
        font-size: 0.85rem;
        color: var(--text-faint);
        max-width: 360px;
        margin: 0 auto;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

vanta_html = """
<script>
const parentDoc = window.parent.document;
if (!parentDoc.getElementById('vanta-three')) {
    const threeScript = parentDoc.createElement('script');
    threeScript.id = 'vanta-three';
    threeScript.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js";
    parentDoc.head.appendChild(threeScript);

    threeScript.onload = () => {
        const vantaScript = parentDoc.createElement('script');
        vantaScript.id = 'vanta-net';
        vantaScript.src = "https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js";
        parentDoc.head.appendChild(vantaScript);

        vantaScript.onload = () => {
            setTimeout(() => {
                window.parent.VANTA.NET({
                    el: parentDoc.querySelector(".stApp"),
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: 200.00,
                    minWidth: 200.00,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    color: 0x03dac6,
                    backgroundColor: 0x121212,
                    points: 10.00,
                    maxDistance: 22.00,
                    spacing: 18.00
                });
            }, 200);
        };
    };
}
</script>
"""
components.html(vanta_html, width=0, height=0)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@st.cache_resource
def load_models():
    vec_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
    best_path = os.path.join(MODELS_DIR, "best_model.pkl")
    if not os.path.exists(vec_path) or not os.path.exists(best_path):
        return None, None
    return joblib.load(vec_path), joblib.load(best_path)

vectorizer, model = load_models()

def predict_local(text):
    clean = clean_text(text)
    if not clean.strip():
        return None, [0.0, 0.0], ""
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    return pred, prob, clean

def check_news_api(query_text):
    words = query_text.split()
    if len(words) < 3:
        return []
    search_query = " OR ".join(words[:5])
    params = {
        'q': search_query,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 5,
        'apiKey': NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get('articles', [])[:5]
        return []
    except Exception:
        return []


st.markdown("""
<div class="hero-section">
    <div class="hero-title">News Verifier Pro</div>
    <div class="hero-sub">Dual-engine verification combining linguistic analysis with live source checking</div>
    <div class="tag-row">
        <span class="tag tag-teal">XGBoost Engine</span>
        <span class="tag tag-purple">NewsAPI Integration</span>
        <span class="tag">99.8% Accuracy</span>
    </div>
</div>
""", unsafe_allow_html=True)

if vectorizer is None or model is None:
    st.error("Models not found. Please run train_model.py first.")
    st.stop()

st.markdown('<div class="input-label">Paste article text or claim</div>', unsafe_allow_html=True)

text_input = st.text_area(
    label="input_text",
    label_visibility="collapsed",
    height=160,
    placeholder="Enter text to analyze for authenticity..."
)

st.markdown('<br>', unsafe_allow_html=True)
analyze_btn = st.button("Verify Authenticity")

if analyze_btn:
    if len(text_input.strip().split()) < 5:
        st.warning("Please provide at least 5 words for a reliable analysis.")
    else:
        with st.spinner("Analyzing patterns and checking sources..."):
            pred, probs, clean_query = predict_local(text_input)
            articles = check_news_api(clean_query) if clean_query else []

        if pred is None:
            st.error("Could not extract meaningful features from the input.")
        else:
            is_fake = (pred == 1)

            if is_fake:
                st.markdown(f"""
                <div class="verdict-panel verdict-fake">
                    <div class="verdict-title">High Probability of Fabrication</div>
                    <div class="verdict-body">Linguistic markers suggest manipulated or inauthentic source material. Confidence: {probs[1]*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="verdict-panel verdict-real">
                    <div class="verdict-title">Consistent with Authentic Reporting</div>
                    <div class="verdict-body">Language patterns align with verified journalistic standards. Confidence: {probs[0]*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

            tab_ai, tab_web = st.tabs(["Analysis Metrics", "External Sources"])

            with tab_ai:
                st.markdown(f"""
                <div class="metrics-row">
                    <div class="metric-box">
                        <div class="metric-label">Authenticity Score</div>
                        <div class="metric-value metric-value-teal">{probs[0]*100:.1f}%</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Fabrication Score</div>
                        <div class="metric-value metric-value-red">{probs[1]*100:.1f}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                word_count = len(text_input.split())
                clean_count = len(clean_query.split()) if clean_query else 0

                st.markdown(f"""
                <div class="metrics-row" style="margin-top: 0.75rem;">
                    <div class="metric-box">
                        <div class="metric-label">Words Processed</div>
                        <div class="metric-value">{word_count}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Features Extracted</div>
                        <div class="metric-value">{clean_count}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with tab_web:
                if articles:
                    st.markdown(f'<p style="color:var(--text-dim); margin: 1rem 0; font-size: 0.9rem;">Found {len(articles)} related article(s) from indexed publications.</p>', unsafe_allow_html=True)

                    for art in articles:
                        title = art.get('title', 'Untitled')
                        source = art.get('source', {}).get('name', 'Unknown')
                        url = art.get('url', '#')
                        published = art.get('publishedAt', '')[:10]

                        st.markdown(f"""
                        <a href="{url}" target="_blank" class="source-card">
                            <div class="source-headline">{title}</div>
                            <div class="source-pub">
                                <span class="source-badge">{source}</span>
                                <span>{published}</span>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="no-results-box">
                        <div class="no-results-title">No Corroborating Sources Found</div>
                        <div class="no-results-desc">No established publishers appear to cover this claim, which may indicate an unsubstantiated or unreliable source.</div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("""
<div class="divider"></div>
<div class="app-footer">
    News Verifier Pro v2.0 &middot; XGBoost + TF-IDF + NewsAPI &middot; Built by Praveen Mishra
</div>
""", unsafe_allow_html=True)
