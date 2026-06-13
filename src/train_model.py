"""
train_model.py — Hybrid ML Training Pipeline for News Verifier Pro.

Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │  Raw Text                                               │
    │    ├── TF-IDF (10k bigram features)  ──┐                │
    │    └── SentenceTransformer embeddings ──┤                │
    │                                        ▼                │
    │                          ┌─────────────────────┐        │
    │                          │  Concatenated Vector │        │
    │                          │  (TF-IDF + Dense)    │        │
    │                          └────────┬────────────┘        │
    │                                   ▼                     │
    │                          ┌─────────────────────┐        │
    │                          │  XGBoost Classifier  │        │
    │                          └─────────────────────┘        │
    └─────────────────────────────────────────────────────────┘

This hybrid approach captures both:
    - Lexical patterns (TF-IDF bigrams: clickbait phrases, sensational wording)
    - Semantic context (Transformer embeddings: meaning, tone, coherence)

Outputs (saved to models/):
    - tfidf_vectorizer.pkl          — Fitted TF-IDF vectorizer
    - xgboost_hybrid_model.pkl      — Trained XGBoost on concatenated features
    - best_model.pkl                — Alias for the best performing model
    - training_metrics.pkl          — Dict of all evaluation metrics for the UI

Usage:
    python src/train_model.py
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
from xgboost import XGBClassifier
from scipy.sparse import hstack, csr_matrix

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "clean_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Sentence-Transformers model — small, fast, and effective
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Training hyperparameters
TFIDF_MAX_FEATURES = 10_000
TFIDF_NGRAM_RANGE = (1, 2)
TEST_SIZE = 0.2
RANDOM_STATE = 42
BATCH_SIZE = 256


# ---------------------------------------------------------------------------
# Embedding Generation
# ---------------------------------------------------------------------------
def generate_embeddings(texts: list[str], model_name: str = EMBEDDING_MODEL_NAME,
                        batch_size: int = BATCH_SIZE) -> np.ndarray:
    """
    Generate dense sentence embeddings using SentenceTransformers.

    Args:
        texts: List of cleaned text strings.
        model_name: HuggingFace model identifier.
        batch_size: Encoding batch size (tune for GPU/CPU memory).

    Returns:
        NumPy array of shape (n_samples, embedding_dim).
    """
    from sentence_transformers import SentenceTransformer

    print(f"Loading SentenceTransformer model: {model_name}")
    st_model = SentenceTransformer(model_name)

    print(f"Encoding {len(texts):,} texts in batches of {batch_size}...")
    embeddings = st_model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    print(f"Embedding shape: {embeddings.shape}")
    return embeddings


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
def evaluate_model(model, X_test, y_test, model_name: str = "Model") -> dict:
    """
    Evaluate a trained classifier and return a metrics dictionary.

    Args:
        model: Fitted sklearn/xgboost estimator.
        X_test: Test feature matrix.
        y_test: True labels.
        model_name: Display name for logging.

    Returns:
        Dictionary containing accuracy, precision, recall, f1, roc_auc,
        and the confusion matrix.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model_name": model_name,
        "accuracy": round(accuracy_score(y_test, y_pred), 5),
        "precision": round(precision_score(y_test, y_pred), 5),
        "recall": round(recall_score(y_test, y_pred), 5),
        "f1_score": round(f1_score(y_test, y_pred), 5),
        "roc_auc": round(roc_auc_score(y_test, y_prob), 5),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    print(f"\n{'='*55}")
    print(f"  {model_name} — Evaluation Results")
    print(f"{'='*55}")
    print(f"  Accuracy   : {metrics['accuracy']:.4f}")
    print(f"  Precision  : {metrics['precision']:.4f}")
    print(f"  Recall     : {metrics['recall']:.4f}")
    print(f"  F1 Score   : {metrics['f1_score']:.4f}")
    print(f"  ROC-AUC    : {metrics['roc_auc']:.4f}")
    print(f"{'='*55}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Real", "Fake"]))

    return metrics


