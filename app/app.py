"""
app/app.py
----------
Streamlit dashboard for Nike Global Product Analysis.

Run:
    cd nike-global-analysis
    streamlit run app/app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.ingestion.load_data import load_country
from src.preprocessing.clean_and_merge import clean, load_config
from src.analysis.pricing import discount_summary, to_usd, top_discounted_products
from src.analysis.availability import oos_rate_by_country, gender_availability
from src.visualization.plots import category_pie, oos_rate_bar

# ---- Config ----
cfg = load_config(str(Path(__file__).parent.parent / "config.yaml"))
COUNTRIES = cfg["data"]["countries"]
RAW_DIR = str(Path(__file__).parent.parent / "data" / "raw")

st.set_page_config(page_title="Nike Global Analysis", layout="wide")
st.title("🏃 Nike Global Product Dashboard")

# ---- Sidebar ----
st.sidebar.header("Settings")
country = st.sidebar.selectbox("Select Country", COUNTRIES, index=COUNTRIES.index("IN"))

# ---- Load ----
@st.cache_data
def get_data(cc):
    raw = load_country(cc, raw_dir=RAW_DIR)
    return clean(raw, cfg)

try:
    df = get_data(country)
    st.sidebar.success(f"Loaded {len(df):,} rows")
except FileNotFoundError:
    st.error(f"No raw data found for {country}. Place Nike_{country}.csv in data/raw/")
    st.stop()

# ---- KPI Row ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total SKUs", f"{len(df):,}")
col2.metric("Unique Products", f"{df['product_id'].nunique():,}")
oos_pct = (df["availability_level"] == "OOS").mean() * 100
col3.metric("OOS Rate", f"{oos_pct:.1f}%")
sale_pct = df["is_on_sale"].mean() * 100
col4.metric("On Sale", f"{sale_pct:.1f}%")

# ---- Category Mix ----
st.subheader("Category Mix")
fig = category_pie(df, country=country)
st.pyplot(fig)
plt.close()

# ---- Discount Table ----
st.subheader("Top Discounted Products")
top_disc = top_discounted_products(df, n=10)
st.dataframe(top_disc, use_container_width=True)

# ---- Availability ----
st.subheader("Availability Breakdown")
avail = df["availability_level"].value_counts().reset_index()
avail.columns = ["Level", "Count"]
st.bar_chart(avail.set_index("Level"))

# ---- Gender Split ----
st.subheader("Gender Segment Split")
gender_counts = df["gender_segment"].value_counts()
st.bar_chart(gender_counts)
