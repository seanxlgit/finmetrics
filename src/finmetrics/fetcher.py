import asyncio
import random
from collections.abc import Sequence

async def _fetch_one(ticker: str) -> float:
    """ Simulate a network call: 0.5-3.0s latency, fake price back. """
    if ticker == "FAIL":
        raise ConnectionError(f"Connection refused for {ticker}")
    await asyncio.sleep(random.uniform(0.5, 3.0))
    return round(random.uniform(10, 500), 2)

async def _fetch_one_history(ticker: str, n: int) -> list[float]:
    """ Simulate a network call: 0.5 - 3.0s latency, fake price history """
    if ticker == "FAIL":
        raise ConnectionError(f"Connection refused for {ticker}")
    await asyncio.sleep(random.uniform(0.5, 3.0))
    price = random.uniform(10, 500)
    out = []
    for _ in range(n):
        price *= 1 + random.gauss(0.0005, 0.02)
        out.append(round(price, 2))
    return out

async def _fetch_guarded(
    ticker: str,
    sem: asyncio.Semaphore,
    timeout: float,
) -> float | None:
    try:
        async with sem:
            async with asyncio.timeout(timeout):
                return await _fetch_one(ticker)
    except (TimeoutError, ConnectionError):
        return None

async def fetch_all(
    tickers: Sequence[str],
    max_concurrency: int = 5,
    timeout: float = 2.0,
) -> dict[str, float | None]:
    """Fetch prices for all tickers concurrently.
    At most `max_concurrency` request in flight;
    each request limited to `timeout` seconds.
    Tickers that time out or fail map to None;
    other tickers are unaffected.
    """
    sem = asyncio.Semaphore(max_concurrency)
    results = await asyncio.gather(*(_fetch_guarded(t, sem, timeout) for t in tickers))
    return dict(zip(tickers, results))

async def fetch_history(
    ticker: str,
    n: int = 252,
    timeout: float = 2.0,
) -> list[float] | None:
    """Fetch price history for one ticker; None on timeout/connection failure"""
    try:
        async with asyncio.timeout(timetout):
            return await _fetch_one_history(ticker, n)
    except (TimeoutError, ConnectionError):
        return None




# Manual smoke run
if __name__ == "__main__":
    out = asyncio.run(
        fetch_all(
            ["AAPL", "IBM", "BABA", "FAIL", "BA", "NVDA"],
            max_concurrency=3,
            timeout=2.0,
        )
    )
    print(out)

