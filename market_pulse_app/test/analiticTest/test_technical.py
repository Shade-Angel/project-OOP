import pandas as pd
import numpy as np
from analytics.metrics.technical import(
    calculate_sma,
    calculate_bollinger,
    calculate_rsi
)


def test_sma():
    """
    Тест, который проверяет, что SMA корректно считает среднее за окно.
    """
    prices = pd.Series([10, 20, 30, 40, 50])
    sma = calculate_sma(prices, window=3)
    assert pd.isna(sma.iloc[0])
    assert pd.isna(sma.iloc[1])
    assert sma.iloc[2] == 20.0
    assert sma.iloc[4] == 40.0


def test_sma_window1():
    """
    Тест проверяет, что SMA с окном 1 должна совпадать с ценой.
    """
    prices = pd.Series([100, 200, 300])
    sma = calculate_sma(prices, window=1)
    assert sma.iloc[0] == 100.0
    assert sma.iloc[2] == 300.0


def test_bollinger_order():
    """
    Тест проверяет, что нижняя полоса < средней < верхней.
    """
    prices = pd.Series([100, 102, 98, 105, 103, 107, 104, 108, 106, 110] * 3)
    lower, middle, upper = calculate_bollinger(prices, window=5)
    assert lower.iloc[-1] < middle.iloc[-1] < upper.iloc[-1]


def test_bollinger_symmetry():
    """
    Тест проверяет, что Полосы симметричны относительно средней.
    """
    prices = pd.Series([100, 102, 98, 105, 103, 107, 104, 108, 106, 110] * 3)
    lower, middle, upper = calculate_bollinger(prices, window=5)
    diff_up = upper.iloc[-1] - middle.iloc[-1]
    diff_lw = middle.iloc[-1] - lower.iloc[-1]
    assert abs(diff_up - diff_lw) < 0.00001


def test_rsi_range():
    """
    Тест проверяет, что RSI находится в диапазоне от 0 до 100.
    """
    prices = pd.Series([100, 102, 98, 105, 103, 107, 104, 108, 106, 110] * 3)
    rsi = calculate_rsi(prices)
    valid = rsi.dropna()
    assert valid.min() >= 0
    assert valid.max() <= 100


def test_rsi_up():
    """
    Тест проверяет, что при устойчивом росте RSI должен быть высоким, перекупленность.
    """
    prices = pd.Series(range(100, 150))
    rsi = calculate_rsi(prices)
    last = rsi.iloc[-1]
    assert last > 70


def test_rsi_dw():
    """
    Тест проверяет, что при устойчивом падении RSI должен быть низким, перепроданность.
    """
    prices = pd.Series(range(150, 100, -1))
    rsi = calculate_rsi(prices)
    last = rsi.iloc[-1]
    assert last < 30