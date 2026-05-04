"""
run_all_analysis.py
-------------------
Comprehensive script to run all analysis notebooks and generate reports.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.load_data import load_country, load_all_countries
from src.preprocessing.clean_and_merge import clean, load_config
from src.analysis.pricing import discount_summary, to_usd, top_discounted_products, price_range_by_category
from src.analysis.availability import oos_rate_by_country, gender_availability, low_stock_products, stock_by_category
from src.visualization.plots import category_pie, discount_heatmap, oos_rate_bar, gender_split

# ---- Config ----
cfg = load_config()
raw_dir = cfg["data"]["raw_dir"]
processed_dir = "data/processed"
reports_dir = "reports"
Path(f"{reports_dir}/figures").mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("NIKE GLOBAL MARKET ANALYSIS - FULL RUN")
print("=" * 80)

# ============================================================================
# ANALYSIS 1: EDA (01_eda.py)
# ============================================================================
print("\n[01] EXPLORATORY DATA ANALYSIS")
print("-" * 80)
try:
    df_raw = load_country("IN", raw_dir=raw_dir)
    df = clean(df_raw, cfg)
    print(f"✓ Loaded India data: {df.shape}")
    print(f"  Columns: {df.shape[1]}")
    print(f"  Data types:\n{df.dtypes}")
    print(f"\n  Missing values (top 5):\n{df.isnull().sum().sort_values(ascending=False).head(5)}")
    print(f"\n  Category distribution:\n{df['category'].value_counts()}")
    print(f"\n  Availability levels:\n{df['availability_level'].value_counts()}")
    print(f"\n  Gender segments:\n{df['gender_segment'].value_counts()}")
    print(f"\n  Products on sale: {df['is_on_sale'].sum():,} ({df['is_on_sale'].mean()*100:.1f}%)")
    print(f"  Discount stats (sales only):\n{df[df['is_on_sale']]['discount_pct'].describe()}")
    print("✓ EDA completed successfully")
except Exception as e:
    print(f"✗ EDA failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# ANALYSIS 2: PRICING ANALYSIS (02_pricing_analysis.py)
# ============================================================================
print("\n[02] PRICING ANALYSIS")
print("-" * 80)
try:
    sample_countries = ["US", "IN", "GB", "JP", "DE", "FR", "CN"]
    frames = []
    for cc in sample_countries:
        try:
            raw = pd.read_csv(f"{raw_dir}/Nike_{cc}.csv", low_memory=False)
            frames.append(clean(raw, cfg))
            print(f"  ✓ Loaded {cc}")
        except FileNotFoundError:
            print(f"  ⚠ Skipping {cc} — file not found")

    df = pd.concat(frames, ignore_index=True)
    df["price_usd"] = to_usd(df)
    print(f"✓ Loaded {len(df):,} rows from {df['country_code'].nunique()} countries")

    # Median USD footwear price by country
    print(f"\n  Median USD footwear price by country:")
    fw_prices = df[df["category"]=="FOOTWEAR"].groupby("country_code")["price_usd"].median().sort_values(ascending=False)
    print(fw_prices)

    # Discount summary
    print(f"\n  Top 5 countries by average discount:")
    disc = discount_summary(df)
    print(disc.head())

    # Top discounted products
    print(f"\n  Top 10 discounted products:")
    top_discs = top_discounted_products(df, n=10)
    print(top_discs)

    # Save discount heatmap
    discount_heatmap(disc.reset_index(), save_path=f"{reports_dir}/figures/discount_heatmap.png")
    print(f"✓ Saved discount heatmap to {reports_dir}/figures/discount_heatmap.png")
    print("✓ Pricing analysis completed successfully")
except Exception as e:
    print(f"✗ Pricing analysis failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# ANALYSIS 3: AVAILABILITY ANALYSIS (03_availability_analysis.py)
# ============================================================================
print("\n[03] AVAILABILITY & STOCK ANALYSIS")
print("-" * 80)
try:
    df_raw = pd.read_csv(f"{raw_dir}/Nike_IN.csv", low_memory=False)
    df = clean(df_raw, cfg)
    print(f"✓ Loaded India data for availability analysis")

    # Availability level breakdown
    print(f"\n  Availability level breakdown (%):")
    avail_pct = df["availability_level"].value_counts(normalize=True).mul(100).round(2)
    print(avail_pct)

    # Gender segment availability
    print(f"\n  Gender segment availability:")
    gender_avail = gender_availability(df)
    print(gender_avail)

    # Low stock products
    print(f"\n  Top 10 low-stock products (candidates for restock):")
    low_stock = low_stock_products(df).head(10)
    print(low_stock)

    # OOS by subcategory
    print(f"\n  Top 10 subcategories with OOS products:")
    oos_subcat = df[df["availability_level"]=="OOS"]["subcategory"].value_counts().head(10)
    print(oos_subcat)

    print("✓ Availability analysis completed successfully")
except Exception as e:
    print(f"✗ Availability analysis failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# ANALYSIS 4: COUNTRY COMPARISON (04_country_comparison.py)
# ============================================================================
print("\n[04] COUNTRY COMPARISON")
print("-" * 80)
try:
    countries = ["US", "IN", "JP", "DE", "GB", "AU", "CN"]
    frames = []
    for cc in countries:
        try:
            raw = pd.read_csv(f"{raw_dir}/Nike_{cc}.csv", low_memory=False)
            frames.append(clean(raw, cfg))
            print(f"  ✓ Loaded {cc}")
        except FileNotFoundError:
            print(f"  ⚠ Skipping {cc}")

    df = pd.concat(frames, ignore_index=True)
    df["price_usd"] = to_usd(df)

    # Median USD footwear price by country
    print(f"\n  Median USD footwear price by country:")
    fw_prices = df[df["category"] == "FOOTWEAR"].groupby("country_code")["price_usd"].median().sort_values(ascending=False)
    print(fw_prices)

    # SKU count by country
    print(f"\n  SKU count by country:")
    sku_count = df.groupby("country_code")["sku"].nunique().sort_values(ascending=False)
    print(sku_count)

    # OOS rate comparison
    print(f"\n  OOS rate by country (%):")
    oos = df.groupby("country_code", group_keys=False)[["availability_level"]].apply(
        lambda x: (x["availability_level"] == "OOS").mean() * 100, include_groups=False
    ).rename("oos_rate_pct").reset_index().sort_values("oos_rate_pct", ascending=False)
    print(oos)

    # Category mix by country
    print(f"\n  Category mix by country (%):")
    cat_pivot = (
        df.groupby(["country_code", "category"])
        .size()
        .unstack(fill_value=0)
    )
    cat_pct = cat_pivot.div(cat_pivot.sum(axis=1), axis=0).mul(100).round(1)
    print(cat_pct)

    print("✓ Country comparison completed successfully")
except Exception as e:
    print(f"✗ Country comparison failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# GLOBAL ANALYSIS
# ============================================================================
print("\n[05] GLOBAL CROSS-COUNTRY ANALYSIS")
print("-" * 80)
try:
    print("  Loading all countries...")
    df_global = load_all_countries(raw_dir=raw_dir, config_path="config.yaml")
    df_global = clean(df_global, cfg)
    df_global["price_usd"] = to_usd(df_global)
    print(f"✓ Loaded global dataset: {len(df_global):,} rows")

    # OOS rate by country (global)
    print(f"\n  OOS rate by country (global dataset):")
    oos_global = oos_rate_by_country(df_global)
    print(oos_global.head(10))

    # Discount summary (global)
    print(f"\n  Top 5 countries by average discount (global):")
    disc_global = discount_summary(df_global)
    print(disc_global.head())

    # Stock by category (sample)
    print(f"\n  Stock distribution sample (first 10 rows):")
    stock_dist = stock_by_category(df_global)
    print(stock_dist.head(10))

    # Generate visualizations
    print(f"\n  Generating visualizations...")

    # Global category pie
    category_pie(df_global, save_path=f"{reports_dir}/figures/global_category_mix.png")
    print(f"    ✓ Saved global category mix pie chart")

    # OOS rate bar chart
    oos_rate_bar(oos_global, top_n=20, save_path=f"{reports_dir}/figures/oos_rate_by_country.png")
    print(f"    ✓ Saved OOS rate bar chart")

    # Gender split pie
    gender_split(df_global, save_path=f"{reports_dir}/figures/global_gender_mix.png")
    print(f"    ✓ Saved global gender split pie chart")

    print("✓ Global analysis completed successfully")
except Exception as e:
    print(f"✗ Global analysis failed: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"Reports and figures saved to: {reports_dir}/")
print(f"Key outputs:")
print(f"  - {reports_dir}/figures/discount_heatmap.png")
print(f"  - {reports_dir}/figures/global_category_mix.png")
print(f"  - {reports_dir}/figures/oos_rate_by_country.png")
print(f"  - {reports_dir}/figures/global_gender_mix.png")
print("\nProject run completed successfully! ✓")
