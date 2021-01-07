"""Routes for tickers api."""
import fastapi

from stocks import dependendies
from stocks.entities import Payment, Ticker
from stocks.repositories.abc import BaseUnitOfWork
from stocks.responses import ListResponse


router = fastapi.APIRouter()


@router.get(
    '',
    response_model=ListResponse[Ticker],
    operation_id='get_tickers',
)
async def tickers(
    uow: BaseUnitOfWork = fastapi.Depends(dependendies.get_uow),
):
    """Return the list of available tickers."""
    return ListResponse(results=[])


@router.get(
    '/{ticker}/payments',
    response_model=ListResponse[Payment],
    operation_id='get_payments',
)
async def payments(
    ticker: str,
    uow: BaseUnitOfWork = fastapi.Depends(dependendies.get_uow),
):
    """Return the list of available tickers."""
    return ListResponse(results=[])
