"""
preprocess.py — Data preprocessing pipeline for News Verifier Pro.

Loads the raw ISOT Fake News dataset (Fake.csv + True.csv), applies the
NLP cleaning pipeline from utils.py, and persists the processed data
to data/processed/clean_data.csv for downstream model training.
"""

import os
import pandas as pd
from utils import clean_text


def load_and_label_data(fake_path: str, true_path: str) -> pd.DataFrame:
    """
    Load and label the raw ISOT dataset CSVs.

    Args:
        fake_path: Absolute path to Fake.csv.
        true_path: Absolute path to True.csv.

    Returns:
        Combined DataFrame with a 'label' column (1 = Fake, 0 = True).
    """
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df["label"] = 1
    true_df["label"] = 0

    df = pd.concat([fake_df, true_df], axis=0).reset_index(drop=True)
    return df


def preprocess_dataset():
    """
    End-to-end preprocessing: load → clean → save.

    Reads raw CSVs from data/raw/, applies text cleaning, and writes
    the result to data/processed/clean_data.csv.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fake_path = os.path.join(base_dir, "data", "raw", "Fake.csv")
    true_path = os.path.join(base_dir, "data", "raw", "True.csv")

    print("Loading raw dataset...")
    df = load_and_label_data(fake_path, true_path)

    df["text"] = df["text"].astype(str)
    print(f"Cleaning {len(df):,} articles... This may take a few minutes.")
    df["clean_text"] = df["text"].apply(clean_text)

    df = df[["clean_text", "label"]]

    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    out_path = os.path.join(processed_dir, "clean_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Preprocessing complete → {out_path}  ({len(df):,} rows)")


if __name__ == "__main__":
    preprocess_dataset()
