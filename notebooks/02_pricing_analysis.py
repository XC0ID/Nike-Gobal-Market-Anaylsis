# %% [markdown]
# # 02 — Pricing Analysis
# Price distributions, discount depth, USD-normalized comparisons across markets

# %%
import pandas as pd
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "..")
from src.preprocessing.clean_and_merge import clean
from src.analysis.pricing import to_usd, discount_summary, top_discounted_products
from src.visualization.plots import discount_heatmap
import yaml

with open("../config.yaml") as f:
    cfg = yaml.safe_load(f)

# %%
# Load a sample of countries for cross-market comparison
sample_countries = ["US", "IN", "GB", "JP", "DE", "FR", "CN"]
frames = []
for cc in sample_countries:
    try:
        raw = pd.read_csv(f"../data/raw/Nike_{cc}.csv", low_memory=False)
        frames.append(clean(raw, cfg))
    except FileNotFoundError:
        print(f"Skipping {cc} — file not found")

df = pd.concat(frames, ignore_index=True)
df["price_usd"] = to_usd(df)
print(f"Loaded {len(df):,} rows from {df['country_code'].nunique()} countries")

# %%
# Median USD footwear price by country
df[df["category"]=="FOOTWEAR"].groupby("country_code")["price_usd"].median().sort_values(ascending=False)

# %%
# Discount summary table
disc = discount_summary(df)
print(disc.head(10))

# %%
# Heatmap of average discount % per country
discount_heatmap(disc.reset_index(), save_path="../reports/figures/discount_heatmap.png")
plt.show()

# %%
# Top discounted products
top_discounted_products(df, n=15)
