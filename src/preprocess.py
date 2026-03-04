import os
import pandas as pd
from utils import clean_text

def load_and_label_data(fake_path, true_path):
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df['label'] = 1   
    true_df['label'] = 0 

    df = pd.concat([fake_df, true_df], axis=0)
    return df

def preprocess_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fake_path = os.path.join(base_dir, "data", "raw", "Fake.csv")
    true_path = os.path.join(base_dir, "data", "raw", "True.csv")
    
    df = load_and_label_data(fake_path, true_path)

    df['text'] = df['text'].astype(str)
    print("Cleaning text data... This may take a moment.")
    df['clean_text'] = df['text'].apply(clean_text)

    df = df[['clean_text', 'label']]
    
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    out_path = os.path.join(processed_dir, "clean_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Data successfully cleaned and saved to {out_path}")

if __name__ == "__main__":
    preprocess_dataset()
