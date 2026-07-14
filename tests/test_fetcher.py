from finmetrics import fetch_all

async def test_tickers_all_prices():
    out = await fetch_all(["AAPL", "IBM", "NVDA"], max_concurrency=3, timeout=10.0)
    assert isinstance(out['AAPL'], float)
    assert isinstance(out['IBM'], float)
    assert isinstance(out['NVDA'], float)

async def test_tickers_all_none():
    out = await fetch_all(["AAPL", "IBM", "NVDA"], max_concurrency=3, timeout=0.01)
    assert out['AAPL'] is None
    assert out['IBM'] is None
    assert out['NVDA'] is None

async def test_tickers_fail_none():
    out = await fetch_all(["AAPL", "FAIL", "MSFT"], max_concurrency=3, timeout=10.0)
    assert isinstance(out['AAPL'], float)
    assert out['FAIL'] is None
    assert isinstance(out['MSFT'], float)

