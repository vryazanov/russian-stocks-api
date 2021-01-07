"""Container for FastAPI application."""
import fastapi
import fastapi.openapi.utils

from stocks.routes import crawler, portfolio, tickers, tokens


app = fastapi.FastAPI()

app.include_router(
    tokens.router,
    prefix='/tokens',
    tags=['tokens'],
)

app.include_router(
    portfolio.router,
    prefix='/portfolio',
    tags=['portfolio'],
)

app.include_router(
    tickers.router,
    prefix='/tickers',
    tags=['tickers'],
)

app.include_router(
    crawler.router,
    prefix='/crawler',
    tags=['crawler'],
)
