import tempfile
from pathlib import Path

from seed.storage import build_dataset_json, save_json, load_json


def quotes():
    return [
        {"ticker": "SBER", "date": "2023-01-03", "open": 100.0, "high": 110.0,
         "low": 95.0, "close": 105.0, "volume": 1000, "source": "moex"},
        {"ticker": "GAZP", "date": "2023-01-04", "open": 200.0, "high": 210.0,
         "low": 195.0, "close": 205.0, "volume": 2000, "source": "synthetic"},
    ]


def test_dataset_has_three_sections():
    assert set(build_dataset_json(quotes(), [])) == {"meta", "assets", "quotes"}


def test_meta_counts_correct():
    dataset = build_dataset_json(quotes(), [])
    assert dataset["meta"]["records_count"] == 2
    assert dataset["meta"]["assets_count"] == 2


def test_save_and_load_returns_same_data():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "t.json"
        data = {"meta": {}, "assets": [], "quotes": []}
        save_json(data, path)
        assert load_json(path) == data