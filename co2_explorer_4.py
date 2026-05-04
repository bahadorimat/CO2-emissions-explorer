"""
CO2 Emissions Explorer
Matin Bahadori, 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


COUNTRIES = ["Germany", "China", "United States", "India", "France"]
COLORS = ["#2196F3", "#F44336", "#FF9800", "#4CAF50", "#9C27B0"]
YEAR_START = 1990
YEAR_END = 2022
DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"


def load_and_clean(url):
    print("Downloading dataset...")
    df = pd.read_csv(url)
    cols = ["country", "year", "co2", "co2_per_capita", "gdp", "population"]
    df = df[cols].copy()
    df = df[df["country"].isin(COUNTRIES)]
    df = df[df["year"].between(YEAR_START, YEAR_END)]
    df = df[df["co2"].notna()]
    print(f"Got {len(df)} rows.\n")
    return df


def setup_ax(ax, fig):
    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")
    ax.tick_params(colors="#bbbbbb")
    ax.xaxis.label.set_color("#bbbbbb")
    ax.yaxis.label.set_color("#bbbbbb")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a2a")
    ax.grid(color="#1e1e1e", linestyle="--", linewidth=0.7)


def plot_trends(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    setup_ax(ax, fig)
    for country, color in zip(COUNTRIES, COLORS):
        data = df[df["country"] == country]
        ax.plot(data["year"], data["co2"], label=country,
                color=color, linewidth=2, marker="o", markersize=2.5)
    ax.set_title("CO2 Emissions Over Time", color="white", fontsize=14, pad=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Million tonnes CO2")
    ax.legend(frameon=False, labelcolor="white", fontsize=10)
    plt.tight_layout()
    os.makedirs("output", exist_ok=True)
    plt.savefig("output/01_trends.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_per_capita(df):
    avg = (df.groupby("country")["co2_per_capita"]
             .mean()
             .reindex(COUNTRIES)
             .sort_values(ascending=False))
    fig, ax = plt.subplots(figsize=(9, 5))
    setup_ax(ax, fig)
    bar_colors = [COLORS[COUNTRIES.index(c)] for c in avg.index]
    bars = ax.barh(avg.index, avg.values, color=bar_colors, height=0.5)
    for bar, val in zip(bars, avg.values):
        ax.text(val + 0.15, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f} t", va="center", color="white", fontsize=9)
    ax.invert_yaxis()
    ax.set_title("Average CO2 Per Capita (1990-2022)", color="white", fontsize=14, pad=12)
    ax.set_xlabel("Tonnes CO2 per person / year")
    plt.tight_layout()
    plt.savefig("output/02_per_capita.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_co2_vs_gdp(df):
    data = df.dropna(subset=["gdp", "co2"])
    fig, ax = plt.subplots(figsize=(10, 6))
    setup_ax(ax, fig)
    for country, color in zip(COUNTRIES, COLORS):
        d = data[data["country"] == country]
        ax.scatter(d["gdp"] / 1e12, d["co2"],
                   label=country, color=color, alpha=0.7, s=30)
    ax.set_title("CO2 vs. GDP", color="white", fontsize=13, pad=12)
    ax.set_xlabel("GDP (trillion USD)")
    ax.set_ylabel("CO2 (million tonnes)")
    ax.legend(frameon=False, labelcolor="white", fontsize=10)
    plt.tight_layout()
    plt.savefig("output/03_co2_vs_gdp.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_decade_change(df):
    decades = [1990, 2000, 2010, 2020]
    records = []
    for country in COUNTRIES:
        row = {"country": country}
        for i in range(len(decades) - 1):
            y0, y1 = decades[i], decades[i + 1]
            v0 = df.loc[(df["country"] == country) & (df["year"] == y0), "co2"]
            v1 = df.loc[(df["country"] == country) & (df["year"] == y1), "co2"]
            if not v0.empty and not v1.empty:
                pct = ((v1.values[0] - v0.values[0]) / v0.values[0]) * 100
                row[f"{y0}s"] = round(pct, 1)
        records.append(row)
    heat = pd.DataFrame(records).set_index("country").dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")
    im = ax.imshow(heat.values, cmap="RdYlGn_r", aspect="auto", vmin=-40, vmax=80)
    ax.set_xticks(range(len(heat.columns)))
    ax.set_xticklabels(heat.columns, color="white")
    ax.set_yticks(range(len(heat.index)))
    ax.set_yticklabels(heat.index, color="white")
    for i in range(len(heat.index)):
        for j in range(len(heat.columns)):
            val = heat.values[i, j]
            label = f"+{val:.0f}%" if val > 0 else f"{val:.0f}%"
            ax.text(j, i, label, ha="center", va="center",
                    color="white", fontsize=10, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).ax.tick_params(colors="white")
    ax.set_title("CO2 Change Per Decade (%)", color="white", fontsize=13, pad=10)
    plt.tight_layout()
    plt.savefig("output/04_decade_heatmap.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()


def print_summary(df):
    summary = df.groupby("country").agg(
        avg_co2=("co2", "mean"),
        latest_co2=("co2", "last"),
        avg_per_capita=("co2_per_capita", "mean")
    ).round(1)
    print(summary)
    summary.to_csv("output/summary.csv")


if __name__ == "__main__":
    df = load_and_clean(DATA_URL)
    plot_trends(df)
    plot_per_capita(df)
    plot_co2_vs_gdp(df)
    plot_decade_change(df)
    print_summary(df)
