import pandas as pd
import numpy as np

def calculate_skewness(returns: pd.Series) -> float:
    """
    Асимметрия распределения доходности.
    0 - симметричное распределение.
    > 0 - правый хвост длиннее (редкие большие прибыли).
    < 0 - левый хвост длиннее (редкие большие убытки).
    """
    if returns.empty or returns.isna().all():
        return 0.0
    return float(returns.dropna().skew())#type: ignore


def calculate_kurtosis(returns: pd.Series) -> float:
    """
    Эксцесс распределения доходности.
    0 - как у нормального распределения.
    > 0 - тяжёлые хвосты.
    < 0 - лёгкие хвосты.
    """
    if returns.empty or returns.isna().all():
        return 0.0
    return float(returns.dropna().kurtosis())# type: ignore


def get_distribution(returns: pd.Series) -> dict:
    """
    Сводная статистика распределения доходности.
    """
    if returns.empty or returns.isna().all():
        return {
            "mean": 0.0,
            "std": 0.0,
            "median": 0.0,
            "min": 0.0,
            "max": 0.0,
            "count": 0
        }
    
    clean = returns.dropna()
    return {
        "mean": float(clean.mean()),
        "std": float(clean.std()),
        "median": float(clean.median()),
        "min": float(clean.min()),
        "max": float(clean.max()),
        "count": int(len(clean))
    }