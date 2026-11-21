import pandas as pd
import numpy as np
from analytics.metrics.risk_metrics import(
    calculate_shape,
    calculate_sortino,
    calculate_max_down,
    calculate_var
)


def test_shape_ratio():
    """
    Тест на проверку, что доходность должена быть положительной для растущего актива.
    """
    returns = pd.Series([0.01, 0.02, -0.005, 0.015, 0.01])
    shape = calculate_shape(returns)
    assert shape > 0

def test_shape_empty():
    """
    Тест проверяет, что доходность для пустого ряда должен быть 0.
    """
    assert calculate_shape(pd.Series()) == 0.0

def test_sortino_ration():
    """
    Тест проверяет, что коэффициент Сортино должен быть положительным для растущего актива.
    """
    returns = pd.Series([0.01, 0.02, -0.005, 0.015, 0.01])
    sortino = calculate_sortino(returns)
    assert sortino > 0

def test_max_drawndown_negative():
    """
    Тест проверяет, что максимальная просадка должен быть отрицательным.
    """
    prices = pd.Series([100, 110, 90, 95, 80])
    max_down = calculate_max_down(prices)
    assert max_down < 0
    assert abs(max_down - (-0.2)) < 0.01

def test_var_negative():
    """
    Тест проверяет, что Убыток должен быть отрицательным.
    """
    returns = pd.Series([0.01, -0.02, 0.005, -0.01, 0.02])
    var = calculate_var(returns, confidence=0.95)
    assert var < 0

def test_drawndown_nodecline():
    """
    Если цена только растёт, просадка должна быть 0.
    """
    prices = pd.Series([100, 110, 120, 130])
    max_down = calculate_max_down(prices)
    assert max_down == 0.0