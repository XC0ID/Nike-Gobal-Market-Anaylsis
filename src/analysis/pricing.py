"""
pricing.py
----------
Pricing analysis utilities: price distribution, discount depth, USD conversion.
"""

import pandas as pd
import numpy as np

# Approximate exchange rates to USD (2026-03 — update from config/external source)
FX_TO_USD = {
    "INR": 0.012, "USD": 1.0, "EUR": 1.09, "GBP": 1.27,
    "JPY": 0.0067, "CNY": 0.138, "KRW": 0.00073, "AUD": 0.65,
    "CAD": 0.74, "CHF": 1.12, "SEK": 0.096, "NOK": 0.095,
    "DKK": 0.146, "PLN": 0.25, "CZK": 0.044, "HUF": 0.0028,
    "RON": 0.22, "HRK": 0.145, "BGN": 0.56, "MXN": 0.052,
    "SGD": 0.74, "MYR": 0.22, "THB": 0.028, "IDR": 0.000063,
    "PHP": 0.018, "VND": 0.000039, "ILS": 0.27, "ZAR": 0.055,
    "TRY": 0.031, "TWD": 0.031, "NZD": 0.60, "HKD": 0.128,
}


def to_usd(df: pd.DataFrame, price_col: str = "effective_price") -> pd.Series:
    """Convert local price column to USD using FX_TO_USD map."""
    return df.apply(
        lambda r: r[price_col] * FX_TO_USD.get(r["currency"], np.nan), axis=1
    )


def discount_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return discount stats grouped by country, sorted by avg discount desc."""
    return (
        df[df["is_on_sale"]]
        .groupby("country_code")["discount_pct"]
        .agg(["mean", "median", "max", "count"])
        .rename(columns={
            "mean": "avg_discount",
            "median": "median_discount",
            "max": "max_discount",
            "count": "sale_items",
        })
        .sort_values("avg_discount", ascending=False)
    )


def price_range_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Min/mean/median/max effective price per country + category."""
    return (
        df.groupby(["country_code", "category"])["effective_price"]
        .agg(["min", "mean", "median", "max"])
        .reset_index()
    )


def top_discounted_products(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Return top N products by discount_pct with key metadata."""
    cols = ["country_code", "product_name", "category", "gender_segment",
            "price_local", "sale_price_local", "discount_pct", "currency"]
    return (
        df[df["is_on_sale"]][cols]
        .sort_values("discount_pct", ascending=False)
        .drop_duplicates(subset=["product_name", "country_code"])
        .head(n)
    )
