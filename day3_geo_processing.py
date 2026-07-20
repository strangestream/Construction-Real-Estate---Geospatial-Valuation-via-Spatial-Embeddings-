"""
day3_geo_processing.py
Day 3 - Project 3: Geospatial Valuation

Runs the Day 3 workflow:
  1. Load the cleaned dataset from Day 2
  2. Convert it into a GeoDataFrame (GeoPandas + Shapely)
  3. Compute a sample Haversine distance matrix as a sanity check
  4. Save the result as a plain CSV (geometry stored as WKT text) --
     this avoids needing GDAL/pyogrio/fiona system libraries, which
     are notoriously fiddly to install correctly on Windows.
  5. Append a summary to reports/week1_summary.md

Run from the repo root: python day3_geo_processing.py
"""

import os
import pandas as pd
from src.geo_utils import to_geodataframe, distance_matrix_sample

CLEANED_PATH = "data/processed/kc_house_cleaned.csv"
GEO_OUTPUT_PATH = "data/processed/kc_house_geo.csv"
REPORT_PATH = "reports/week1_summary.md"


def build_day3_report(gdf, sample_matrix) -> str:
    lines = []
    lines.append("## Day 3 - Geospatial Conversion & Haversine Distance\n")
    lines.append(f"- Converted **{len(gdf):,}** properties into a GeoDataFrame (CRS: {gdf.crs}).")
    lines.append(f"- Sample 5x5 Haversine distance matrix (km) computed to sanity-check distances.")
    lines.append(f"- Closest sample pair distance: **{sample_matrix.values[sample_matrix.values > 0].min():.2f} km**")
    lines.append(f"- Farthest sample pair distance: **{sample_matrix.values.max():.2f} km**")
    return "\n".join(lines) + "\n"


def main():
    df = pd.read_csv(CLEANED_PATH)
    print(f"[day3] Loaded {len(df):,} rows from {CLEANED_PATH}")

    gdf = to_geodataframe(df)

    sample_matrix = distance_matrix_sample(gdf, n=5)
    print("\n--- Sample 5x5 distance matrix (km) ---")
    print(sample_matrix.round(2))

    # Save as plain CSV with geometry as WKT text -- avoids needing
    # GDAL/pyogrio/fiona, which require extra system-level setup on Windows.
    os.makedirs(os.path.dirname(GEO_OUTPUT_PATH), exist_ok=True)
    gdf_out = gdf.copy()
    gdf_out["geometry"] = gdf_out["geometry"].astype(str)  # WKT-like text representation
    gdf_out.to_csv(GEO_OUTPUT_PATH, index=False)
    print(f"\n[day3] Saved GeoDataFrame (as CSV with WKT geometry) to {GEO_OUTPUT_PATH}")

    report_text = build_day3_report(gdf, sample_matrix)
    with open(REPORT_PATH, "a") as f:
        f.write("\n" + report_text)
    print(f"[day3] Report appended to {REPORT_PATH}")


if __name__ == "__main__":
    main()
