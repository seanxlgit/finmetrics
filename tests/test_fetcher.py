import pytest

from finmetrics import fetch_all
from finmetrics.config import Settings

@pytest.fixture
def fast_success() -> Settings:
    """No latency, generous timeout """
    return Settings(
        fetch_timeout = 0.006,
        max_concurrency = 3,
        min_latency = 0.001,
        max_latency = 0.005
    )

@pytest.fixture
def fast_timeout() -> Settings:
    """over latency > timeout """
    return Settings(
        fetch_timeout = 0.0005,
        max_concurrency = 3,
        min_latency = 0.001,
        max_latency = 0.005
    )


async def test_tickers_all_prices(fast_success):
    out = await fetch_all(["AAPL", "IBM", "NVDA"], fast_success)
    assert all(isinstance(v, float) for v in out.values())

async def test_tickers_all_none(fast_timeout):
    out = await fetch_all(["AAPL", "IBM", "NVDA"], fast_timeout)
    assert all(v is None for v in out.values())

async def test_tickers_fail_none(fast_success):
    out = await fetch_all(["AAPL", "FAIL", "MSFT"], fast_success)
    assert isinstance(out['AAPL'], float)
    assert out['FAIL'] is None
    assert isinstance(out['MSFT'], float)

@pytest.mark.slow
async def test_realistic_latency_defaults():
    """Smoke test against production-default settings (real sleeps)."""
    out = await fetch_all(["AAPL", "IBM"])          # no settings -> get_settings()
    assert set(out) == {"AAPL", "IBM"}
    assert all(v is None or isinstance(v, float) for v in out.values())


