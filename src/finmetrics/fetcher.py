import asyncio
import random
from collections.abc import Sequence

async def _fetch_one(ticker: str) -> float:
    """ Simulate a network call: 0.5-3.0s latency, fake price back. """
    if ticker == "FAIL":
        raise ConnectionError(f"Connection refused for {ticker}")
    await asyncio.sleep(random.uniform(0.5, 3.0))
    return round(random.uniform(10, 500), 2)

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

