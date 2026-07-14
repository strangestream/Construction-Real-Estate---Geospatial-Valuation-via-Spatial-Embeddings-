"""
cleaning_utils.py
Day 2 - Project 3: Geospatial Valuation

Purpose:
    Clean the raw housing data:
      - drop exact duplicate rows
      - handle missing values
      - fix data types
      - validate lat/long are within King County's real bounds
      - identify and normalize the 5 most extreme price outliers

Usage:
    from src.cleaning_utils import clean_dataset

    df_clean = clean_dataset(df)
"""

import pandas as pd
import numpy as np

# Rough King County, WA bounding box - used to catch corrupted coordinates.
LAT_BOUNDS = (47.1, 47.85)
LONG_BOUNDS = (-122.6, -121.0)


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    print(f"[cleaning_utils] Removed {removed} duplicate row(s).")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Numeric columns: fill with the column median (keeps distribution stable).
    Non-numeric columns: fill with the column mode.
    """
    df = df.copy()
    for col in df.columns:
        n_missing = df[col].isnull().sum()
        if n_missing == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            fill_value = df[col].median()
        else:
            mode_vals = df[col].mode()
            fill_value = mode_vals.iloc[0] if not mode_vals.empty else ""

        df[col] = df[col].fillna(fill_value)
        print(f"[cleaning_utils] Filled {n_missing} missing value(s) in '{col}' with {fill_value}")

    return df


def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "zipcode" in df.columns:
        df["zipcode"] = df["zipcode"].astype(str)
    for col in ["price", "sqft_living", "sqft_lot", "lat", "long", "bathrooms", "floors"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def validate_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows whose lat/long fall outside King County's real bounds."""
    if "lat" not in df.columns or "long" not in df.columns:
        return df

    before = len(df)
    mask = (
        df["lat"].between(*LAT_BOUNDS)
        & df["long"].between(*LONG_BOUNDS)
    )
    df = df[mask].copy()
    removed = before - len(df)
    if removed > 0:
        print(f"[cleaning_utils] Removed {removed} row(s) with out-of-bounds coordinates.")
    return df


def normalize_price_outliers(df: pd.DataFrame, n_outliers: int = 5) -> pd.DataFrame:
    """
    Identify the N most extreme price outliers (by absolute distance from
    the median in z-score terms) and cap them at the 99th percentile value
    instead of dropping them, to avoid losing potentially valid high-end
    sales while removing their distortive effect on model training.
    """
    df = df.copy()
    if "price" not in df.columns:
        return df

    mean_price = df["price"].mean()
    std_price = df["price"].std()
    df["_price_zscore"] = (df["price"] - mean_price) / std_price

    outlier_idx = df["_price_zscore"].abs().sort_values(ascending=False).head(n_outliers).index
    cap_value = df["price"].quantile(0.99)

    print(f"[cleaning_utils] Identified {len(outlier_idx)} extreme price outlier(s):")
    print(df.loc[outlier_idx, ["price"]] if "price" in df.columns else outlier_idx)

    df.loc[outlier_idx, "price"] = df.loc[outlier_idx, "price"].clip(upper=cap_value)
    df = df.drop(columns=["_price_zscore"])

    print(f"[cleaning_utils] Capped {len(outlier_idx)} outlier price(s) at 99th percentile (${cap_value:,.0f}).")
    return df


def clean_dataset(df: pd.DataFrame, n_outliers: int = 5) -> pd.DataFrame:
    """Run the full Day 2 cleaning pipeline in order."""
    df = drop_duplicates(df)
    df = fix_dtypes(df)
    df = handle_missing_values(df)
    df = validate_coordinates(df)
    df = normalize_price_outliers(df, n_outliers=n_outliers)
    print(f"[cleaning_utils] Final cleaned shape: {df.shape}")
    return df


if __name__ == "__main__":
    from data_loader import load_raw_data
    df = load_raw_data()
    df_clean = clean_dataset(df)
    df_clean.to_csv("data/processed/kc_house_cleaned.csv", index=False)
    print("[cleaning_utils] Saved cleaned dataset to data/processed/kc_house_cleaned.csv")
