# Nike Global Product Analysis

A structured data science project for analyzing Nike's global product catalog across 46 countries — covering pricing, availability, discounts, inventory levels, and category trends.

---

## Dataset Overview

| Property | Details |
|---|---|
| Source | `archive.zip` (Nike global scrape) |
| Countries | 46 (AT, AU, BE, BG, CA, CH, CN, CZ, DE, DK, EG, ES, FI, FR, GB, GR, HR, HU, ID, IE, IL, IN, IT, JP, KR, LU, MX, MY, NL, NO, NZ, PH, PL, PT, RO, SE, SG, SI, SK, TH, TR, TW, US, VN, ZA) |
| Snapshot Date | 2026-03-19 |
| Key Files | `Global_Nike.csv` + per-country CSVs |

### Columns

| Column | Description |
|---|---|
| `snapshot_date` | Date of data capture |
| `country_code` | ISO country code |
| `product_name` | Full product title |
| `model_number` | Nike model/style ID |
| `currency` | Local currency |
| `price_local` | Regular price in local currency |
| `sale_price_local` | Discounted price (if applicable) |
| `gender_segment` | MENS / WOMENS / BOYS / GIRLS / UNISEX |
| `category` | FOOTWEAR / APPAREL / EQUIPMENT |
| `subcategory` | Product subcategory |
| `in_stock` | Boolean stock status |
| `available` | Product availability |
| `availability_level` | OOS / LOW / MED / HIGH |
| `discount_pct` | Discount percentage |
| `sport_tags` | Sport association tags |

---

## Project Structure

```
nike-global-analysis/
│
├── data/
│   ├── raw/               # Original CSVs from archive.zip (place here)
│   ├── processed/         # Cleaned, merged, feature-engineered data
│   └── external/          # Exchange rates, region mappings, etc.
│
├── notebooks/             # Exploratory & reporting notebooks
│   ├── 01_eda.ipynb
│   ├── 02_pricing_analysis.ipynb
│   ├── 03_availability_analysis.ipynb
│   └── 04_country_comparison.ipynb
│
├── src/
│   ├── ingestion/         # Data loading & extraction scripts
│   ├── preprocessing/     # Cleaning, merging, feature engineering
│   ├── analysis/          # Business logic & metrics
│   └── visualization/     # Reusable chart functions
│
├── models/                # ML models (demand forecast, price elasticity)
├── app/                   # Dashboard / API
├── reports/               # Final outputs
│   ├── figures/
│   └── outputs/
│
├── README.md
├── requirements.txt
└── config.yaml
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Extract raw data into data/raw/
unzip archive.zip -d data/raw/

# 3. Run preprocessing
python src/preprocessing/clean_and_merge.py

# 4. Launch notebooks
jupyter lab notebooks/
```

---

## Analysis Goals

- **Pricing Intelligence** — Compare price points across countries; identify premium vs discount markets
- **Availability & Stock** — Track OOS rates by country, category, gender
- **Discount Strategy** — Analyze discount depth and frequency by region
- **Category Mix** — Understand Footwear vs Apparel vs Equipment split globally
- **Top Products** — Surface best-selling / most-available SKUs per market
