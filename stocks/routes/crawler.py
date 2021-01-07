"""Routes for importing data."""
import typing

import fastapi
import fastapi.security

from stocks import dependendies, responses, settings
from stocks.entities import PaymentCreate, QuoteCreate, Ticker
from stocks.repositories.uow import UoW


router = fastapi.APIRouter()

http_bearer = fastapi.security.HTTPBearer()


def check_import_token(
    auth: fastapi.security.HTTPBearer = fastapi.Depends(http_bearer),
    settings: settings.Settings = fastapi.Depends(dependendies.get_settings),
) -> None:
    """Check if token has permission to import data."""
    if auth.credentials != settings.import_token:  # type: ignore
        raise fastapi.HTTPException(status_code=403, detail='Invalid token.')


def within_uow(
    uow: UoW = fastapi.Depends(dependendies.get_uow),
) -> typing.Iterable[UoW]:
    """Wrap into UoW transaction."""
    with uow:
        yield uow
        uow.commit()


@router.post(
    '/tickers/',
    response_model=responses.Ok,
    operation_id='import_tickers',
    summary='Import tickers.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def tickers(
    entity: Ticker, uow: UoW = fastapi.Depends(within_uow),
) -> responses.Ok:
    """Take a list of tickers and save to db."""
    if not uow.tickers.exists(entity):
        uow.tickers.add(entity)
    return responses.Ok()


@router.post(
    '/payments/',
    response_model=responses.Ok,
    operation_id='import_payments',
    summary='Import dividend payments.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def payments(
    entity: PaymentCreate, uow: UoW = fastapi.Depends(within_uow),
) -> responses.Ok:
    """Save payment to the db."""
    if not uow.payments.exists(entity):
        uow.payments.add(entity)
    return responses.Ok()


@router.post(
    '/quotes/',
    response_model=responses.Ok,
    operation_id='import_quotes',
    summary='Import stock quotes.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def quotes(
    entity: QuoteCreate, uow: UoW = fastapi.Depends(within_uow),
) -> responses.Ok:
    """Take a list of tickers and save to db."""
    if not uow.quotes.exists(entity):
        uow.quotes.add(entity)
    return responses.Ok()
