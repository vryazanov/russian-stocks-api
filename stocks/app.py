"""Container for FastAPI application."""
import fastapi

from stocks.routes import crawler, tickers


app = fastapi.FastAPI()

app.include_router(
    crawler.router,
    prefix='/crawler',
    tags=['crawler'],
)

app.include_router(
    tickers.router,
    prefix='/tickers',
    tags=['tickers'],
)
