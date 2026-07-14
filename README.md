# Project 3: Construction & Real Estate — Geospatial Valuation via Spatial Embeddings

**Objective:** Build a hyper-accurate property valuation engine that proves spatial dependencies (graph/attention-based models) outperform traditional tabular ML baselines (XGBoost, Linear Regression), measured primarily via **MAPE** on a holdout set.

---

## 📁 Repository Structure

```
Project3_Geospatial_Valuation/
│
├── data/
│   ├── raw/                        # Original King County housing data
│   ├── processed/                  # Cleaned, outlier-treated, feature-engineered data
│   └── graph/                      # Node/edge lists, adjacency matrices, embeddings
│
├── notebooks/
│   ├── Week1_Geospatial_Data_Processing.ipynb
│   ├── Week2_Feature_Engineering_Baseline.ipynb
│   ├── Week3_Graph_Construction_Embeddings.ipynb
│   └── Week4_GNN_Attention_Model.ipynb
│
├── src/
│   ├── geo_utils.py                 # Haversine distance, GeoDataFrame helpers
│   ├── cleaning_utils.py            # Missing values, dedup, outlier treatment
│   ├── feature_engineering.py       # Age, distance-to-CBD, tabular features
│   ├── baseline_model.py            # XGBoost / Linear Regression training + eval
│   ├── graph_builder.py             # KNN graph construction, embeddings
│   ├── gnn_model.py                 # GNN / attention-based architecture (PyTorch/DGL)
│   └── metrics.py                   # MAPE, RMSE, model comparison utilities
│
├── maps/                             # Folium/Kepler.gl HTML outputs
├── models/                           # Saved model weights/checkpoints
├── reports/
│   ├── week1_summary.md
│   ├── week2_summary.md
│   ├── week3_summary.md
│   └── week4_summary.md
│
├── app/
│   └── streamlit_dashboard.py        # Final geospatial valuation dashboard
│
├── requirements.txt
└── README.md
```

---

## 🗓️ Weekly Log

### **Week 1 — Geospatial Data Acquisition & Processing**
**Goal:** Get clean, spatially-valid data ready for modeling.

- Acquired the **King County Housing Dataset** (lat/long, price, sqft, bedrooms, bathrooms, year built, zipcode).
- Cleaned data: handled missing values, removed duplicates, fixed dtypes, validated coordinate ranges.
- Identified and normalized **5 extreme price outliers** using IQR/z-score thresholding.
- Converted data into a `GeoDataFrame` using **GeoPandas** and **Shapely** Point geometries.
- Implemented **Haversine distance** calculations between properties.
- Plotted properties on interactive maps (**Folium** / Kepler.gl) — price heatmaps and price-per-sqft heatmaps — to visually inspect spatial pricing trends (waterfront premiums, urban-core gradients, zipcode-level clustering).

**Deliverables:** `data/processed/kc_house_cleaned.csv`, `maps/price_heatmap.html`, `reports/week1_summary.md`

---

### **Week 2 — Feature Engineering & Baseline ML**
**Goal:** Establish the benchmark the spatial model must beat.

- Engineered standard tabular features: **age of house** (from year built/renovated), **distance to city center** (Seattle CBD, via Haversine), plus existing structural features (sqft, bed/bath, condition, grade).
- Split data into train/holdout sets (time-aware split to avoid leakage where relevant).
- Trained an **XGBoost regressor** as the primary baseline; trained a **Linear Regression** as a secondary/simpler baseline.
- Calculated and documented baseline **MAPE** and **RMSE** on the holdout set.
- Performed error analysis: identified where the baseline underperforms — specifically **rapidly gentrifying neighborhoods**, waterfront outliers, and zipcodes with sparse comparable sales — and documented these as motivating evidence for spatial modeling.

**Deliverables:** `src/baseline_model.py`, `models/xgboost_baseline.json`, `reports/week2_summary.md` (baseline MAPE/RMSE table + gentrification error analysis)

---

### **Week 3 — Spatial Embeddings & Graph Construction**
**Goal:** Encode neighborhood context mathematically.

- Converted the dataset into a **graph structure**: each house = a node; edges connect each house to its **K-nearest neighbors** based on physical (Haversine) distance.
- Tuned *K* and explored alternative graph construction strategies (radius-based, Delaunay triangulation) for comparison.
- Attached node features (tabular features from Week 2) and edge weights (inverse distance) to the graph.
- Generated **spatial embeddings** (e.g., via node2vec, or a learned embedding layer) to represent localized neighborhood context in a dense vector form.
- Validated embeddings qualitatively (e.g., t-SNE/UMAP plot colored by price or zipcode) to confirm spatially coherent neighborhoods cluster together in embedding space.

**Deliverables:** `data/graph/edges.csv`, `data/graph/node_embeddings.npy`, `src/graph_builder.py`, `reports/week3_summary.md`

---

### **Week 4 — GNN / Attention Modeling & Geospatial Dashboard**
**Goal:** Prove spatial modeling beats the baseline, and ship a usable tool.

- Built and trained a **Graph Neural Network (GNN)** or **attention-based spatial model** (PyTorch / DGL) that aggregates neighboring properties' pricing signals, with attention weights indicating which neighbors matter most for a given target house.
- Evaluated on the same holdout set as Week 2 for a fair comparison; computed **MAPE** and **RMSE**.
- Documented the **MAPE improvement over the XGBoost baseline**, with particular focus on the gentrifying-neighborhood cases identified in Week 2.
- Extracted **top-5 most influential neighbors** per prediction (via attention weights) to support the Appraiser persona's workflow.
- Built and deployed a **Streamlit dashboard**: address-based lookup → predicted price + top-5 influential neighbors; spatial heatmap view for the Investment Strategist persona to spot undervalued hotspots.
- Finalized version control: all code, notebooks, and model artifacts committed to GitHub with clear commit history across the 4 weeks.

**Deliverables:** `src/gnn_model.py`, `models/gnn_final.pt`, `app/streamlit_dashboard.py`, `reports/week4_summary.md` (final MAPE comparison: XGBoost vs. GNN/Attention)

---

## ✅ Success Criteria (Recap)
- Baseline (XGBoost) MAPE established on holdout set (Week 2).
- Spatial/GNN model MAPE measured on the **same** holdout set (Week 4).
- Spatial model demonstrably **outperforms** the tabular baseline, especially in spatially complex areas (gentrifying neighborhoods, sparse-comp zipcodes).
- Working Streamlit dashboard supporting both personas: Real Estate Appraiser (address → price + top-5 neighbors) and Investment Strategist (heatmap of hotspots).

## 📦 Requirements
```
geopandas
shapely
pandas
numpy
scikit-learn
xgboost
folium
torch
dgl
node2vec
streamlit
matplotlib
seaborn
jupyter
```
