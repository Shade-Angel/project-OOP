import urllib.request
import urllib.parse
import json
import time
import ssl
import urllib.error
from config import START_DATE, END_DATE



def _open_url(url: str):
    try:
        return urllib.request.urlopen(url, timeout=30)
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            context = ssl._create_unverified_context()
            return urllib.request.urlopen(url, timeout=30, context=context)
        raise


def fetch_moex(ticker: str) -> list[dict]:
    base_url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{ticker}/candles.json"

    all_rows = []
    start = 0
    limit = 500

    while True:
        params = urllib.parse.urlencode({
            "from": START_DATE,
            "till": END_DATE,
            "interval": 24,
            "start": start,
        })
        url = f"{base_url}?{params}"

        try:
            with _open_url(url) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(e)
            return []

        candles = data.get("candles", {})
        rows = candles.get("data", [])
        columns = candles.get("columns", [])

        if not rows:
            break

        for row in rows:
            item = dict(zip(columns, row))
            all_rows.append(item)

        if len(rows) < limit:
            break

        start += len(rows)
        time.sleep(0.2)

    if not all_rows:
        return []

    result = []
    for item in all_rows:
        result.append({
            "ticker": ticker,
            "date": item["begin"][:10],
            "open": float(item["open"]),
            "high": float(item["high"]),
            "low": float(item["low"]),
            "close": float(item["close"]),
            "volume": int(item["value"]),
            "source": "moex",
        })

    return result