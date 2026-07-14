"""
data_loader.py
Day 1 - Project 3: Geospatial Valuation

Loads the King County housing dataset. If it isn't found locally,
downloads it automatically from a public mirror (no login needed).
"""

import pandas as pd
import os
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

DOWNLOAD_URL = "https://geodacenter.github.io/data-and-lab//data/kingcounty.zip"

REQUIRED_COLUMNS = [
    "id", "date", "price", "bedrooms", "bathrooms", "sqft_living",
    "sqft_lot", "floors", "waterfront", "condition", "grade",
    "yr_built", "yr_renovated", "zipcode", "lat", "long",
]


def download_dataset(filepath: str) -> None:
    print(f"[data_loader] '{filepath}' not found locally. Downloading from mirror...")
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with urlopen(DOWNLOAD_URL) as resp:
        with ZipFile(BytesIO(resp.read())) as z:
            with z.open("kingcounty/kc_house_data.csv") as source:
                with open(filepath, "wb") as target:
                    target.write(source.read())

    print(f"[data_loader] Download complete. Saved to '{filepath}'.")


def load_raw_data(filepath: str = "data/raw/kc_house_data.csv") -> pd.DataFrame:
    if not os.path.exists(filepath):
        download_dataset(filepath)

    df = pd.read_csv(filepath)
    print(f"[data_loader] Loaded {len(df):,} rows and {len(df.columns)} columns from {filepath}")
    return df


def validate_columns(df: pd.DataFrame, required_columns=None) -> None:
    required_columns = required_columns or REQUIRED_COLUMNS
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"[data_loader] Missing required columns: {missing}")
    print("[data_loader] All required columns present.")


def quick_summary(df: pd.DataFrame) -> None:
    print("\n--- Shape ---")
    print(df.shape)

    print("\n--- Dtypes ---")
    print(df.dtypes)

    print("\n--- Null counts (columns with any nulls) ---")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "No nulls found.")

    print("\n--- Duplicate rows ---")
    print(f"{df.duplicated().sum():,} duplicate rows")

    if "price" in df.columns:
        print("\n--- Price stats ---")
        print(df["price"].describe())

    if "lat" in df.columns and "long" in df.columns:
        print("\n--- Coordinate bounds ---")
        print(f"lat:  min={df['lat'].min()}, max={df['lat'].max()}")
        print(f"long: min={df['long'].min()}, max={df['long'].max()}")


if __name__ == "__main__":
    df = load_raw_data()
    validate_columns(df)
    quick_summary(df)
