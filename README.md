# 🛡️ News Verifier Pro (Fake News Detection V2)

**News Verifier Pro** is an advanced, dual-engine machine learning application designed to automatically identify and flag fabricated news articles, headlines, and social media claims.

We have recently completely overhauled this project to feature an **XGBoost Machine Learning Engine** alongside **Live Web Fact-Checking via NewsAPI**, all wrapped in a stunning, high-performance **3D WebGL UI**.

---

## 🌟 Overview

Misinformation spreads faster than ever. This tool provides a highly accurate, two-step verification process:
1. **Linguistic Analysis (AI)**: An NLP pipeline uses TF-IDF and an XGBoost classifier to detect language patterns typical of fabricated content.
2. **Web Corroboration (Live Search)**: The system extracts key entities and queries the NewsAPI to cross-reference the claim against established, verified news publishers in real-time.

---

## 🚀 Key Features

* **Advanced ML Engine**: Upgraded from Logistic Regression to **XGBoost** for state-of-the-art classification accuracy (99.8% on validation data).
* **Live Source Checking**: Automatically queries **NewsAPI** to find real-world corroborating coverage for the submitted claim.
* **Premium User Interface**: A meticulously designed **Streamlit** dashboard featuring:
  * Interactive **3D WebGL Particle Background** (Vanta.js).
  * Modern **Glassmorphism** aesthetics with translucent frosted-glass cards.
  * Clean, minimal typography utilizing the modern **Outfit** font.
* **Robust NLP Pipeline**: Custom text cleaning (stopword removal, lemmatization, special char stripping) paired with Bigram TF-IDF vectorization.

---

## 🛠 Technologies & Stack

* **Language**: Python 3
* **Machine Learning**: `xgboost`, `scikit-learn`, `pandas`, `numpy`
* **NLP**: `nltk` (Tokenization, Lemmatization)
* **Frontend/UI**: `streamlit`, Custom CSS, `vanta.js` (Three.js WebGL)
* **APIs**: `requests`, [NewsAPI.org](https://newsapi.org/)

---

## 💻 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Myself-Praveen/Fake_news_detection.git
cd Fake_news_detection
```

### 2. Set up a Virtual Environment & Install Dependencies

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Generate the ML Models 
To train the Logistic Regression, Naive Bayes, and XGBoost models on your dataset and generate the required `.pkl` model files:
```bash
python src/train_model.py
```
*(Note: Ensure you have your raw dataset files inside the `data/raw/` directory before training.)*

### 4. Boot up the Streamlit UI

```bash
streamlit run src/app.py
```
The application will automatically open in your browser at `http://localhost:8501`.

---

## ☁️ Deployment

This project is fully ready to be deployed on **Streamlit Community Cloud**.
1. Push your code to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your repository, point the main file path to `src/app.py`, and click **Deploy**.

---

## 🤝 How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/update`)
3. Commit your changes (`git commit -m 'Added cool features'`)
4. Push to the branch (`git push origin feature/update`)
5. Open a Pull Request

---

## 🎨 Author

**Praveen Mishra**  
GitHub: [Myself-Praveen](https://github.com/Myself-Praveen)
