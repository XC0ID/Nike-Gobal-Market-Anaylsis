# %% [markdown]
# # 01 — Exploratory Data Analysis
# Nike Global Product Catalog — snapshot 2026-03-19
#
# Run as a Jupyter notebook: `jupyter lab` → open this file
# Or convert: `jupytext --to notebook 01_eda.py`

# %%
import pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "..")
from src.ingestion.load_data import load_country
from src.preprocessing.clean_and_merge import clean
import yaml

with open("../config.yaml") as f:
    cfg = yaml.safe_load(f)

# %%
# Load one country for fast EDA (swap to load_global() for full dataset)
df_raw = load_country("IN", raw_dir="../data/raw")
df = clean(df_raw, cfg)
print(f"Shape: {df.shape}")

# %%
df.dtypes

# %%
df.describe(include="all").T

# %%
# Missing values
df.isnull().sum().sort_values(ascending=False).head(15)

# %%
# Category distribution
df["category"].value_counts()

# %%
# Availability levels
df["availability_level"].value_counts()

# %%
# Gender segment split
df["gender_segment"].value_counts()

# %%
# Sale / discount overview
print(f"Products on sale: {df['is_on_sale'].sum():,} ({df['is_on_sale'].mean()*100:.1f}%)")
df[df["is_on_sale"]]["discount_pct"].describe()
