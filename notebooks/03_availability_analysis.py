# %% [markdown]
# # 03 — Availability & Stock Analysis
# OOS rates, gender availability, low-stock products

# %%
import pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "..")
from src.preprocessing.clean_and_merge import clean
from src.analysis.availability import oos_rate_by_country, gender_availability, low_stock_products
from src.visualization.plots import oos_rate_bar
import yaml

with open("../config.yaml") as f:
    cfg = yaml.safe_load(f)

# %%
df_raw = pd.read_csv("../data/raw/Nike_IN.csv", low_memory=False)
df = clean(df_raw, cfg)

# %%
# Availability level breakdown
df["availability_level"].value_counts(normalize=True).mul(100).round(2)

# %%
# Gender segment availability
gender_availability(df)

# %%
# Products with LOW stock (restock candidates)
low_stock_products(df).head(20)

# %%
# OOS by subcategory
df[df["availability_level"]=="OOS"]["subcategory"].value_counts().head(15)
