from seed.clean import clean_data


def row(**changes):
    base = {
        "ticker": "SBER", "date": "2023-01-03",
        "open": 100.0, "high": 110.0, "low": 95.0, "close": 105.0,
        "volume": 1000, "source": "moex",
    }
    base.update(changes)
    return base


def test_removes_duplicates():
    assert len(clean_data([row(), row()])) == 1


def test_drops_zero_and_negative_prices():
    assert clean_data([row(open=0)]) == []
    assert clean_data([row(close=-5)]) == []


def test_fixes_swapped_high_low():
    fixed = clean_data([row(high=90.0, low=110.0)])[0]
    assert fixed["high"] == 110.0
    assert fixed["low"] == 90.0


def test_sorts_by_ticker_and_date():
    data = clean_data([row(ticker="GAZP"), row(date="2023-01-04"), row()])
    keys = [(r["ticker"], r["date"]) for r in data]
    assert keys == [("GAZP", "2023-01-03"), ("SBER", "2023-01-03"), ("SBER", "2023-01-04")]

def test_empty_input_returns_empty():
    assert clean_data([]) == []