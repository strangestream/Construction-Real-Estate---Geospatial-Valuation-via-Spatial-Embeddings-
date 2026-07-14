"""
day1_eda.py
Day 1 - Project 3: Geospatial Valuation

Runs the Day 1 workflow: load -> validate -> summarize -> append report.
Run from the repo root: python day1_eda.py
"""

import pandas as pd
from src.data_loader import load_raw_data, validate_columns, quick_summary

RAW_PATH = "data/raw/kc_house_data.csv"
REPORT_PATH = "reports/week1_summary.md"


def build_day1_report(df: pd.DataFrame) -> str:
    lines = []
    lines.append("## Day 1 - Data Acquisition & Initial Inspection\n")
    lines.append(f"- Rows: **{len(df):,}**, Columns: **{len(df.columns)}**")
    lines.append(f"- Duplicate rows: **{df.duplicated().sum():,}**")

    null_cols = df.isnull().sum()
    null_cols = null_cols[null_cols > 0]
    if len(null_cols) > 0:
        lines.append(f"- Columns with missing values: {list(null_cols.index)}")
    else:
        lines.append("- No missing values detected.")

    if "price" in df.columns:
        lines.append(
            f"- Price range: **${df['price'].min():,.0f}** to **${df['price'].max():,.0f}**, "
            f"median **${df['price'].median():,.0f}**"
        )

    if "lat" in df.columns and "long" in df.columns:
        lines.append(
            f"- Coordinate bounds: lat [{df['lat'].min():.4f}, {df['lat'].max():.4f}], "
            f"long [{df['long'].min():.4f}, {df['long'].max():.4f}]"
        )

    return "\n".join(lines) + "\n"


def main():
    df = load_raw_data(RAW_PATH)
    validate_columns(df)
    quick_summary(df)

    report_text = build_day1_report(df)

    with open(REPORT_PATH, "a") as f:
        f.write("\n" + report_text)

    print(f"\n[day1_eda] Report appended to {REPORT_PATH}")


if __name__ == "__main__":
    main()
