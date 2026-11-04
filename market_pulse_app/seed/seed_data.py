import time
from config import ASSETS, OUTPUT_FILE
from load import fetch_moex
from generate import generate_synthetic
from clean import clean_data
from storage import save_json, build_dataset_json


def main():

    all_quotes = []
    failed = []

    total = len(ASSETS)
    for i, (ticker, name, sector) in enumerate(ASSETS, 1):
        print(f"  [{i}/{total}] {ticker} ({name})...", end=" ")
        rows = fetch_moex(ticker)
        if rows:
            all_quotes.extend(rows)
            print(f"{len(rows)} записей")
        else:
            print("данных нет")
            failed.append((ticker, name, sector))
        time.sleep(0.3)

    if failed:
        for ticker, name, sector in failed:
            print(f"  {ticker} ({name})...", end=" ")
            rows = generate_synthetic(ticker)
            all_quotes.extend(rows)
            print(f"{len(rows)} записей")


    quotes = clean_data(all_quotes)

    assets_meta = [
        {"ticker": t, "name": n, "sector": s}
        for t, n, s in ASSETS
    ]

    dataset = build_dataset_json(quotes, assets_meta)

    save_json(dataset, OUTPUT_FILE)

    print("")
    print(f"Активов: {dataset['meta']['assets_count']}")
    print(f"Записей: {dataset['meta']['records_count']:,}")
    print(f"Период: {dataset['meta']['start_date']} — {dataset['meta']['end_date']}")
    print(f"Источники: {', '.join(dataset['meta']['sources'])}")
    print(f"Файл: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()