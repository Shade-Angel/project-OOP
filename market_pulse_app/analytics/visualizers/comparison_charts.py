import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import cm

plt.style.use("seaborn-v0_8-darkgrid")


def plot_leaders(metrics: pd.DataFrame, reports_dir: Path):
    top_up = metrics.nlargest(5, "total")
    top_down = metrics.nsmallest(5, "total")
    combined = pd.concat([top_up, top_down]).sort_values("total")
    
    plt.figure(figsize=(10, 6))
    colors = ["green" if x > 0 else "red" for x in combined["total"]]
    plt.barh(combined["ticker"], combined["total"] * 100, color=colors)
    plt.title("Топ-5 лидеров роста и падения")
    plt.xlabel("Доходность в %")
    plt.tight_layout()
    plt.savefig(reports_dir / "leaders.png", dpi=300)
    plt.close()


def plot_volatility(metrics: pd.DataFrame, reports_dir: Path):
    top = metrics.nlargest(10, "volatility")
    
    plt.figure(figsize=(10, 6))
    plt.barh(top["ticker"], top["volatility"] * 100, color="blue")
    plt.title("Топ-10 по волатильности")
    plt.xlabel("Волатильность в %")
    plt.tight_layout()
    plt.savefig(reports_dir / "volatility.png", dpi=300)
    plt.close()


def plot_correlation(corr_matrix: pd.DataFrame, reports_dir: Path):
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f", 
                linewidths=0.5, annot_kws={"size": 8})
    plt.title("Матрица корреляции доходностей")
    plt.tight_layout()
    plt.savefig(reports_dir / "correlation.png", dpi=300)
    plt.close()


def plot_risk_return(metrics: pd.DataFrame, reports_dir: Path):
    plt.figure(figsize=(12, 8))
    
    sectors = metrics["sector"].unique()
    palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]
    
    for i, sector in enumerate(sectors):
        data = metrics[metrics["sector"] == sector]
        color = palette[i % len(palette)]
        plt.scatter(data["volatility"] * 100, data["total"] * 100, 
                   c=color, label=sector, s=100, alpha=0.7, edgecolors="black")
    
    plt.title("Риск и Доходность по секторам")
    plt.xlabel("Волатильность в %")
    plt.ylabel("Доходность в %")
    plt.legend(title="Сектор", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(reports_dir / "risk_return.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_sectors(sector_df: pd.DataFrame, reports_dir: Path):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].barh(sector_df.index, sector_df["total"] * 100, color="green")
    axes[0, 0].set_title("Средняя доходность в %")
    
    axes[0, 1].barh(sector_df.index, sector_df["volatility"] * 100, color="red")
    axes[0, 1].set_title("Средняя волатильность в %")
    
    axes[1, 0].barh(sector_df.index, sector_df["sharpe"], color="blue")
    axes[1, 0].set_title("Средний Sharpe")
    
    axes[1, 1].barh(sector_df.index, sector_df["assets_count"], color="purple")
    axes[1, 1].set_title("Количество активов")
    
    plt.suptitle("Сравнение секторов", fontsize=16, y=0.98)
    plt.tight_layout()
    plt.savefig(reports_dir / "sectors.png", dpi=300)
    plt.close()


def generate_comparison_charts(metrics: pd.DataFrame, corr_matrix: pd.DataFrame, 
    sector_df: pd.DataFrame, reports_dir: Path):
    print("Общие графики")
    plot_leaders(metrics, reports_dir)
    plot_volatility(metrics, reports_dir)
    plot_correlation(corr_matrix, reports_dir)
    plot_risk_return(metrics, reports_dir)
    plot_sectors(sector_df, reports_dir)