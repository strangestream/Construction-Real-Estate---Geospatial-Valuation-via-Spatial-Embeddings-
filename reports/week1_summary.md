## Day 1 - Data Acquisition & Initial Inspection

- Rows: **21,613**, Columns: **21**
- Duplicate rows: **0**
- No missing values detected.
- Price range: **$75,000** to **$7,700,000**, median **$450,000**
- Coordinate bounds: lat [47.1559, 47.7776], long [-122.5190, -121.3150]

## Day 2 - Data Cleaning & Outlier Normalization

- Rows before cleaning: **21,613**
- Rows after cleaning: **21,613**
- 5 most extreme price outliers identified and capped at the 99th percentile.
- Post-cleaning price range: **$75,000** to **$5,300,000**

## Day 3 - Geospatial Conversion & Haversine Distance

- Converted **21,613** properties into a GeoDataFrame (CRS: EPSG:4326).
- Sample 5x5 Haversine distance matrix (km) computed to sanity-check distances.
- Closest sample pair distance: **6.70 km**
- Farthest sample pair distance: **28.21 km**

## Day 4 - Interactive Spatial Heatmaps

- Built a raw price heatmap: `maps/price_heatmap.html`
- Built a price-per-sqft heatmap (normalizes for house size): `maps/price_per_sqft_heatmap.html`
- Mapped **21,613** properties across King County.
- Next: visually inspect both maps for waterfront premiums, urban-core gradients, and zipcode-level clustering.
