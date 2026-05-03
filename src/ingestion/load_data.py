"""
load_data.py
------------
Utilities for loading Nike CSVs from data/raw/.
Supports per-country files and the combined Global_Nike.csv.
"""

import pandas as pd
import yaml
from pathlib import Path


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_country(country_code: str, raw_dir: str = "data/raw", **kwargs) -> pd.DataFrame:
    """Load a single country CSV."""
    path = Path(raw_dir) / f"Nike_{country_code}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No file for country: {country_code} at {path}")
    df = pd.read_csv(path, **kwargs)
    print(f"[{country_code}] Loaded {len(df):,} rows")
    return df


def load_global(raw_dir: str = "data/raw", **kwargs) -> pd.DataFrame:
    """Load the combined Global_Nike.csv (~880MB uncompressed)."""
    path = Path(raw_dir) / "Global_Nike.csv"
    print("Loading Global_Nike.csv — this may take a moment...")
    df = pd.read_csv(path, **kwargs)
    print(f"[GLOBAL] Loaded {len(df):,} rows across {df['country_code'].nunique()} countries")
    return df


def load_all_countries(raw_dir: str = "data/raw", config_path: str = "config.yaml") -> pd.DataFrame:
    """Load and concatenate all per-country CSVs (lighter than Global)."""
    cfg = load_config(config_path)
    countries = cfg["data"]["countries"]
    frames = []
    for cc in countries:
        fpath = Path(raw_dir) / f"Nike_{cc}.csv"
        if fpath.exists():
            frames.append(pd.read_csv(fpath, low_memory=False))
        else:
            print(f"  [SKIP] Nike_{cc}.csv not found")
    df = pd.concat(frames, ignore_index=True)
    print(f"[ALL] Loaded {len(df):,} rows from {len(frames)} countries")
    return df


if __name__ == "__main__":
    df = load_country("IN")
    print(df.dtypes)
    print(df.head(3))
