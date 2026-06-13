"""
utils.py — Core NLP utilities for the News Verifier Pro pipeline.

Provides text cleaning, entity extraction, and NLTK bootstrapping
used by both the training pipeline and the Streamlit inference app.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# ---------------------------------------------------------------------------
# NLTK Bootstrap — download required corpora silently on first run
# ---------------------------------------------------------------------------
def setup_nltk():
    """Download required NLTK data packages, forcing re-download if corrupted."""
    packages = [
        "stopwords",
        "punkt",
        "punkt_tab",
        "wordnet",
        "averaged_perceptron_tagger",
        "maxent_ne_chunker",
        "words",
    ]
    for name in packages:
        nltk.download(name, quiet=True)


setup_nltk()

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# ---------------------------------------------------------------------------
# Text Cleaning
# ---------------------------------------------------------------------------
def clean_text(text: str) -> str:
    """
    Clean raw text for NLP feature extraction.

    Pipeline:
        1. Lowercase
        2. Strip URLs
        3. Strip special characters / digits
        4. Tokenize
        5. Remove stopwords
        6. Lemmatize

    Args:
        text: Raw article or headline string.

    Returns:
        Cleaned, whitespace-joined token string.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)

    tokens = nltk.word_tokenize(text)
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words and len(word) > 1
    ]
    return " ".join(tokens)


# ---------------------------------------------------------------------------
# Entity Extraction (for Live Fact-Check)
# ---------------------------------------------------------------------------
def extract_entities(text: str) -> list[str]:
    """
    Extract named entities from raw text using NLTK chunking.

    Falls back to a simple capitalized-word heuristic when
    the NE chunker yields no results.

    Args:
        text: Raw (uncleaned) article text.

    Returns:
        List of unique entity strings, capped at 8.
    """
    entities = []
    try:
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        chunks = nltk.ne_chunk(tagged)
        for subtree in chunks:
            if hasattr(subtree, "label"):
                entity = " ".join(word for word, tag in subtree.leaves())
                if entity not in entities:
                    entities.append(entity)
    except Exception:
        pass

    # Fallback: grab capitalized multi-word phrases
    if len(entities) < 3:
        caps = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", text)
        for c in caps:
            if c not in entities:
                entities.append(c)

    return entities[:8]
