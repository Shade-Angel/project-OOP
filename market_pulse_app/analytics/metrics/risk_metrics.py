import numpy as np
import pandas as pd

def calculate_shape(returns: pd.Series, risk: float = 0.07) -> float:
    """
    Доходность на единицу риска.
    Формула: (годовая доходность - безрисковая ставка) / годовая волатильность
    """

    if returns.empty or returns.isna().all():
        return 0.0

    clear = returns.dropna()
    volatility = np.std(clear) * np.sqrt(252)

    if volatility == 0:
        return 0.0

    annual = (1 + clear.mean()) ** 252 - 1
    excess_return = annual - risk

    return excess_return / volatility

def calculate_sortino(returns: pd.Series, risk_free: float = 0.07) -> float:
    """
    Учитывает только негативную волатильность (риск убытков).
    """

    if returns.empty or returns.isna().all():
        return 0.0

    clean = returns.dropna()
    downside = clean[clean < 0]

    if downside.empty:
        return 0.0

    downside_devation = np.std(downside) * np.sqrt(252)

    if downside_devation == 0:
        return 0.0

    annual = (1 + clean.mean()) ** 252 - 1
    excess_return = annual - risk_free

    return excess_return / downside_devation

def calculate_max_down(prices: pd.Series) -> float:
    """
    Максимальная просадка от пика (отрицательное число).
    """

    if prices.empty:
        return 0.0

    rolling = prices.cummax()
    drawndown = (prices / rolling) - 1

    return drawndown.min()


def calculate_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """
    Максимальный ожидаемый убыток за день с заданной вероятностью.
    confidence=0.95 означает, что в 95% случаев убыток не превысит это значение.
    """

    if returns.empty or returns.isna().all():
        return 0.0

    clean = returns.dropna()
    percentile = (1 - confidence) * 100

    return np.percentile(clean, percentile)