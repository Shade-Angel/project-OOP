import json
from pathlib import Path
from datetime import datetime


def save_json(data: dict, filepath: Path) -> None:
    """Сохраняет данные в JSON файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {filepath}")


def load_json(filepath: Path) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_dataset_json(quotes: list[dict], assets_meta: list[dict]) -> dict:
    tickers = set(q["ticker"] for q in quotes)
    dates = sorted(set(q["date"] for q in quotes))
    sources = set(q["source"] for q in quotes)

    return {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "start_date": dates[0] if dates else None,
            "end_date": dates[-1] if dates else None,
            "assets_count": len(tickers),
            "records_count": len(quotes),
            "sources": sorted(sources),
        },
        "assets": assets_meta,
        "quotes": quotes,
    }