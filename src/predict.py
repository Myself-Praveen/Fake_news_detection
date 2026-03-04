import os
import joblib
from utils import clean_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pkl")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(MODELS_DIR, "logistic_model.pkl")

try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print("Models not found. Please run src/train_model.py first.")
    exit(1)

def predict(text, model=model):
    clean = clean_text(text)
    vec = vectorizer.transform([clean])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    return pred, prob

if __name__ == "__main__":
    print("--- Fake News Detection ---")
    print("Type 'exit' to quit.")
    while True:
        text = input("\nEnter news text: ")
        if text.lower() == "exit":
            break
        prediction, probabilities = predict(text)
        label = "Fake" if prediction == 1 else "True"
        print(f"Prediction: {label}")
        print(f"Probabilities: True={probabilities[0]:.3f}, Fake={probabilities[1]:.3f}")
