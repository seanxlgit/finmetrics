import httpx
import pytest

from finmetrics.api import app
from finmetrics.config import Settings, get_settings

@pytest.fixture
def generous_timeouts():
    app.dependency_overrides[get_settings] = lambda: Settings(
        fetch_timeout=10.0,
        min_latency=0.001,
        max_latency=0.005,
    )
    yield
    app.dependency_overrides.clear()

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

async def test_get_price_ok(client, generous_timeouts):
    resp = await client.get("/prices/AAPL")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ticker"] == "AAPL"
    assert isinstance(body["price"], float)

async def test_batch_happy(client, generous_timeouts):
    resp = await client.post("/prices", json={'tickers': ["AAPL", "NVDA"]})
    assert resp.status_code == 200
    result = resp.json()['prices']
    assert set(result) == {"AAPL", "NVDA"}
    assert all(isinstance(t, float) for t in result.values())

async def test_batch_with_FAIL(client, generous_timeouts):
    resp = await client.post("/prices", json={'tickers': ["AAPL", "FAIL"]})
    assert resp.status_code == 200
    result = resp.json()['prices']
    assert isinstance(result['AAPL'], float)
    assert result['FAIL'] is None

async def test_empty_batch(client, generous_timeouts):
    resp = await client.post("/prices", json={'tickers': []})
    assert resp.status_code == 422

async def test_invalid_metric(client, generous_timeouts):
    resp = await client.get("/metrics/AAPL?metric=beta")
    assert resp.status_code == 422

@pytest.mark.parametrize("metric, check", [
    ("mdd", lambda v: v <= 0.0),
    ("vol", lambda v: v >= 0.0),
])
async def test_metrics_invariants(client, generous_timeouts, metric, check):
    resp = await client.get(f"/metrics/AAPL?metric={metric}")
    assert resp.status_code == 200
    assert isinstance(resp.json()['value'], float)
    assert check(resp.json()['value'])

async def test_upstream_502(client, generous_timeouts):
    resp = await client.get("/prices/FAIL")
    assert resp.status_code == 502


