"""Routes for tickers api."""
import datetime

import fastapi

from stocks import dependendies
from stocks.entities import Payment, Quote, Ticker
from stocks.repositories import UoW
from stocks.responses import ListResponse


router = fastapi.APIRouter()


@router.get('', response_model=ListResponse[Ticker])
async def tickers(
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> ListResponse[Ticker]:
    """Return the list of available tickers."""
    with uow:
        results = uow.tickers.iterator({})
    return ListResponse(results=results)


@router.get('/{ticker}/payments', response_model=ListResponse[Payment])
async def payments(
    ticker: str,
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> ListResponse[Ticker]:
    """Return the list of available tickers."""
    with uow:
        results = uow.payments.iterator({'ticker': ticker})
    return ListResponse(results=results)


@router.get('/{ticker}/quotes/{date}', response_model=ListResponse[Quote])
async def quotes(
    ticker: str, date: datetime.date,
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> ListResponse[Ticker]:
    """Return the list of available tickers."""
    with uow:
        results = uow.quotes.iterator({'ticker': ticker, 'date': date})
    return ListResponse(results=results)
