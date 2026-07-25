import httpx
import pytest

from finmetrics.api import app
from finmetrics.config import Settings, get_settings

@pytest.fixture
def generous_timeouts():
    app.dependency_overrides[get_settings] = lambda: Settings(fetch_timeout=10.0)
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

