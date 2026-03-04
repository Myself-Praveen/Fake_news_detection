import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "clean_data.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def evaluate(model, X_test, y_test, name="Model"):
    y_pred = model.predict(X_test)
    print(f"\n--- {name} ---")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

def main():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Data not found at {PROCESSED_DATA_PATH}. Please run src/preprocess.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df = df.dropna(subset=['clean_text'])

    print("Vectorizing text (TF-IDF with unigrams and bigrams)...")
    # Increased max_features and added ngrams for better context catching
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label']

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Naive Bayes": MultinomialNB(),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }

    best_model_name = None
    best_accuracy = 0
    best_model = None

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        evaluate(model, X_test, y_test, name)
        
        # Save each model just in case
        joblib.dump(model, os.path.join(MODELS_DIR, f"{name.lower().replace(' ', '_')}_model.pkl"))
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model = model

    print(f"\nBest Model: {best_model_name} with Accuracy {best_accuracy:.4f}")

    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))
    joblib.dump(best_model, os.path.join(MODELS_DIR, "best_model.pkl"))
    print("Models and vectorizer saved successfully in 'models/' folder.")

if __name__ == "__main__":
    main()
