import math
import random
from datetime import datetime, timedelta
from config import START_DATE, END_DATE, BASE_PRICES


def _generate_dates() -> list:
    dates = []
    current = datetime.strptime(START_DATE, "%Y-%m-%d")
    end = datetime.strptime(END_DATE, "%Y-%m-%d")
    while current <= end:
        if current.weekday() < 5:
            dates.append(current.date())
        current += timedelta(days=1)
    return dates


def generate_synthetic(ticker: str) -> list[dict]:
    start_price = BASE_PRICES.get(ticker, 100)

    random.seed(hash(ticker) % 1000)

    mu = random.uniform(-0.05, 0.20)
    sigma = random.uniform(0.15, 0.40)

    dates = _generate_dates()
    n = len(dates)

    dt = 1 / 252
    prices = [float(start_price)]
    for _ in range(n - 1):
        shock = random.gauss(0, 1)
        ret = (mu - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * shock
        prices.append(prices[-1] * math.exp(ret))

    result = []
    for i, d in enumerate(dates):
        close = prices[i]
        open_ = close * (1 + random.gauss(0, 0.005))
        high = max(open_, close) * (1 + abs(random.gauss(0, 0.008)))
        low = min(open_, close) * (1 - abs(random.gauss(0, 0.008)))
        volume = random.randint(500_000, 30_000_000)

        result.append({
            "ticker": ticker,
            "date": d.isoformat(),
            "open": round(open_, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "close": round(close, 2),
            "volume": volume,
            "source": "synthetic",
        })

    return result