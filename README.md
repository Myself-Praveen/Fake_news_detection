# Fake News Detection

A machine learning project that detects whether a news article is **True** or **Fake** using NLP techniques. Built with **TF-IDF vectorization** and **Logistic Regression & Naive Bayes** classifiers. Includes an interactive **Streamlit UI** for live predictions.

## Features
- Cleans and preprocesses text: lowercasing, removing URLs/special characters, stopwords removal, lemmatization.
- Converts text to numeric features using TF-IDF.
- Trains Logistic Regression and Multinomial Naive Bayes models.
- Evaluates models with accuracy, confusion matrix, and classification report.
- Streamlit app for live predictions.

## Folder Structure

fake-news-detection/
│
├── data/
│ ├── raw/ # Original CSV datasets
│ └── processed/ # Cleaned dataset
│
├── models/ # Trained models & vectorizer
│ ├── logistic_model.pkl
│ ├── naive_bayes_model.pkl
│ └── tfidf_vectorizer.pkl
│
├── src/
│ ├── preprocess.py
│ ├── train_model.py
│ └── app.py # Streamlit UI
│
├── assets/ # Screenshots or other media
│ └── streamlit_ui.png
│
├── requirements.txt
└── README.md

yaml
Copy code

## Screenshot

![Fake News Detection UI](assets/streamlit_ui.png)

---

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd fake-news-detection
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
# Git Bash
source venv/Scripts/activate
# PowerShell
.\venv\Scripts\Activate.ps1
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Preprocess & Train Models
bash
Copy code
python src/preprocess.py
python src/train_model.py
Launch Streamlit UI
bash
Copy code
streamlit run src/app.py
Enter a news article in the textbox.

Click Predict to see if it is True or Fake, along with probabilities.

Model Performance
Logistic Regression

Accuracy: 98.7%

High precision and recall for both classes

Naive Bayes

Accuracy: 93.1%

Slightly lower but still effective

Technologies
Python 3

pandas, numpy, scikit-learn

nltk for text preprocessing

Streamlit for UI

Joblib for saving/loading models

