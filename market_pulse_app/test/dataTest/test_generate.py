from seed.generate import generate_synthetic

FIELDS = {"ticker", "date", "open", "high", "low", "close", "volume", "source"}


def test_returns_non_empty_list():
    assert len(generate_synthetic("SBER")) > 0


def test_records_have_all_fields():
    assert set(generate_synthetic("SBER")[0]) == FIELDS


def test_prices_positive_and_ohlc_consistent():
    for r in generate_synthetic("SBER"):
        assert r["open"] > 0 and r["close"] > 0
        assert r["high"] >= max(r["open"], r["close"])
        assert r["low"] <= min(r["open"], r["close"])


def test_same_ticker_gives_same_result():
    assert generate_synthetic("SBER")[0]["close"] == generate_synthetic("SBER")[0]["close"]


def test_different_tickers_give_different_result():
    assert generate_synthetic("SBER")[0]["close"] != generate_synthetic("GAZP")[0]["close"]