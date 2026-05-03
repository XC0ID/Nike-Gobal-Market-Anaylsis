"""
availability.py
---------------
Availability & stock analysis across countries and categories.
"""

import pandas as pd


def oos_rate_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """Out-of-stock rate per country (% of SKUs with availability_level == OOS)."""
    grp = df.groupby("country_code")
    total = grp["sku"].count().rename("total_skus")
    oos = grp.apply(lambda x: (x["availability_level"] == "OOS").sum()).rename("oos_skus")
    result = pd.concat([total, oos], axis=1)
    result["oos_rate_pct"] = (result["oos_skus"] / result["total_skus"] * 100).round(2)
    return result.sort_values("oos_rate_pct", ascending=False).reset_index()


def stock_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Count of SKUs per (country, category, availability_level)."""
    return (
        df.groupby(["country_code", "category", "availability_level"])
        .size()
        .reset_index(name="count")
    )


def gender_availability(df: pd.DataFrame) -> pd.DataFrame:
    """In-stock rate by gender segment."""
    return (
        df.groupby("gender_segment")["in_stock"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
        .reset_index(name="pct")
    )


def low_stock_products(df: pd.DataFrame) -> pd.DataFrame:
    """Products with LOW availability — useful for demand forecasting."""
    return df[df["availability_level"] == "LOW"][
        ["country_code", "product_name", "category", "subcategory",
         "gender_segment", "size_count", "available_size_count"]
    ].drop_duplicates()
