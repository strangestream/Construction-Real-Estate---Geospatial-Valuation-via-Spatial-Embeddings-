
## Day 2 - Data Cleaning & Outlier Normalization

- Rows before cleaning: **21,613**
- Rows after cleaning: **21,613**
- 5 most extreme price outliers identified and capped at the 99th percentile.
- Post-cleaning price range: **$75,000** to **$5,300,000**

## Day 1 - Data Acquisition & Initial Inspection

- Rows: **21,613**, Columns: **21**
- Duplicate rows: **0**
- No missing values detected.
- Price range: **$75,000** to **$7,700,000**, median **$450,000**
- Coordinate bounds: lat [47.1559, 47.7776], long [-122.5190, -121.3150]

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
