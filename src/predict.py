import os
import joblib
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
LR_MODEL_PATH = os.path.join(MODELS_DIR, "logistic_model.pkl")
NB_MODEL_PATH = os.path.join(MODELS_DIR, "naive_bayes_model.pkl")

vectorizer = joblib.load(VECTORIZER_PATH)
lr_model = joblib.load(LR_MODEL_PATH)
nb_model = joblib.load(NB_MODEL_PATH)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

def predict(text, model=lr_model):
    clean = clean_text(text)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    return pred, prob

if __name__ == "__main__":
    print("Fake News Detection")
    print("Type 'exit' to quit.")
    while True:
        text = input("\nEnter news text: ")
        if text.lower() == "exit":
            break
        prediction, probabilities = predict(text)
        label = "Fake" if prediction == 1 else "True"
        print(f"Prediction: {label}")
        print(f"Probabilities: True={probabilities[0]:.3f}, Fake={probabilities[1]:.3f}")