# ---------------------------------------------------------------------------
# Main Training Pipeline
# ---------------------------------------------------------------------------
def main():
    """
    Train the hybrid TF-IDF + Transformer + XGBoost pipeline.

    Steps:
        1. Load preprocessed data
        2. Generate TF-IDF features (lexical)
        3. Generate SentenceTransformer embeddings (semantic)
        4. Concatenate feature spaces
        5. Train XGBoost on the hybrid feature matrix
        6. Evaluate and persist all artifacts
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"ERROR: Data not found at {PROCESSED_DATA_PATH}")
        print("Please run `python src/preprocess.py` first.")
        sys.exit(1)

    # ── Step 1: Load Data ──
    print("\n[1/6] Loading preprocessed data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df = df.dropna(subset=["clean_text"])
    texts = df["clean_text"].tolist()
    labels = df["label"].values
    print(f"  → {len(texts):,} samples loaded")

    # ── Step 2: TF-IDF Features ──
    print(f"\n[2/6] Building TF-IDF features ({TFIDF_MAX_FEATURES:,} features, "
          f"ngrams={TFIDF_NGRAM_RANGE})...")
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        sublinear_tf=True,
    )
    X_tfidf = vectorizer.fit_transform(texts)
    print(f"  → TF-IDF matrix: {X_tfidf.shape}")

    # ── Step 3: Transformer Embeddings ──
    print(f"\n[3/6] Generating Transformer embeddings ({EMBEDDING_MODEL_NAME})...")
    t0 = time.time()
    X_dense = generate_embeddings(texts)
    embed_time = time.time() - t0
    print(f"  → Embedding time: {embed_time:.1f}s")

    # ── Step 4: Concatenate Feature Spaces ──
    print("\n[4/6] Concatenating feature spaces (TF-IDF + Dense)...")
    X_dense_sparse = csr_matrix(X_dense)
    X_hybrid = hstack([X_tfidf, X_dense_sparse])
    print(f"  → Hybrid feature matrix: {X_hybrid.shape}")

    # ── Step 5: Train/Test Split + Training ──
    print(f"\n[5/6] Splitting data ({1 - TEST_SIZE:.0%} train / {TEST_SIZE:.0%} test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_hybrid, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=labels
    )
    print(f"  → Train: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")

    print("\n  Training XGBoost Hybrid Classifier...")
    xgb_model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    t0 = time.time()
    xgb_model.fit(X_train, y_train)
    train_time = time.time() - t0
    print(f"  → Training time: {train_time:.1f}s")

    # ── Step 6: Evaluate + Save ──
    print("\n[6/6] Evaluating and saving artifacts...")
    metrics = evaluate_model(xgb_model, X_test, y_test, "XGBoost Hybrid (TF-IDF + Transformer)")
    metrics["train_time_seconds"] = round(train_time, 2)
    metrics["embedding_time_seconds"] = round(embed_time, 2)
    metrics["embedding_model"] = EMBEDDING_MODEL_NAME
    metrics["tfidf_features"] = TFIDF_MAX_FEATURES
    metrics["embedding_dim"] = X_dense.shape[1]
    metrics["total_features"] = X_hybrid.shape[1]
    metrics["train_samples"] = X_train.shape[0]
    metrics["test_samples"] = X_test.shape[0]

    # Save artifacts
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))
    joblib.dump(xgb_model, os.path.join(MODELS_DIR, "xgboost_hybrid_model.pkl"))
    joblib.dump(xgb_model, os.path.join(MODELS_DIR, "best_model.pkl"))
    joblib.dump(metrics, os.path.join(MODELS_DIR, "training_metrics.pkl"))

    print(f"\n{'='*55}")
    print("  All artifacts saved to models/")
    print(f"  → tfidf_vectorizer.pkl")
    print(f"  → xgboost_hybrid_model.pkl")
    print(f"  → best_model.pkl")
    print(f"  → training_metrics.pkl")
    print(f"{'='*55}")
    print("\nDone. Run `streamlit run src/app.py` to launch the UI.")


if __name__ == "__main__":
    main()
