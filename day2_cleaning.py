"""
day2_cleaning.py
Day 2 - Project 3: Geospatial Valuation

Runs the Day 2 workflow:
  1. Load raw data
  2. Clean it (duplicates, missing values, dtypes, coordinate validation)
  3. Normalize the 5 most extreme price outliers
  4. Save the cleaned dataset to data/processed/kc_house_cleaned.csv
  5. Append a summary to reports/week1_summary.md

Run from the repo root: python day2_cleaning.py
"""

import os
from src.data_loader import load_raw_data
from src.cleaning_utils import clean_dataset

RAW_PATH = "data/raw/kc_house_data.csv"
PROCESSED_PATH = "data/processed/kc_house_cleaned.csv"
REPORT_PATH = "reports/week1_summary.md"


def build_day2_report(df_before, df_after) -> str:
    lines = []
    lines.append("## Day 2 - Data Cleaning & Outlier Normalization\n")
    lines.append(f"- Rows before cleaning: **{len(df_before):,}**")
    lines.append(f"- Rows after cleaning: **{len(df_after):,}**")
    lines.append("- 5 most extreme price outliers identified and capped at the 99th percentile.")
    if "price" in df_after.columns:
        lines.append(
            f"- Post-cleaning price range: **${df_after['price'].min():,.0f}** to "
            f"**${df_after['price'].max():,.0f}**"
        )
    return "\n".join(lines) + "\n"


def main():
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    df = load_raw_data(RAW_PATH)
    df_clean = clean_dataset(df, n_outliers=5)

    df_clean.to_csv(PROCESSED_PATH, index=False)
    print(f"[day2_cleaning] Saved cleaned dataset to {PROCESSED_PATH}")

    report_text = build_day2_report(df, df_clean)
    with open(REPORT_PATH, "a") as f:
        f.write("\n" + report_text)

    print(f"[day2_cleaning] Report appended to {REPORT_PATH}")


if __name__ == "__main__":
    main()
