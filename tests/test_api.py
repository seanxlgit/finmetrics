import httpx
from finmetrics.api import app

async def test_get_price_ok():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/prices/AAPL")
    assert resp.status_code == 200
    body = resp.json()
    assert body['ticker'] == "AAPL"
    assert isinstance(body['price'], float)

