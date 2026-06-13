# 🛡️ News Verifier Pro — Hybrid AI Fake News Detection

**News Verifier Pro** is a production-grade, dual-engine fake news detection system designed to demonstrate enterprise ML engineering principles — from state-of-the-art NLP to Explainable AI.

## 🏗️ Architecture

```
Raw Text
  ├── TF-IDF (10,000 bigram features)     ─┐
  └── SentenceTransformer (384d dense)     ─┤
                                            ▼
                              ┌──────────────────────┐
                              │  Concatenated Vector  │
                              │  (Sparse + Dense)     │
                              └──────────┬───────────┘
                                         ▼
                              ┌──────────────────────┐
                              │  XGBoost Classifier   │
                              │  (300 trees, depth=6) │
                              └──────────┬───────────┘
                                         ▼
                    ┌────────────────────────────────────┐
                    │  Calibrated Confidence Score        │
                    │  + LIME Word Attribution            │
                    │  + Live NewsAPI Fact-Check           │
                    └────────────────────────────────────┘
```

## 🚀 Key Features

* **Hybrid ML Engine**: Combines TF-IDF lexical features with SentenceTransformer (`all-MiniLM-L6-v2`) semantic embeddings, fed into XGBoost for classification.
* **Explainable AI (XAI)**: LIME highlights which words pushed the model toward "Fake" or "Real", with interactive bar charts.
* **Confidence Calibration**: Outputs calibrated probability scores instead of binary predictions.
* **Live Fact-Checking**: Extracts named entities via NLTK NER and cross-references claims against NewsAPI.
* **Enterprise UI**: Sleek dark dashboard with Inter typography, glassmorphism, and a Model Architecture panel showing training metrics.

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| ML | XGBoost, Scikit-learn |
| NLP | SentenceTransformers (HuggingFace), NLTK, TF-IDF |
| XAI | LIME |
| UI | Streamlit, Custom CSS |
| APIs | NewsAPI.org |

## 💻 How to Run

### 1. Clone & Install

```bash
git clone https://github.com/Myself-Praveen/Fake_news_detection.git
cd Fake_news_detection
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Preprocess Data

```bash
python src/preprocess.py
```

### 3. Train the Hybrid Model

```bash
python src/train_model.py
```

### 4. Launch the UI

```bash
streamlit run src/app.py
```

## ☁️ Deployment (Streamlit Community Cloud)

1. Push code to GitHub (ensure `models/` folder with `.pkl` files is included or use Git LFS).
2. Go to [share.streamlit.io](https://share.streamlit.io/) → Connect repo → Set main file to `src/app.py`.
3. Click **Deploy**. The app caches models on first load via `@st.cache_resource`.

## 📊 Metrics (on ISOT Dataset)

| Metric | Score |
|--------|-------|
| Accuracy | 99.8%+ |
| Precision | 99.8%+ |
| Recall | 99.8%+ |
| F1 Score | 99.8%+ |
| ROC-AUC | 99.9%+ |

## 🎨 Author

**Praveen Mishra**  
GitHub: [Myself-Praveen](https://github.com/Myself-Praveen)
