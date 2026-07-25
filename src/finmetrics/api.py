from typing import Literal
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from finmetrics.fetcher import fetch_all, fetch_history
from finmetrics.config import Settings, get_settings
from finmetrics.metrics import annualized_volatility, max_drawdown

app = FastAPI(title="Market Data API")

class PriceResponse(BaseModel):
    ticker: str
    price: float

class BatchPriceRequest(BaseModel):
    tickers: list[str] = Field(min_length=1, max_length=100)

class BatchPriceResponse(BaseModel):
    prices: dict[str, float | None]

class MetricResponse(BaseModel):
    ticker: str
    metric: str
    value: float
    n_observations: int


@app.get("/prices/{ticker}", response_model=PriceResponse)
async def get_price(ticker: str) -> PriceResponse:
    result = await fetch_all([ticker])
    price = result[ticker]
    if price is None:
        raise HTTPException(status_code=502, detail=f"Upstream fetch failed for {ticker}")
    return PriceResponse(ticker=ticker, price=price)

@app.post("/prices", response_model=BatchPriceResponse)
async def get_prices(
    req: BatchPriceRequest,
    settings: Settings = Depends(get_settings),
) -> BatchPriceResponse:
    # POST, not GET: this is a query with a request BODY. GET bodies are
    # ignored/stripped by proxies and caches; a 100-ticker list doesn't
    # belong in a URL. POST-as-query is standard for batch reads.
    results = await fetch_all(req.tickers, settings.max_concurrency, settings.fetch_timeout)
    return BatchPriceResponse(prices=results)

@app.get("/metrics/{ticker}", response_model=MetricResponse)
async def get_metric(
    ticker: str,
    metric: Literal["mdd", "vol"],
    settings: Settings = Depends(get_settings),
) -> MetricResponse:
    prices = await fetch_history(ticker, timeout=settings.fetch_timeout)
    if prices is None:
        raise HTTPException(status_code=502, detail=f"Upstream fetch failed for {ticker}")
    if metric == "mdd":
        value = max_drawdown(prices)
    else:
        returns = [(b - a) / a for a, b in zip(prices, prices[1:])]
        value = annualized_volatility(returns)
    return MetricResponse(ticker=ticker, metric=metric, value=value, n_observations=len(prices))


