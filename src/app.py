"""
app.py — News Verifier Pro: Enterprise Fake News Detection Dashboard.

Architecture: Hybrid TF-IDF + SentenceTransformer + XGBoost
Features: LIME Explainability, Live Fact-Checking, Confidence Calibration
"""

import streamlit as st
import os
import sys
import time
import joblib
import requests
import numpy as np
import html as html_lib

from scipy.sparse import hstack, csr_matrix
from utils import clean_text, extract_entities
from styles import APP_CSS

# ---------------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="News Verifier Pro — Fake News Detection",
    page_icon="NV",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(APP_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NEWS_API_KEY = "7d2e0341566e473e8c4c9b7b7986b5a6"
NEWS_API_URL = "https://newsapi.org/v2/everything"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")


# ---------------------------------------------------------------------------
# Model Loading (Cached)
# ---------------------------------------------------------------------------
@st.cache_resource
def load_tfidf():
    path = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
    return joblib.load(path) if os.path.exists(path) else None


@st.cache_resource
def load_model():
    path = os.path.join(MODELS_DIR, "best_model.pkl")
    return joblib.load(path) if os.path.exists(path) else None


@st.cache_resource
def load_sentence_transformer():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_metrics():
    path = os.path.join(MODELS_DIR, "training_metrics.pkl")
    return joblib.load(path) if os.path.exists(path) else None


vectorizer = load_tfidf()
model = load_model()
metrics_data = load_metrics()


# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------
def predict_hybrid(text: str) -> dict:
    """Run hybrid inference: TF-IDF + Transformer → XGBoost."""
    t0 = time.perf_counter()
    clean = clean_text(text)
    if not clean.strip():
        return None

    st_model = load_sentence_transformer()
    X_tfidf = vectorizer.transform([clean])
    X_dense = st_model.encode([clean], normalize_embeddings=True)
    X_hybrid = hstack([X_tfidf, csr_matrix(X_dense)])

    pred = model.predict(X_hybrid)[0]
    prob = model.predict_proba(X_hybrid)[0]
    elapsed = (time.perf_counter() - t0) * 1000

    return {
        "prediction": int(pred),
        "label": "Fake" if pred == 1 else "Real",
        "confidence": float(max(prob)),
        "prob_real": float(prob[0]),
        "prob_fake": float(prob[1]),
        "clean_text": clean,
        "inference_ms": round(elapsed, 1),
    }


# ---------------------------------------------------------------------------
# LIME Explainability
# ---------------------------------------------------------------------------
def get_lime_explanation(text: str, num_features: int = 12) -> list:
    """Generate LIME explanations for the prediction."""
    try:
        from lime.lime_text import LimeTextExplainer
        explainer = LimeTextExplainer(class_names=["Real", "Fake"])
        st_model = load_sentence_transformer()

        def predict_fn(texts):
            results = []
            for t in texts:
                X_tfidf = vectorizer.transform([t])
                X_dense = st_model.encode([t], normalize_embeddings=True)
                X_h = hstack([X_tfidf, csr_matrix(X_dense)])
                results.append(model.predict_proba(X_h)[0])
            return np.array(results)

        clean = clean_text(text)
        exp = explainer.explain_instance(
            clean, predict_fn, num_features=num_features, num_samples=200
        )
        return exp.as_list()
    except Exception as e:
        return []


def highlight_text(raw_text: str, lime_features: list) -> str:
    """Create HTML with LIME-highlighted words."""
    words = raw_text.split()
    feature_dict = {f.lower(): w for f, w in lime_features}

    highlighted = []
    for word in words:
        clean_w = word.lower().strip(".,!?;:'\"()-")
        escaped = html_lib.escape(word)
        if clean_w in feature_dict:
            weight = feature_dict[clean_w]
            if weight > 0:
                highlighted.append(f'<span class="hw-fake">{escaped}</span>')
            else:
                highlighted.append(f'<span class="hw-real">{escaped}</span>')
        else:
            highlighted.append(escaped)

    return " ".join(highlighted)


# ---------------------------------------------------------------------------
# NewsAPI Fact-Check
# ---------------------------------------------------------------------------
def check_news_api(text: str) -> tuple:
    """Query NewsAPI with extracted entities."""
    entities = extract_entities(text)
    if not entities:
        words = text.split()[:5]
        search_q = " OR ".join(words)
        entities = words[:3]
    else:
        search_q = " OR ".join(entities[:4])

    params = {
        "q": search_q,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY,
    }
    try:
        resp = requests.get(NEWS_API_URL, params=params, timeout=5)
        articles = resp.json().get("articles", [])[:5] if resp.status_code == 200 else []
    except Exception:
        articles = []

    return articles, entities, search_q


# ---------------------------------------------------------------------------
# UI: Hero Section
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">Enterprise ML System</div>
    <div class="hero-title">News Verifier Pro</div>
    <div class="hero-sub">Hybrid AI verification combining Transformer embeddings + XGBoost classification with live source corroboration</div>
    <div class="tag-row">
        <span class="tag tag-blue">SentenceTransformer</span>
        <span class="tag tag-cyan">XGBoost Hybrid</span>
        <span class="tag tag-purple">LIME Explainability</span>
        <span class="tag">Live Fact-Check</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Check models
if vectorizer is None or model is None:
    st.error("Models not found. Run `python src/train_model.py` first.")
    st.stop()

# ---------------------------------------------------------------------------
# UI: Input
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">Input — Paste article text or claim</div>', unsafe_allow_html=True)
text_input = st.text_area(
    label="input_text",
    label_visibility="collapsed",
    height=140,
    placeholder="Enter a news article, headline, or social media claim to analyze...",
)

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("Run Verification Pipeline")

# ---------------------------------------------------------------------------
# UI: Results
# ---------------------------------------------------------------------------
if analyze_btn:
    if len(text_input.strip().split()) < 5:
        st.warning("Please provide at least 5 words for reliable analysis.")
    else:
        with st.spinner("Running hybrid inference pipeline..."):
            result = predict_hybrid(text_input)
            articles, entities, search_query = check_news_api(text_input)

        if result is None:
            st.error("Could not extract meaningful features from the input.")
        else:
            is_fake = result["prediction"] == 1

            # ── Verdict Panel ──
            if is_fake:
                st.markdown(f"""
                <div class="verdict-panel verdict-fake">
                    <div class="verdict-title">High Probability of Fabrication</div>
                    <div class="verdict-body">Linguistic and semantic markers indicate manipulated or inauthentic content</div>
                    <div class="verdict-conf">{result['prob_fake']*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="verdict-panel verdict-real">
                    <div class="verdict-title">Consistent with Authentic Reporting</div>
                    <div class="verdict-body">Language patterns and semantic context align with verified journalistic standards</div>
                    <div class="verdict-conf">{result['prob_real']*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Quick Metrics Row ──
            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-label">P(Authentic)</div>
                    <div class="metric-value mv-green">{result['prob_real']*100:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">P(Fabricated)</div>
                    <div class="metric-value mv-red">{result['prob_fake']*100:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Confidence</div>
                    <div class="metric-value mv-cyan">{result['confidence']*100:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Latency</div>
                    <div class="metric-value mv-amber">{result['inference_ms']}ms</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Tabs ──
            tab_xai, tab_web, tab_arch = st.tabs([
                "Explainability (XAI)",
                "Live Fact-Check",
                "Model Architecture",
            ])

            # ── Tab 1: Explainability ──
            with tab_xai:
                with st.spinner("Computing LIME explanations..."):
                    lime_feats = get_lime_explanation(text_input)

                if lime_feats:
                    st.markdown("""
                    <div class="xai-section">
                        <div class="xai-title">LIME Word Attribution Analysis</div>
                        <div style="font-size:0.72rem; color:#475569; margin-bottom:0.8rem;">
                            <span class="hw-fake" style="background:rgba(239,68,68,0.2);color:#fca5a5;padding:0.1rem 0.3rem;border-radius:3px;">Red = pushes toward Fake</span>
                            &nbsp;&nbsp;
                            <span class="hw-real" style="background:rgba(16,185,129,0.15);color:#6ee7b7;padding:0.1rem 0.3rem;border-radius:3px;">Green = pushes toward Real</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    highlighted = highlight_text(text_input, lime_feats)
                    st.markdown(f"""
                    <div class="xai-section" style="margin-top:0.6rem;">
                        <div class="xai-title">Highlighted Input Text</div>
                        <div class="xai-text">{highlighted}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Feature importance bars
                    top_n = min(10, len(lime_feats))
                    feats_sorted = sorted(lime_feats, key=lambda x: abs(x[1]), reverse=True)[:top_n]
                    max_w = max(abs(w) for _, w in feats_sorted) if feats_sorted else 1

                    bars_html = ""
                    for word, weight in feats_sorted:
                        pct = abs(weight) / max_w * 100
                        color = "#ef4444" if weight > 0 else "#10b981"
                        direction = "→ Fake" if weight > 0 else "→ Real"
                        dir_color = "#fca5a5" if weight > 0 else "#6ee7b7"
                        escaped_word = html_lib.escape(word)
                        bars_html += (
                            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">'
                            f'<span style="min-width:90px;font-size:0.78rem;font-weight:600;color:#cbd5e1;text-align:right;">{escaped_word}</span>'
                            f'<div style="flex:1;height:16px;background:rgba(255,255,255,0.03);border-radius:3px;overflow:hidden;">'
                            f'<div style="width:{pct:.0f}%;height:100%;background:{color};border-radius:3px;"></div>'
                            f'</div>'
                            f'<span style="font-size:0.65rem;color:{dir_color};min-width:50px;">{direction}</span>'
                            f'</div>'
                        )
                    import streamlit.components.v1 as components
                    bars_full_html = (
                        f'<div style="background:rgba(15,20,35,0.85);border:1px solid rgba(148,163,184,0.08);'
                        f'border-radius:8px;padding:1.2rem;font-family:Inter,sans-serif;">'
                        f'<div style="font-size:0.7rem;font-weight:700;color:#8b5cf6;text-transform:uppercase;'
                        f'letter-spacing:1px;margin-bottom:0.8rem;">Top Feature Importance</div>'
                        f'{bars_html}'
                        f'</div>'
                    )
                    components.html(bars_full_html, height=40 + len(feats_sorted) * 28, scrolling=False)
                else:
                    st.info("LIME explainability requires the `lime` package. Install with: `pip install lime`")

            # ── Tab 2: Live Fact-Check ──
            with tab_web:
                st.markdown(f"""
                <div class="xai-section">
                    <div class="xai-title">Threat Intelligence Query</div>
                    <div class="arch-row">
                        <span class="arch-label">Entities</span>
                        <span class="arch-val">{', '.join(entities) if entities else 'N/A'}</span>
                    </div>
                    <div class="arch-row">
                        <span class="arch-label">Search Query</span>
                        <span class="arch-val" style="font-size:0.72rem;">{html_lib.escape(search_query)}</span>
                    </div>
                    <div class="arch-row">
                        <span class="arch-label">Sources Found</span>
                        <span class="arch-val">{len(articles)}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if articles:
                    for art in articles:
                        title = html_lib.escape(art.get("title", "Untitled") or "Untitled")
                        source = html_lib.escape(art.get("source", {}).get("name", "Unknown"))
                        url = art.get("url", "#")
                        published = art.get("publishedAt", "")[:10]

                        st.markdown(f"""
                        <a href="{url}" target="_blank" class="source-card">
                            <div class="source-headline">{title}</div>
                            <div class="source-meta">
                                <span class="source-badge">{source}</span>
                                <span>{published}</span>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="no-results-box">
                        <div class="no-results-title">No Corroborating Sources Found</div>
                        <div class="no-results-desc">No established publishers cover this claim — potentially unsubstantiated.</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Tab 3: Model Architecture ──
            with tab_arch:
                if metrics_data:
                    m = metrics_data
                    st.markdown(f"""
                    <div class="arch-box">
                        <div class="xai-title">Training Metrics</div>
                        <div class="arch-row"><span class="arch-label">Accuracy</span><span class="arch-val">{m.get('accuracy', 0)*100:.2f}%</span></div>
                        <div class="arch-row"><span class="arch-label">Precision</span><span class="arch-val">{m.get('precision', 0)*100:.2f}%</span></div>
                        <div class="arch-row"><span class="arch-label">Recall</span><span class="arch-val">{m.get('recall', 0)*100:.2f}%</span></div>
                        <div class="arch-row"><span class="arch-label">F1 Score</span><span class="arch-val">{m.get('f1_score', 0)*100:.2f}%</span></div>
                        <div class="arch-row"><span class="arch-label">ROC-AUC</span><span class="arch-val">{m.get('roc_auc', 0)*100:.2f}%</span></div>
                    </div>
                    <div class="arch-box">
                        <div class="xai-title">Architecture Details</div>
                        <div class="arch-row"><span class="arch-label">Embeddings</span><span class="arch-val">SentenceTransformer ({m.get('embedding_model', 'all-MiniLM-L6-v2')})</span></div>
                        <div class="arch-row"><span class="arch-label">Embed Dim</span><span class="arch-val">{m.get('embedding_dim', 384)}</span></div>
                        <div class="arch-row"><span class="arch-label">TF-IDF Features</span><span class="arch-val">{m.get('tfidf_features', 10000):,}</span></div>
                        <div class="arch-row"><span class="arch-label">Total Features</span><span class="arch-val">{m.get('total_features', 0):,}</span></div>
                        <div class="arch-row"><span class="arch-label">Classifier</span><span class="arch-val">XGBoost (300 trees, depth=6)</span></div>
                        <div class="arch-row"><span class="arch-label">Train Time</span><span class="arch-val">{m.get('train_time_seconds', 0):.1f}s</span></div>
                        <div class="arch-row"><span class="arch-label">Train Samples</span><span class="arch-val">{m.get('train_samples', 0):,}</span></div>
                        <div class="arch-row"><span class="arch-label">Test Samples</span><span class="arch-val">{m.get('test_samples', 0):,}</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="arch-box">
                        <div class="xai-title">Architecture</div>
                        <div class="arch-row"><span class="arch-label">Pipeline</span><span class="arch-val">TF-IDF (10k bigrams) + SentenceTransformer (384d) → XGBoost</span></div>
                        <div class="arch-row"><span class="arch-label">XAI</span><span class="arch-val">LIME (Local Interpretable Model-Agnostic Explanations)</span></div>
                        <div class="arch-row"><span class="arch-label">Fact-Check</span><span class="arch-val">NewsAPI + NER Entity Extraction</span></div>
                    </div>
                    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("""
<div class="divider"></div>
<div class="app-footer">
    News Verifier Pro v3.0 · Hybrid Transformer + XGBoost · LIME XAI · NewsAPI · Built by Praveen Mishra
</div>
""", unsafe_allow_html=True)
