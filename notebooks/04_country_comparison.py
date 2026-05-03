# %% [markdown]
# # 04 — Country Comparison
# Cross-country product mix, pricing tiers, and availability benchmarks

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys; sys.path.insert(0, "..")
from src.preprocessing.clean_and_merge import clean
from src.analysis.pricing import price_range_by_category, to_usd
from src.analysis.availability import oos_rate_by_country
import yaml

with open("../config.yaml") as f:
    cfg = yaml.safe_load(f)

# %%
countries = ["US", "IN", "JP", "DE", "GB", "AU", "CN"]
frames = []
for cc in countries:
    try:
        raw = pd.read_csv(f"../data/raw/Nike_{cc}.csv", low_memory=False)
        frames.append(clean(raw, cfg))
    except FileNotFoundError:
        print(f"Skipping {cc}")
df = pd.concat(frames, ignore_index=True)
df["price_usd"] = to_usd(df)

# %%
# Median USD footwear price by country
footwear = df[df["category"] == "FOOTWEAR"]
footwear.groupby("country_code")["price_usd"].median().sort_values(ascending=False)

# %%
# SKU count by country
df.groupby("country_code")["sku"].nunique().sort_values(ascending=False)

# %%
# OOS rate comparison
oos = df.groupby("country_code").apply(
    lambda x: (x["availability_level"] == "OOS").mean() * 100
).rename("oos_rate_pct").reset_index()
oos.sort_values("oos_rate_pct", ascending=False)

# %%
# Category mix by country (pivot)
cat_pivot = (
    df.groupby(["country_code", "category"])
    .size()
    .unstack(fill_value=0)
)
cat_pivot.div(cat_pivot.sum(axis=1), axis=0).mul(100).round(1)
