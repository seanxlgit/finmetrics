from finmetrics import fetch_all

async def test_tickers_all_prices():
    out = await fetch_all(["AAPL", "IBM", "NVDA"], max_concurrency=3, timeout=10.0)
    assert all(isinstance(v, float) for v in out.values())

async def test_tickers_all_none():
    out = await fetch_all(["AAPL", "IBM", "NVDA"], max_concurrency=3, timeout=0.01)
    assert all(v is None for v in out.values())

async def test_tickers_fail_none():
    out = await fetch_all(["AAPL", "FAIL", "MSFT"], max_concurrency=3, timeout=10.0)
    assert isinstance(out['AAPL'], float)
    assert out['FAIL'] is None
    assert isinstance(out['MSFT'], float)

