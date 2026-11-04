def clean_data(rows: list[dict]) -> list[dict]:
    seen = set()
    unique_rows = []
    for row in rows:
        key = (row["ticker"], row["date"])
        if key not in seen:
            seen.add(key)
            unique_rows.append(row)

    cleaned = []
    for row in unique_rows:
        if row["open"] <= 0 or row["close"] <= 0:
            continue

        if row["high"] < row["low"]:
            row["high"], row["low"] = row["low"], row["high"]

        cleaned.append(row)

    cleaned.sort(key=lambda r: (r["ticker"], r["date"]))

    return cleaned