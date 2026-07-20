"""
day4_maps.py
Day 4 - Project 3: Geospatial Valuation

Runs the Day 4 workflow:
  1. Load the cleaned dataset
  2. Build a price heatmap and a price-per-sqft heatmap (Folium)
  3. Save both as interactive HTML files in maps/
  4. Append a summary to reports/week1_summary.md

Run from the repo root: python day4_maps.py
"""

import pandas as pd
from src.map_utils import build_price_heatmap, build_price_per_sqft_heatmap

CLEANED_PATH = "data/processed/kc_house_cleaned.csv"
PRICE_MAP_PATH = "maps/price_heatmap.html"
PSF_MAP_PATH = "maps/price_per_sqft_heatmap.html"
REPORT_PATH = "reports/week1_summary.md"


def build_day4_report(df: pd.DataFrame) -> str:
    lines = []
    lines.append("## Day 4 - Interactive Spatial Heatmaps\n")
    lines.append(f"- Built a raw price heatmap: `{PRICE_MAP_PATH}`")
    lines.append(f"- Built a price-per-sqft heatmap (normalizes for house size): `{PSF_MAP_PATH}`")
    lines.append(f"- Mapped **{len(df):,}** properties across King County.")
    lines.append("- Next: visually inspect both maps for waterfront premiums, urban-core gradients, and zipcode-level clustering.")
    return "\n".join(lines) + "\n"


def main():
    df = pd.read_csv(CLEANED_PATH)
    print(f"[day4] Loaded {len(df):,} rows from {CLEANED_PATH}")

    build_price_heatmap(df, PRICE_MAP_PATH)
    build_price_per_sqft_heatmap(df, PSF_MAP_PATH)

    report_text = build_day4_report(df)
    with open(REPORT_PATH, "a") as f:
        f.write("\n" + report_text)
    print(f"[day4] Report appended to {REPORT_PATH}")


if __name__ == "__main__":
    main()
