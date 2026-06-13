"""
predict.py — Inference module for News Verifier Pro.

Loads the trained hybrid model (TF-IDF + Transformer + XGBoost)
and provides a predict() function used by both the CLI and Streamlit UI.
"""

import os
import time
import numpy as np
import joblib
from scipy.sparse import hstack, csr_matrix
from utils import clean_text

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")

# ---------------------------------------------------------------------------
# Lazy Model Loading (for import-time safety)
# ---------------------------------------------------------------------------
_vectorizer = None
_model = None
_st_model = None


def _load_models():
    """Load TF-IDF vectorizer and XGBoost model from disk."""
    global _vectorizer, _model
    if _vectorizer is None:
        _vectorizer = joblib.load(VECTORIZER_PATH)
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _vectorizer, _model


def _load_sentence_transformer():
    """Load the SentenceTransformer model (cached after first call)."""
    global _st_model
    if _st_model is None:
        from sentence_transformers import SentenceTransformer
        _st_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _st_model


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def predict(text: str) -> dict:
    """
    Run the full hybrid inference pipeline on a single text input.

    Args:
        text: Raw article or claim text.

    Returns:
        Dictionary with keys:
            - prediction (int): 0 = Real, 1 = Fake
            - label (str): "Fake" or "Real"
            - confidence (float): Probability of the predicted class
            - prob_real (float): P(Real)
            - prob_fake (float): P(Fake)
            - clean_text (str): Cleaned text used for features
            - inference_ms (float): End-to-end inference latency
    """
    t0 = time.perf_counter()

    vectorizer, model = _load_models()
    st_model = _load_sentence_transformer()

    clean = clean_text(text)
    if not clean.strip():
        return {
            "prediction": None,
            "label": "Unknown",
            "confidence": 0.0,
            "prob_real": 0.0,
            "prob_fake": 0.0,
            "clean_text": "",
            "inference_ms": 0.0,
        }

    # TF-IDF features
    X_tfidf = vectorizer.transform([clean])

    # Transformer embeddings
    X_dense = st_model.encode([clean], normalize_embeddings=True)
    X_dense_sparse = csr_matrix(X_dense)

    # Concatenate
    X_hybrid = hstack([X_tfidf, X_dense_sparse])

    # Predict
    pred = model.predict(X_hybrid)[0]
    prob = model.predict_proba(X_hybrid)[0]

    elapsed = (time.perf_counter() - t0) * 1000  # ms

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
# CLI Interface
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("  News Verifier Pro — CLI Inference")
    print("=" * 50)
    print("Type 'exit' to quit.\n")

    while True:
        text = input("Enter news text: ")
        if text.lower() == "exit":
            break

        result = predict(text)
        print(f"\n  Verdict    : {result['label']}")
        print(f"  Confidence : {result['confidence']*100:.1f}%")
        print(f"  P(Real)    : {result['prob_real']*100:.1f}%")
        print(f"  P(Fake)    : {result['prob_fake']*100:.1f}%")
        print(f"  Latency    : {result['inference_ms']:.1f} ms\n")
