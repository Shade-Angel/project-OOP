import pandas as pd

def calculate_sma(prices: pd.Series, window: int = 20) -> pd.Series:
    """
    Скользящая средняя
    """
    return prices.rolling(window=window).mean()


def calculate_bollinger(
    prices: pd.Series, window: int = 20, num: float = 2.0
) ->tuple[pd.Series, pd.Series, pd.Series]:
    """
    Полосы Боллинджера, возращает(lower, middle, upper)
    """
    middle = prices.rolling(window=window).mean()  
    std = prices.rolling(window=window).std()
    upper = middle + (std * num)
    lower = middle - (std * num)
    return lower, middle, upper


def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """
    Индикатор перекупленности/перепроданности.
    Принимает значения от 0 до 100. Выше 70 - перекупленность, ниже 30 - перепроданность.
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi