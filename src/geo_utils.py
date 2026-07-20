"""
geo_utils.py
Day 3 - Project 3: Geospatial Valuation

Purpose:
    Convert the cleaned housing DataFrame into a GeoPandas GeoDataFrame
    using Shapely Point geometries, and provide a Haversine distance
    function for computing real-world distances between properties.

Usage:
    from src.geo_utils import to_geodataframe, haversine_distance

    gdf = to_geodataframe(df)
    dist_km = haversine_distance(lat1, lon1, lat2, lon2)
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

EARTH_RADIUS_KM = 6371.0


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """
    Compute the great-circle (Haversine) distance in kilometers between
    two lat/long points. Works with scalars or numpy arrays.
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return EARTH_RADIUS_KM * c


def to_geodataframe(df: pd.DataFrame, lat_col: str = "lat", lon_col: str = "long") -> gpd.GeoDataFrame:
    """
    Convert a pandas DataFrame with lat/long columns into a GeoDataFrame
    with Shapely Point geometries, using WGS84 (EPSG:4326) as the CRS.
    """
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError(f"[geo_utils] DataFrame must contain '{lat_col}' and '{lon_col}' columns.")

    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

    print(f"[geo_utils] Converted DataFrame to GeoDataFrame with {len(gdf):,} points (CRS: {gdf.crs}).")
    return gdf


def distance_matrix_sample(gdf: gpd.GeoDataFrame, n: int = 5) -> pd.DataFrame:
    """
    Quick sanity check: compute a small Haversine distance matrix
    (in km) between the first n properties, so we can visually
    confirm distances look reasonable.
    """
    sample = gdf.head(n)
    lats = sample["lat"].values
    lons = sample["long"].values

    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i, j] = haversine_distance(lats[i], lons[i], lats[j], lons[j])

    ids = sample["id"].values if "id" in sample.columns else range(n)
    return pd.DataFrame(matrix, index=ids, columns=ids)


if __name__ == "__main__":
    df = pd.read_csv("data/processed/kc_house_cleaned.csv")
    print(f"[geo_utils] Loaded {len(df):,} rows from data/processed/kc_house_cleaned.csv")
    gdf = to_geodataframe(df)

    print("\n--- GeoDataFrame head ---")
    print(gdf[["id", "lat", "long", "geometry"]].head())

    print("\n--- Sample 5x5 distance matrix (km) ---")
    print(distance_matrix_sample(gdf, n=5).round(2))
