"""
clean_and_merge.py
------------------
Cleans raw Nike data and saves processed Parquet files.

Usage:
    python src/preprocessing/clean_and_merge.py         # All countries
    python src/preprocessing/clean_and_merge.py IN      # Single country
"""

import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import sys


def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def clean(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Apply standard cleaning steps to a Nike dataframe."""
    cols = cfg["columns"]

    # Parse date
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

    # Numeric coercion
    for c in cols["numeric_cols"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Boolean coercion
    for c in cols["bool_cols"]:
        if c in df.columns:
            df[c] = df[c].map({"True": True, "False": False, True: True, False: False})

    # Strip whitespace on categoricals
    for c in cols["categorical_cols"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    # Derived features
    df["is_on_sale"] = df["sale_price_local"].notna() & (df["sale_price_local"] < df["price_local"])
    df["effective_price"] = df["sale_price_local"].fillna(df["price_local"])

    return df


def run(country=None, output_dir="data/processed"):
    cfg = load_config()
    raw_dir = cfg["data"]["raw_dir"]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if country:
        fpath = Path(raw_dir) / f"Nike_{country}.csv"
        df = pd.read_csv(fpath, low_memory=False)
        df = clean(df, cfg)
        out = Path(output_dir) / f"Nike_{country}_clean.parquet"
        df.to_parquet(out, index=False)
        print(f"Saved -> {out}")
    else:
        for fpath in sorted(Path(raw_dir).glob("Nike_*.csv")):
            cc = fpath.stem.split("_")[1]
            df = pd.read_csv(fpath, low_memory=False)
            df = clean(df, cfg)
            out = Path(output_dir) / f"Nike_{cc}_clean.parquet"
            df.to_parquet(out, index=False)
            print(f"  Saved -> {out}")


if __name__ == "__main__":
    country = sys.argv[1] if len(sys.argv) > 1 else None
    run(country)
