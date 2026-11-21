import pandas as pd
import numpy as np
from analytics.metrics.statistics import(
    calculate_skewness,
    calculate_kurtosis,
    get_distribution
)


def test_skewn_symmetric():
    """
    Тест проверяет, что у симметричного распределения асимметрия близка к 0.
    """
    returns = pd.Series([-0.02, -0.01, 0.0, 0.01, 0.02])
    skew = calculate_skewness(returns)
    assert abs(skew) < 0.1


def test_skewn_positive():
    """
    Тест, который проверяет Правый хвост длиннее с Положительной асимметрий.
    """
    returns = pd.Series([-0.01, 0.0, 0.01, 0.02, 0.10])
    skew = calculate_skewness(returns)
    assert skew > 0


def test_skewn_negative():
    """
    Тест, который проверяет Левый хвост длиннее с Отрицательной асимметрий.
    """
    returns = pd.Series([-0.10, -0.02, -0.01, 0.0, 0.01])
    skew = calculate_skewness(returns)
    assert skew < 0


def test_skewn_empty():
    """
    Для пустого ряда асимметрия = 0.
    """
    assert calculate_skewness(pd.Series()) == 0.0


def test_kurtosis_normal():
    """
    Тест проверяет, что у нормального распределения эксцесс близок к 0.
    """
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0, 0.01, 1000))
    kurt = calculate_kurtosis(returns)
    assert abs(kurt) < 0.5


def test_kurtosis_tails():
    """
    Тест проверяет, что распределение с выбросами имеет положительный эксцесс.
    """
    returns = pd.Series([0.01] * 100 + [0.5, -0.5])
    kurt = calculate_kurtosis(returns)
    assert kurt > 0


def test_kurtosis_empty():
    """
    Для пустого ряда эксцесс = 0.
    """
    assert calculate_kurtosis(pd.Series()) == 0.0


def test_distribution_keys():
    """
    Тест проверяет, что словарь распределения должен содержать все ключи.
    "mean", "std", "median", "min", "max", "count"
    """
    returns = pd.Series([0.01, 0.02, -0.005, 0.015, 0.01])
    dist = get_distribution(returns)
    expected_keys = {"mean", "std", "median", "min", "max", "count"}
    assert set(dist.keys()) == expected_keys


def test_distribution_values():
    """
    Тест, проверяет конкретные значений распределения.
    """
    returns = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    dist = get_distribution(returns)
    assert dist["mean"] == 3.0
    assert dist["median"] == 3.0
    assert dist["min"] == 1.0
    assert dist["max"] == 5.0
    assert dist["count"] == 5


def test_distribution_empty():
    """
    Для пустого ряда все значения = 0.
    """
    dist = get_distribution(pd.Series())
    assert dist["mean"] == 0.0
    assert dist["count"] == 0