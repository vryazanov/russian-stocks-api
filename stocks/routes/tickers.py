"""Routes for tickers api."""
import datetime

import fastapi

from stocks import dependendies
from stocks.entities import Payment, Ticker, Quote
from stocks.repositories.uow import UoW
from stocks.responses import ListResponse


router = fastapi.APIRouter()


@router.get(
    '',
    response_model=ListResponse[Ticker],
    operation_id='get_tickers',
)
async def tickers(
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> ListResponse[Ticker]:
    """Return the list of available tickers."""
    with uow:
        return ListResponse(results=uow.tickers.iterator({}))


@router.get(
    '/{ticker}/payments',
    response_model=ListResponse[Payment],
    operation_id='get_payments',
)
async def payments(
    ticker: str,
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> ListResponse[Ticker]:
    """Return the list of available tickers."""
    with uow:
        return ListResponse(results=uow.payments.iterator({'ticker': ticker}))


@router.get(
    '/{ticker}/quotes/{date}',
    response_model=ListResponse[Quote],
    operation_id='get_quotes',
)
async def quotes(
    ticker: str, date: datetime.date,
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> ListResponse[Ticker]:
    """Return the list of available tickers."""
    with uow:
        return ListResponse(results=uow.quotes.iterator({
            'ticker': ticker,
            'date': date,
        }))
