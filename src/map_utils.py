"""
map_utils.py
Day 4 - Project 3: Geospatial Valuation

Purpose:
    Build interactive Folium maps to visually inspect spatial pricing
    trends: a raw price heatmap and a price-per-sqft heatmap (which
    normalizes for house size to reveal true location premium).

Usage:
    from src.map_utils import build_price_heatmap, build_price_per_sqft_heatmap

    build_price_heatmap(df, "maps/price_heatmap.html")
    build_price_per_sqft_heatmap(df, "maps/price_per_sqft_heatmap.html")
"""

import os
import pandas as pd
import folium
from folium.plugins import HeatMap

KING_COUNTY_CENTER = [47.45, -121.9]


def build_price_heatmap(df: pd.DataFrame, output_path: str, zoom_start: int = 9) -> folium.Map:
    """
    Build a Folium heatmap weighted by raw sale price.
    """
    required = {"lat", "long", "price"}
    if not required.issubset(df.columns):
        raise ValueError(f"[map_utils] DataFrame must contain columns: {required}")

    m = folium.Map(location=KING_COUNTY_CENTER, zoom_start=zoom_start, tiles="cartodbpositron")

    heat_data = df[["lat", "long", "price"]].dropna().values.tolist()
    HeatMap(heat_data, radius=12, blur=15, max_zoom=13).add_to(m)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    print(f"[map_utils] Saved price heatmap to {output_path}")
    return m


def build_price_per_sqft_heatmap(df: pd.DataFrame, output_path: str, zoom_start: int = 9) -> folium.Map:
    """
    Build a Folium heatmap weighted by price-per-sqft, which normalizes
    for house size and better reveals the pure "location premium".
    """
    required = {"lat", "long", "price", "sqft_living"}
    if not required.issubset(df.columns):
        raise ValueError(f"[map_utils] DataFrame must contain columns: {required}")

    df = df.copy()
    df = df[df["sqft_living"] > 0]
    df["price_per_sqft"] = df["price"] / df["sqft_living"]

    m = folium.Map(location=KING_COUNTY_CENTER, zoom_start=zoom_start, tiles="cartodbpositron")

    heat_data = df[["lat", "long", "price_per_sqft"]].dropna().values.tolist()
    HeatMap(heat_data, radius=12, blur=15, max_zoom=13).add_to(m)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    print(f"[map_utils] Saved price-per-sqft heatmap to {output_path}")
    return m


def add_sample_markers(m: folium.Map, df: pd.DataFrame, n: int = 20) -> folium.Map:
    """
    Add a small number of clickable markers with price popups, so the
    map isn't purely a heatmap and individual listings can be inspected.
    """
    sample = df.dropna(subset=["lat", "long", "price"]).sample(min(n, len(df)), random_state=42)
    for _, row in sample.iterrows():
        popup_text = f"${row['price']:,.0f}"
        if "bedrooms" in row and "bathrooms" in row:
            popup_text += f" | {row['bedrooms']} bd / {row['bathrooms']} ba"
        folium.CircleMarker(
            location=[row["lat"], row["long"]],
            radius=4,
            popup=popup_text,
            color="#2c7fb8",
            fill=True,
            fill_opacity=0.7,
        ).add_to(m)
    return m


if __name__ == "__main__":
    df = pd.read_csv("data/processed/kc_house_cleaned.csv")
    print(f"[map_utils] Loaded {len(df):,} rows for mapping")

    m1 = build_price_heatmap(df, "maps/price_heatmap.html")
    m2 = build_price_per_sqft_heatmap(df, "maps/price_per_sqft_heatmap.html")
