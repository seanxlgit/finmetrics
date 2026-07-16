from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from finmetrics.fetcher import fetch_all

app = FastAPI(title="Market Data API")

class PriceResponse(BaseModel):
    ticker: str
    price: float

@app.get("/prices/{ticker}", response_model=PriceResponse)
async def get_price(ticker: str) -> PriceResponse:
    result = await fetch_all([ticker])
    price = result[ticker]
    if price is None:
        raise HTTPException(status_code=502, detail=f"Upstream fetch failed for {ticker}")
    return PriceResponse(ticker=ticker, price=price)

