import pandas as pd
import numpy as np
from analytics.metrics.risk_metrics import(
    calculate_shape,
    calculate_sortino,
    calculate_max_down,
    calculate_var
)
from analytics.metrics.technical import calculate_rsi
from analytics.metrics.statistics import(
    calculate_skewness,
    calculate_kurtosis,
    get_distribution
)


def calculate_metrics(df: pd.DataFrame, assets_meta: list[dict]) -> pd.DataFrame:
    res = []

    for ticker in df["ticker"].unique():
        ticker_df = df[df["ticker"] == ticker].sort_index()
        daily = ticker_df["close"].pct_change()

        total = (ticker_df["close"]).iloc[-1] / ticker_df["close"].iloc[0] - 1
        if len(ticker_df) >= 21:
            monthly = ticker_df["close"].pct_change(21).iloc[-1]
        else:
            monthly = 0.0
        volatility = np.std(daily.dropna()) * np.sqrt(252)

        sharpe = calculate_shape(daily)
        sortino = calculate_sortino(daily)
        max_down = calculate_max_down(ticker_df["close"])
        var_95 = calculate_var(daily)

        rsi = 0.0
        if len(ticker_df) > 14:
            rsi_last = calculate_rsi(ticker_df["close"]).iloc[-1]
            if pd.notna(rsi_last):
                rsi = float(rsi_last)

        skewness = calculate_skewness(daily)
        kurtosis = calculate_kurtosis(daily)
        distribution = get_distribution(daily)

        meta = {}
        for a in assets_meta:
            if a["ticker"] == ticker:
                meta = a
                break

        res.append({
            "ticker": ticker,
            "name": meta.get("name", ticker),
            "sector": meta.get("sector", "Unknown"),
            "last_price": ticker_df["close"].iloc[-1],
            "total": total,
            "monthly": monthly,
            "volatility": volatility,
            "sharpe": sharpe,
            "sortino": sortino,
            "max_down": max_down,
            "var_95": var_95,
            "rsi": rsi,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "mean": distribution["mean"],
            "return_std": distribution["std"]
        })  

    return pd.DataFrame(res)


def calculate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.pivot_table(values="close", index="date", columns="ticker").pct_change()
    pivot = pivot.dropna(axis=1, thresh=int(len(pivot) * 0.8))
    return pivot.corr()


def calculate_sector(metrics: pd.DataFrame) -> pd.DataFrame:
    sector = metrics.groupby("sector").agg({
        "total": "mean",
        "volatility": "mean",
        "sharpe": "mean",
        "max_down": "mean",
        "ticker": "count"
    }).rename(columns={"ticker": "assets_count"})

    return sector.sort_values("total", ascending=False)