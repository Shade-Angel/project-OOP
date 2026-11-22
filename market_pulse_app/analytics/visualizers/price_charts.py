import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from analytics.metrics.technical import(
    calculate_sma, 
    calculate_bollinger,
    calculate_rsi
)

plt.style.use("seaborn-v0_8-darkgrid")

def plot_price(df: pd.DataFrame, ticker: str, reports_dir: Path):
    ticker_df = df[df["ticker"] == ticker].sort_index()
    close = ticker_df["close"]
    sma20 = calculate_sma(close, 20)
    sma50 = calculate_sma(close, 50)
    lower, middle, upper = calculate_bollinger(close)

    plt.figure(figsize=(14, 7))
    plt.plot(ticker_df.index, close, label="Цена", alpha=0.7)
    plt.plot(ticker_df.index, sma20, label="SMA 20", linestyle="--")
    plt.plot(ticker_df.index, sma50, label="SMA 50", linestyle="--")
    plt.fill_between(ticker_df.index, lower, upper, alpha=0.1, color="gray")

    plt.title(f"Цена и индикаторы: {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("Цена в рублях")
    plt.legend()
    plt.tight_layout()
    plt.savefig(reports_dir / f"price_{ticker}.png", dpi=300)
    plt.close()   


def plot_rsi(df: pd.DataFrame, ticker: str, reports_dir: Path):
    ticker_df = df[df["ticker"] == ticker].sort_index()
    rsi = calculate_rsi(ticker_df["close"])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])
    
    ax1.plot(ticker_df.index, ticker_df["close"])
    ax1.set_title(f"Цена и RSI: {ticker}")
    ax1.set_ylabel("Цена")
    
    ax2.plot(rsi.index, rsi, color="orange")
    ax2.axhline(y=70, color="red", linestyle="--")
    ax2.axhline(y=30, color="green", linestyle="--")
    ax2.fill_between(rsi.index, 70, 100, alpha=0.1, color="red")
    ax2.fill_between(rsi.index, 0, 30, alpha=0.1, color="green")
    ax2.set_ylabel("RSI")
    ax2.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig(reports_dir / f"rsi_{ticker}.png", dpi=300)
    plt.close() 


def plot_drawdown(df: pd.DataFrame, ticker: str, reports_dir: Path):
    ticker_df = df[df["ticker"] == ticker].sort_index()
    rolling_max = ticker_df["close"].cummax()
    drawdown = (ticker_df["close"] / rolling_max) - 1
    
    plt.figure(figsize=(12, 6))
    plt.fill_between(drawdown.index, drawdown * 100, 0, color="red", alpha=0.6)
    plt.plot(drawdown.index, drawdown * 100, color="red")
    
    plt.title(f"Просадка: {ticker}")
    plt.xlabel("Дата")
    plt.ylabel("Просадка в %")
    plt.tight_layout()
    plt.savefig(reports_dir / f"drawdown_{ticker}.png", dpi=300)
    plt.close()


def plot_distribution(df: pd.DataFrame, ticker: str, reports_dir: Path):
    ticker_df = df[df["ticker"] == ticker].sort_index()
    returns = ticker_df["close"].pct_change().dropna() * 100
    
    plt.figure(figsize=(10, 6))
    plt.hist(returns, bins=50, color="blue", alpha=0.7, edgecolor="black")
    
    plt.title(f"Распределение доходности: {ticker}")
    plt.xlabel("Доходность в %")
    plt.ylabel("Частота")
    plt.tight_layout()
    plt.savefig(reports_dir / f"distribution_{ticker}.png", dpi=300)
    plt.close()


def generate_price_charts(df: pd.DataFrame, tickers: list[str], reports_dir: Path):
    print("price_charts.py")
    for ticker in tickers:
        if ticker in df["ticker"].values:
            print(f"{ticker}")
            plot_price(df, ticker, reports_dir)
            plot_rsi(df, ticker, reports_dir)
            plot_drawdown(df, ticker, reports_dir)
            plot_distribution(df, ticker, reports_dir)