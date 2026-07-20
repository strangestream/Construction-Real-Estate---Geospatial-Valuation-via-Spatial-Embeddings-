"""
day5_week1_wrapup.py
Day 5 - Project 3: Geospatial Valuation

Runs the Day 5 / Week 1 wrap-up workflow:
  1. Load the cleaned + geo-processed dataset
  2. Compute zipcode-level spatial pricing stats (median price,
     median price/sqft) to identify high/low-value clusters
  3. Finalize reports/week1_summary.md with a "Week 1 Wrap-Up" section
     summarizing spatial trends observed, ready to hand off to Week 2

Run from the repo root: python day5_week1_wrapup.py
"""

import pandas as pd

CLEANED_PATH = "data/processed/kc_house_cleaned.csv"
REPORT_PATH = "reports/week1_summary.md"


def zipcode_spatial_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate price and price-per-sqft by zipcode to spot high/low
    value clusters -- a simple, interpretable proxy for the spatial
    trends the Week 3-4 graph/GNN model will later capture explicitly.
    """
    df = df.copy()
    df = df[df["sqft_living"] > 0]
    df["price_per_sqft"] = df["price"] / df["sqft_living"]

    summary = (
        df.groupby("zipcode")
        .agg(
            median_price=("price", "median"),
            median_price_per_sqft=("price_per_sqft", "median"),
            n_sales=("price", "count"),
        )
        .sort_values("median_price_per_sqft", ascending=False)
    )
    return summary


def build_day5_report(df: pd.DataFrame, zip_summary: pd.DataFrame) -> str:
    top_zip = zip_summary.index[0]
    bottom_zip = zip_summary.index[-1]

    lines = []
    lines.append("## Day 5 - Week 1 Wrap-Up: Spatial Pricing Trends\n")
    lines.append(f"- Analyzed **{df['zipcode'].nunique()}** distinct zipcodes across **{len(df):,}** properties.")
    lines.append(
        f"- Highest median price/sqft zipcode: **{top_zip}** "
        f"(${zip_summary.loc[top_zip, 'median_price_per_sqft']:,.0f}/sqft)"
    )
    lines.append(
        f"- Lowest median price/sqft zipcode: **{bottom_zip}** "
        f"(${zip_summary.loc[bottom_zip, 'median_price_per_sqft']:,.0f}/sqft)"
    )
    lines.append(
        "- This zipcode-level gap is the first quantitative evidence of location-driven "
        "price variation that flat tabular features (sqft, bedrooms) don't explain on "
        "their own -- motivating the spatial graph/embedding work starting Week 3."
    )
    lines.append("\n### Week 1 Summary")
    lines.append("Week 1 delivered: a cleaned, outlier-normalized King County housing dataset, "
                  "a GeoDataFrame with Haversine distance capability, and interactive heatmaps "
                  "confirming meaningful spatial price variation. Ready to proceed to Week 2 "
                  "(feature engineering + XGBoost baseline).")
    return "\n".join(lines) + "\n"


def main():
    df = pd.read_csv(CLEANED_PATH)
    print(f"[day5] Loaded {len(df):,} rows from {CLEANED_PATH}")

    zip_summary = zipcode_spatial_summary(df)
    print("\n--- Zipcode spatial summary (top 5 by price/sqft) ---")
    print(zip_summary.head())

    report_text = build_day5_report(df, zip_summary)
    with open(REPORT_PATH, "a") as f:
        f.write("\n" + report_text)
    print(f"\n[day5] Week 1 wrap-up appended to {REPORT_PATH}")


if __name__ == "__main__":
    main()
