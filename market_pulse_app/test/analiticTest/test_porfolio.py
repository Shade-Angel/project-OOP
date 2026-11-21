import pandas as pd
import numpy as np
from analytics.metrics.portfolio import(
    calculate_metrics,
    calculate_correlation_matrix,
    calculate_sector
)

def _make_df(mode: str = "single") -> pd.DataFrame:
    """
    "single" - один актив (SBER, 50 дней, рост)
    "two" - два актива (SBER + GAZP, по 25 дней)
    """
    if mode == "single":
        data = {
            "date": pd.date_range("2023-01-01", periods=50),
            "ticker": ["SBER"] * 50,
            "close": [100 + i * 0.5 for i in range(50)]
        }
    elif mode == "two":
        dates = pd.date_range("2023-01-01", periods=25)
        data = {
            "date": list(dates) * 2,
            "ticker": ["SBER"] * 25 + ["GAZP"] * 25,
            "close": [100 + i * 0.5 for i in range(25)] + [200 - i * 0.3 for i in range(25)]
        }
    else:
        raise ValueError(f"Неизвестный mode: {mode}. Допустимые: 'single', 'two'")
    
    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)
    return df


def _make_assets_meta(ticker: str = "SBER", name: str = "Сбербанк", sector: str = "Финансы") -> list[dict]:
    return [{"ticker": ticker, "name": name, "sector": sector}]

def _make_metrics_df() -> pd.DataFrame:
    return pd.DataFrame({
        "ticker": ["SBER", "GAZP", "LKOH"],
        "sector": ["Финансы", "Нефть", "Нефть"],
        "total": [0.1, 0.2, 0.15],
        "volatility": [0.3, 0.4, 0.35],
        "sharpe": [1.0, 1.5, 1.2],
        "max_down": [-0.2, -0.3, -0.25]
    })


def test_metrics_dataframe():
    """
    Функция calculate_metrics должна возвращать DataFrame.
    """
    df = _make_df(mode="single")
    meta = _make_assets_meta()
    res = calculate_metrics(df, meta)
    assert isinstance(res, pd.DataFrame)
    assert len(res) == 1


def test_metrics_has_columns():
    """
    Тест проверяет, что приходящей DataFrame содержит все необходимые колонки.
    """
    df = _make_df(mode="single")
    meta = _make_assets_meta()
    res = calculate_metrics(df, meta)
    req_col = {
        "ticker", "name", "sector", "last_price", "total",
        "volatility", "sharpe", "max_down", "rsi"
    }
    assert req_col.issubset(set(res.columns))


def test_correlation_matrix():
    """
    Тест проверяет, что корреляционная матрица является квадратной.
    """
    df = _make_df(mode="two")
    corr = calculate_correlation_matrix(df)
    assert isinstance(corr, pd.DataFrame)
    assert corr.shape[0] == corr.shape[1]
    assert "SBER" in corr.columns
    assert "GAZP" in corr.columns


def test_diagonal_matrix():
    """
    Тест проверяет диагональ корреляционной матрицы, котора  должна быть равна 1.
    """
    df = _make_df(mode="two")
    corr = calculate_correlation_matrix(df)
    assert abs(float(corr.loc["SBER", "SBER"]) - 1.0) < 0.01  # type: ignore
    assert abs(float(corr.loc["GAZP", "GAZP"]) - 1.0) < 0.01  # type: ignore


def test_sector_dataframe():
    """
    Проверяет, что calculate_sector_metrics возращает DataFrame.
    """
    metrics = _make_metrics_df()
    result = calculate_sector(metrics)
    assert isinstance(result, pd.DataFrame)
    assert "Нефть" in result.index
    assert result.loc["Нефть", "assets_count"] == 2


def test_sector_sort():
    """
    Тест проверяет, что сектора должны быть отсортированы по доходности.
    """
    metrics = pd.DataFrame({
        "ticker": ["A", "B", "C"],
        "sector": ["Сектор1", "Сектор2", "Сектор3"],
        "total": [0.1, 0.3, 0.2],
        "volatility": [0.3, 0.4, 0.35],
        "sharpe": [1.0, 1.5, 1.2],
        "max_down": [-0.2, -0.3, -0.25]
    })
    result = calculate_sector(metrics)
    returns = result["total"].tolist()
    assert returns == sorted(returns, reverse=True)