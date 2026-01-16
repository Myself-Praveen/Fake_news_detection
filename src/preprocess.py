import pandas as pd
import re
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)

    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)



def load_and_label_data(fake_path, true_path):
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df['label'] = 1   
    true_df['label'] = 0 

    df = pd.concat([fake_df, true_df], axis=0)
    return df


def preprocess_dataset():
    df = load_and_label_data(
        "data/raw/Fake.csv",
        "data/raw/True.csv"
    )

    df['text'] = df['text'].astype(str)
    df['clean_text'] = df['text'].apply(clean_text)

    df = df[['clean_text', 'label']]
    df.to_csv("data/processed/clean_data.csv", index=False)


if __name__ == "__main__":
    preprocess_dataset()
