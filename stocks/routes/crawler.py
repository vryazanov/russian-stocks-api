"""Routes for importing data."""
import typing

import fastapi
import fastapi.security

from stocks import dependendies, responses, settings
from stocks.entities import PaymentCreate, QuoteCreate, Ticker
from stocks.repositories.abc import BaseUnitOfWork


router = fastapi.APIRouter()

http_bearer = fastapi.security.HTTPBearer()


def check_import_token(
    auth: fastapi.security.HTTPBearer = fastapi.Depends(http_bearer),
    settings: settings.Settings = fastapi.Depends(dependendies.get_settings),
):
    """Check if token has permission to import data."""
    if auth.credentials != settings.import_token:
        raise fastapi.HTTPException(status_code=403, detail='Invalid token.')


def within_uow(uow: BaseUnitOfWork = fastapi.Depends(dependendies.get_uow)):
    """Wrap into UoW transaction."""
    with uow:
        yield uow
        uow.commit()


def create_many(repository, entities):
    """Create entities if they dont exist."""
    for entity in entities:
        if not repository.exists(entity):
            repository.add(entity)


@router.post(
    '/tickers/',
    response_model=responses.Ok,
    operation_id='import_tickers',
    summary='Import tickers.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def tickers(
    entities: typing.List[Ticker],
    uow: BaseUnitOfWork = fastapi.Depends(within_uow),
) -> responses.Ok:
    """Take a list of tickers and save to db."""
    create_many(uow.tickers, entities)
    return responses.Ok()


@router.post(
    '/payments/',
    response_model=responses.Ok,
    operation_id='import_payments',
    summary='Import dividend payments.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def payments(
    entities: typing.List[PaymentCreate],
    uow: BaseUnitOfWork = fastapi.Depends(within_uow),
) -> responses.Ok:
    """Take a list of tickers and save to db."""
    create_many(uow.payments, entities)
    return responses.Ok()


@router.post(
    '/quotes/',
    response_model=responses.Ok,
    operation_id='import_quotes',
    summary='Import stock quotes.',
    dependencies=[fastapi.Depends(check_import_token)],
)
async def quotes(
    entities: typing.List[QuoteCreate],
    uow: BaseUnitOfWork = fastapi.Depends(within_uow),
) -> responses.Ok:
    """Take a list of tickers and save to db."""
    create_many(uow.quotes, entities)
    return responses.Ok()
