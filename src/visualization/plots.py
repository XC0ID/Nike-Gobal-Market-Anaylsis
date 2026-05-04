"""
plots.py
--------
Reusable chart functions for Nike global analysis.
All functions return a matplotlib Figure for easy saving or display in notebooks.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

PALETTE = sns.color_palette("Set2")
plt.rcParams.update({"figure.dpi": 120, "font.size": 11})


def bar_country(df: pd.DataFrame, value_col: str, title: str, ylabel: str,
                top_n: int = 20, save_path: str = None) -> plt.Figure:
    """Horizontal bar chart of a metric by country."""
    fig, ax = plt.subplots(figsize=(14, 5))
    data = df.nlargest(top_n, value_col) if len(df) > top_n else df
    ax.bar(data["country_code"], data[value_col], color=PALETTE[0])
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Country")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def category_pie(df: pd.DataFrame, country: str = None,
                 save_path: str = None) -> plt.Figure:
    """Pie chart of product category mix."""
    subset = df[df["country_code"] == country] if country else df
    counts = subset["category"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=PALETTE)
    ax.set_title(f"Category Mix — {country or 'Global'}")
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def discount_heatmap(discount_df: pd.DataFrame, save_path: str = None) -> plt.Figure:
    """Heatmap of avg discount % across countries."""
    fig, ax = plt.subplots(figsize=(16, 3))
    
    # Handle empty dataframe case
    if discount_df.empty or len(discount_df) == 0:
        ax.text(0.5, 0.5, 'No discount data available', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        ax.set_title("Average Discount % by Country")
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        pivot = discount_df[["avg_discount"]].T
        sns.heatmap(pivot, ax=ax, cmap="YlOrRd", annot=True, fmt=".1f", linewidths=0.5)
        ax.set_title("Average Discount % by Country")
    
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def oos_rate_bar(oos_df: pd.DataFrame, top_n: int = 20,
                 save_path: str = None) -> plt.Figure:
    """Bar chart of OOS rate by country."""
    data = oos_df.nlargest(top_n, "oos_rate_pct")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(data["country_code"], data["oos_rate_pct"], color=PALETTE[1])
    ax.set_title(f"Top {top_n} Countries by Out-of-Stock Rate (%)")
    ax.set_xlabel("Country")
    ax.set_ylabel("OOS Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def gender_split(df: pd.DataFrame, country: str = None,
                 save_path: str = None) -> plt.Figure:
    """Bar chart of SKU count by gender segment."""
    subset = df[df["country_code"] == country] if country else df
    counts = subset["gender_segment"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(counts.index, counts.values, color=PALETTE[2])
    ax.set_title(f"SKUs by Gender Segment — {country or 'Global'}")
    ax.set_xlabel("Gender Segment")
    ax.set_ylabel("SKU Count")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig
